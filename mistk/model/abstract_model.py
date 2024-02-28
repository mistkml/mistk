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

from mistk.data import ServiceError
from mistk.model.service import ModelInstanceEndpoint
from mistk import logger
import sys

# The model states
_model_states = {'started', 'initializing', 'initialized', 'failed', 'loading_data',
                 'building_model', 'building_ensemble', 'ready', 'pausing', 'paused', 'unpausing', 'training', 'updating_properties',
                 'predicting', 'generating', 'miniaturizing', 'saving_model', 'saving_predictions', 'saving_generations',
                 'terminating', 'terminated', 'resetting'}

class AbstractModel (metaclass=ABCMeta):
    """
    The definition of an abstract Model to be implemented by Model developers.
    """
    
    @abstractmethod
    def __init__(self):
        """
        Initializes the Model and registers the default state machine transitions 
        available to all models.
        """
        self.state = None
        self._endpoint_service = None
        states = [State(n, on_enter='new_state_entered') for n in _model_states]
        self._machine = Machine(model=self, states=states, initial='started', auto_transitions=False)
        self._machine.add_transition(trigger='fail', source=list(_model_states-{'terminated'}), dest='failed')
        self._machine.add_transition(trigger='initialize', source='started', dest='initializing', after='_do_initialize')
        self._machine.add_transition(trigger='initialized', source=['initializing', 'loading_data'], dest='initialized')
        self._machine.add_transition(trigger='load_data', source=['initialized', 'ready'], dest='loading_data', after='_do_load_data')
        self._machine.add_transition(trigger='build_model', source='initialized', dest='building_model', after='_do_build_model')
        self._machine.add_transition(trigger='build_ensemble', source='initialized', dest='building_ensemble', after='_do_build_ensemble')
        self._machine.add_transition(trigger='ready', source=['loading_data', 'building_model', 'building_ensemble', 'training', 'updating_properties', 'predicting', 'generating', 'miniaturizing', 'saving_model', 'saving_predictions', 'saving_generations', 'resetting'], dest='ready')
        self._machine.add_transition(trigger='train', source='ready', dest='training', after='_do_train')
        self._machine.add_transition(trigger='pause', source=['training', 'predicting'], dest='pausing', after='_do_pause')
        self._machine.add_transition(trigger='paused', source='pausing', dest='paused')
        self._machine.add_transition(trigger='resume_training', source='paused', dest='training', after='_do_resume_training')
        self._machine.add_transition(trigger='resume_predicting', source='paused', dest='predicting', after='_do_resume_predict')
        self._machine.add_transition(trigger='save_model', source=['ready', 'paused'], dest='saving_model', after='_do_save_model')
        self._machine.add_transition(trigger='predict', source='ready', dest='predicting', after='_do_predict')
        self._machine.add_transition(trigger='stream_predict', source='ready', dest='predicting', after='_do_stream_predict')
        self._machine.add_transition(trigger='update_stream_properties', source='ready', dest='updating_properties', after='_do_update_stream_properties')
        self._machine.add_transition(trigger='save_predictions', source='ready', dest='saving_predictions', after='_do_save_predictions')
        self._machine.add_transition(trigger='generate', source='ready', dest='generating', after='_do_generate')
        self._machine.add_transition(trigger='miniaturize', source='ready', dest='miniaturizing', after='_do_miniaturize')
        self._machine.add_transition(trigger='save_generations', source='ready', dest='saving_generations', after='_do_save_generations')
        self._machine.add_transition(trigger='terminate', source=list(_model_states-{'terminating', 'terminated', 'failed'}), dest='terminating', after='_do_terminate')
        self._machine.add_transition(trigger='terminated', source='terminating', dest='terminated')
        self._machine.add_transition(trigger='reset', source=list(_model_states-{'terminating', 'terminated'}), dest='resetting', after='_do_reset')        
        
        self._model_built = False
        self._ensemble_built = False
        self._response = None
        
    def update_status(self, payload):
        """
        Provides additional details to the current state of the model.  If the model is 
        training, then this might contain the number of records that have been trained.
        
        :param payload: Extra information regarding the status update
        """
        self.endpoint_service.update_state(state=None, payload=payload)
                
    @property
    def endpoint_service(self) -> ModelInstanceEndpoint:
        """
        Returns the endpoint service for this Model
        """
        return self._endpoint_service
        
    @endpoint_service.setter
    def endpoint_service(self, endpoint_service: ModelInstanceEndpoint):
        """
        Sets the endpoint service to the provided ModelEndpointService
        
        :param endpoint_service: The new ModelEndpointService         
        """
        self._endpoint_service = endpoint_service
        
    def new_state_entered(self, *args, **kwargs):
        """
        Notifies the endpoint service that the current state of the state machine has been update 
        
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
        Triggers the model to enter the failed state.
        This method should not be implemented or overwritten by subclasses.  It will be 
        created by the state machine.
        
        :param reason: The reason why the state machine is transitioned into the failure state
        """
        pass
    
    def initialize(self, objectives, props, hparams):
        """
        Triggers the model to enter the initializing state.  A subsequent call to
        do_initialize with the given parameters will be made as a result.
        This method should not be implemented or overwritten by subclasses.  It will be 
        created by the state machine.
        
        :param objectives: The objectives of this model. Possible values include 'training', 'prediction', 
            'streaming_prediction', and 'transfer_learning'.
        :param props: A dictionary that is parsed from a JSON string. These are settings that are passed from the ecosystem, 
            but are not really considered hyperparameters.  They are not used by the model, but rather the endpoint itself 
            (e.g., where should heartbeats be sent and how often, etc).
        :param hparams: A dictionary that is parsed from a JSON string. These are the hyperparameters that are used by the model.
        """
        logger.debug('Called abstractModel.initialize')
        pass
    
    def initialized(self):
        """
        Triggers the model to enter the initialized state.  It is expected that this 
        method will only be called by the implementing model subclass.

        This method should not be implemented or overwritten by subclasses.  It will be 
        created by the state machine.
        """
        logger.debug('Called abstractModel.initialized')
        pass
            
    def load_data(self, dataset_map):
        """
        Triggers the model to enter the loading_data state.  A subsequent call to
        do_load_data with the given parameters will be made as a result.

        This method should not be implemented or overwritten by subclasses.  It will be 
        created by the state machine.
        
        :param dataset_map: A dictionary that maps string keys {train, test, generation} to a
            Dataset object that contains information on the dataset to load
        """
        pass

    def build_model(self, path=None):
        """
        Triggers the model to enter the building_model state.  A subsequent call to
        do_build_model with the given parameters will be made as a result.

        This method should not be implemented or overwritten by subclasses.  It will be 
        created by the state machine.
        
        :param path: The path to the model file
        """
        pass
    
    def build_ensemble(self, ensemble_path=None, model_paths: dict=None):
        """
        Triggers the model to enter the building_ensemble state.  A subsequent call to
        do_build_ensemble with the given parameters will be made as a result.

        This method should not be implemented or overwritten by subclasses.  It will be 
        created by the state machine.
        
        :param ensemble_path: The path to the ensemble model file
        :param model_paths: The paths to the model files in a dictionary. The key is the model name with the value being the model path.
        """
        pass
    
    def miniaturize(self, dataPath, includeHalfPrecision):
        """
        Triggers the model to enter the miniaturize state.  A subsequent call to
        do_miniaturize with the given parameters will be made as a result.

        This method should not be implemented or overwritten by subclasses.  It will be
        created by the state machine.

        :param dataPath: miniaturized model with be saved
        :param includeHalfPrecision: a flag to indicate whether to use half precision for the miniaturized model
        """
        pass

    
    def ready(self):
        """
        Triggers the model to enter the ready state.  It is expected that this 
        method will only be called by the implementing model subclass.

        This method should not be implemented or overwritten by subclasses.  It will be 
        created by the state machine.
        """
        pass
    
    def train(self):
        """
        Triggers the model to enter the training state.  A subsequent call to
        do_train with the given parameters will be made as a result.

        This method should not be implemented or overwritten by subclasses.  It will be 
        created by the state machine.
        """
        pass

    def pause(self):
        """
        Triggers the model to enter the pausing state.  A subsequent call to
        do_pause with the given parameters will be made as a result.

        This method should not be implemented or overwritten by subclasses.  It will be 
        created by the state machine.
        """
        pass
    
    def paused(self):
        """
        Triggers the model to enter the paused state.  It is expected that this 
        method will only be called by the implementing model subclass.

        This method should not be implemented or overwritten by subclasses.  It will be 
        created by the state machine.
        """        
        pass
    
    def unpause(self):
        """
        Triggers the model to enter the unpausing state.  A subsequent call to
        do_unpause with the given parameters will be made as a result.

        This method should not be implemented or overwritten by subclasses.  It will be 
        created by the state machine.
        """
        pass
    
    def save_model(self, path):
        """
        Triggers the model to enter the unpausing state.  A subsequent call to
        do_unpause with the given parameters will be made as a result.

        This method should not be implemented or overwritten by subclasses.  It will be 
        created by the state machine.
        """
        pass
        
    def predict(self):
        """
        Triggers the model to enter the predicting state.  A subsequent call to
        do_predict with the given parameters will be made as a result.

        This method should not be implemented or overwritten by subclasses.  It will be 
        created by the state machine.
        """
        pass
    
    def stream_predict(self, data_map, details):
        """
        Triggers the model to enter the predicting state.  A subsequent call to
        do_stream_predict with the given parameters will be made as a result.

        This method should not be implemented or overwritten by subclasses.  It will be 
        created by the state machine.

        :param data_map: A dictionary of ID keys to base64 encoded data
        :param details: Optional parameter for the model to provide additional details
        """
        pass

    def update_stream_properties(self, props):
        """
        Triggers the model to update the streaming properties.  A subsequent call to
        do_update_stream_properties with the given parameters will be made as a result.

        This method should not be implemented or overwritten by subclasses.  It will be 
        created by the state machine.

        :param props: A dictionary of metadata properties to be used by the model
        """
        pass
    
    def save_predictions(self, dataPath):
        """
        Triggers the model to enter the saving_predictions state.  A subsequent call to
        do_save_predictions with the given parameters will be made as a result.

        This method should not be implemented or overwritten by subclasses.  It will be 
        created by the state machine.
        
        :param dataPath: The file path to where the model predictions will be saved. This can be the local
            file system or on the distributed file system 
        """
        pass
    
    def generate(self):
        """
        Triggers the model to enter the generating state.  A subsequent call to
        do_generate with the given parameters will be made as a result.

        This method should not be implemented or overwritten by subclasses.  It will be 
        created by the state machine.
        """
        pass
    
    def save_generations(self, dataPath):
        """
        Triggers the model to enter the saving_generations state.  A subsequent call to
        do_save_generations with the given parameters will be made as a result.

        This method should not be implemented or overwritten by subclasses.  It will be 
        created by the state machine.
        
        :param dataPath: The file path to where the model generations will be saved. This can be the local
            file system or on the distributed file system 
        """
        pass

    def report_failure(self, reason):
        """
        Reports the failure of a model during its operations
        
        :param reason: The error message explaining why the model failed. 
        """
        logger.info ('Model has failed: ' + str(reason))
        
    def terminated(self):
        """
        Terminates the model
        """
        logger.info("Shutting down")
        sys.exit()
        
    
    def reset(self):
        """
        Resets the model container instance
        """
        pass
    
            
    def _do_initialize(self, objectives : list, props : dict, hparams : dict):
        """
        Called once the endpoint service has launched.  This would typically be the first call made to the service. 
        
        :param objectives: The objectives for the model. Possible values include 'training', 'prediction', 
            'streaming_prediction', 'generation', and 'transfer_learning'.
        :param props: A dictionary that is parsed from a JSON string. These are settings that are passed from the ecosystem, 
            but are not really considered hyperparameters.  They are not used by the model, but rather the endpoint itself 
            (e.g., where should heartbeats be sent and how often, etc).
        :param hparams: A dictionary that is parsed from a JSON string. These are the hyperparameters that are used by the model.
        """        
        try:
            logger.debug("_do_initialize called")
            self.do_initialize(objectives, props, hparams)
            logger.debug("Changing state to 'initialized'")
            self.initialized()
            logger.debug("_do_initialize complete")
        except Exception as ex: #pylint: disable=broad-except
            logger.exception("Error running do_initalize")
            self.fail(str(ex))
            
    @abstractmethod
    def do_initialize(self, objectives : list, props : dict, hparams : dict):
        """
        Called once the endpoint service has launched.  This would typically be the first call made to the service. 
        
        :param objective: The objectives for the model. Possible values include 'training', 'prediction', 
            'streaming_prediction', 'generation', and 'transfer_learning'.
        :param props: A dictionary that is parsed from a JSON string. These are settings that are passed from the ecosystem, 
            but are not really considered hyperparameters.  They are not used by the model, but rather the endpoint itself 
            (e.g., where should heartbeats be sent and how often, etc).
        :param hparams: A dictionary that is parsed from a JSON string. These are the hyperparameters that are used by the model.
        """
        pass
    
    def _do_load_data(self, dataset_map: dict):
        """
        Instructs the container to load data (or at least record in memory where the data is, if it’s actually to be loaded during training).
        
        :param dataset_map: A dictionary that maps string keys {train, test, generation} to a
            Dataset object that contains information on the dataset to load
        """
        try:
            self.do_load_data(dataset_map)
            if self._model_built:
                self.ready()
            else:
                self.initialized()
        except Exception as ex: #pylint: disable=broad-except
            logger.exception("Error running do_load_data")
            self.fail(str(ex))    
    
    @abstractmethod
    def do_load_data(self, dataset_map: dict):
        """
        Instructs the container to load data (or at least record in memory where the data is, if it’s actually to be loaded during training).
        
        :param dataset_map: A dictionary that maps string keys {train, test, generation} to a
            Dataset object that contains information on the dataset to load
        """
        pass
            
    def _do_build_model(self, path=None):
        """
        Instructs the service to build all necessary data structures given the architecture and selected hyperparameters.
        
        :param path: The path to the model file
        """
        try:
            if path=='None': path=None
            self.do_build_model(path)
            self._model_built = True            
            self.ready()
        except Exception as ex: #pylint: disable=broad-except
            logger.exception("Error running do_build_model")
            self.fail(str(ex))    
            
    @abstractmethod
    def do_build_model(self, path=None):
        """
        Instructs the service to build all necessary data structures given the architecture and selected hyperparameters.
        
        :param path: The directory path to the model file
        """
        pass

    
    def _do_build_ensemble(self, ensemble_path=None, model_paths: dict=None):
        """
        Instructs the service to build all necessary models used for the ensemble model.
        :param ensemble_path: The directory path to the ensemble model file
        :param model_paths: The directory paths to the model files in a dictionary. The key is the model name with the value being the model path.
        """
        try:
            if model_paths=='None': model_paths=None
            self.do_build_ensemble(ensemble_path, model_paths)
            self._ensemble_built = True            
            self._do_build_model(ensemble_path)
        except Exception as ex: #pylint: disable=broad-except
            logger.exception("Error running do_build_ensemble")
            self.fail(str(ex))

    #@abstractmethod
    def do_build_ensemble(self, ensemble_path=None, model_paths: dict=None):
        """
        Instructs the service to build all necessary ensemble data structures given the architecture and selected hyperparameters.
        
        :param ensemble_path: The path to the ensemble model file
        :param model_paths: The paths to the model files in a dictionary. The key is the model name with the value being the model path.
        """
        pass

    def _do_train(self):
        """
        Executes/resumes the training activity
        """
        logger.debug("_do_train started")
        try:
            logger.info("Calling do_train method.")
            self.do_train()
            self.ready()
        except Exception as ex: #pylint: disable=broad-except
            logger.exception("Error running do_train")
            self.fail(str(ex))
        logger.debug("_do_train complete")
            
    @abstractmethod
    def do_train(self):
        """
        Executes/resumes the training activity
        """
        pass
    
    def _do_save_model(self, path):
        """
        Save the model to an agreed upon location. It will be up to some other process to make sure 
        the saved model ends up back in the repository. This call could be a NOOP if, for instance, 
        the model is saved periodically throughout the training process.
        
        :param path: The path to which the model should be saved. 
        """
        try:
            self.do_save_model(path)
            self.ready()
        except Exception as ex: #pylint: disable=broad-except
            logger.exception("Error running do_save_model")
            self.fail(str(ex))
                
    @abstractmethod
    def do_save_model(self, path):
        """
        Save the model to an agreed upon location. It will be up to some other process to make sure 
        the saved model ends up back in the repository. This call could be a NOOP if, for instance, 
        the model is saved periodically throughout the training process.
        
        :param path: The path to which the model should be saved. 
        """
        pass

    def _do_pause(self):
        """
        Pauses the current activity (training or prediction).
        """
        try:
            self.do_pause()
            self.paused()
        except Exception as ex: #pylint: disable=broad-except
            logger.exception("Error running do_pause")
            self.fail(str(ex))
    
    @abstractmethod
    def do_pause(self):
        """
        Pauses the current activity (training or prediction).
        This operation is currently not supported. 
        """
        pass

    def _do_resume_training(self):
        """
        Unpauses the current activity (training or prediction).
        """
        try:
            self.do_resume_training()
        except Exception as ex: #pylint: disable=broad-except
            logger.exception("Error running do_resume_training")
            self.fail(str(ex))
    
    @abstractmethod
    def do_resume_training(self):
        """
        Unpauses the current activity (training or prediction).
        This operation is currently not supported. 
        """
        pass

    def _do_resume_predict(self):    
        """
        Executes/resumes the prediction activity
        """
        try:
            self.do_resume_predict()
        except Exception as ex: #pylint: disable=broad-except
            logger.exception("Error running do_resume_predict")
            self.fail(str(ex))
    
    @abstractmethod
    def do_resume_predict(self):
        """
        Executes/resumes the prediction activity
        """
        pass
    
    def _do_predict(self):
        """
        Executes/resumes the prediction activity
        """
        try:
            self.do_predict()
            self.ready()
        except Exception as ex: #pylint: disable=broad-except
            logger.exception("Error running do_predict")
            self.fail(str(ex))
            
    @abstractmethod
    def do_predict(self):
        """
        Executes/resumes the prediction activity
        """
        pass
    
    def _do_stream_predict(self, data_map: dict, details: bool=False):
        """
        Executes/resumes the stream prediction activity. 
        Perform predictions on the input dict of id's to base64 encoded data and return a dict of id's
        to predicted values. The underlying format of the base64 encoded data should be the native input 
        format for the model.
        
        :param data_map: Dictionary for streaming data. Generally, the key would be the data id or file name and the 
            value would be the base64 encoded data.
        :param details: Optional parameter for the model to provide additional details (in Markdown or HTML) within 
            the response dictionary under the key 'details'.
        """
        try:
            response = self.do_stream_predict(data_map, details)
            self.endpoint_service.put_response(response)
            self.ready()
        except Exception as ex: #pylint: disable=broad-except
            logger.exception("Error running do_stream_predict")
            msg = "Unexpected error occurred while running stream predict: %s" % str(ex)
            self.endpoint_service.put_response(ServiceError(500, msg))
            self.fail(str(ex))
    
    @abstractmethod
    def do_stream_predict(self, data_map: dict, details: bool=False):
        """
        Executes/resumes the prediction activity

        :param data_map: A dictionary of ID keys to base64 encoded data
        :param details: Optional parameter for the model to provide additional details
        """
        pass

    def _do_update_stream_properties(self, props: dict):
        """
        Updates the stream prediction properties

        :param props: A dictionary of streaming properties
        """
        try:
            self.do_update_stream_properties(props)
            self.ready()
        except Exception as ex: #pylint: disable=broad-except
            logger.exception("Error running do_update_stream_properties")
            self.fail(str(ex))

    #@abstractmethod
    def do_update_stream_properties(self, props: dict):
        """
        Updates the stream prediction properties

        :param props: A dictionary of streaming properties
        """
        pass
    
    def _do_save_predictions(self, dataPath):
        """
        Saves the current prediction to the location specified
        
        :param dataPath: The location on the local file system or distributed 
            file system where the predictions will be saved
        """
        try:
            self.do_save_predictions(dataPath)
            self.ready()
        except Exception as ex:  #pylint: disable=broad-except
            logger.exception("Error running do_save_predictions")
            self.fail(str(ex))
            
    @abstractmethod
    def do_save_predictions(self, dataPath):
        """
        Saves the current prediction to the location specified
        
        :param dataPath: The location on the local file system or distributed 
            file system where the predictions will be saved
        """
        pass
    
    def _do_generate(self):
        """
        Executes/resumes the generation activity
        """
        try:
            self.do_generate()
            self.ready()
        except Exception as ex: #pylint: disable=broad-except
            logger.exception("Error running do_generate")
            self.fail(str(ex))
            
    @abstractmethod
    def do_generate(self):
        """
        Executes/resumes the generate activity
        """
        pass
    
    def _do_save_generations(self, dataPath):
        """
        Saves the current generations to the location specified
        
        :param dataPath: The location on the local file system or distributed 
            file system where the generations will be saved
        """
        try:
            self.do_save_generations(dataPath)
            self.ready()
        except Exception as ex:  #pylint: disable=broad-except
            logger.exception("Error running do_save_generations")
            self.fail(str(ex))
            
    @abstractmethod
    def do_save_generations(self, dataPath):
        """
        Saves the current generations to the location specified
        
        :param dataPath: The location on the local file system or distributed 
            file system where the generations will be saved
        """
        pass
    
    def _do_terminate(self):
        """
        Stops all processing and releases any resources that are in use in
        preparation for being shut down.
        """
        try:
            self.do_terminate()
            self.terminated()
        except Exception as ex:  #pylint: disable=broad-except
            logger.exception("Error running do_terminate")
            self.fail(str(ex))
    
    @abstractmethod
    def do_terminate(self):
        """
        Stops all processing and releases any resources that are in use in
        preparation for being shut down.
        """
        pass
    
    def _do_reset(self):
        """
        Resets the model into its initial state
        """
        try:
            self.do_reset()
            self._model_built = False
            self.ready()
        except Exception as ex:  #pylint: disable=broad-except
            logger.exception("Error running do_reset")
            self.fail(str(ex))
    
    @abstractmethod
    def do_reset(self):
        """
        Resets the model into its initial state
        """
        pass

    def _do_miniaturize(self, dataPath, includeHalfPrecision):
        """
        Executes/resumes the miniaturize activity
        
        :param dataPath: The path to which the miniaturized model should be saved. 
        :param includeHalfPrecision: Miniaturize using half point precision format (FP16) for the model
        """
        try:
            self.do_miniaturize(dataPath, includeHalfPrecision)
            self.ready()
        except Exception as ex: #pylint: disable=broad-except
            logger.exception("Error running do_miniaturize")
            self.fail(str(ex))

    #@abstractmethod
    def do_miniaturize(self, dataPath, includeHalfPrecision):
        """
        Executes/resumes the miniaturize activity
        
        :param dataPath: The path to which the miniaturized model should be saved. 
        :param includeHalfPrecision: Miniaturize using half point precision format (FP16) for the model
        """
        pass