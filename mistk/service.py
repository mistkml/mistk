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
import inspect
import itertools
import uuid

from queue import Queue
from flask import Response
from rwlock.rwlock import RWLock

import connexion as cx
from mistk import logger
from mistk.data import ModelInstanceInitParams as InitParams
from mistk.data import ObjectInfo, ModelInstanceStatus, ServiceError, MistkDataset
from mistk.watch import watch_manager
from mistk.server.controllers import model_instance_endpoint_controller
import mistk.data.utils as datautils
import yaml
import os, sys
import pkg_resources
import wsgiserver

class ModelInstanceTask:
    """
    A task to be submitted to the Model Instance that will be performed and report status of.
    """
    
    def __init__(self, operation, parameters = None, submitted = None, 
                 completed = None, status = None, message = None):
        """
        Initializes the Model Instance Task
        
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
     
class ModelInstanceEndpoint():
    
    def __init__(self):
        """
        Initializes the Model Instance Endpoint service
        """
    
        initializeEndpointController(self, model_instance_endpoint_controller)

        self.app = cx.FlaskApp('mistk_server')
        self.app.app.json_encoder = datautils.PresumptiveJSONEncoder
        self.app.add_api(self._load_api_spec())
        self.http_server = None
        
        self._state_machine = None
        self._model = None
        self._current_task = None
        
        self._status_lock = RWLock() 
        self._task_lock = RWLock()
        
        self._response_queue = Queue()
         
        self._old_tasks = list()
        self._thread_pool = ThreadPoolExecutor()
        
        info = ObjectInfo('ModelInstanceStatus', resource_version=1)
        self._status = ModelInstanceStatus(object_info=info, state='started')

    def start_server(self, port=8080):
        """
        Starts the http server of the Service
        
        :param port: The port on which to start the server, defaults to 8080
        """
        self.http_server = wsgiserver.WSGIServer(self.app, port=port)
        self.http_server.start()

    def _load_api_spec(self):
        """
        Gets the API specification of the module specified
        
        :param module: THe name of the module
        """
        return yaml.load(pkg_resources.ResourceManager().resource_stream('mistk', '/server/swagger/swagger.yaml'))

    @property
    def state_machine(self):
        """
        Retrieves the state machine associated with this ModelEndpointService
        
        :return: the state machine
        """
        return self._state_machine
    
    @state_machine.setter
    def state_machine(self, state_machine):
        """
        Sets the state machine associated with this ModelEndpointService
        
        :param state_machine: The new state machine to set
        """
        self._state_machine = state_machine

    @property
    def model(self):
        """
        Retrieves the model associated with this ModelEndpointService
        
        :return: the model
        """
        return self._model
    
    @model.setter
    def model(self, model):
        """
        Sets the model associated with this ModelEndpointService
        
        :param model: the new model to set
        """
        self._model = model
                
    def initialize_model(self, initializationParameters):
        """
        Creates and returns an Task which initializes the model with the 
        optional parameters provided
        
        :param initializationParameters: The parameters used for initialization
        :return: The created Task object
        """
        logger.debug("Initialize model called")
        try:
            params = initializationParameters
            if not isinstance(params, InitParams) and cx.request.is_json:
                params = datautils.deserialize_model(cx.request.get_json(), InitParams)
            assert isinstance(params, InitParams)
           
            task = ModelInstanceTask(operation='initialize',
                parameters={"objectives": params.objectives, 
                            "props": params.model_properties, 
                            "hparams": params.hyperparameters})
            logger.debug('Created initialize model task: %s' % str(task))
        except RuntimeError as inst:
            return ServiceError(500, str(inst)), 500
        
        self.add_task(task)
        
    def build_model(self, modelPath=None):
        """
        Creates and returns a Task which builds the model using the modelPath provided
        
        :param modelPath: The path to where the model image can be found
        :return: The created Task object
        """
        logger.debug("build model called")
        try:
            task = ModelInstanceTask(operation="build_model", 
                                        parameters = {"path": modelPath})
            self.add_task(task)
        except RuntimeError as inst:
            return ServiceError(500, str(inst)), 500    
        
    def load_data(self, datasets):
        """
        Creates and returns a Task which loads data into a model using the bindings provided
        
        :param datasets: dictionary mapping dataset function to dataset
        :return: The create Task object
        """
        logger.debug("Load data called")
        try:            
            if not isinstance(list(datasets.values())[0], MistkDataset) and cx.request.is_json:
                datasets = {key : datautils.deserialize_model(ds, MistkDataset) for 
                            key, ds in cx.request.get_json().items()}
                        
            task = ModelInstanceTask(operation="load_data",
                        parameters = {"dataset_map": datasets})
            self.add_task(task)
        except RuntimeError as inst:
            return ServiceError(500, str(inst)), 500 

    def train(self):
        """
        Creates and returns a Task which kicks off a training activity
        
        :return: The created Task object
        """
        logger.debug("Train called")
        try:
            self.add_task(ModelInstanceTask(operation="train"))
        except RuntimeError as inst:
            return ServiceError(500, str(inst)), 500
        
    def save_model(self, modelPath):
        """
        Creates and returns a Task which saves the model to the path provided
        
        :param modelPath: The path where the model will be saved. 
        :return: The created Task object
        """
        try:
            task = ModelInstanceTask(operation="save_model", 
                                    parameters = {"path": modelPath})
            self.add_task(task)
        except RuntimeError as inst:
            return ServiceError(500, str(inst)), 500            
        
    def predict(self):
        """
        Creates and returns a Task which kicks off a prediction activity
        
        :return: The created Task object
        """
        logger.debug("Predict called")
        try:
            self.add_task(ModelInstanceTask(operation="predict"))
        except RuntimeError as inst:
            return ServiceError(500, str(inst)), 500
        
    def stream_predict(self, dataMap):
        """
        Creates a Task which kicks off a stream prediction activity
        
        :param dataMap: Dictionary of IDs to b64 encoded data
        :return: Dictionary of IDs to predictions
        """
        try:
            task = ModelInstanceTask(operation="stream_predict", 
                                    parameters = {"data_map": dataMap})
            self.add_task(task)
            return self._get_response()
        except RuntimeError as inst:
            return ServiceError(500, str(inst)), 500    
        
    def save_predictions(self, dataset):
        """
        Creates and returns a Task which saves the predictions generated by a model
        to the path specified
        
        :param dataPath: The location in which to save the model predictions
        :return: The created Task object
        """
        try:
            if not isinstance(dataset, MistkDataset) and cx.request.is_json:
                dataset = datautils.deserialize_model(cx.request.get_json(), MistkDataset)
        
            task = ModelInstanceTask(
                operation="save_predictions",
                parameters = {"dataPath": dataset.data_path})

            self.add_task(task)
        except RuntimeError as inst:
            return ServiceError(500, str(inst)), 500             
        
    def pause (self):
        """
        Pauses the model during its current operation
        This operation is currently not supported. 
        """
        return ServiceError(500, "Not implemented"), 500
    
    def resume_training(self):
        """
        Resumes a paused model into its training operation
        This operation is currently not supported. 
        """
        return ServiceError(500, "Not implemented"), 500
    
    def resume_predict(self):
        """
        Resumes a paused model into its prediction operation
        This operation is currently not supported. 
        """
        return ServiceError(500, "Not implemented"), 500
        
    def terminate(self):
        """
        Shuts down the model and the endpoint service
        """
        logger.debug("Terminate called")
        try:
            self.add_task(ModelInstanceTask(operation="terminate"))
        except RuntimeError as inst:
            return ServiceError(500, str(inst)), 500
    
    def reset(self):
        """
        Resets the model
        """
        try:
            def generate():
                try:
                    yield "resetting..."
                finally:
                    os.execv(sys.executable, ['python'] + sys.argv)
            return Response(generate(), mimetype='text/plain')
        except RuntimeError as inst:
            return ServiceError(500, str(inst)), 500 
            
    
    def get_status(self, watch=None, resourceVersion=None):
        """
        Retrieves the status of this ModelEndpointService
        
        :param watch: Optional flag indicating whether state changes should be monitored
        :param resourceVersion: Optional version id that will be used as the minimum version number
            for watched status changes. 
        :return: The current status of this ModelEndpointService
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
            return ServiceError(500, str(inst)), 500
      
    def delete_task(self, task):
        """
        Deletes the specified Task.
        This function is currently not supported
        
        :param task: The task to delete
        """
        logger.debug("Ignoring delete task request: %s", str(task))
        return ServiceError(501, "Not currently supported"), 501
     
    def add_task(self, task):
        """
        Adds a task to this ModelEndpointService and starts it using a pool of worker threads
        
        :param task: The Task to register and start
        :return: The running task
        """
        try:
            task.id = uuid.uuid4().hex
            task.status = 'queued'
            task.submitted = datetime.now()
            ops = ['initialize', 'load_data', 'build_model', 'train', 'pause', 
                   'unpause', 'save_model', 'predict', 'save_predictions', 'stream_predict'] 
             
            if not task.operation in ops:
                return ServiceError(400, "Operation %s must be one of %s" % 
                                (str(task.operation), str(ops))), 400
         
            with self._task_lock.writer_lock:
                if isinstance(self._current_task, ModelInstanceTask):
                    status = self._current_task.status
                    if not status == 'complete' and not status == 'failed':
                        return "Cannot submit a task while current task is not complete.  Current task status is " + status, 400
                if self._current_task:
                    self._old_tasks.insert(0, self._current_task)
                self._current_task = task
                task.status = 'running'

            self._thread_pool.submit(self._process_task)
            return task
        
        except RuntimeError as inst:
            return ServiceError(500, str(inst)), 500

    def update_state(self, state=None, payload=None):
        """
        Updates the state of the ModelEndpointService
        
        :param state: The new state. If not given, the current state will be used.
        :param payload: Additional data to attach to the state
        """
        try:
            with self._status_lock.writer_lock:
                state = state or self._status.state
                ver = self._status.object_info.resource_version + 1
                info = ObjectInfo('ModelInstanceStatus', resource_version=ver)
                self._status = ModelInstanceStatus(info, state=state, payload=payload)
                watch_manager.notify_watch('status', item=self._status)
        except RuntimeError as inst:
            return ServiceError(500, str(inst)), 500
        
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
                     
    def _process_task(self):
        """
        Processes the currently queued Task and updates its status as appropriate        
        """
        try:
            logger.info('Processing task %s', self._current_task.operation)
            m = getattr(self.model, self._current_task.operation)
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
        assert sig1 == sig2, "Can't redirect " + name +" : " + str(sig1) + "-" + str(sig2)
        globals()[name] = getattr(handler, name)
