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
import sys
import time

from mistk.abstract_model import AbstractModel
from mistk.data import ModelInstanceInitParams, MistkDataset, ObjectInfo
from mistk.service import ModelInstanceEndpoint
from mistk_test_harness import model_service_wrapper

class TestHarness(object):

    def __init__(self):
        self._model_service = None
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
        self.wait_for_state('initialize', 'initialized')
        
        self._model_service.build_model(model_path)
        self.wait_for_state('build_model', 'ready')
        
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
            self.wait_for_state('load_data', 'ready')  

    def model_train(self, model_path=None):
        """
        Call train and, if model_path is supplied, save_model on model.
        Output model status.
        """       
        self._model_service.train()
        self.wait_for_state('train', 'ready')
        
        if model_path:
            self._model_service.save_model(model_path)
            self.wait_for_state('save_model', 'ready')

    def model_predict(self, predictions_path=None):
        """
        Call predict and, if prediction_path is supplied, save_predictions on model.
        Output model status.
        """
        self._model_service.predict()
        self.wait_for_state('predict', 'ready')
        
        if predictions_path:
            dataset = MistkDataset(object_info=ObjectInfo(name='predictions-data'),
                                        data_path=predictions_path)
            self._model_service.save_predictions(dataset)
            self.wait_for_state('save_predictions', 'ready')
            
    def model_stream_predict(self, stream_input):
        """
        Call stream_predict with supplied stream_input.
        Output model predictions.
        """
        predictions = self._model_service.stream_predict(stream_input)
        print('Stream prediction results:')
        print(predictions)
        
    def wait_for_state(self, stage, state):
        print('Called \'' + stage + '\' on model, waiting for state change to \'' + state + '\'')
        time.sleep(1)
        st = self._model_service.get_status()
        while self._status_version == st.object_info.resource_version:
            time.sleep(1)
            st = self._model_service.get_status()
            
        while not st.state == state and not st.state == 'failed':
            if self._status_version != st.object_info.resource_version:
                print('Model state: %s (%s)' % (st.state, str(st.payload)))
                self._status_version = st.object_info.resource_version
            time.sleep(1)
            st = self._model_service.get_status()
            
        print('Model state: %s' % st.state)
        self._status_version = st.object_info.resource_version
        
        if st.state == 'failed':
            print('Model in failed state, exiting')
            sys.exit()
