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
import json

from sklearn.linear_model import LogisticRegression
from logistic_regression_mistk.dataset_mnist import load_training_data, load_test_data
from mistk.abstract_model import AbstractModel
from mistk.data import MistkDataRecordList, MistkDataRecord
from mistk.data.utils import serialize_model
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
        self._max_iter = 1000
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
        dataPath = os.path.join(dataPath, "predictions.json")
        logger.info("Saving predictions to " + dataPath)
        
        recordList = MistkDataRecordList()
        recordList.items = []
        for i in range(self._predictions.shape[0]):
            record = MistkDataRecord(record_id = self._Z_test[i])
            recordValue = {}
            recordValue['label'] = str(self._predictions[i])
            recordValue['confidence'] = str(self._confidence[i])
            record.values = [recordValue]
            recordList.items.append(record)
        # write out a results json that can be evaluated
        with open(dataPath, 'w') as pred_file:
            pred_file.write(json.dumps(serialize_model(recordList), indent=2))  
        
                
    def do_stream_predict(self, data_map: dict):
        predictions = {}
        for key, value in data_map.items():
            logger.debug('Predicting class for key ' + key)
            prediction = self._regr.predict(value.reshape(1, -1))
            logger.debug('Predicting: ' + str(prediction))
            predictions[key] = prediction[0]
        return predictions
    
    def do_update_stream_properties(self, props: dict):
        logger.debug('do_update_stream_properties called')
        logger.debug(f'stream props: {props}')
        self._stream_props = props   
        
    def do_stream_predict_source(self, source: str, format: str, props: dict):
        msg = "this model doesn't support 'stream_predict_source'"
        raise NotImplementedError(msg)

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
    
    def do_miniaturize(self, dataPath, includeHalfPrecision):
        msg = "this model doesn't support 'miniaturize'"
        raise NotImplementedError(msg)
    
    def do_build_ensemble(self, ensemble_path=None, model_paths: dict=None):
        msg = "this model doesn't support 'build_ensemble'"
        raise NotImplementedError(msg)
        