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
import os
import time

from mistk.data import AgentInstanceInitParams, OrchestratorInstanceInitParams
from mistk.agent.service import AgentInstanceEndpoint
from mistk.agent.abstract_agent import AbstractAgent
from mistk.orchestrator.service import OrchestratorInstanceEndpoint
from mistk.orchestrator.abstract_orchestrator import AbstractOrchestrator
from mistk_test_harness.gaming import agent_service_wrapper, orchestrator_service_wrapper

class TestHarness(object):

    def __init__(self):
        """
        Initializes the test harness
        """
        self._agent_service = None
        self._orchestrator_service = None
        self._status_version = 0
        
        self._processes = []

    def agent_init(self, agent, model_path=None, model_props=None, hyperparams=None, port=8081):
        """
        Instantiate agent or remote endpoint wrapper.
        Call initialize and build_model on agent.
        Output agent status.

        :param agent: agent module/package or service endpoint URL
        :param model_path: local folder path of saved model files
        :param model_props: A JSON dictionary of model properties to override.
        :param hyperparams: A JSON dictionary of model hyperparameters to override. 
        :param port: service endpoint port if using module/package  
        """        
        if agent.startswith('http:'):
            self._agent_service = agent_service_wrapper.AgentServiceWrapper(os.path.join(agent, 'v1/mistk/agent'))
        else:
            self._agent_service = AgentInstanceEndpoint()
            path = agent.rsplit('.', 1)
            module = importlib.import_module(path[0])
            agent_impl = getattr(module, path[1])()
            self._agent_service.agent = agent_impl
            assert isinstance(agent_impl, AbstractAgent)
            agent_impl.endpoint_service = self._agent_service
            process = self._agent_service.start_server(process=True)  
            self._processes.append(process)  
            self._agent_service = agent_service_wrapper.AgentServiceWrapper(os.path.join(f'http://localhost:{port}', 'v1/mistk/agent'))
                
        ip = AgentInstanceInitParams(model_properties=model_props, hyperparameters=hyperparams)
        self._agent_service.initialize_agent(ip)
        self.wait_for_state(self._agent_service, 'initialize', 'initialized')
        
      
        self._agent_service.build_model(model_path)
        self.wait_for_state(self._agent_service, 'build_model', 'initialized')
        

    def agent_save(self, model_save_path=None):
        """
        Call save_model on the agent.
        Output agent status.
        
        :param model_save_path: The path to which the final model checkpoint/snapshot should be saved.
        """       
        
        if model_save_path:
            self._agent_service.save_model(model_save_path)
            self.wait_for_state(self._agent_service, 'save_model', ['initialized','ready'])

    def agent_reset(self, unload_model=True):
        """
        Call reset on the agent.
        Output agent status.
        
        :param unload_model: Unload (reset) the built model or keep the current built model
        """       

        self._agent_service.reset(unload_model)
        self.wait_for_state(self._agent_service, 'reset', ['initialized','started'])
            
    
    def wait_for_state(self, service, stage, state):
        """
        Waits for a model or transform service wrapper to change their 
        state to the desired state
        
        :param service: The model, transform, evaluation, agent, or orchestrator service to get status for
        :param stage: The current stage of the container
        :param state: The desired state of the container        
        """
        print(f'Called \'{stage}\' on container, waiting for state change to \'{state}\'')
        status_version = 0
        initial_delay = 1
        delay = .5
        time.sleep(initial_delay)
        st = service.get_status()
        while status_version == st.object_info.resource_version:
            time.sleep(delay)
            st = service.get_status()
        
        if isinstance(state, str):
            state = [state]
        
        while not st.state in state and not st.state == 'failed':
            if status_version != st.object_info.resource_version:
                print('Endpoint state: %s (%s)' % (st.state, str(st.payload)))
                status_version = st.object_info.resource_version
            time.sleep(delay)
            st = service.get_status()
            
        print('Endpoint state: %s' % st.state)
        status_version = st.object_info.resource_version
        
        if st.state == 'failed':
            msg = 'Endpoint in failed state, exiting'
            print(msg)
            raise Exception(msg)
    
    
    def orchestrator_init(self, orchestrator, env_props=None, agents_needed=1, port=8080):
        """
        Instantiate orchestrator or remote endpoint wrapper.
        Call initialize on orchestrator.
        Output orchestrator status.

        :param orchestrator: orchestrator module/package or service endpoint URL
        :param env_props: A JSON dictionary of env properties to override. 
        :param agents_needed: number of agents required to start an episode
        :param port: service endpoint port if using module/package 
        """       
        print(orchestrator) 
        if orchestrator.startswith('http:'):
            self._orchestrator_service = orchestrator_service_wrapper.OrchestratorServiceWrapper(os.path.join(orchestrator, 'v1/mistk/orchestrator'))
        else:
            self._orchestrator_service = OrchestratorInstanceEndpoint()
            path = orchestrator.rsplit('.', 1)
            module = importlib.import_module(path[0])
            orch_impl = getattr(module, path[1])()
            self._orchestrator_service.orchestrator = orch_impl
            assert isinstance(orch_impl, AbstractOrchestrator)
            orch_impl.endpoint_service = self._orchestrator_service
            process = self._orchestrator_service.start_server(process=True)
            self._processes.append(process)
            self._orchestrator_service = orchestrator_service_wrapper.OrchestratorServiceWrapper(os.path.join(f'http://localhost:{port}', 'v1/mistk/orchestrator'))
  
        if env_props is None:
            env_props = {}
                
        ip = OrchestratorInstanceInitParams(env=env_props,agents_needed=agents_needed)
        self._orchestrator_service.initialize(ip)
        self.wait_for_state(self._orchestrator_service, 'initialize', 'waiting_for_agents')
        
    
    def orchestrator_register_agent(self, agent_name, agent_service_name, agent_service_port, skip_train=False):
        agent_url = f'{agent_service_name}:{agent_service_port}'
        agent_url = os.path.join('http://', agent_url, 'v1/mistk/agent')
        print(f'registering agent: {agent_name} at {agent_url}')
        self._orchestrator_service.register_agent(agent_name, agent_url, skip_train)
        self.wait_for_state(self._orchestrator_service, 'registering_agent', ['waiting_for_agents', 'ready'])
    
    def orchestrator_ready_to_start_episode(self):    
        self.wait_for_state(self._orchestrator_service, 'registering_agent', 'ready')
           
    def orchestrator_start_episode(self, episodeCfg, episode_save_path=None):    
        self._orchestrator_service.start_episode(episodeCfg)
        self.wait_for_state(self._orchestrator_service, 'start_episode', 'completed_episode')
        if episode_save_path:
            self._orchestrator_service.save_episode(episode_save_path)
            self.wait_for_state(self._orchestrator_service, 'save_episode', 'completed_episode')
    
    def orchestrator_stop_episode(self):    
        self._orchestrator_service.stop_episode()
        self.wait_for_state(self._orchestrator_service, 'stop_episode', 'ready')
    
    def orchestrator_reset(self):
        """
        Call reset on the orchestrator.
        Output orchestrator status.
        """ 

        self._orchestrator_service.reset()
        self.wait_for_state(self._orchestrator_service, 'reset', 'uninitialized')
        
    def shutdown(self):
        for process in self._processes:
            process.terminate()
            
        
    