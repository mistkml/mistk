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
import json
import logging
import os
import time
import pandas
import numpy as np
from io import StringIO
from sklearn.preprocessing import MultiLabelBinarizer

import mistk.data.utils as utils
from mistk.data import Metric

def perform_assessment(eval_type, predictions_path, ground_truth_path):
    full_predictions_path = os.path.join(predictions_path, "predictions.csv")
    logging.info("Reading results from " + full_predictions_path)
    with open(full_predictions_path) as reader:
        results_csv = reader.read()
    
    full_ground_truth_path = os.path.join(ground_truth_path, "ground_truth.csv")
    logging.info("Reading ground truth from " + full_ground_truth_path)
    with open(full_ground_truth_path) as reader:
        truth_csv = reader.read()     
        
    results_df = pandas.read_csv(StringIO(results_csv), header=None, names=['rowid', 'labels', 'confidence', 'bounds'])
    truth_df = pandas.read_csv(StringIO(truth_csv), header=None, names=['rowid', 'labels', 'bounds'])
    
    # sort the rows by id
    results_df.sort_values(by='rowid', inplace=True)
    truth_df.sort_values(by='rowid', inplace=True)
    
    if eval_type == "MultilabelClassification" or eval_type == "MulticlassClassification":
        # create matrices for labels and confidence
        label_mlb = MultiLabelBinarizer()
        parsed_truth_labels = (truth_df['labels'].str.split().values.tolist()
                               if truth_df['labels'].dtype == 'object' 
                               else np.array(np.transpose(np.matrix(truth_df['labels'].values))))
        parsed_results_labels = (results_df['labels'].str.split().values.tolist()
                                 if results_df['labels'].dtype == 'object' 
                                 else np.array(np.transpose(np.matrix(results_df['labels'].values))))
        label_mlb.fit(np.append(parsed_truth_labels, parsed_results_labels, axis=0))
        truth_labels_matrix = label_mlb.transform(parsed_truth_labels)
        results_labels_matrix = label_mlb.transform(parsed_results_labels)
        
        if not results_df['confidence'].hasnans:
            parsed_confidence = (results_df['confidence'].str.split().values.tolist()
                                 if results_df['confidence'].dtype == 'object' 
                                 else np.array(np.transpose(np.matrix(results_df['confidence'].values))))
            confidence_matrix = np.empty(results_labels_matrix.shape)
            label_classes = label_mlb.classes_.tolist()
            for row_index, row in enumerate(parsed_results_labels):
                confidence_row = np.zeros(results_labels_matrix.shape[1])
                for col_index, col in enumerate(row):
                    label_pos = label_classes.index(col)
                    confidence_row[label_pos] = np.float64(parsed_confidence[row_index][col_index])  #pylint: disable=no-member
                confidence_matrix[row_index] = confidence_row
    elif eval_type == "Regression":
        if truth_df['labels'].dtype == 'object':
            truth_labels_matrix = truth_df['labels'].str.split().values.tolist()
            for index, item in enumerate(truth_labels_matrix):
                truth_labels_matrix[index] = np.array(item, dtype=np.float64)  #pylint: disable=no-member
        else:
            truth_labels_matrix = truth_df['labels'].values
            
        if results_df['labels'].dtype == 'object':
            results_labels_matrix = results_df['labels'].str.split().values.tolist()
            for index, item in enumerate(results_labels_matrix):
                results_labels_matrix[index] = np.array(item, dtype=np.float64)  #pylint: disable=no-member
        else:
            results_labels_matrix = results_df['labels'].values
            
        if results_df['confidence'].dtype == 'object':
            confidence_matrix = results_df['confidence'].str.split().values.tolist()
            for index, item in enumerate(confidence_matrix):
                confidence_matrix[index] = np.array(item, dtype=np.float64)  #pylint: disable=no-member
        else:
            confidence_matrix = results_df['confidence'].values
    else:
        truth_labels_matrix = (truth_df['labels'].str.split().values.tolist()
                               if truth_df['labels'].dtype == 'object' 
                               else truth_df['labels'].values)
        results_labels_matrix = (results_df['labels'].str.split().values.tolist() 
                                 if results_df['labels'].dtype == 'object' 
                                 else results_df['labels'].values)
        confidence_matrix = (results_df['confidence'].str.split().values.tolist() 
                             if results_df['confidence'].dtype == 'object' 
                             else results_df['confidence'].values)
    
    eval_dict = {}
    modules_cache = {}
    
    with open(os.path.join(os.path.dirname(__file__), 'defaults.json')) as reader:
        default_metrics = json.load(reader)
        
    metric_objects = {}
    with open(os.path.join(os.path.dirname(__file__), 'metrics.json')) as reader:
        metric_dict_list = json.load(reader)
    for metric_dict in metric_dict_list:
        metric_object = utils.deserialize_model(metric_dict, Metric)
        metric_objects[metric_object.package + '.' + metric_object.method] = metric_object
        
    metrics_list = []
    for metric_name in default_metrics.get(eval_type, []):
        metric_object = metric_objects.get(metric_name, None)
        if metric_object:
            metrics_list.append(metric_object)
    
    for counter, metric in enumerate(metrics_list):
        logging.info(metric.package + " : " +  metric.method)
        if metric.package not in modules_cache:
            module = importlib.import_module(metric.package)
            if module:
                modules_cache[metric.package] = module
            else:
                logging.warn("Cannot load " + metric.package)
                continue
        else:
            logging.debug("Loading cached module")
            module = modules_cache[metric.package]
            
        if hasattr(module, metric.method):
            logging.debug("Calling " + metric.method + " in " + metric.package)
            method = getattr(module, metric.method)
            
            args = metric.default_args or {}
            if metric.data_parameters.truth_labels:
                args[metric.data_parameters.truth_labels] = truth_labels_matrix
                    
            if metric.data_parameters.truth_bounds and not truth_df['bounds'].hasnans:
                args[metric.data_parameters.truth_bounds] = truth_df['bounds'].values
                
            if metric.data_parameters.prediction_labels:
                args[metric.data_parameters.prediction_labels] = results_labels_matrix
                    
            if metric.data_parameters.prediction_scores and not results_df['confidence'].hasnans:           
                args[metric.data_parameters.prediction_scores] = confidence_matrix
                
            if metric.data_parameters.prediction_bounds and not results_df['bounds'].hasnans:
                args[metric.data_parameters.prediction_bounds] = results_df['bounds'].values
                                        
            try:
                evalResult = method(**args)
            except Exception:
                logging.error("Something bad happened calling " + metric.method, exc_info=True)
            else:
                logging.debug("Result is " + str(evalResult))
                if isinstance(evalResult, np.ndarray):
                    # convert to native types
                    evalResultAsList = evalResult.tolist()
                    if eval_type == "MultilabelClassification" or eval_type == "MulticlassClassification":
                        # map labels to their values in the results
                        label_classes = label_mlb.classes_.tolist()
                        if len(evalResultAsList) == len(label_classes):
                            evalResultAsDict = {}
                            for index, label in enumerate(label_classes):
                                evalResultAsDict[label] = evalResultAsList[index]
                            eval_dict[metric.method] = evalResultAsDict
                        else:
                            eval_dict[metric.method] = evalResultAsList
                    else:
                        eval_dict[metric.method] = evalResultAsList
                elif isinstance(evalResult, np.generic):
                    # convert to native type
                    evalResultAsScalar = np.asscalar(evalResult)
                    eval_dict[metric.method] = evalResultAsScalar
                elif isinstance(evalResult, tuple) or isinstance(evalResult, list):
                    # kind of a cheat to cover the case where a native type has numpy elements
                    # which some scikit-learn methods inexplicably return
                    eval_dict[metric.method] = np.array(evalResult).tolist()
                else:
                    eval_dict[metric.method] = evalResult
        else:
            logging.warn(metric.method + " does not exist in " + metric.package)  
            
        logging.info("Completed metric " + str(counter + 1))
            
    eval_dict_json = json.dumps(eval_dict, indent=2) 
    filename = predictions_path + "/eval_results_" + str(int(time.time())) + ".json"
    logging.info("Writing eval results to " + filename) 
    with open(filename, mode='w') as writer:
        writer.write(eval_dict_json)
