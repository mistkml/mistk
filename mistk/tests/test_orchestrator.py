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

import time
from mistk.agent.client import AgentInstanceEndpointApi
from mistk.orchestrator.client import OrchestratorInstanceEndpointApi
from mistk.watch.wait import wait_for_state
from mistk.clients import get_mistk_agent_client, get_mistk_orchestrator_client



# Example test run of an Orchestrator and single Agent using client APIs
def test_run():
    
    # Orchestrator Client
    domain = 'localhost'
    orchestrator_url = 'http://' + domain + ':8080/v1/mistk/orchestrator'
    o_client = OrchestratorInstanceEndpointApi(get_mistk_orchestrator_client(orchestrator_url))
    print(o_client.api_client.configuration.host)
    print(o_client.get_status().state)
    
    # Agent Client
    domain = 'localhost'
    agent_url = 'http://' + domain + ':8081/v1/mistk/agent'
    agent_client = AgentInstanceEndpointApi(get_mistk_agent_client(agent_url))
    
    # Initialize Agent
    agent_client.initialize_agent({})
    wait_for_state(agent_client, 'initialize_agent', 'initialized')
    
    # Initialize Orchestrator
    o_client.initialize({})
    wait_for_state(o_client, 'initialize', 'waiting_for_agents')
            
    # Build agent
    agent_client.build_model()
    wait_for_state(agent_client, 'build_model', 'initialized')
 
    # Register agent to orchestrator
    agent_name = 'agent1'
    agent_url = 'http://localhost:8081/v1/mistk/agent'
    o_client.register_agent(agent_name, agent_url)
    wait_for_state(o_client, 'register_agent', ['waiting_for_agents', 'ready'])

    # Run episode
    o_client.start_episode({'e':1})
    wait_for_state(o_client, 'start_episode', 'completed_episode')
    
    # Episode completed; stop it
    print('stopping...')
    o_client.stop_episode()
    wait_for_state(o_client, 'stop_episode', 'ready')
    
    print('end')

if __name__ == '__main__':
    test_run()
    