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

import json
from typing import Union
from mistk import logger
from mistk.data import MistkDataRecordList
from mistk.data.utils import deserialize_model, serialize_model

def validate_json(json_file: str) -> bool:
    """
    Validates a JSON file is MISTK output compliant.
    
    :param json_file: The JSON file to validate
        
    :returns: True if the JSON file is valid, false otherwise
    """
    
    with open(json_file, 'r') as f:
        try:
            data = json.load(f)
            m = deserialize_model(data, MistkDataRecordList)
            if m.items is None:
                logger.warning(f'No items field in file: {json_file}')
                return False
            line = 0
            for item in m.items:
                if item.record_id is None:
                    logger.warning(f'No recordId field for line {line} in file: {json_file}')
                    return False
                if item.values is None:
                    logger.warning(f'No values field for line {line} in file: {json_file}')
                    return False
                line += 1
            return True
        except:
            return False
        
    
    
    
def json_to_mistk_data_record_list(json_file: str) -> MistkDataRecordList:
    """
    Takes a json file and deserializes to a MistkDataRecordList object
    
    :param json_file: The JSON file to convert to MistkDataRecordList object
        
    :returns: MistkDataRecordList object
    """
    with open(json_file, 'r') as f:
        data = json.load(f)
        return deserialize_model(data, MistkDataRecordList)

def mistk_data_record_list_to_json_file(records: MistkDataRecordList, json_file: str, indent: Union[int, str]='0'):
    """
    Takes a MistkDataRecordList object and serializes to a JSON file
    
    :param records: The MistkDataRecordList object to save to a file
    :param json_file: The JSON file to write the MistkDataRecordList object
    :param indent: pretty print indent level, 0 indicates no pretty printing
        
    """
    with open(json_file, 'w') as pred_file:
        if str(indent) == '0':
            pred_file.write(json.dumps(serialize_model(records))) 
        else:
            pred_file.write(json.dumps(serialize_model(records), indent=indent)) 

    