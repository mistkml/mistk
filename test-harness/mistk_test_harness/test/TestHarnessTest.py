'''
Created on Feb 07, 2019

@author: tsiedlec
'''
import unittest

import os
import glob
import logging

from mistk_test_harness.test_harness import TestHarness
from mistk_test_harness.container import Container

class TestHarnessTest(unittest.TestCase):


    def setUp(self):
        self.harness = TestHarness()
        self.model_file = 'scikit-logistic-regression-model.bin'
        
    def tearDown(self):
        pass

    def test_01_LogitTrainModel(self):
        logging.info("\nStarting LogisticRegression Model Train test")
                      
        # setup model parameters        
        dataset_map = {}
        objectives = []

        # volume for image
        volumes = {}
        model_train_data_path = '/tmp/train'
        volumes[model_train_data_path] = {'bind': '/tmp/train', 'mode': 'ro'}
  
        model_save_path = '/tmp/model'
        volumes[model_save_path] = {'bind': '/tmp/model', 'mode': 'rw'}
              
        dataset_map['train'] = model_train_data_path
        objectives.append('training')
        
        model = 'logistic_regression_mistk.logistic_regression.ScikitLearnLogisticRegressionModel'
        logging.info('Starting model %s' % model)
        
        try:
            # initialize model
            self.harness.model_init(model, objectives, dataset_map)

            # train model
            self.harness.model_train(model_save_path)
        except Exception as ex:
            logging.exception(str(ex))
       
        model_saved = os.path.join(model_save_path, self.model_file) 
        self.assertTrue(os.path.exists(model_saved), 'Trained model was not saved to the file %s' % model_saved)
    
    def test_02_LogitTestModel(self):
        logging.info("\nStarting LogisticRegression Model Test test")
                      
        # setup model parameters        
        dataset_map = {}
        objectives = []

        # volume for image
        volumes = {}
        model_test_data_path = '/tmp/train'
        volumes[model_test_data_path] = {'bind': '/tmp/train', 'mode': 'ro'}
  
        model_save_path = '/tmp/model'
        volumes[model_save_path] = {'bind': '/tmp/model', 'mode': 'rw'}
              
        dataset_map['test'] = model_test_data_path
        objectives.append('prediction')
        
        model = 'logistic_regression_mistk.logistic_regression.ScikitLearnLogisticRegressionModel'
        logging.info('Starting model %s' % model)
        
        try:
            # initialize model
            self.harness.model_init(model, objectives, dataset_map, model_path=model_save_path)
    
            # test model
            self.harness.model_predict(model_save_path)
        except Exception as ex:
            logging.exception(str(ex))
       
        #self.assertTrue(len(eval_records.items) > 0, "Did not receive the expected number of evaluation set records, received %s" % str(len(eval_records.items)))
        preds_saved = os.path.join(model_save_path, 'predictions.csv') 
        self.assertTrue(os.path.exists(preds_saved), "Predictions from model was not saved to the file %s" % preds_saved)
    

    def test_03_GroundTruthTransform(self):
        logging.info("\nStarting Ground Truth Transform test")
        
        # volume for image 
        volumes = {}
        # Configure the input directories  
        input_dirs = []
        transform_input_paths = []
        transform_input_paths.append('/tmp/train')
#         for dir_path in transform_input_paths:
#             base_name = os.path.basename(os.path.normpath(dir_path))
#             volumes[dir_path] = {'bind': '/tmp/input/%s' % base_name, 'mode': 'ro'}
#             input_dirs.append('/tmp/input/%s' % base_name)
#         transform_input_paths = input_dirs
        # Configure the output directories
        
        transform_output_path = '/tmp/model'
        volumes[transform_output_path] = {'bind': '/tmp/model', 'mode': 'rw'}
        
        transform = 'groundtruth_mnist.groundtruth_mnist_plugin.ground_truth_transform'
        logging.info('Starting transform %s' % transform)
           
        try:
            # transform
            logging.info('Performing data transformation')
            self.harness.transform(transform, transform_input_paths, transform_output_path, None)
            logging.info('Data transformation is complete, output data can be found at %s' % transform_output_path)

        except Exception as ex:
            logging.exception(str(ex))
    
    
    def test_04_LogitEvaluateModel(self):
        logging.info("\nStarting LogisticRegression Model Evaluation test")
                      
        # setup eval parameters        
        assessment_type = 'MulticlassClassification'
        
        # volume for image 
        volumes = {}
        model_data_path = '/tmp/model'
        volumes[model_data_path] = {'bind': '/tmp/model', 'mode': 'rw'}
        
        evaluation = 'sklearn_evaluations.evaluation.SklearnEvaluation'
        logging.info('Starting evaluation %s' % evaluation)
        
        try:
            # evaluate model
            self.harness.evaluate(evaluation, assessment_type, None, model_data_path, model_data_path, 'predictions', model_data_path, model_data_path, model_data_path)

        except Exception as ex:
            logging.exception(str(ex))
       
        eval_saved = glob.glob(model_data_path + '/eval*.json')
        self.assertTrue(eval_saved, "Metrics json file from evaluation was not saved to the folder %s" % model_data_path)
    
 

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
