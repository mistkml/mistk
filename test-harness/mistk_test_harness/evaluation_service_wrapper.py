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

from mistk.evaluation.client import ApiClient, Configuration, EvaluationPluginEndpointApi
from mistk.data import EvaluationSpecificationInitParams

class EvaluationServiceWrapper(object):
    """
    A wrapper class for interacting with the EvaluationPluginEndpointApi
    """
    
    def __init__(self, evaluation_url):
        """
        Initializes this class and creates the client connection to the 
        EvaluationPlugin implementation via the EvaluationPluginEndpointApi
        
        :param evaluation_url: The URL at which the EvaluationPlugin instance is running
        """
        ti_api_cfg = Configuration()
        ti_api_cfg.host = evaluation_url
        tie_api = ApiClient(configuration=ti_api_cfg)
        self._ti_api = EvaluationPluginEndpointApi(tie_api)
        
    def get_status(self):
        """
        Get the status of the EvaluationPlugin
        """
        return self._ti_api.get_status()
    
    def terminate(self):
        """
        Initiates shutdown procedures for the EvaluationPlugin
        """
        self._mi_api.terminate()
        
    def evaluate(self, init_params: EvaluationSpecificationInitParams):
        """
        Performs the EvaluationPlugin's evaluation on the parameters
        provided.
        
        :param init_param: An instance of the EvaluationSpecificationInitParams
            which includes the metrics, input (predictions and ground_truth) directories, output directory, and
            evaluation properties
        """
        self._ti_api.evaluate(init_params=init_params)
        
    def get_metrics(self):
        """
        Get the metrics defined for this specific evaluation that can be used to evaluate a model.
        """
    
        return self._ti_api.get_metrics()
        