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
from mistk.data import OrchestratorInstanceInitParams as InitParams
from mistk.data import ObjectInfo, OrchestratorInstanceStatus, ServiceError
from mistk.watch import watch_manager
from mistk.orchestrator.server.controllers import orchestrator_instance_endpoint_controller
import mistk.data.utils as datautils

class OrchestratorInstanceTask:
    """
    A task to be submitted to the Orchestrator Instance that will be performed and report status of.
    """

    def __init__(self, operation, parameters = None, submitted = None,
                 completed = None, status = None, message = None):
        """
        Initializes the Orchestrator Instance Task

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

class OrchestratorInstanceEndpoint():

    def __init__(self):
        """
        Initializes the Orchestrator Instance Endpoint service
        """

        initializeEndpointController(self, orchestrator_instance_endpoint_controller)

        self.app = cx.FlaskApp('mistk_server')
        self.app.app.json_encoder = datautils.PresumptiveJSONEncoder
        self.app.add_api(self._load_api_spec())
        self.http_server = None

        self._state_machine = None
        self._orchestrator = None
        self._current_task = None

        self._status_lock = RWLock()
        self._task_lock = RWLock()

        self._response_queue = Queue()

        self._old_tasks = list()
        self._thread_pool = ThreadPoolExecutor()

        info = ObjectInfo('OrchestratorInstanceStatus', resource_version=1)
        self._status = OrchestratorInstanceStatus(object_info=info, state='uninitialized')

        self._header_json = ("Content-Type","application/json")

    def start_server(self, port=8080, process=False):
        """
        Starts the http server of the Service

        :param port: The port on which to start the server, defaults to 8080
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
        return yaml.load(pkg_resources.ResourceManager().resource_stream('mistk', '/orchestrator/server/swagger/swagger.yaml'), Loader=yaml.SafeLoader)

    @property
    def state_machine(self):
        """
        Retrieves the state machine associated with this OrchestratorEndpointService

        :return: the state machine
        """
        return self._state_machine

    @state_machine.setter
    def state_machine(self, state_machine):
        """
        Sets the state machine associated with this OrchestratorEndpointService

        :param state_machine: The new state machine to set
        """
        self._state_machine = state_machine

    @property
    def orchestrator(self):
        """
        Retrieves the orchestrator associated with this OrchestratorEndpointService

        :return: the orchestrator
        """
        return self._orchestrator

    @orchestrator.setter
    def orchestrator(self, orchestrator):
        """
        Sets the orchestrator associated with this OrchestratorEndpointService

        :param orchestrator: the new orchestrator to set
        """
        self._orchestrator = orchestrator

    def initialize(self, initializationParameters):
        """
        Creates and returns an Task which initializes the orchestrator with the
        optional parameters provided

        :param initializationParameters: The parameters used for initialization
        :return: The created Task object
        """
        logger.debug("Initialize orchestrator called")
        try:
            params = initializationParameters
            if not isinstance(params, InitParams) and cx.request.is_json:
                params = datautils.deserialize_model(cx.request.get_json(), InitParams)
            assert isinstance(params, InitParams)

            task = OrchestratorInstanceTask(operation='initialize',
                parameters={"env": params.env,
                            "agents_needed": params.agents_needed})
            logger.debug('Created initialize orchestrator task', extra={'orchestrator_task': task})

            self.add_task(task)
            return Response(status=200, headers=[self._header_json])
        except RuntimeError as inst:
            msg = "Error during orchestrator initialization: %s" % str(inst)
            logger.exception(msg)
            return ServiceError(500, msg), 500

    def register_agent(self, agentName, agentUrl, skipTrain=None):
        """
        Creates & returns a Task which registers an agent to the orchestrator

        :param agentName: The name of the agent
        :param agentUrl: The URL to the agent object
        :param skipTrain: If we shouldn't train this agent [Default = False]
        :return: The created Task object
        """
        logger.debug("build orchestrator called")
        try:
            task = OrchestratorInstanceTask(operation="register_agent",
                                            parameters={"agent_name": agentName,
                                                        "agent_url": agentUrl,
                                                        "skip_train": skipTrain})
            self.add_task(task)
            return Response(status=200, headers=[self._header_json])
        except RuntimeError as inst:
            msg = "Error while adding agent to the orchestrator: %s" % str(inst)
            logger.exception(msg)
            return ServiceError(500, msg), 500

    def start_episode(self, episodeCfg):
        """
        Starts an episode of playing the game

        :param episode_cfg: Dictionary with the episode's config settings
        :return: The created Task object
        """
        logger.debug("Start Episode called")
        if not episodeCfg:
            episodeCfg = {}
        try:
            self.add_task(OrchestratorInstanceTask(operation="start_episode",
                                                   parameters={"episode_cfg": episodeCfg}))
            return Response(status=200, headers=[self._header_json])
        except RuntimeError as inst:
            msg = "Error while starting episode: %s" % str(inst)
            logger.exception(msg)
            return ServiceError(500, msg), 500

    def stop_episode(self):
        """
        Stops the episode
        """
        logger.debug("Stop episode called")
        try:
            self.add_task(OrchestratorInstanceTask(operation="stop_episode"))
            return Response(status=200, headers=[self._header_json])
        except RuntimeError as inst:
            msg = "Error while stopping the episode: %s" % str(inst)
            logger.exception(msg)
            return ServiceError(500, msg), 500

    def save_episode(self, path):
        """
        Saves the episode
        """
        logger.debug("Save episode called")
        try:
            self.add_task(OrchestratorInstanceTask(operation="save_episode",
                                                   parameters={"path": path}))
            return Response(status=200, headers=[self._header_json])
        except RuntimeError as inst:
            msg = "Error while saving the episode: %s" % str(inst)
            logger.exception(msg)
            return ServiceError(500, msg), 500

    def reset(self):
        """
        Resets the orchestrator
        """
        logger.debug("Reset called")
        try:
            self.add_task(OrchestratorInstanceTask(operation="reset"))
            return Response(status=200, headers=[self._header_json])
        except RuntimeError as inst:
            msg = "Error while stopping the episode: %s" % str(inst)
            logger.exception(msg)
            return ServiceError(500, msg), 500


    def get_status(self, watch=None, resourceVersion=None):
        """
        Retrieves the status of this OrchestratorEndpointService

        :param watch: Optional flag indicating whether state changes should be monitored
        :param resourceVersion: Optional version id that will be used as the minimum version number
            for watched status changes.
        :return: The current status of this OrchestratorEndpointService
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
            msg = "Error while retrieving status for OrchestratorEndpointService: %s" % str(inst)
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
        Adds a task to this OrchestratorEndpointService and starts it using a pool of worker threads

        :param task: The Task to register and start
        :return: The running task
        """
        try:
            task.id = uuid.uuid4().hex
            task.status = 'queued'
            task.submitted = datetime.now()
            ops = ['initialize', 'load_data', 'build_orchestrator',
                   'register_agent', 'pause', 'unpause',
                   'start_episode', 'stop_episode', 'save_episode',
                   'register_agent', 'reset']

            if not task.operation in ops:
                msg = "Operation %s must be one of %s" % (str(task.operation), str(ops))
                logger.error(msg)
                return ServiceError(400, msg), 400

            with self._task_lock.writer_lock:
                if isinstance(self._current_task, OrchestratorInstanceTask):
                    status = self._current_task.status
                    if not status == 'complete' and not status == 'failed':
                        return "Cannot submit a task while current task is not complete.  Current task status is " + status, 400
                if self._current_task:
                    self._old_tasks.insert(0, self._current_task)
                self._current_task = task
                task.status = 'running'

            if not self._valid_task_transition():
                msg = "Operation %s invalid from state %s" % (str(self._current_task.operation), str(self.orchestrator.state))
                self._current_task.status = 'failed'
                logger.exception(msg)
                raise RuntimeError(msg)

            self._thread_pool.submit(self._process_task)
            return task

        except RuntimeError as inst:
            msg = "Error while adding task to OrchestratorEndpointService and starting the task. %s" % str(inst)
            logger.exception(msg)
            raise RuntimeError(msg)

    def update_state(self, state=None, payload=None):
        """
        Updates the state of the OrchestratorEndpointService

        :param state: The new state. If not given, the current state will be used.
        :param payload: Additional data to attach to the state
        """
        try:
            with self._status_lock.writer_lock:
                state = state or self._status.state
                ver = self._status.object_info.resource_version + 1
                info = ObjectInfo('OrchestratorInstanceStatus', resource_version=ver)
                self._status = OrchestratorInstanceStatus(info, state=state, payload=payload)
                watch_manager.notify_watch('status', item=self._status)
        except RuntimeError as inst:
            msg = "Error while updating state of the OrchestratorEndpointService. %s" % str(inst)
            logger.exception(msg)
            return ServiceError(500, msg), 500

    def put_response(self, response):
        """
        Adds a response to the response queue
        """
        self._response_queue.put(response)

    def _get_response(self):
        """
        Pops the latest response on the response queue
        """
        return self._response_queue.get()

    def _valid_task_transition(self) -> bool:
        """
        Valid operation task from current state

        :return: True if a valid transition, False if a invalid transition
        """

        logger.debug(f'valid state: {self.orchestrator._machine.get_triggers(self.orchestrator.state)}')
        if self._current_task.operation in self.orchestrator._machine.get_triggers(self.orchestrator.state):
            return True
        else:
            return False

    def _process_task(self):
        """
        Processes the currently queued Task and updates its status as appropriate
        """
        try:
            logger.info('Processing task %s', self._current_task.operation)
            m = getattr(self.orchestrator, self._current_task.operation)
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
