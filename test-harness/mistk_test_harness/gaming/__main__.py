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

import argparse
import json
import re
import sys, os
import logging, traceback

from mistk_test_harness.container import Container
from mistk_test_harness.network import Network
from mistk_test_harness.gaming.test_harness import TestHarness
from mistk_test_harness.gaming.test_harness_config import TestHarnessConfig

parser = argparse.ArgumentParser(description='Test harness for validating gaming orchestrator and agent implementations',
                                prog='python -m mistk_test_harness.gaming',
                                formatter_class=argparse.RawDescriptionHelpFormatter,
                                epilog='Examples: \n' + 
                                'python -m mistk_test_harness.gaming --config /my/config/file \n' 
                                )

parser.add_argument('--config', metavar='FILE',
                    help='Gaming test harness configuration')


args = parser.parse_args()

if not args.config:
    print("Config file for orchestrator and agents required")
    sys.exit()

with open(args.config) as data:
    config_data = data.read()
    
try:
    config = TestHarnessConfig.from_json(config_data)  # @UndefinedVariable
except Exception as e:
    print (f"Error loading config file - {e}")
    sys.exit()

if not config.logs:
    logging.getLogger().setLevel(logging.FATAL)

objectives = []


# Check valid file locations and json files
if config.orchestrator.properties:
    with open(config.orchestrator.properties) as file:
        orch_props = json.load(file)
else:
    orch_props = None

for agent in config.agents:    
    if agent.properties:
        with open(agent.properties) as file:
            json.load(file)   
    if agent.hyperparameters:
        with open(agent.hyperparameters) as file:
            json.load(file)


# Set up the test harness for orchestrator
try:
    orchestrator_container = None  
    agent_containers = []
    network = None      
    network_name = 'mistk'
    if config.orchestrator:
        orch_config = config.orchestrator
        svc = config.orchestrator.service 
        
        # check that only one service type is defined
        svc_types = (svc.url, svc.module, svc.image)
        ct_types = sum(1 for ct in svc_types if ct)
        if ct_types > 1:
            print("Error, for orchestrator service, only one of url, module, and image can be defined")
            sys.exit()
        
        orchestrator = (svc.url or svc.module or svc.image)
        name = svc.container
        port = svc.port
        if not orchestrator:
            print('Please define the image, url, or module for the orchestrator')
            
        episode_save_path = os.path.abspath(orch_config.episode_save_path) if orch_config.episode_save_path else None
        orch_config.episode_save_path = episode_save_path
        
        # Build the docker orchestrator_container for the model
        if not orchestrator.startswith('http:') and re.match('[\w:-]*/[\w:-]*', orchestrator) is not None:    
            volumes = {}
            # for now default to tmp for mount
            volumes['/tmp'] = {'bind': '/tmp', 'mode': 'rw'}
            if episode_save_path:
                volumes[episode_save_path] = {'bind': '/tmp/orch', 'mode': 'rw'}
                episode_save_path = '/tmp/orch'
                orch_config.episode_save_path = episode_save_path
           
            orchestrator_container = Container(orchestrator) 
            # remove previous container if running
            if orchestrator_container.remove(name):
                print(f'Warning - orchestrator {name} container already running; stopping previous container...')
            print('Starting orchestrator_container ' + orchestrator)
            name = orchestrator_container.run(volumes, port, name)
            # network
            network = Network(network_name)
            network.create_network()
            if network.created:
                print(f'Created docker network {network.name}')
            orchestrator_container.add_network(network.network)
            
            orchestrator = f'http://localhost:{port}'
     
    for agent_conf in config.agents:
        svc = agent_conf.service 
        
        # check that only one service type is defined
        svc_types = (svc.url, svc.module, svc.image)
        ct_types = sum(1 for ct in svc_types if ct)
        if ct_types > 1:
            print("Error, for agent service, only one of url, module, and image can be defined")
            sys.exit()
        
        agent = (svc.url or svc.module or svc.image)
        name = svc.container
        port = svc.port
        model_path = os.path.abspath(agent_conf.model_path) if agent_conf.model_path else None
        model_save_path = os.path.abspath(agent_conf.model_save_path) if agent_conf.model_save_path else None
        agent_conf.model_save_path = model_save_path
        
        # Build the docker model_container for the model
        if not agent.startswith('http:') and re.match('[\w:-]*/[\w:-]*', agent) is not None:
            volumes = {}
            if model_save_path:
                volumes[model_save_path] = {'bind': '/tmp/model', 'mode': 'rw'}
                model_save_path = '/tmp/model'
                agent_conf.model_save_path = model_save_path
            if model_path:
                if model_path in volumes:
                    print(f'{agent} - model_path must be unique from model_save_path volume mounting')
                    sys.exit()
                volumes[model_path] = {'bind': '/tmp/checkpoint', 'mode': 'ro'}
                model_path = '/tmp/checkpoint'  
           

            agent_container = Container(agent)            
            # remove previous container if running
            if agent_container.remove(name):
                print(f'Warning - {agent} {name} container already running; stopping previous container...')
            print('Starting agent_container ' + agent)
            name = agent_container.run(volumes, port, svc.container)
            
            # network
            if not network:       
                network = Network(network_name)
                network.create_network()
                if network.created:
                    print(f'Created docker network {network.name}')
            agent_container.add_network(network.network)
            
            # container started, now use url
            svc.url = f'http://localhost:{port}'
            agent_containers.append(agent_container)
    
        #if agent_conf.replay:
        #    objectives.append('replay')
except Exception as ex:
    print('Received the following exception: %s' % ex)
    traceback.print_exc()
    for agent_container in agent_containers:
        if not config.disable_container_shutdown and agent_container:
            print(f'Stopping agent_container {agent_container._container.name} (image: {agent_container._image})')
            agent_container.stop()
            print(f'Container {agent_container._container.name} stopped')
        
    if not config.disable_container_shutdown and orchestrator_container:
        print(f'Stopping orchestrator_container {orchestrator_container._image}')   
        orchestrator_container.stop()
        print(f'Container {orchestrator_container._image} stopped')
        
    if network and network.created:
        network.delete_network()
        print(f'Deleted docker network {network.name}')
    sys.exit() 
    
# Now create test harness and run workflow
harness = TestHarness()
try:
    if orchestrator:
        print('Orchestrator initializing...')
        agents_needed = len(config.agents)
        harness.orchestrator_init(orchestrator, orch_props, agents_needed, config.orchestrator.service.port)
        print('Orchestrator initialized')
        
    # Register agents
    for agent_conf in config.agents:    
        if agent_conf.properties:
            with open(agent_conf.properties) as file:
                agent_props = json.load(file)
        else:
            agent_props = None
            
        if agent_conf.hyperparameters:
            with open(agent_conf.hyperparameters) as file:
                agent_hparams = json.load(file)
        else:
            agent_hparams = None
        agent = (agent_conf.service.url or agent_conf.service.module)
        harness.agent_init(agent, model_path, agent_props, agent_hparams, agent_conf.service.port)
        
        # if not a container (or orchestrator is running locally), make sure localhost is used for registering agent
        if agent_conf.service.container and not config.orchestrator.service.module:
            agent_service_name = agent_conf.service.container
        else:
            agent_service_name = 'localhost'    
        harness.orchestrator_register_agent(agent_conf.name, agent_service_name, agent_conf.service.port, not agent_conf.replay)
    
    # Run each episode
    for i in range(config.orchestrator.episodes):
        harness.orchestrator_ready_to_start_episode()
        cfgs = config.orchestrator.episode_cfgs
        if i < len(cfgs):
            with open(cfgs[i]) as file:
                episode_cfg = json.load(file)
        else:
            episode_cfg = {}
        harness.orchestrator_start_episode(episode_cfg, config.orchestrator.episode_save_path)
        
        harness.orchestrator_stop_episode()
    
    for agent_conf in config.agents:  
        # save model
        if agent_conf.model_save_path:
            harness.agent_save(agent_conf.model_save_path)
        # reset model
        if agent_conf.reset:
            harness.agent_reset(agent_conf.reset)
    
    if config.orchestrator.reset:
        harness.orchestrator_reset()
   
    harness.shutdown()
    print("Completed")
except Exception as ex:
    print('Received the following exception: %s' % ex)
    traceback.print_exc()

    # Save the container logs to a file
    for agent_container in agent_containers:
        output_file = agent_container.save_logs(os.getenv('MISTK_LOG_DIR', '/tmp'))
        print('Agent container logs are available at %s' % output_file)
    if orchestrator_container:
        output_file = orchestrator_container.save_logs(os.getenv('MISTK_LOG_DIR', '/tmp'))
        print('Orchestrator container logs are available at %s' % output_file)
finally:
    for agent_container in agent_containers:
        if not config.disable_container_shutdown and agent_container:
            print(f'Stopping agent_container {agent_container._container.name} (image: {agent_container._image})')
            agent_container.stop()
            print('Container stopped')
        
    if not config.disable_container_shutdown and orchestrator_container:
        print(f'Stopping orchestrator_container {orchestrator_container._image}')   
        orchestrator_container.stop()
        print('Container stopped')
        
    if network and network.created:
        network.delete_network()
        print(f'Deleted docker network {network.name}')
        
        
        
