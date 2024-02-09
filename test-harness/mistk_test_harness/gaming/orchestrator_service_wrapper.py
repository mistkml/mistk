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

from mistk.orchestrator.client import ApiClient, Configuration, OrchestratorInstanceEndpointApi
from mistk.data import OrchestratorInstanceInitParams

class OrchestratorServiceWrapper(object):
    """
    A wrapper class for interacting with the OrchestratorInstanceEndpointApi
    """
    
    def __init__(self, orch_url):
        """
        Initializes this class and creates the client connection to the 
        AbstractOrchestrator implementation via the OrchestratorInstanceEndpointApi
        
        :param orch_url: The URL at which the AbstractOrchestrator instance is running
        """
        mi_api_cfg = Configuration()
        mi_api_cfg.host = orch_url
        mie_api = ApiClient(configuration=mi_api_cfg)
        self._mi_api = OrchestratorInstanceEndpointApi(mie_api)

    def initialize(self, initialization_parameters: OrchestratorInstanceInitParams):
        """
        Executes the orchestrators instance's initialize method with the parameters provided
        
        :param initialization_parameters: An instance of the OrchestratorInstanceInitParams
            which includes the objectives and orchestrators properties
        """
        self._mi_api.initialize(initialization_parameters=initialization_parameters)        
    
    def register_agent(self, agent_name, agent_url, skip_train):
        """
        Executes the orchestrators instance's register_agent method with the input provided
        
        :param agent_name: The name of the agent
        :param agent_url: The agent URL
        :param skip_train: Pass `true` if we should NOT train the given agent
        """
        self._mi_api.register_agent(agent_name, agent_url, skip_train=skip_train)
        
    def start_episode(self, episode_cfg):
        """
        Executes the orchestrators instance's start_episode method with the input provided
        
        :param episode_cfg: Episode configuration dictionary
        """
        self._mi_api.start_episode(episode_cfg)
        
    def save_episode(self, path):
        """
        Executes the orchestrators instance's save_episode method
        """
        self._mi_api.save_episode(path)
        
    def stop_episode(self):
        """
        Executes the orchestrators instance's stop_episode method
        """
        self._mi_api.stop_episode()
        
    def reset(self):
        """
        Executes the orchestrators instance's reset method
        """
        self._mi_api.reset()

    def pause(self):
        """
        Executes the orchestrators instance's pause method
        """
        self._mi_api.pause()
    
    def get_status(self):
        """
        Executes the orchestrators instance's get_status method
        """
        return self._mi_api.get_status()
    
    def terminate(self):
        """
        Initiates shutdown procedures for the orchestrators instance 
        """
        self._mi_api.terminate()
