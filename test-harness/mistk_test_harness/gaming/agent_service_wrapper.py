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

from mistk.agent.client import ApiClient, Configuration, AgentInstanceEndpointApi
from mistk.data import AgentInstanceInitParams

class AgentServiceWrapper(object):
    """
    A wrapper class for interacting with the AgentInstanceEndpointApi
    """
    
    def __init__(self, agent_url):
        """
        Initializes this class and creates the client connection to the 
        AbstractModel implementation via the AgentInstanceEndpointApi
        
        :param agent_url: The URL at which the AbstractAgent instance is running
        """
        mi_api_cfg = Configuration()
        mi_api_cfg.host = agent_url
        mie_api = ApiClient(configuration=mi_api_cfg)
        self._mi_api = AgentInstanceEndpointApi(mie_api)

    def initialize_agent(self, initialization_parameters: AgentInstanceInitParams):
        """
        Executes the agent instance's initialize_agent method with the parameters provided
        
        :param initialization_parameters: An instance of the AgentInstanceInitParams
            which includes the objectives, agent hyperparameters, and
            agent properties
        """
        self._mi_api.initialize_agent(initialization_parameters=initialization_parameters)

    def build_model(self, model_path=None):
        """
        Executes the agent instance's build_model method with the input provided
        
        :param model_path: The directory path to where the model's snapshot file can
            be loaded
        """
        self._mi_api.build_model(model_path=model_path)

    def save_model(self, model_path):
        """
        Executes the agent instance's save_model method
        
        :param model_path: The path to which the model checkpoint should be saved.
        """
        self._mi_api.save_model(model_path=model_path)
        
    def reset(self, unload_model):
        """
        Executes the agent instance's reset method
        
        :param unload_model: Unload (reset) the built model or keep the current built model
        """
        self._mi_api.reset(unload_model=unload_model)
        
    def pause(self):
        """
        Executes the agent instance's pause method
        """
        self._mi_api.pause()
    
    def get_status(self):
        """
        Executes the agent instance's get_status method
        """
        return self._mi_api.get_status()
    
    def terminate(self):
        """
        Initiates shutdown procedures for the agent instance 
        """
        self._mi_api.terminate()
