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

from mistk.transform.client import ApiClient, Configuration, TransformPluginEndpointApi
from mistk.data import TransformSpecificationInitParams

class TransformServiceWrapper(object):
    """
    A wrapper class for interacting with the TransformPluginEndpointApi
    """
    
    def __init__(self, transform_url):
        """
        Initializes this class and creates the client connection to the 
        TransformPlugin implementation via the TransformPluginEndpointApi
        
        :param transform_url: The URL at which the TransformPlugin instance is running
        """
        ti_api_cfg = Configuration()
        ti_api_cfg.host = transform_url
        tie_api = ApiClient(configuration=ti_api_cfg)
        self._ti_api = TransformPluginEndpointApi(tie_api)
        
    def get_status(self):
        """
        Get the status of the TransformPlugin
        """
        return self._ti_api.get_status()
    
    def terminate(self):
        """
        Initiates shutdown procedures for the TransformPlugin
        """
        self._mi_api.terminate()
        
    def transform(self, init_params: TransformSpecificationInitParams):
        """
        Performs the TransformPlugin's transformation on the parameters
        provided.
        
        :param init_param: An instance of the TransformSpecificationInitParams
            which includes the input directories, output directories, and
            transformation properties
        """
        self._ti_api.transform(init_params=init_params)
        