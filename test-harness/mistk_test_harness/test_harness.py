##############################################################################
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
##############################################################################

import importlib
import os
import time

from mistk.model.abstract_model import AbstractModel
from mistk.transform.abstract_transform_plugin import AbstractTransformPlugin
from mistk.data import ModelInstanceInitParams, MistkDataset, ObjectInfo, TransformSpecificationInitParams, EvaluationSpecificationInitParams
from mistk.model.service import ModelInstanceEndpoint
from mistk.transform.service import TransformPluginEndpoint
from mistk.evaluation.service import EvaluationPluginEndpoint
from mistk_test_harness import model_service_wrapper, transform_service_wrapper, evaluation_service_wrapper
from mistk.evaluation.abstract_evaluation_plugin import AbstractEvaluationPlugin
from mistk.utils.csv_utils import validate_predictions_csv, validate_groundtruth_csv


class TestHarness(object):

    def __init__(self):
        """
        Initializes the test harness
        """
        self._model_service = None
        self._transform_service = None
        self._evaluation_service = None
        self._status_version = 0

    def model_init(self, model, objectives, dataset_map, model_path=None, model_props=None, hyperparams=None):
        """
        Instantiate model or remote endpoint wrapper.
        Call initialize, load_data, build_model on model.
        Output model status.

        :param model: model module/package or service endpoint URL
        :param objectives: model objectives
        :param dataset_map: dict of train/test dataset URIs
        :param model_path: local folder path of saved model files
        :param model_props: A JSON dictionary of model properties to override.
        :param hyperparams: A JSON dictionary of model hyperparameters to override.  
        """        
        if model.startswith('http:'):
            self._model_service = model_service_wrapper.ModelServiceWrapper(os.path.join(model, 'v1/mistk'))
        else:
            self._model_service = ModelInstanceEndpoint()
            path = model.rsplit('.', 1)
            module = importlib.import_module(path[0])
            model_impl = getattr(module, path[1])()
            assert isinstance(model_impl, AbstractModel)
            self._model_service.model = model_impl
            model_impl.endpoint_service = self._model_service
                
        ip = ModelInstanceInitParams(objectives=objectives, model_properties=model_props, hyperparameters=hyperparams)
        self._model_service.initialize_model(ip)
        self.wait_for_state(self._model_service, 'initialize', 'initialized')
        
        self._model_service.build_model(model_path)
        self.wait_for_state(self._model_service, 'build_model', 'ready')
        
        if dataset_map:
            bindings = {}
            if 'train' in dataset_map:
                training_data = MistkDataset(object_info=ObjectInfo(name='train-data'),
                                        data_path=dataset_map['train'])
                bindings['train'] = training_data
            if 'test' in dataset_map:
                test_data =  MistkDataset(object_info=ObjectInfo(name='test-data'),
                                        data_path=dataset_map['test'])
                bindings['test'] = test_data
                
            self._model_service.load_data(bindings)
            self.wait_for_state(self._model_service, 'load_data', 'ready')  

    def model_train(self, model_save_path=None):
        """
        Call train and, if model_save_path is supplied, save_model on model.
        Output model status.
        
        :param model_save_path: The path to which the final model checkpoint/snapshot should be saved.
        """       
        self._model_service.train()
        self.wait_for_state(self._model_service, 'train', 'ready')
        
        if model_save_path:
            self._model_service.save_model(model_save_path)
            self.wait_for_state(self._model_service, 'save_model', 'ready')

    def model_predict(self, predictions_path=None, predictions_validation_path=None):
        """
        Call predict and, if prediction_path is supplied, save_predictions on model.
        Output model status.
        
        :param predictions_path: The path to which the model's prediction results should be saved
        :param predictions_validation_path: The path to which the model's prediction results will be validated
        """
        self._model_service.predict()
        self.wait_for_state(self._model_service, 'predict', 'ready')
        
        if predictions_path:
            self._model_service.save_predictions(predictions_path)
            self.wait_for_state(self._model_service, 'save_predictions', 'ready')
            if predictions_validation_path:
                if not validate_predictions_csv(predictions_validation_path):
                    raise Exception("Failed to validate predictions csv file at %s" % predictions_validation_path)
            
    def model_stream_predict(self, stream_input):
        """
        Call stream_predict with supplied stream_input.
        Output model predictions.
        
        :param stream_input: A JSON dictionary of streaming input to send to a running model.
        """
        predictions = self._model_service.stream_predict(stream_input)
        print('Stream prediction results:')
        print(predictions)

    def model_update_stream_properties(self, stream_properties):
        """
        Call update_stream_properties with the supplied stream_properties dict.

        :param stream_properties: A JSON dictionary of metadata properties to be used by the model
        """
        self._model_service.update_stream_properties(stream_properties)
        
    def model_generate(self, generations_path=None):
        """
        Call generate and, if generations_path is supplied, save_generationss on model.
        Output model status.
        
        :param generations_path: The path to which the model's generations should be saved
        """
        self._model_service.generate()
        self.wait_for_state(self._model_service, 'generate', 'ready')
        
        if generations_path:
            self._model_service.save_generations(generations_path)
            self.wait_for_state(self._model_service, 'save_generations', 'ready')
        
    def wait_for_state(self, service, stage, state):
        """
        Waits for a model or transform service wrapper to change their 
        state to the desired state
        
        :param service: The model, transform, or evaluation service to get status for
        :param stage: The current stage of the container
        :param state: The desired state of the container        
        """
        print('Called \'' + stage + '\' on container, waiting for state change to \'' + state + '\'')
        time.sleep(1)
        st = service.get_status()
        while self._status_version == st.object_info.resource_version:
            time.sleep(1)
            st = service.get_status()
            
        while not st.state == state and not st.state == 'failed':
            if self._status_version != st.object_info.resource_version:
                print('Endpoint state: %s (%s)' % (st.state, str(st.payload)))
                self._status_version = st.object_info.resource_version
            time.sleep(1)
            st = service.get_status()
            
        print('Endpoint state: %s' % st.state)
        self._status_version = st.object_info.resource_version
        
        if st.state == 'failed':
            msg = 'Endpoint in failed state, exiting'
            print(msg)
            raise Exception(msg)
        
    def transform(self, transform, input_dirs, output_dir, properties):
        """
        Creates a transform service wrapper and performs the data transform
        on the dataset(s) provided.
        
        :param transform: The Transform that will be formed. Will be one of the following forms:
            - URL of running transform instance (ie. http://localhost:8080)
            - Python package and module (ie. mypackage.mymodule.MyTransformPluginClass
        :param input_dirs: A list of directory paths to be used for input in the transformation
        :param output_dir: A directory path to where all of the output files should be stored
        :param properties: A JSON dictionary of properties relevant to this transformation
        """
        if transform.startswith('http:'):
            self._transform_service = transform_service_wrapper.TransformServiceWrapper(os.path.join(transform, 'v1/mistk/transform'))
        else:
            self._transform_service = TransformPluginEndpoint()
            path = transform.rsplit('.', 1)
            module = importlib.import_module(path[0])
            transform_impl = getattr(module, path[1])()
            assert isinstance(transform_impl, AbstractTransformPlugin)
            self._transform_service.transform_plugin = transform_impl
            transform_impl.endpoint_service = self._transform_service
        
        st = self._transform_service.get_status().state
        if  st == 'start':
            self.wait_for_state(self._transform_service, 'start', 'started')
        elif st == 'started' or st == 'ready':
            pass
        else:
            assert False, ("Invalid state to start transform: %s" % st)
        
        mistk_input_dirs = []
        for input_dir in input_dirs:
            mistk_input_dir = MistkDataset(object_info=ObjectInfo(name=os.path.basename(os.path.normpath(input_dir))),
                                        data_path=input_dir)
            mistk_input_dirs.append(mistk_input_dir)
        
        mistk_output_dir = MistkDataset(object_info=ObjectInfo(name=os.path.basename(os.path.normpath(output_dir))),
                                        data_path=output_dir)
        ip = TransformSpecificationInitParams(input_datasets=mistk_input_dirs, output_dataset=mistk_output_dir, properties=properties)
        self._transform_service.transform(ip)
        
        self.wait_for_state(self._transform_service, 'transform', 'ready')
        
        
    def evaluate(self, evaluation, assessment_type, metrics_names, input_data_path, input_data_validation_path, evaluation_input_format, gt_path, gt_validation_path, evaluation_path, properties=None):
        """
        Creates a evaluation service wrapper and performs the metrics evaluation
        on the dataset(s) provided.
        
        :param evaluation: The Evaluation that will be formed. Will be one of the following forms:
            - URL of running transform instance (ie. http://localhost:8080)
            - Python package and module (ie. mypackage.mymodule.MyEvaluationPluginClass
        :param assessment_type: The evaluation type. One of {'BinaryClassification', 
        'MultilabelClassification', 'MulticlassClassification', 'Regression'}
        :param metric_names: Specific metrics to evaluate against instead of all metrics defined by assessment_type
        :param input_data_path: Path to input data for the evaluation
        :param input_data_validation_path: Path to input data for the evaluation to be validated
        :param evaluation_input_format: The format of the input data
        :param gt_path: The directory path where the ground_truth.csv file is located
        :param gt_validation_path: The directory path where the ground_truth.csv file will be validated
        :param evaluation_path: A directory path to where all of the output files should be stored
        :param properties: A JSON dictionary of properties relevant to this evaluation
        """
        print('Evaluating...')
        
        # Validate the input ground truth and predictions csv file
        if not validate_groundtruth_csv(gt_validation_path):
            msg = "Failed to validate ground truth csv file at %s" % gt_path
            raise Exception(msg)
        if "predictions" == evaluation_input_format and not validate_predictions_csv(input_data_validation_path):
            msg = "Failed to validate predictions csv file at %s" % input_data_path
            raise Exception(msg)
        
        if evaluation.startswith('http:'):
            self._evaluation_service = evaluation_service_wrapper.EvaluationServiceWrapper(os.path.join(evaluation, 'v1/mistk/evaluation'))
        else:
            self._evaluation_service = EvaluationPluginEndpoint()
            path = evaluation.rsplit('.', 1)
            module = importlib.import_module(path[0])
            evaluation_impl = getattr(module, path[1])()
            assert isinstance(evaluation_impl, AbstractEvaluationPlugin)
            self._evaluation_service.evaluation_plugin = evaluation_impl
            evaluation_impl.endpoint_service = self._evaluation_service
            self._evaluation_service.load_metrics_spec(module)
        
        st = self._evaluation_service.get_status().state
        if  st == 'start':
            self.wait_for_state(self._evaluation_service, 'start', 'started')
        elif st == 'started' or st == 'ready':
            pass
        else:
            assert False, ("Invalid state to start evaluation: %s" % st)

        all_metrics = self._evaluation_service.get_metrics()
        metrics = []
        # get all metrics for assessment type
        if metrics_names is None:
            for metric in all_metrics:
                if assessment_type in metric.assessment_types:
                    metrics.append(metric)
        # get metrics by name for assessment type
        else:
            all_metric_names = []
            for metric in all_metrics:
                all_metric_names.append(metric.object_info.name)
            for metric_name in metrics_names:
                assert metric_name in all_metric_names, ("Invalid metric name: %s . No metric exists with this name." % metric_name)
                metric = all_metrics[all_metric_names.index(metric_name)]
                assert assessment_type in metric.assessment_types, ("Metric %s cannot be evaluated for assessment type %s" % (metric_name, assessment_type))      
                metrics.append(metric)
    
        # evaluate for metrics
        ip = EvaluationSpecificationInitParams(assessment_type, metrics, input_data_path, evaluation_input_format, gt_path, evaluation_path, properties)
        self._evaluation_service.evaluate(ip)        

        self.wait_for_state(self._evaluation_service, 'evaluate', 'ready')
