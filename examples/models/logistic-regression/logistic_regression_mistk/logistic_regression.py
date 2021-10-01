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


# coding=utf8

import os
import pickle
import numpy as np 
import base64, pkg_resources

from sklearn.linear_model import LogisticRegression
from logistic_regression_mistk.dataset_mnist import load_training_data, load_test_data
from mistk.abstract_model import AbstractModel
import mistk.log, logging
logger = mistk.log.get_logger()

class ScikitLearnLogisticRegressionModel(AbstractModel):
    def __init__(self):
        AbstractModel.__init__(self)
        logger.setLevel(logging.DEBUG)
        
        # property attributes
        self._props = None
        self._hparams = None
        self._objectives = None
        
        # the model
        self._regr = None
        
        # the model init parameters
        # lbfgs solver chosen as default for speed over default liblinear
        self._solver = 'lbfgs'  
        self._penality = 'l2'
        self._tolerance = 1e-4
        self._C = 1.0
        self._fit_intercept = True
        self._class_weight = None
        self._max_iter = 100
        self._n_jobs = None
        
        # the data
        # training images
        self._X_train = None
        # training labels
        self._Y_train = None
        # training ids
        self._Z_train = None
        # test images
        self._X_test = None
        # test ids
        self._Z_test = None
        self._data_loaded = False
        
        # saved model file name
        self._model_file_name = 'scikit-logistic-regression-model.bin'

        # prediction attributes
        self._predictions = None
        self._confidence = None
  
    def do_initialize(self, objectives: list, props : dict, hparams : dict):
        logger.debug('do_initialize called')
        self._props = props or {}
        self._hparams = hparams or {}
        self._objectives = objectives
        
        logger.info('properties: ' + str(self._props))
        
        # set model parameters from properties
        if 'model_file_name' in self._props:
            self._model_file_name = self._props['model_file_name']
        if 'solver' in self._props:
            self._solver = self._props['solver']
        if 'penality' in self._props:
            self._penality = self._props['penality']
        if 'tol' in self._props:
            self._tolerance = self._props['tol']
        if 'C' in self._props:
            self._C = self._props['C']
        if 'fit_intercept' in self._props:
            self._fit_intercept = self._props['fit_intercept']   
        if 'class_weight' in self._props:
            self._class_weight = self._props['class_weight']
        if 'max_iter' in self._props:
            self._max_iter = self._props['max_iter']    
        if 'n_jobs' in self._props:
            self._n_jobs = self._props['n_jobs']
        
    def do_load_data(self, dataset_map: dict): 
        logger.debug('do_load_data called')
        # Check for and load training data and/or test data
        if 'train' not in dataset_map and 'test' not in dataset_map:
            raise RuntimeError('No datasets provided')
        # NOTE this model is coded to this particular MNIST dataset format
        if 'train' in dataset_map:
            dataset = dataset_map['train']
            
            train_image, train_label, train_ids = load_training_data(dataset.data_path)
            logger.debug('training label size: ' + str(len(train_label)))
            logger.info('training image size: ' + str(len(train_image)))

            self._X_train = train_image
            self._Y_train = train_label
            self._Z_train = train_ids
            
        if 'test' in dataset_map:
            dataset = dataset_map['test']
            test_image, _, test_ids = load_test_data(dataset.data_path)
            
            logger.info('testing image size: ' + str(len(test_image)))
            
            self._X_test = test_image
            self._Z_test = test_ids

    def do_build_model(self, path=None):
        logger.debug('do_build_model called')
        if path:
            # if we got a path to a saved model then load it
            path = os.path.join(path, self._model_file_name)
            if os.path.exists(path):
                logger.debug("Loading model " + path)
                
                with open(path, mode='rb') as reader:
                    # we decided to use python pickle to save and load
                    # model checkpoints in this model, but other models
                    # are free to use any format they desire
                    self._regr = pickle.load(reader)
                assert isinstance(self._regr, LogisticRegression)
            else:
                logger.debug("Building model")
                # the model initialization w/ parameters
                self._regr = LogisticRegression(solver = self._solver, penalty = self._penality,
                                                tol = self._tolerance, C = self._C,
                                                fit_intercept = self._fit_intercept, class_weight = self._class_weight,
                                                max_iter = self._max_iter, n_jobs = self._n_jobs)
        else:
            logger.debug("Building model")           
            self._regr = LogisticRegression(solver = self._solver, penalty = self._penality,
                                                tol = self._tolerance, C = self._C,
                                                fit_intercept = self._fit_intercept, class_weight = self._class_weight,
                                                max_iter = self._max_iter, n_jobs = self._n_jobs)

    def do_train(self):
        logger.debug("do_train called")
        # train with our previously loaded data
        self._regr.fit(self._X_train, self._Y_train)
        self.update_status({"samples_fit": len(self._X_train)})
    
    def do_save_model(self, path):
        path = os.path.join(path, self._model_file_name)
        logger.info("Saving model to " + path)
        
        # just saving a simple 'pickled' model to disk
        with open(path, mode='wb') as writer:
            writer.write(pickle.dumps(self._regr))
            
    def do_pause(self):
        # this model doesn't support 'pause'
        raise NotImplementedError()

    def do_resume_training(self):
        raise NotImplementedError()
    
    def do_resume_predict(self):
        raise NotImplementedError()
    
    def do_predict(self):
        logger.debug("do_predict called")
        # predict with our previously loaded data
        self._predictions = self._regr.predict(self._X_test)

        # get probability associated with only the predicted value
        class_probs = self._regr.predict_proba(self._X_test)
        pred_conf = []
        for i in range(len(class_probs)):
            pred_conf.append(class_probs[i][self._predictions[i]])
        self._confidence = np.asarray(pred_conf)
        
        # alert sample predicted size
        self.update_status({"samples_predicted": len(self._X_test)})
    
    def do_save_predictions(self, dataPath):
        dataPath = os.path.join(dataPath, "predictions.csv")
        logger.info("Saving predictions to " + dataPath)
        
        with open(dataPath, mode='w') as writer:
            writer.write("id,label,confidence\n")
            for i in range(self._predictions.shape[0]):
                # write out a results csv that can be evaluated
                writer.write(self._Z_test[i] + "," + str(self._predictions[i])
                    + "," + str(self._confidence[i]) + "\n")
                
    def do_stream_predict(self, data_map: dict, details: bool=False):
        # predictions
        predictions = {}
        detailed_data = {}
        for key, value in data_map.items():
            logger.debug('Predicting class for key ' + key)
            # assumes image has already been reshaped appropriately for the model
            image = base64.b64decode(value)
            image = np.frombuffer(image)
            prediction = self._regr.predict([image])
            detailed_data[key] = self._regr.predict_proba([image])
            logger.debug('Predicting: ' + str(prediction))
            predictions[key] = int(prediction[0])
            
        if details:
            # additional details for predictions
            predictions["details"] = self._format_stream_predict_details(predictions, detailed_data)
              
        return predictions
    
        
    def _format_stream_predict_details(self, predictions, prediction_details):
        """
        Format stream predict details in the form of NGX Markdown 
        :param predictions: predictions for each streaming image
        :param prediction_details: prediction probabilities for each streaming image
        
        """
        details = "# ATL Logistic Regression Model Results"
        details += "\nThese section contains details about the **ATL Logistic Regression Model Results**.<br/><br/>"
        details += "<br/><br/>"
        
        metric_image_path = 'metrics-test.png'
        metric_image_data = pkg_resources.ResourceManager().resource_stream(__name__, 'metrics-test.png')
        encoded_bytes = base64.b64encode(metric_image_data.read()).decode('UTF-8')
        details += "\n## Initial Training Results\n"
        details += f"\n![Test](data:image/png;base64,{encoded_bytes})"
        details += "<br/><br/>"
        
        details += "\n## Trained Model Streaming Results"
        details += "<br/><br/>"
        
        for image, preds in prediction_details.items():
            details += f"\n#### For image {image} with prediction of {predictions[image]}"
            details += "\n\n| Class        | Probability |"
            details += "\n| ------------- |:-------------:|"
            for i in range(len(self._regr.classes_)): 
                details += f"\n| {self._regr.classes_[i]}        | {round(preds[0][i], 3)} |"
            details += "\n\n"
    
        
        return details

    def _example_image_reshape(self, image_path):
        """
        Example to reshape image (if needed) for streaming prediction. Must be done to image prior to stream_predict.
        :param image_path: path to image
        """
        
        im = PIL.Image.open(image_path)
        image_data = np.array(im)
        # Convert from [0, 255] -> [0.0, 1.0].
        image = np.multiply(image, 1.0 / 255.0) 
        return image

    def do_generate(self):
        """
        Executes/resumes the generate activity
        This operation is currently not supported. 
        """
        msg = "this model doesn't support 'generate'"
        raise NotImplementedError(msg)
    
    def do_save_generations(self, dataPath):
        """
        Saves the current generations to the location specified
        
        :param dataPath: The location on the local file system or distributed 
            file system where the generations will be saved
        """
        msg = "this model doesn't support 'save_generations'"
        raise NotImplementedError(msg)


    def do_terminate(self):
        pass

    def do_reset(self):
        pass

