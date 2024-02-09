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

from concurrent.futures.thread import ThreadPoolExecutor
from datetime import datetime
import inspect, itertools, uuid
import yaml, pkg_resources, wsgiserver

import connexion as cx
from queue import Queue
from flask import Response
from rwlock.rwlock import RWLock
from multiprocessing import Process

from mistk import logger
from mistk.data import AgentInstanceInitParams as InitParams
from mistk.data import ObjectInfo, AgentInstanceStatus, ServiceError
from mistk.watch import watch_manager
from mistk.agent.server.controllers import agent_instance_endpoint_controller
import mistk.data.utils as datautils

class AgentInstanceTask:
    """
    A task to be submitted to the Agent Instance that will be performed and report status of.
    """

    def __init__(self, operation, parameters = None, submitted = None,
                 completed = None, status = None, message = None):
        """
        Initializes the Agent Instance Task

        :param operation: The operation to be performed by this task
        :param parameters: Optional parameters for this specific operation
        :param submitted: Optional flag indicating whether the task was submitted
        :param completed: Optional flag indicating whether the task was completed
        :param status: Optional status of the task
        :param message: Optional text message regarding the status of the task
        """
        self.operation = operation
        self.parameters = parameters
        self.submitted = submitted
        self.completed = completed
        self.status = status
        self.message = message

class AgentInstanceEndpoint():

    def __init__(self):
        """
        Initializes the Agent Instance Endpoint service
        """

        initializeEndpointController(self, agent_instance_endpoint_controller)

        self.app = cx.FlaskApp('mistk.agent.server')
        self.app.app.json_encoder = datautils.PresumptiveJSONEncoder
        self.app.add_api(self._load_api_spec())
        self.http_server = None

        self._state_machine = None
        self._agent = None
        self._current_task = None

        self._status_lock = RWLock()
        self._task_lock = RWLock()

        self._response_action_queue = Queue()

        self._old_tasks = list()
        self._thread_pool = ThreadPoolExecutor()

        info = ObjectInfo('AgentInstanceStatus', resource_version=1)
        self._status = AgentInstanceStatus(object_info=info, state='started')

        self._header_json = ("Content-Type","application/json")


    def start_server(self, port=8081, process=False):
        """
        Starts the http server of the Service

        :param port: The port on which to start the server, defaults to 8081
        :param process: Start on another process
        """

        self.http_server = wsgiserver.WSGIServer(self.app, port=port)
        if process:
            process = Process(target=self.http_server.start)
            process.start()
            return process
        else:
            self.http_server.start()

    def _load_api_spec(self):
        """
        Gets the API specification of the module specified

        :param module: THe name of the module
        """
        return yaml.load(pkg_resources.ResourceManager().resource_stream('mistk', '/agent/server/swagger/swagger.yaml'), Loader=yaml.SafeLoader)

    @property
    def state_machine(self):
        """
        Retrieves the state machine associated with this AgentEndpointService

        :return: the state machine
        """
        return self._state_machine

    @state_machine.setter
    def state_machine(self, state_machine):
        """
        Sets the state machine associated with this AgentEndpointService

        :param state_machine: The new state machine to set
        """
        self._state_machine = state_machine

    @property
    def agent(self):
        """
        Retrieves the agent associated with this AgentEndpointService

        :return: the agent
        """
        return self._agent

    @agent.setter
    def agent(self, agent):
        """
        Sets the agent associated with this AgentEndpointService

        :param agent: the new agent to set
        """
        self._agent = agent

    def initialize_agent(self, initializationParameters):
        """
        Creates and returns an Task which initializes the agent with the
        optional parameters provided

        :param initializationParameters: The parameters used for initialization
        :return: The created Task object
        """
        logger.debug("Initialize agent called")
        try:
            params = initializationParameters
            if not isinstance(params, InitParams) and cx.request.is_json:
                params = datautils.deserialize_model(cx.request.get_json(), InitParams)
            assert isinstance(params, InitParams)

            task = AgentInstanceTask(operation='initialize',
                parameters={"props": params.model_properties,
                            "hparams": params.hyperparameters})
            logger.debug('Created initialize agent task', extra={'agent_task': task})

            self.add_task(task)
            return Response(status=200, headers=[self._header_json])
        except RuntimeError as inst:
            msg = "Error during agent initialization: %s" % str(inst)
            logger.exception(msg)
            return ServiceError(500, msg), 500

    def build_model(self, modelPath=None):
        """
        Creates and returns a Task which builds the model using the modelPath provided

        :param modelPath: The path where the model will be loaded from.

        :return: The created Task object
        """
        logger.debug("Build model called")
        try:
            task = AgentInstanceTask(operation="build_model",
                                     parameters = {"path": modelPath})
            self.add_task(task)
            return Response(status=200, headers=[self._header_json])
        except RuntimeError as inst:
            msg = "Error while building model: %s" % str(inst)
            logger.exception(msg)
            return ServiceError(500, msg), 500

    def save_model(self, modelPath):
        """
        Creates and returns a Task which saves the model to the path provided

        :param modelPath: The path where the model will be saved.
        :return: The created Task object
        """
        try:
            task = AgentInstanceTask(operation="save_model",
                                     parameters = {"path": modelPath})
            self.add_task(task)
            return Response(status=200, headers=[self._header_json])
        except RuntimeError as inst:
            msg = "Error while saving model to path provided: %s" % str(inst)
            logger.exception(msg)
            return ServiceError(500, msg), 500

    def agent_registered(self, agentCfg=None):
        """
        Creates & returns a Task when the agent is now registered to the orchestrator

        :param agent_cfg: A dictionary for the agent configuration from the orchestrator
        :return: The created Task object
        """
        logger.debug("Agent registered called")
        try:
            task = AgentInstanceTask(operation="agent_registered",
                                            parameters={"agent_cfg": agentCfg})
            self.add_task(task)
            return Response(status=200, headers=[self._header_json])
        except RuntimeError as inst:
            msg = "Error while agent registered: %s" % str(inst)
            logger.exception(msg)
            return ServiceError(500, msg), 500

    def episode_started(self, episodeCfg = None):
        """
        Instructs the agent that the episode has started

        :param episodeCfg: Dictionary with the episode's config settings
        :return: The created Task object
        """
        logger.debug("Episode Started called")
        if not episodeCfg:
            episodeCfg = {}
        try:
            self.add_task(AgentInstanceTask(operation="episode_started",
                                                   parameters={"episode_cfg": episodeCfg}))
            return Response(status=200, headers=[self._header_json])
        except RuntimeError as inst:
            msg = "Error while starting episode: %s" % str(inst)
            logger.exception(msg)
            return ServiceError(500, msg), 500

    def get_action(self, obs):
        """
        Gives the agent the observations to perform action

        :param obs: A list of observations
        """
        logger.debug("Get Action called")
        try:
            self.add_task(AgentInstanceTask(operation="get_action",
                                                   parameters={"obs": obs}))

            resp = self._get_action_response()
            logger.debug('Action response ready.')
            # check if error from action queue response
            if isinstance(resp, ServiceError):
                return resp, 500
            else:
                return resp
        except RuntimeError as inst:
            msg = "Error while getting action: %s" % str(inst)
            logger.exception(msg)
            return ServiceError(500, msg), 500

    def replay_action(self, obs):
        """
        Gives the agent the observations to perform replay for learning

        :param obs: A dict with keys for prev_obs (prior observations),
            rewards (the agent got), actions (actions the agent took),
            and new_obs (new observations after this step)
        """
        logger.debug("Replay Action called")
        try:
            self.add_task(AgentInstanceTask(operation="replay_action",
                                            parameters={"obs": obs}))
            return Response(status=200, headers=[self._header_json])
        except RuntimeError as inst:
            msg = "Error while replaying action: %s" % str(inst)
            logger.exception(msg)
            return ServiceError(500, msg), 500

    def episode_stopped(self):
        """
        Instructs the agent that the episode has stopped
        """
        logger.debug("Stop episode called")
        try:
            self.add_task(AgentInstanceTask(operation="episode_stopped"))
            return Response(status=200, headers=[self._header_json])
        except RuntimeError as inst:
            msg = "Error while stopping the episode: %s" % str(inst)
            logger.exception(msg)
            return ServiceError(500, msg), 500

    def reset(self, unloadModel):
        """
        Resets the agent
        """
        logger.debug("Reset called")
        try:
            self.add_task(AgentInstanceTask(operation="reset",
                                                parameters={"unload_model": unloadModel}))
            return Response(status=200, headers=[self._header_json])
        except RuntimeError as inst:
            msg = "Error while stopping the episode: %s" % str(inst)
            logger.exception(msg)
            return ServiceError(500, msg), 500

    def terminate(self):
        """
        Shuts down the model and the endpoint service
        """
        logger.debug("Terminate called")
        try:
            self.add_task(AgentInstanceTask(operation="terminate"))
        except RuntimeError as inst:
            msg = "Error while terminating the model: %s" % str(inst)
            logger.exception(msg)
            return ServiceError(500, msg), 500

    def get_status(self, watch=None, resourceVersion=None):
        """
        Retrieves the status of this AgentEndpointService

        :param watch: Optional flag indicating whether state changes should be monitored
        :param resourceVersion: Optional version id that will be used as the minimum version number
            for watched status changes.
        :return: The current status of this AgentEndpointService
        """
        logger.debug("Get Status called")
        try:
            with self._status_lock.reader_lock:
                if watch:
                    return Response(
                        watch_manager.watch('status', resourceVersion, self._status),
                        mimetype="application/json")
                else:
                    return self._status
        except RuntimeError as inst:
            msg = "Error while retrieving status for AgentEndpointService: %s" % str(inst)
            logger.exception(msg)
            return ServiceError(500, msg), 500

    def get_api_version(self):
        """
        Returns the version of the MISTK API

        :return: The MISTK API version as text
        """
        try:
            version = pkg_resources.require("mistk")[0].version
            return version, 200
        except Exception as ex:
            msg = 'Error occurred while attempting to retrieve MISTK API version: %s' % str(ex)
            logger.exception(msg)
            return ServiceError(500, msg), 500


    def delete_task(self, task):
        """
        Deletes the specified Task.
        This function is currently not supported

        :param task: The task to delete
        """
        logger.debug("Ignoring delete task request", extra={'task':task})
        return ServiceError(501, "Not currently supported"), 501

    def add_task(self, task):
        """
        Adds a task to this AgentEndpointService and starts it using a pool of worker threads

        :param task: The Task to register and start
        :return: The running task
        """
        try:
            task.id = uuid.uuid4().hex
            task.status = 'queued'
            task.submitted = datetime.now()
            ops = ['initialize', 'build_model', 'save_model', 'agent_registered', 'episode_started',
                   'get_action', 'replay_action', 'episode_stopped', 'reset']

            if not task.operation in ops:
                msg = "Operation %s must be one of %s" % (str(task.operation), str(ops))
                logger.error(msg)
                raise RuntimeError(msg)

            with self._task_lock.writer_lock:
                if isinstance(self._current_task, AgentInstanceTask):
                    status = self._current_task.status
                    if not status == 'complete' and not status == 'failed':
                        return "Cannot submit a task while current task is not complete.  Current task status is " + status, 400
                if self._current_task:
                    self._old_tasks.insert(0, self._current_task)
                self._current_task = task
                task.status = 'running'

            if not self._valid_task_transition():
                msg = "Operation %s invalid from state %s" % (str(self._current_task.operation), str(self.agent.state))
                self._current_task.status = 'failed'
                logger.exception(msg)
                raise RuntimeError(msg)

            self._thread_pool.submit(self._process_task)
            return task

        except RuntimeError as inst:
            msg = "Error while adding task to AgentEndpointService and starting the task: %s" % str(inst)
            logger.exception(msg)
            raise RuntimeError(msg)

    def update_state(self, state=None, payload=None):
        """
        Updates the state of the AgentEndpointService

        :param state: The new state. If not given, the current state will be used.
        :param payload: Additional data to attach to the state
        """
        try:
            with self._status_lock.writer_lock:
                state = state or self._status.state
                ver = self._status.object_info.resource_version + 1
                info = ObjectInfo('AgentInstanceStatus', resource_version=ver)
                self._status = AgentInstanceStatus(info, state=state, payload=payload)
                watch_manager.notify_watch('status', item=self._status)
        except RuntimeError as inst:
            msg = "Error while updating state of the AgentEndpointService. %s" % str(inst)
            logger.exception(msg)
            return ServiceError(500, msg), 500

    def put_action_response(self, response):
        """
        Adds a response to the get action response queue
        """
        self._response_action_queue.put(response)

    def _get_action_response(self):
        """
        Pops the latest response on the get action response queue
        """
        return self._response_action_queue.get()

    def _valid_task_transition(self) -> bool:
        """
        Valid operation task from current state

        :return: True if a valid transition, False if a invalid transition
        """

        # TODO: Try to update transition package to 0.9.0 for check transitions
        #m = getattr(self.agent, f'may_{self._current_task.operation}')
        #m(**(self._current_task.parameters or {}))

        logger.debug(f'valid state: {self.agent._machine.get_triggers(self.agent.state)}')
        if self._current_task.operation in self.agent._machine.get_triggers(self.agent.state):
            return True
        else:
            return False

    def _process_task(self):
        """
        Processes the currently queued Task and updates its status as appropriate
        """
        try:
            logger.info('Processing task %s', self._current_task.operation)
            m = getattr(self.agent, self._current_task.operation)
            m(**(self._current_task.parameters or {}))
            with self._task_lock.writer_lock:
                self._current_task.status = 'complete'
                self._current_task.completed = datetime.now()
            logger.info('Processing of task is complete')
        except Exception as ex:  #pylint: disable=broad-except
            logger.exception("Error occurred running task")
            self._current_task.status = 'failed'
            self._current_task.message = str(ex)
            raise


def initializeEndpointController(handler, *modules):
    """
    This method iterates over the functions defined in the auto-generated flask modules
    And creates a function in this package which points bound member methods of the
    handler

    :param handler: The handler object which must implement bound member methods which
        otherwise have the same signature as those defined in the controller_modules
    :param modules: These are the autogenerated swagger controller modules
    """

    fns = itertools.chain(*[inspect.getmembers(m, inspect.isfunction) for m in modules])
    for name, fn1 in fns:
        sig1 = inspect.signature(fn1)
        logger.debug("Building redirect for " + name + str(sig1))

        fn2 = getattr(handler, name)
        sig2 = inspect.signature(fn2)
        assert sig1 == sig2, f"Can't redirect {name} : {sig1} - {sig2})"
        globals()[name] = getattr(handler, name)
