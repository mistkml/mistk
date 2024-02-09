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
from typing import Dict, List, Union

from abc import ABCMeta, abstractmethod
import os

from mistk.data import ServiceError
from mistk.agent.service import AgentInstanceEndpoint
from mistk import logger
import sys

# The agent states
_agent_states = {'started', 'initializing', 'initialized', 'failed', 'building_model', 'saving_model_init',
                        'saving_model_ready', 'agent_registering', 'ready', 'episode_starting', 'in_episode',
                        'getting_action', 'replaying_action', 'episode_stopping', 'resetting',
                        'terminating', 'terminated'}

class AbstractAgent (metaclass=ABCMeta):
    """
    The definition of an abstract Agent to be implemented by Agent
    developers.
    """

    @abstractmethod
    def __init__(self):
        """
        Initializes the Agent and registers the default state machine transitions
        available to all agents.
        """
        self.state = None
        self._endpoint_service = None
        states = [State(n, on_enter='new_state_entered') for n in _agent_states]
        self._machine = Machine(model=self, states=states, initial='started', auto_transitions=False)
        self._machine.add_transition(trigger='started', source='resetting', dest='started')
        self._machine.add_transition(trigger='fail', source=list(_agent_states-{'terminated'}), dest='failed')
        self._machine.add_transition(trigger='initialize', source='started', dest='initializing', after='_do_initialize')
        self._machine.add_transition(trigger='initialized', source=['initializing', 'building_model', 'saving_model_init', 'resetting'], dest='initialized')
        self._machine.add_transition(trigger='build_model', source='initialized', dest='building_model', after='_do_build_model')
        self._machine.add_transition(trigger='save_model', source='initialized', dest='saving_model_init', after='_do_save_model')
        self._machine.add_transition(trigger='save_model', source='ready', dest='saving_model_ready', after='_do_save_model')
        self._machine.add_transition(trigger='agent_registered', source='initialized', dest='agent_registering', after='_do_agent_registered')
        self._machine.add_transition(trigger='ready', source=['agent_registering', 'saving_model_ready', 'episode_stopping'], dest='ready')
        self._machine.add_transition(trigger='episode_started', source='ready', dest='episode_starting', after='_do_episode_started')
        self._machine.add_transition(trigger='in_episode', source=['episode_starting', 'getting_action', 'replaying_action'],  dest= 'in_episode')
        self._machine.add_transition(trigger='get_action', source='in_episode',  dest= 'getting_action', after='_do_get_action')
        self._machine.add_transition(trigger='replay_action', source='in_episode',  dest= 'replaying_action', after='_do_replay_action')
        self._machine.add_transition(trigger='episode_stopped', source='in_episode',  dest= 'episode_stopping', after='_do_episode_stopped')
        self._machine.add_transition(trigger='terminate', source=list(_agent_states-{'terminating', 'terminated', 'failed'}), dest='terminating', after='_do_terminate')
        self._machine.add_transition(trigger='terminated', source='terminating', dest='terminated')
        self._machine.add_transition(trigger='reset', source=list(_agent_states-{'terminating', 'terminated'}), dest='resetting', after='_do_reset')

        self.agent_name = 'agent0'
        self._model_built = False
        self._model_learning = False
        self._response = None

    def update_status(self, payload):
        """
        Provides additional details to the current state of the agent.

        :param payload: Extra information regarding the status update
        """
        self.endpoint_service.update_state(state=None, payload=payload)

    @property
    def endpoint_service(self) -> AgentInstanceEndpoint:
        """
        Returns the endpoint service for this agent
        """
        return self._endpoint_service

    @endpoint_service.setter
    def endpoint_service(self, endpoint_service: AgentInstanceEndpoint):
        """
        Sets the endpoint service to the provided AgentInstanceEndpoint

        :param endpoint_service: The new AgentInstanceEndpoint
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
        Triggers the agent to enter the failed state.

        This method should not be implemented or overwritten by subclasses.  It will be
        created by the state machine.

        :param reason: The reason why the state machine is transitioned into the failure state
        """
        pass

    def started(self):
        """
        Triggers the agent to enter the started state.

        It is expected that this method will only be called by the
        implementing agent subclass.

        This method should not be implemented or overwritten by subclasses.
        It will be created by the state machine.
        """
        logger.debug('Called abstractAgent.started')
        pass

    def initialize(self, props, hparams):
        """
        Triggers the agent to enter the initializing state.

        A subsequent call to do_initialize with the given parameters will be
        made as a result.

        This method should not be implemented or overwritten by subclasses.
        It will be created by the state machine.

        :param props: A dictionary that is parsed from a JSON string.
            These are settings that are passed from the ecosystem,
            but are not really considered hyperparameters.  They are not used
            by the agent, but rather the endpoint itself
            (e.g., where should heartbeats be sent and how often, etc).
        :param hparams: A dictionary that is parsed from a JSON string.
            These are the hyperparameters that are used by the agent.
        """
        logger.debug('Called abstractAgent.initialize')
        pass

    def initialized(self):
        """
        Triggers the agent to enter the initialized state.

        It is expected that this method will only be called by the
        implementing agent subclass.

        This method should not be implemented or overwritten by subclasses.
        It will be created by the state machine.
        """
        logger.debug('Called abstractAgent.initialized')
        pass

    def build_model(self, path: str = ''):
        """
        Triggers the agent to enter the building_model state.  A subsequent call to
        do_build_model with the given parameters will be made as a result.

        This method should not be implemented or overwritten by subclasses.  It will be
        created by the state machine.

        :param path: The path to the model file
        """
        pass

    def save_model(self, path: str):
        """
        Triggers the agent to enter the saving_model state.  A subsequent call to
        do_save_model with the given parameters will be made as a result.

        This method should not be implemented or overwritten by subclasses.  It will be
        created by the state machine.

        :param path: The path where to save the agent model file
        """
        pass

    def agent_registered(self, agent_cfg: dict):
        """
        Triggers the agent to enter the agent_registering state. A subsequent call
        to do_agent_registered with the given parameters will be made as a result.

        This method should not be implemented or overwritten by subclasses.
        It will be created by the state machine.

        :param agent_cfg: A dictionary that maps string keys that contains
            information on the agent to run
        """
        logger.debug('Called abstractAgent.agent_registered')
        pass

    def ready(self):
        """
        Triggers the agent to enter the ready state.

        It is expected that this method will only be called by the
        implementing agent subclass.

        This method should not be implemented or overwritten by subclasses.
        It will be created by the state machine.
        """
        pass

    def in_episode(self):
        """
        Triggers the agent to enter the in episode state.

        It is expected that this method will only be called by the
        implementing agent subclass.

        This method should not be implemented or overwritten by subclasses.
        It will be created by the state machine.
        """
        pass

    def episode_started(self, episode_cfg: dict):
        """
        Triggers the agent to know the episode started. A subsequent call
        to do_episode_started with the given parameters will be made as a result.

        This method should not be implemented or overwritten by subclasses.
        It will be created by the state machine.

        :param episode_cfg: Dict with the episode's config settings. A key
            must be `obs`, with a List of the env's initial observation.
        """
        logger.debug('Called abstractAgent.episode_started')
        pass

    def get_action(self, obs: Dict[str, List[Union[int, float]]]) -> Dict[str, List[Union[int, float]]]:
        """
        Triggers the agent to get an action.  A subsequent call to
        do_get_action with the given parameters will be made as a result.

        This method should not be implemented or overwritten by subclasses.  It will be
        created by the state machine.

        :param obs: A dictionary of each agent's list of int or float
                    observations. The keys of the dict are each agent's name.
        """
        pass

    def replay_action(self, prev_obs: list, rewards: list,
                      actions: list, new_obs: list):
        """
        Triggers the agent to replay action.  A subsequent call to
        do_replay_action with the given parameters will be made as a result.

        This method should not be implemented or overwritten by subclasses.  It will be
        created by the state machine.

        :param prev_obs: A list of env observations prior to taking this step
        :param rewards: A list of rewards for this agent on this turn
        :param actions: A list of actions this agent took
        :param new_obs: A list of env observations after taking this step
        """
        pass


    def episode_stopped(self):
        """
        Triggers the agent to stop the episode. A subsequent call
        to do_episode_stopped with the given parameters will be made as a result.

        This method should not be implemented or overwritten by subclasses.
        It will be created by the state machine.
        """
        logger.debug('Called abstractOrchestrator.stop_episode')
        pass


    def report_failure(self, reason):
        """
        Reports the failure of a agent during its operations

        :param reason: Error message explaining why the agent failed.
        """
        logger.info ('Agent has failed: ' + str(reason))

    def terminated(self):
        """
        Terminates the agent
        """
        logger.info("Shutting down the agent")
        sys.exit()

    def reset(self, unload_model: bool = True):
        """
        Resets the agent container instance
        """
        pass

    def _do_initialize(self, props: dict, hparams: dict):
        """
        Called once the endpoint service has launched.
        This would typically be the first call made to the service.

        :param props: A dictionary that is parsed from a JSON string.
            These are settings which defines the agent's name and its learner's
            specifications, if applicable. It's a best practice to make these
            fields optional. Most learners will want `state_size` to be a
            mandatory argument, specified in this dictionary.
        :param hparams: A dictionary that is parsed from a JSON string.
            Currently not used.
        """
        # Grabs the Agent Properties
        logger.debug("_do_initialize called")
        self.agent_name = props.get('name', self.agent_name)
        self._model_file_name = props.get('model_file_name', self._model_file_name)

        try:  # Actually runs the agent's do initialize method
            self.do_initialize(props, hparams)
        except Exception as ex: #pylint: disable=broad-except
            logger.exception("Error running do_initalize")
            self.fail(str(ex))

        logger.debug("Changing state to 'initialized'")
        self.initialized()
        logger.debug("_do_initialize complete")

    @abstractmethod
    def do_initialize(self, props: dict, hparams: dict):
        """
        Called once the endpoint service has launched.
        This would typically be the first call made to the service.

        :param props: A dictionary that is parsed from a JSON string.
            These are settings which defines the agent's name and its learner's
            specifications, if applicable. It's a best practice to make these
            fields optional. Most learners will want `state_size` to be a
            mandatory argument, specified in this dictionary.
        :param hparams: A dictionary that is parsed from a JSON string.
            Currently not used.
        """
        pass

    def _do_build_model(self, path: str = ''):
        """
        Instructs the container to construct a model

        :param path: Path to a model file, if you're using a pretrained one
        """
        if path=='None' or path=='':
            path = None
            logger.info(f'Will try to build {self.agent_name} model')
        elif path:
            path = os.path.expanduser(os.path.abspath(path))
            logger.info(f"Will try to load {self.agent_name} model from {path}/{self._model_file_name}")

        try:
            self.do_build_model(path)
            self._model_built = True
        except Exception as ex: #pylint: disable=broad-except
            logger.exception("Error running do_build_model")
            self.fail(str(ex))
        self.initialized()

    @abstractmethod
    def do_build_model(self, path: str = ''):
        """
        Instructs the container to construct the model

        :param path: The path to the model file
        """
        pass

    def _do_save_model(self, path: str):
        """
        Instructs the container to serialize the model to the specified path

        :param path: The path where to save the model file
        """
        path = os.path.expanduser(os.path.abspath(path))
        logger.info(f"Will try to save models to {path}/{self._model_file_name}")

        # Tries to delete the existing model
        proposed_path = os.path.join(path, self._model_file_name)
        if os.path.exists(proposed_path):
            try:
                os.remove(proposed_path)
            except Exception as ex:
                logger.info(f"{proposed_path} exists but we couldn't delete it, so we're continuing on")

        try:  # Actually saves the model
            self.do_save_model(path)
            if self.state == 'saving_model_init':
                self.initialized()
            else:
                self.ready()
        except Exception as ex: #pylint: disable=broad-except
            logger.exception("Error running do_save_model")
            self.fail(str(ex))

    @abstractmethod
    def do_save_model(self, path: str):
        """
        Instructs the container to serialize the model to the specified path

        :param path: The path where to save the model file
        """
        pass

    def _do_agent_registered(self, agent_cfg: dict):
        """
        Instructs the service that the agent has been registered to a orchestrator

        :param agent_cfg: A dictionary for the agent configuration from the orchestrator
        """
        logger.info('Will register this agent to an orchestrator')
        try:
            self.do_agent_registered(agent_cfg)
            self.agent_name = agent_cfg['name']
            self.ready()
            logger.debug('This agent is registered')
        except Exception as ex: #pylint: disable=broad-except
            logger.exception("Error running do_agent_registered")
            self.fail(str(ex))

    @abstractmethod
    def do_agent_registered(self, agent_cfg: dict):
        """
        Instructs the service that the agent has been registered to a orchestrator

        :param agent_cfg: A dictionary for the agent configuration from the orchestrator
        """
        pass

    def _do_episode_started(self, episode_cfg: dict):
        """
        Instructs the agent that the episode has started.
        This method must also include a way to reset the agent's learner with
        the current observations, if the learner has this expectation.

        :param episode_cfg: Dict with the episode's config settings. A key
            must be `obs`, with a List of the env's initial observation.
        """
        logger.debug("_do_episode_started started")
        assert 'obs' in episode_cfg, "'obs' must be a key in episode_cfg"
        try:
            self.do_episode_started(episode_cfg)
            self.in_episode()
        except Exception as ex: #pylint: disable=broad-except
            logger.exception("Error running do_episode_started")
            self.fail(str(ex))
        logger.debug("_do_episode_started complete")

    @abstractmethod
    def do_episode_started(self, episode_cfg: dict):
        """
        Instructs the agent that the episode has started.
        This method must also include a way to reset the agent's learner with
        the current observations, if the learner has this expectation.

        :param episode_cfg: Dict with the episode's config settings. A key
            must be `obs`, with a List of the env's initial observation.
        """
        pass

    def _do_get_action(self, obs: Dict[str, List[Union[int, float]]]) -> Dict[str, List[Union[int, float]]]:
        """
        Gives the agent the observations to perform action(s)

        In normal operating conditions, this Agent class is only controlling
        one player/entity in your game/environment. In this situation, we
        assume both the input `obs` and output will be a dictionary containing
        that singular agent, whose name is self.agent_name, as defined in
        do_start_episode.

        However, if this Agent class is controlling multiple players/entities
        for some reason, the input & output of this method would be a dict
        with each of those players/entities represented.

        :param obs: A dictionary of each agent's list of int or float
                    observations. The keys of the dict are each agent's name.
        :return: A dict of lists. Each list contains the int/float actions an
                 agent should take.
        """
        logger.debug(f"_do_get_action started with obs from {list(obs.keys())}")
        try:  # Calls the child's agent so it can get actions from the learner
            response = self.do_get_action(obs)
            self.endpoint_service.put_action_response(response)
            self.in_episode()
        except Exception as ex: #pylint: disable=broad-except
            msg = f"Unexpected error occurred while running get action for {self.agent_name}: {ex}"
            self.endpoint_service.put_action_response(ServiceError(500, msg))
            logger.exception("Error running do_get_action")
            self.fail(str(ex))
        logger.debug("_do_get_action complete")

    @abstractmethod
    def do_get_action(self, obs: Dict[str, List[Union[int, float]]]) -> Dict[str, List[Union[int, float]]]:
        """
        Gives the agent the observations to perform action(s)

        In normal operating conditions, this Agent class is only controlling
        one player/entity in your game/environment. In this situation, we
        assume both the input `obs` and output will be a dictionary containing
        that singular agent, whose name is self.agent_name, as defined in
        do_start_episode.

        However, if this Agent class is controlling multiple players/entities
        for some reason, the input & output of this method would be a dict
        with each of those players/entities represented.

        :param obs: A dictionary of each agent's list of int or float
                    observations. The keys of the dict are each agent's name.
        :return: A dict of lists. Each list contains the int/float actions an
                 agent should take.
        """
        pass

    def _do_replay_action(self, obs: Dict[str, Union[List[Union[int, float]], bool]]):
        """
        Reviews action that the agent taken against the env observations so
        the agent can learn.

        :param obs: In general, this will be a dictionary of:
                    prev_obs: A list of env observations prior to taking this step,
                    rewards: A list of rewards for this agent on this turn,
                    actions: A list of actions this agent took,
                    new_obs: A list of env observations after taking this step
                    done: Boolean if the game is over
        """
        logger.debug(f"_do_replay_action started with these inputs: {list(obs.keys())}")

        try:
            logger.info("Calling do_replay_action method.")
            self.do_replay_action(obs=obs)
            self.in_episode()
        except Exception as ex: #pylint: disable=broad-except
            logger.exception("Error running do_replay_action")
            self.fail(str(ex))
        logger.debug("_do_replay_action complete")

    @abstractmethod
    def do_replay_action(self, obs: Dict[str, Union[List[Union[int, float]], bool]]):
        """
        Reviews action that the agent taken against the env observations so
        the agent can learn.

        :param obs: In general, this will be a dictionary of:
                    prev_obs: A list of env observations prior to taking this step,
                    rewards: A list of rewards for this agent on this turn,
                    actions: A list of actions this agent took,
                    new_obs: A list of env observations after taking this step
                    done: Boolean if the game is over
        """
        pass

    def _do_episode_stopped(self):
        """
        Instructs the agent that the episode has stopped

        """
        logger.debug("_do_episode_stopped started")
        try:
            self.do_episode_stopped()
            self.ready()
        except Exception as ex: #pylint: disable=broad-except
            logger.exception("Error running do_episode_stopped")
            self.fail(str(ex))
        logger.debug("_do_episode_stopped complete")

    @abstractmethod
    def do_episode_stopped(self):
        """
        Instructs the agent that the episode has stopped

        """
        pass

    def _do_reset(self, unload_model: bool = True):
        """
        Resets the model into its initial state

        :param unload_model: Unload (reset) the built model or keep the current built model
        """
        try:
            self.do_reset(unload_model)
            if unload_model:
                self._model_built = False
                self.started()
            else:
                self.initialized()
        except Exception as ex:  #pylint: disable=broad-except
            logger.exception("Error running do_reset")
            self.fail(str(ex))

    @abstractmethod
    def do_reset(self, unload_model: bool = True):
        """
        Resets the model into its initial state

        :param unload_model: Unload (reset) the built model or keep the current built model
        """
        pass
