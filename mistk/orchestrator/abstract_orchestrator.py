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

from transitions.extensions import LockedMachine as Machine
from transitions import State

from abc import ABCMeta, abstractmethod

from mistk.orchestrator.service import OrchestratorInstanceEndpoint
from mistk import logger

from mistk.agent.client import AgentInstanceEndpointApi
from mistk.clients import get_mistk_agent_client

import os
import sys

# The orchestrator states
_orchestrator_states = {'uninitialized', 'failed', 'initializing', 'waiting_for_agents',
                        'registering_agent', 'ready', 'running',
                        'completed_episode', 'stopping_episode',
                        'saving_episode', 'resetting',
                        'terminating', 'terminated'}

class AbstractOrchestrator (metaclass=ABCMeta):
    """
    The definition of an abstract Orchestrator to be implemented by Orchestrator
    developers.
    """

    @abstractmethod
    def __init__(self):
        """
        Initializes the Orchestrator and registers the default state machine transitions
        available to all orchestrators.
        """
        self.state = None
        self._endpoint_service = None
        states = [State(n, on_enter='new_state_entered') for n in _orchestrator_states]
        self._machine = Machine(model=self, states=states, initial='uninitialized', auto_transitions=False)
        self._machine.add_transition(trigger='uninitialized', source='resetting', dest='uninitialized')
        self._machine.add_transition(trigger='fail', source=list(_orchestrator_states-{'terminated'}), dest='failed')
        self._machine.add_transition(trigger='initialize', source='uninitialized', dest='initializing', after='_do_initialize')
        self._machine.add_transition(trigger='waiting_for_agents', source=['initializing', 'registering_agent'], dest='waiting_for_agents')
        self._machine.add_transition(trigger='register_agent', source=['waiting_for_agents'], dest='registering_agent', after='_do_register_agent')
        self._machine.add_transition(trigger='ready', source=['registering_agent', 'stopping_episode'], dest='ready')
        self._machine.add_transition(trigger='start_episode', source='ready', dest='running', after='_do_start_episode')
        self._machine.add_transition(trigger='completed_episode', source=['running', 'saving_episode'], dest='completed_episode')
        self._machine.add_transition(trigger='stop_episode', source='completed_episode', dest='stopping_episode', after='_do_stop_episode')
        self._machine.add_transition(trigger='save_episode', source='completed_episode', dest='saving_episode', after='_do_save_episode')
        self._machine.add_transition(trigger='reset', source=list(_orchestrator_states-{'terminating', 'terminated'}), dest='resetting', after='_do_reset')

        self._orchestrator_built = False
        self._response = None

        # Objects to store environment & agent reqs, set in do_initialize()
        self.env_obj = NotImplemented  # The object to your environment/game
        self._agents_needed = 1  # This will be set later

        # Objects to store agent information, set in do_register_agents()
        self._agents = {}  # Logs each agent's object against its name
        self._skip_train = {}  # Logs if we should skip training for an agent
        self._agents_registered = 0  # This will be set later

        # Objects to store game observation/actions info
        self._steps = 10  # TODO: Must make this configurable
        self.obs = {}
        self.actions = {}
        self.rewards = {}

    def update_status(self, payload):
        """
        Provides additional details to the current state of the orchestrator.

        :param payload: Extra information regarding the status update
        """
        self.endpoint_service.update_state(state=None, payload=payload)

    @property
    def endpoint_service(self) -> OrchestratorInstanceEndpoint:
        """
        Returns the endpoint service for this orchestrator
        """
        return self._endpoint_service

    @endpoint_service.setter
    def endpoint_service(self, endpoint_service: OrchestratorInstanceEndpoint):
        """
        Sets the endpoint service to the provided OrchestratorInstanceEndpoint

        :param endpoint_service: The new OrchestratorInstanceEndpoint
        """
        self._endpoint_service = endpoint_service

    def new_state_entered(self, *args, **kwargs):
        """
        Notifies the endpoint service that the current state of the state machine has
        been updated

        :param args: Optional non-keyworded variable length arguments to pass in
        :param kwargs: Optional keyworded variable length arguments to pass in
        """
        logger.debug("New state entered - %s {args: %s}", self.state, args)
        if self.state == 'failed' and len(args) > 0:
            self.endpoint_service.update_state(self.state, payload=args[0])
        else:
            self.endpoint_service.update_state(self.state)

    def fail(self, reason):
        """
        Triggers the orchestrator to enter the failed state.

        This method should not be implemented or overwritten by subclasses.  It will be
        created by the state machine.

        :param reason: The reason why the state machine is transitioned into the failure state
        """
        pass

    def uninitialized(self):
        """
        Triggers the agent to enter the uninitialized state.

        It is expected that this method will only be called by the
        implementing agent subclass.

        This method should not be implemented or overwritten by subclasses.
        It will be created by the state machine.
        """
        logger.debug('Called abstractAgent.uninitialized')
        pass

    def initialize(self, env = {}, agents_needed = 1):
        """
        Triggers the orchestrator to enter the initializing state.

        A subsequent call to do_initialize with the given parameters will be
        made as a result.

        This method should not be implemented or overwritten by subclasses.
        It will be created by the state machine.

        Args:
            env (dict, optional): Dict with has keyword args for the env/game
            agents_needed (int, optional): Number of expected agents
        """
        logger.debug('Called abstractOrchestrator.initialize')
        pass

    def waiting_for_agents(self):
        """
        Triggers the orchestrator to enter the waiting_for_agents state.

        It is expected that this method will only be called by the
        implementing orchestrator subclass.

        This method should not be implemented or overwritten by subclasses.
        It will be created by the state machine.
        """
        logger.debug('Called abstractOrchestrator.waiting_for_agents')
        pass

    def register_agent(self, agent_name, agent_url, skip_train):
        """
        Triggers the orchestrator to enter the register agent state. A subsequent call
        to do_register_agent with the given parameters will be made as a result.

        It is expected that this method will only be called by the
        state machine.

        This method should not be implemented or overwritten by subclasses.
        It will be created by the state machine.
        """
        logger.debug('Called abstractOrchestrator.register_agent')
        pass

    def ready(self):
        """
        Triggers the orchestrator to enter the ready state.

        It is expected that this method will only be called by the
        implementing orchestrator subclass.

        This method should not be implemented or overwritten by subclasses.
        It will be created by the state machine.
        """
        pass

    def start_episode(self, episode_cfg):
        """
        Triggers the orchestrator to start the episode.

        It is expected that this method will only be called by the
        implementing orchestrator subclass.

        This method should not be implemented or overwritten by subclasses.
        It will be created by the state machine.

        :param episode_cfg: A dictionary that maps string keys {TBD} that contains
            information on the episode to run
        """
        logger.debug('Called abstractOrchestrator.start_episode')
        pass

    def stop_episode(self):
        """
        Triggers the orchestrator to stop the episode.

        It is expected that this method will only be called by the
        implementing orchestrator subclass.

        This method should not be implemented or overwritten by subclasses.
        It will be created by the state machine.
        """
        logger.debug('Called abstractOrchestrator.stop_episode')
        pass

    def save_episode(self, path: str):
        """
        Saves the game episode's state and/or output

        It is expected that this method will only be called by the
        implementing orchestrator subclass.

        This method should not be implemented or overwritten by subclasses.
        It will be created by the state machine.

        :param path: The path to save the game to
        """
        logger.debug('Called abstractOrchestrator.save_episode')
        pass

    def report_failure(self, reason):
        """
        Reports the failure of a orchestrator during its operations

        :param reason: Error message explaining why the orchestrator failed.
        """
        logger.info ('Orchestrator has failed: ' + str(reason))

    def terminated(self):
        """
        Terminates the orchestrator
        """
        logger.info("Shutting down the orchestrator")
        sys.exit()

    def reset(self):
        """
        Resets the orchestrator container instance
        """
        pass

    def _do_initialize(self, env: dict = {}, agents_needed: int = 1):
        """
        Called once the endpoint service has launched.
        This would typically be the first call made to the service.

        :param objectives: The objectives for the orchestrator.
            Possible values include TBD
        :param props: A dictionary that is parsed from a JSON string.
            These are settings that are passed from the ecosystem,
            but are not really considered hyperparameters. They are not used
            by the orchestrator, but rather the endpoint itself
            (e.g., where should heartbeats be sent and how often, etc).
        :param hparams: A dictionary that is parsed from a JSON string.
            These are the hyperparameters that are used by the orchestrator.
        """
        try:  # Grabs number of agents needed
            self._agents_needed = int(agents_needed)
        except Exception as ex:
            logger.exception(f"We didn't get a valid agents_needed={agents_needed}")
            self.fail(str(ex))

        try:  # Initializes the orchestrator
            logger.debug("_do_initialize called")
            self.do_initialize(env=env, agents_needed=agents_needed)
        except Exception as ex: #pylint: disable=broad-except
            logger.exception("Error initializing the Orchestrator in _do_initalize")
            self.fail(str(ex))

        try:  # Changes state
            logger.debug("Changing state to 'initialized'")
            self._orchestrator_built = True
            self.waiting_for_agents()
            logger.debug("_do_initialize complete")
        except Exception as ex: #pylint: disable=broad-except
            logger.exception("Error changing state in _do_initalize")
            self.fail(str(ex))

    @abstractmethod
    def do_initialize(self, env: dict = {}, agents_needed: int = 1):
        """
        Called once the endpoint service has launched.
        This would typically be the first call made to the service.

        Args:
            env (dict, optional): Dict with has keyword args for the env/game
            agents_needed (int, optional): Number of expected agents
        """
        pass

    def _do_register_agent(self, agent_name: str, agent_url: str,
                           skip_train: bool = None):
        """
        Instructs the service to register all of the agents this orchestrator
        will work with.

        :param agent_name: The name of the agent
        :param agent_url: The URL to the agent
        :param skip_train: If we shouldn't train this agent [Default = False]
        """
        logger.info(f"Will register with {agent_name} agent at {agent_url}")
        try:  # Try to find the agent object
            agent_client = AgentInstanceEndpointApi(get_mistk_agent_client(agent_url))
            self._agents[agent_name] = agent_client
        except Exception as ex: #pylint: disable=broad-except
            logger.exception("Agent could not be found by _do_register_agent")
            self.fail(str(ex))

        try:  # Registers the agent against this orchestrator
            agent_client.agent_registered(agent_cfg={'name': agent_name,
                                                     'url': agent_url})
            self._agents_registered = len(self._agents)
            logger.info(f"We have {self._agents_registered} agents out of {self._agents_needed} agents needed.")
        except Exception as ex: #pylint: disable=broad-except
            logger.exception("Error registering agent in _do_register_agent")
            self._agents.pop(agent_name, None)
            self.fail(str(ex))

        # Logs this agent's skip_train state; by default, we train all agents
        self._skip_train[agent_name] = skip_train if skip_train else False

        try:  # Runs user's do_register_agent method & transitons state
            self.do_register_agent(agent_name=agent_name, agent_url=agent_client)
            self.obs[agent_name] = []
            self.actions[agent_name] = []
            self.rewards[agent_name] = []
            if self._agents_registered == self._agents_needed:
                self.ready()
            else:
                self.waiting_for_agents()
        except Exception as ex: #pylint: disable=broad-except
            logger.exception("Error running user's do_register_agent and/or transitioning state")
            self._agents.pop(agent_name, None)
            self.fail(str(ex))

    @abstractmethod
    def do_register_agent(self, agent_name: str, agent_url: str):
        """
        Instructs the service to register all of the agents this orchestrator
        will work with.

        :param agent_name: The name of the agent
        :param agent_url: The URL to the agent
        """
        pass

    def _do_start_episode(self, episode_cfg: dict = None):
        """
        Begins starting the episode of playing the game

        :param episode_cfg: Dictionary with the episode's config settings
        """
        logger.debug("_do_start_episode started")
        if not episode_cfg:
            episode_cfg = {}

        # Ensures Obs + Actions + Agents Objects are in sync
        assert len(self._agents) == self._agents_needed, f"We needed {self._agents_needed} Agents and we got {len(self._agents)}"
        for agent in self._agents:
            if agent not in self.obs:
                logger.exception(f"{agent} was not added to the Obs dict")
                self.fail(f"{agent} was not added to the Obs dict")
            elif agent not in self.actions:
                logger.exception(f"{agent} was not added to the Actions dict")
                self.fail(f"{agent} was not added to the Actions dict")
            elif agent not in self.rewards:
                logger.exception(f"{agent} was not added to the Rewards dict")
                self.fail(f"{agent} was not added to the Rewards dict")

        # Starts Episode
        try:
            logger.info("Calling do_start_episode method.")
            self.do_start_episode(episode_cfg=episode_cfg)
            self.completed_episode()
        except Exception as ex: #pylint: disable=broad-except
            logger.exception("Error running do_start_episode")
            self.fail(str(ex))
        logger.debug("_do_start_episode complete")

    @abstractmethod
    def do_start_episode(self, episode_cfg: dict):
        """
        Begins starting the episode of playing the game

        :param episode_cfg: Dictionary with the episode's config settings
        """
        pass

    def _do_stop_episode(self):
        """
        Stops all processing and releases any resources that are in use in
        preparation for being shut down.
        """
        try:  # Tries to stop each agent
            for agent in self._agents:
                self._agents[agent].episode_stopped()
        except Exception as ex:  #pylint: disable=broad-except
            logger.exception("Error stopping each agent in do_stop_episode")
            self.fail(str(ex))
        try:  # Runs each orchestrator's stop episode method
            self.do_stop_episode()
        except Exception as ex:  #pylint: disable=broad-except
            logger.exception("Error stopping the orchestrator in do_stop_episode")
            self.fail(str(ex))
        try:  # Transitions state
            self.ready()
        except Exception as ex:  #pylint: disable=broad-except
            logger.exception("Error transitioning state in do_stop_episode")
            self.fail(str(ex))

    @abstractmethod
    def do_stop_episode(self):
        """
        Stops all processing and releases any resources that are in use in
        preparation for being shut down.
        """
        pass

    def _do_save_episode(self, path: str):
        """
        Saves the game episode's state and/or output

        :param path: The path to save the game to
        """
        logger.info(f"Saving an episode to {path}")
        try:  # Saves episode
            path = os.path.expanduser(os.path.abspath(path))
            self.do_save_episode(path=path)
        except Exception as ex:  #pylint: disable=broad-except
            logger.exception("Error saving episode in do_save_episode")
            self.fail(str(ex))
        try:  # Transitions state
            self.completed_episode()
        except Exception as ex:  #pylint: disable=broad-except
            logger.exception("Error transitioning state in do_save_episode")
            self.fail(str(ex))
        pass

    @abstractmethod
    def do_save_episode(self, path: str):
        """
        Saves the game's state and/or output
        """
        pass

    def _do_reset(self):
        """
        Resets the model into its initial state
        """
        try:
            self.do_reset()
            self._agents_registered = 0
            self._agents = {}
            self._orchestrator_built = False
            self.uninitialized()
        except Exception as ex:  #pylint: disable=broad-except
            logger.exception("Error running do_reset")
            self.fail(str(ex))

    @abstractmethod
    def do_reset(self):
        """
        Resets the model into its initial state
        """
        pass
