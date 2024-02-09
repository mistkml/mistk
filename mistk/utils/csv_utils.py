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

import sys, os, csv
from csvvalidator import CSVValidator, write_problems

from mistk import logger


def validate_predictions_csv(file_path):
    """
    Validates a predictions csv file
    
    :param path: The directory or file path where the predictions 
        csv file can be found
    :returns: True if the csv file is valid, false otherwise.
    """
    logger.info("Validating Predictions CSV file at %s" % file_path)
    csv_file = ''
    if os.path.isfile(file_path):
        csv_file = file_path
    elif os.path.isdir(file_path) and os.path.isfile(os.path.join(file_path, "predictions.csv")):
        csv_file = os.path.join(file_path, "predictions.csv")
    else:
        logger.error("No predictions file exists at %s" % file_path)
        return False
    
    return validate_csv(csv_file)

def validate_groundtruth_csv(file_path):
    """
    Validates a ground truth csv file
    
    :param path: The directory or file path where the ground truth 
        csv file can be found
    :returns: True if the csv file is valid, false otherwise. 
    """
    logger.info("Validating Ground Truth CSV file at %s" % file_path)
    csv_file = ''
    if os.path.isfile(file_path):
        csv_file = file_path
    elif os.path.isdir(file_path) and os.path.isfile(os.path.join(file_path, "ground_truth.csv")):
        csv_file = os.path.join(file_path, "ground_truth.csv")
    else:
        logger.error("No groundtruth file exists at %s" % file_path)
        return False
    
    return validate_csv(csv_file)

def validate_csv(csv_file, output_file=None):
    """
    Validates a CSV file.
    
    :param csv_file: The CSV file to validate
    :param output_file: The optional output file to which problems should
        be written
        
    :returns: True if the CSV file is valid, false otherwise
    """
    field_names = _get_header(csv_file)
    
    if field_names:
        validator = CSVValidator(field_names)
        # basic header and record length checks
        validator.add_header_check('EX1', 'bad header')
        validator.add_record_length_check('EX2', 'unexpected record length')
        
        with open(csv_file) as fp:
            data = csv.reader(fp)
            problems = validator.validate(data)
        
            if problems:
                write_problems(problems, output_file or sys.stdout)
                return False
            else:
                return True
    else:
        logger.warning("No header in csv")
        return True
        
def _get_header(csv_file):
    """
    Retireves the header for a CSV file as a list of column names
    if it exists. Otherwise, returns None.
    
    :param csv_file: The path to the CSV file
    
    :returns: A list of header column names
    """    
    with open(csv_file) as fp:
        has_header = csv.Sniffer().has_header(fp.read(2048))
        fp.seek(0)  # Rewind.
        reader = csv.reader(fp)
        # ignore header for now
        if has_header:
            return next(reader)
        else:
            return None