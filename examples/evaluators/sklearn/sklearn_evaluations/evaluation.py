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
import numpy as np
import json
import time

from sklearn.preprocessing import MultiLabelBinarizer

from mistk.evaluation.abstract_evaluation_plugin import AbstractEvaluationPlugin
from mistk.evaluation.util.convert import csv_predictions_to_dataframe, csv_groundtruth_to_dataframe
from mistk import logger

class SklearnEvaluation (AbstractEvaluationPlugin):
    def __init__(self):
        AbstractEvaluationPlugin.__init__(self)
        self._props = None
        self._predictions = None
  
    def do_evaluate(self, assessment_type, metrics, input_data_path, evaluation_input_format, ground_truth_path, evaluation_path, properties):
        """
        Performs metrics' evaluation using the predictions and ground truth files provided.
        Stored the assessment results as a JSON file in the evaluation_path
        
        :param assessment_type: The evaluation assessment type. One of {'BinaryClassification', 
            'MultilabelClassification', 'MulticlassClassification', 'Regression'}
        :param metrics: Specific metrics to evaluate against instead of all metrics defined by assessment_type
        :param input_data_path: Path to input data for the evaluation
        :param evaluation_input_format: The format of the input data
        :param ground_truth_path: The directory path where the ground_truth.csv file is located
        :param evaluation_path: A directory path to where the evaluation.json output file will be stored
        :param properties: A dictionary of key value pairs for evaluation plugin arguments. 
        """
        if evaluation_input_format not in "predictions":
            msg = "EvaluationInputFormat %s is not supported by this Metric Evaluator, only 'predictions' are supported" % evaluation_input_format
            logger.error(msg)
            raise Exception(msg)
 
        # load prediction results
        full_predictions_path = os.path.join(input_data_path, "predictions.csv")
        results_df = csv_predictions_to_dataframe(full_predictions_path)
        
        # load ground truth
        full_ground_truth_path = os.path.join(ground_truth_path, "ground_truth.csv")
        truth_df = csv_groundtruth_to_dataframe(full_ground_truth_path)
        
        # match ground truth to results by id 
        truth_df = truth_df.loc[truth_df['rowid'].isin(results_df['rowid'])]
            
        # sort the rows by id
        results_df.sort_values(by='rowid', inplace=True)
        truth_df.sort_values(by='rowid', inplace=True)
        
        logger.debug('Running for metrics %s' % metrics)
            
        if assessment_type == "MultilabelClassification" or assessment_type == "MulticlassClassification":
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
            
            if 'confidence' in results_df and not results_df['confidence'].hasnans:
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
        elif assessment_type == "Regression":
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
        
        for counter, metric in enumerate(metrics):
            logger.info(metric.package + " : " +  metric.method)
            if metric.package not in modules_cache:
                module = None
                name = metric.package
                try:
                    importlib.invalidate_caches()
                    module = importlib.import_module(name)
                except Exception:
                    logger.exception("Exception importing plugin module " + name)
                if module:
                    modules_cache[metric.package] = module
                else:
                    logger.warn("Cannot load " + metric.package)
                    continue
            else:
                logger.debug("Loading cached module")
                module = modules_cache[metric.package]
                        
            if hasattr(module, metric.method):
                logger.debug("Calling " + metric.method + " in " + metric.package)
                method = getattr(module, metric.method)
                
                args = metric.default_args or {}
                if metric.data_parameters.truth_labels:
                    args[metric.data_parameters.truth_labels] = truth_labels_matrix
                        
                if metric.data_parameters.truth_bounds and not truth_df['bounds'].hasnans:
                    args[metric.data_parameters.truth_bounds] = truth_df['bounds'].values
                    
                if metric.data_parameters.prediction_labels:
                    args[metric.data_parameters.prediction_labels] = results_labels_matrix
                        
                if metric.data_parameters.prediction_scores and 'confidence' in results_df and not results_df['confidence'].hasnans:           
                    args[metric.data_parameters.prediction_scores] = confidence_matrix
                    
                if metric.data_parameters.prediction_bounds and not results_df['bounds'].hasnans:
                    args[metric.data_parameters.prediction_bounds] = results_df['bounds'].values
                                            
                try:
                    evalResult = method(**args)
                except Exception:
                    logger.error("Something bad happened calling " + metric.method, exc_info=True)
                else:
                    logger.debug("Result is " + str(evalResult))
                    if isinstance(evalResult, np.ndarray):
                        # convert to native types
                        evalResultAsList = evalResult.tolist()
                        if assessment_type == "MultilabelClassification" or assessment_type == "MulticlassClassification":
                            # map labels to their values in the results
                            label_classes = label_mlb.classes_.tolist()
                            if len(evalResultAsList) == len(label_classes):
                                evalResultAsDict = {}
                                for index, label in enumerate(label_classes):
                                    evalResultAsDict[str(label)] = evalResultAsList[index]
                                eval_dict[metric.object_info.name] = evalResultAsDict
                            else:
                                eval_dict[metric.object_info.name] = evalResultAsList
                        else:
                            eval_dict[metric.object_info.name] = evalResultAsList
                    elif isinstance(evalResult, np.generic):
                        # convert to native type
                        evalResultAsScalar = np.asscalar(evalResult)
                        eval_dict[metric.object_info.name] = evalResultAsScalar
                    elif isinstance(evalResult, tuple) or isinstance(evalResult, list):
                        # kind of a cheat to cover the case where a native type has numpy elements
                        # which some scikit-learn methods inexplicably return
                        eval_dict[metric.object_info.name] = np.array(evalResult).tolist()
                    else:
                        eval_dict[metric.object_info.name] = evalResult
            else:
                logger.warn(metric.method + " does not exist in " + metric.package)  
                
            logger.info("Completed metric " + str(counter + 1))
                
        eval_dict_json = json.dumps(eval_dict, indent=2) 
        filename = evaluation_path + "/eval_results_" + str(int(time.time())) + ".json"
        logger.info("Writing eval results to " + filename) 
        with open(filename, mode='w') as writer:
            writer.write(eval_dict_json)
    
    def do_terminate(self):
        AbstractEvaluationPlugin.do_terminate(self)
