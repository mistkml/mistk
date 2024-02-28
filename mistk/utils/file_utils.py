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

import os
from mistk import logger
from mistk.utils.csv_utils import validate_csv
from mistk.utils.json_utils import validate_json


def validate_predictions(file_path: str) -> bool:
    """
    Validates a predictions file. The predictions file can either have a 
    csv or json extension.
    
    :param path: The directory or file path where the predictions 
        file can be found
    :returns: True if the file is valid, false otherwise.
    """
    
    logger.info("Validating Predictions file at %s" % file_path)
    pred_file = ''
    if os.path.isfile(file_path):
        pred_file = file_path
    elif os.path.isdir(file_path) and os.path.isfile(os.path.join(file_path, "predictions.csv")):
        pred_file = os.path.join(file_path, "predictions.csv")
    elif os.path.isdir(file_path) and os.path.isfile(os.path.join(file_path, "predictions.json")):
        pred_file = os.path.join(file_path, "predictions.json")
    else:
        logger.error("No predictions file exists at %s" % file_path)
        return False
    
    if pred_file.endswith('.csv'):
        valid = validate_csv(pred_file)
    elif pred_file.endswith('.json'):
        valid = validate_json(pred_file)
    else:
        valid = False
    return valid

def validate_groundtruth(file_path: str) -> bool:
    """
    Validates a ground truth file. The ground truth file can either have a 
    csv or json extension.
    
    :param path: The directory or file path where the ground truth 
        file can be found
    :returns: True if the file is valid, false otherwise.
    """
    
    logger.info("Validating Ground Truth file at %s" % file_path)
    pred_file = ''
    if os.path.isfile(file_path):
        pred_file = file_path
    elif os.path.isdir(file_path) and os.path.isfile(os.path.join(file_path, "ground_truth.csv")):
        pred_file = os.path.join(file_path, "ground_truth.csv")
    elif os.path.isdir(file_path) and os.path.isfile(os.path.join(file_path, "ground_truth.json")):
        pred_file = os.path.join(file_path, "ground_truth.json")
    else:
        logger.error("No ground truth file exists at %s" % file_path)
        return False
    
    if pred_file.endswith('.csv'):
        valid = validate_csv(pred_file)
    elif pred_file.endswith('.json'):
        valid = validate_json(pred_file)
    else:
        valid = False
    return valid
    
    