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
import sys
import os.path, shutil
from pathlib import Path
from configparser import ConfigParser
from mistk import logger
from mistk.model.client import Metric, MistkMetric
import mistk.data.utils as datautils

class EREPluginManager(object):
        
    def __init__(self, module):  
        self._metric_dict = {}
        self._metric_list = []
        self._default_metrics = {}
        self._plugins_path = ''
        
        self._module_loaded = module
        path = Path(module.__file__)
        self._module_directory = path.parent

        self.reload()
                    
    def get_default_metrics_list(self, assessment_type):
        return self._default_metrics.get(assessment_type, [])
    
    def get_metrics_list(self):
        return self._metric_list
        
    def get_object_for_metric(self, metric):
        return self._metric_dict.get(metric, None)
    
    def get_plugin(self, name):
        try:
            importlib.invalidate_caches()
            return importlib.import_module(name)
        except Exception as e:
            logger.exception("Exception importing plugin module " + name)
            return None
        
    def reload(self):
        new_path = self._get_metrics_uri()
        if new_path != self._plugins_path:
            self._plugins_path = new_path
            sys.path.append(new_path)
    
        self._read_metrics(new_path)
    
    def _get_metrics_uri(self):
        return os.path.join(self._module_directory, "metrics.json")
    
    def _read(self, path, **kwargs):
        return open(path, mode='r', **kwargs)
             
    def _read_metrics(self, uri):
        if not os.path.exists(uri):
            logger.warn("Plugin defaults file does not exist at %s."
                        "It will now be created and populated with"
                        " default values", uri)
            os.makedirs(os.path.dirname(uri),exist_ok=True)
            src=os.path.join(os.path.dirname(__file__), "metrics.json")
            shutil.copy(src, uri)
        
        with self._read(uri) as reader:
            metric_dict_list = json.load(reader)
            self._default_metrics = metric_dict_list
            
            for metric_dict in metric_dict_list:
                logger.info('metric json loading: ' + str(metric_dict))
                metric_object = datautils.deserialize_model(metric_dict, MistkMetric)
                logger.info('metric loaded: ' + str(metric_object))
                if metric_object.package and metric_object.method:
                    self._metric_dict[metric_object.package + '.' + metric_object.method] = metric_object
                else:
                    self._metric_dict[metric_object.object_info.name] = metric_object
                self._metric_list.append(metric_object)
    
        logger.info('Metrics loaded.')
  
