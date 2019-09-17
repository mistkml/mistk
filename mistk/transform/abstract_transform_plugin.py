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

from mistk.transform.service import TransformPluginEndpoint
import mistk.transform
from mistk import logger

# The model states
_transform_states = {'started', 'ready', 'failed', 
                  'transforming','terminating', 'terminated'}


class AbstractTransformPlugin (metaclass=ABCMeta):
    """
    classdocs
    """

    @abstractmethod
    def __init__(self):
        """
        Initializes the Model and registers the default state machine transitions 
        available to all models.ctor
        """
        
        self.state = None
        self._endpoint_service = None
        states = [State(n, on_enter='new_state_entered') for n in _transform_states]
        self._machine = Machine(model=self, states=states, initial='started', auto_transitions=False)
        self._machine.add_transition(trigger='fail', source=list(_transform_states-{'terminated'}), dest='failed')
        self._machine.add_transition(trigger='ready', source=['started', 'transforming'], dest='ready')
        self._machine.add_transition(trigger='transform', source=['started', 'ready'], dest='transforming', after='_do_transform')
        self._machine.add_transition(trigger='terminate', source=list(_transform_states-{'terminating', 'terminated', 'failed'}), dest='terminating', after='_do_terminate')
        self._machine.add_transition(trigger='terminated', source='terminating', dest='terminated')
    
    def update_status(self, payload):
        """
        Provides additional details to the current state of the model.  If the model is 
        training, then this might contain the number of records that have been trained.
        
        :param payload: Extra information regarding the status update
        """
        self.endpoint_service.update_state(state=None, payload=payload)
                
    @property
    def endpoint_service(self) -> TransformPluginEndpoint:
        """
        Returns the endpoint service for this Model
        """
        return self._endpoint_service
        
    @endpoint_service.setter
    def endpoint_service(self, endpoint_service: TransformPluginEndpoint):
        """
        Sets the endpoint service to the provided TransformPluginService
        
        :param endpoint_service: The new TransformPluginService         
        """
        self._endpoint_service = endpoint_service
        
    def new_state_entered(self, *args, **kwargs):
        """
        Notifies the endpoint service that the current state of the state machine has been update 
        
        :param args: Optional non-keyworded variable length arguments to pass in
        :param kwargs: Optional keyworded variable length arguments to pass in
        """
        logger.info("New state entered - %s {args: %s, kwargs: %s}", self.state, args, kwargs)
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
        
    def ready(self):
        """
        Triggers the model to enter the ready state.  It is expected that this 
        method will only be called by the implementing model subclass.

        This method should not be implemented or overwritten by subclasses.  It will be 
        created by the state machine.
        """
        pass

    def transform(self, inputDirs, outputDir, properties):
        """
        Triggers the model to enter the training state.  A subsequent call to
        do_train with the given parameters will be made as a result.

        This method should not be implemented or overwritten by subclasses.  It will be 
        created by the state machine.
        """
        pass
    
    def report_failure(self, reason):
        """
        Reports the failure of a model during its operations
        
        :param reason: The error message explaining why the model failed. 
        """
        logger.info ('Plugin has failed: ' + str(reason))
        
    def terminated(self):
        """
        Shutdowns the transform plugin
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
    
    def _do_transform(self, inputDirs, outputDir, properties):
        """
        Executes the transform activity
        """
        logger.debug("_do_transform started")
        try:
            logger.info("Calling do_transform method.")
            self.do_transform(inputDirs, outputDir, properties)
            self.ready()
        except Exception as ex: #pylint: disable=broad-except
            logger.exception("Error running do_transform")
            self.fail(str(ex))
        logger.debug("_do_transform complete")
    
    @abstractmethod    
    def do_transform(self, inputDirs, outputDir, properties):  # noqa: E501
        """
        Executes the transform activity
        """
        pass
