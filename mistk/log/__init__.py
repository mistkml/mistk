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

"""
Logging module that configures the logger used by a specific component in the
MISTK architecture. 
"""

import os
import json
import logging.config
import mistk.cfg as cfg

DEFAULT_CFG_FILE=os.path.join(os.path.dirname(__file__), "../../conf/log_config.json")

def config(component, file = cfg.get("CLUSTER", "mistk.log.config", DEFAULT_CFG_FILE)):
    """
    Loads the logging configuration file for the component.
    
    :param component: The component name to use for the log file name
    :param file: The path to the configuration file that will be loaded. 
        Defaults to the file location defined in the ConfigParser property mistk.log.config
    """
    with open(file) as reader:
        log_config = json.load(reader)
        
    log_path = log_config['handlers']['file_handler']['filename']
    log_name = component + '.log'
    log_config['handlers']['file_handler']['filename'] = os.path.join(log_path, log_name)
    logging.config.dictConfig(log_config)

def get_logger(name=None):
    """
    Retrieves the logger associated with the name provided.
    
    :param name: The name of the logger. Defaults to None
    :return: A python logger. 
    """
    return logging.getLogger(name)