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
from configparser import ConfigParser
import logging

DEFAULT_CFG_FILE=os.path.join(os.path.dirname(__file__), "../../conf/mistk_config.ini")

def get_config(file = os.getenv("MISTK_CONFIG_FILE", DEFAULT_CFG_FILE)) -> ConfigParser:
    """
    Retrieves a ConfigParser that has a MISTK Config file loaded. 
    
    :param file: The path to the configuration file that will be loaded. Defaults to the file
        location defined by the environment variable MISTK_CONFIG_FILE
    :return: A ConfigParser with loaded configuration file. 
    """
    if not file:
        logging.warning("No MISTK_CONFIG_FILE defined.")
        return
    
    config = ConfigParser()
    config.read(file)
    return config

def get(section, key, fallback=None):
    """
    Retrieves the configuration property with the key provided in the section specified
    
    :param section: The section of the ConfigParser in which to search for the property key
    :param key: The property key
    :param fallback: The fall back value of the property to return if the key does not exist. Defaults to None. 
    :return: The property value if it exists, None otherwise. 
    """
    config = get_config()
    if config:
        return config.get(section, key, fallback=fallback)
    else:
        return None

