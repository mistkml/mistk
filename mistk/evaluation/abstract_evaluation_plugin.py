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

from mistk.evaluation.service import EvaluationPluginEndpoint
import mistk.evaluation
from mistk import logger

# The model states
_evaluation_states = {'started', 'ready', 'failed', 
                  'evaluating','terminating', 'terminated'}


class AbstractEvaluationPlugin (metaclass=ABCMeta):
    """
    classdocs
    """
    
    @abstractmethod
    def __init__(self):
        """
        Initializes the Metrics and registers the default state machine transitions 
        available to all clients.
        """
        
        self.state = None
        self._endpoint_service = None
        states = [State(n, on_enter='new_state_entered') for n in _evaluation_states]
        self._machine = Machine(model=self, states=states, initial='started', auto_transitions=False)
        self._machine.add_transition(trigger='fail', source=list(_evaluation_states-{'terminated'}), dest='failed')
        self._machine.add_transition(trigger='ready', source=['started', 'evaluating'], dest='ready')
        self._machine.add_transition(trigger='evaluate', source=['started', 'ready'], dest='evaluating', after='_do_evaluate')
        self._machine.add_transition(trigger='terminate', source=list(_evaluation_states-{'terminating', 'terminated', 'failed'}), dest='terminating', after='_do_terminate')
        self._machine.add_transition(trigger='terminated', source='terminating', dest='terminated')
    
    def update_status(self, payload):
        """
        Provides additional details to the current state of the evaluation. 
        
        :param payload: Extra information regarding the status update
        """
        self.endpoint_service.update_state(state=None, payload=payload)
                
    @property
    def endpoint_service(self) -> EvaluationPluginEndpoint:
        """
        Returns the endpoint service for this Evaluation
        """
        return self._endpoint_service
        
    @endpoint_service.setter
    def endpoint_service(self, endpoint_service: EvaluationPluginEndpoint):
        """
        Sets the endpoint service to the provided EvaluationPluginService
        
        :param endpoint_service: The new EvaluationPluginService         
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

    def evaluate(self, assessment_type, metrics, input_data_path, evaluation_input_format, ground_truth_path, evaluation_path, properties):
        """
        Triggers the model to enter the evaluation state.  A subsequent call to
        do_evaluate with the given parameters will be made as a result.

        This method should not be implemented or overwritten by subclasses.  It will be 
        created by the state machine.
        """
        pass
    
    def metrics(self):
        """
        Metrics that can be performed by the evaluate method
        """
        logger.debug("metrics started")
        try:
            metrics_list = self.plugin_manager.get_metrics_list()
            logger.debug("metrics complete")
        except Exception as ex:
            logger.exception("Error running metrics")
            self.fail(str(ex))
            
        return metrics_list
        
    def assessment_types(self):
        """
        Assessment types that are supported by the evaluate method
        """
        types = []
        try:
            metrics_list = self.plugin_manager.get_metrics_list()
            for metric in metrics_list:
                for assessment_types in metric.assessment_types():
                    if type not in assessment_types:
                        types.append(type)
        except Exception as ex:
            logger.exception("Error running metrics")
            self.fail(str(ex))
            
        return types  
    
    def report_failure(self, reason):
        """
        Reports the failure of a model during its operations
        
        :param reason: The error message explaining why the model failed. 
        """
        logger.info ('Plugin has failed: ' + str(reason))
        
    def terminated(self):
        """
        Shutdowns the evaluation plugin
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
    
    def _do_evaluate(self, assessment_type, metrics, input_data_path, evaluation_input_format, ground_truth_path, evaluation_path, properties):
        """
    Performs metrics' evaluation using the predictions and ground truth files provided.
    Stored the assessment results as a JSON file in the evaluation_path
    
    :param assessment_type: The evaluation type. One of {'BinaryClassification', 
        'MultilabelClassification', 'MulticlassClassification', 'Regression'}
    :param metrics: Specific metrics to evaluate against instead of all metrics defined by assessment_type
    :param input_data_path: Path to input data for the evaluation
    :param evaluation_input_format: The format of the input data
    :param ground_truth_path: The directory path where the ground_truth.csv file is located
    :param evaluation_path: A directory path to where the evaluation.json output file will be stored
    :param properties: A dictionary of key value pairs for evaluation plugin arguments. 
    """
    
        logger.debug("_do_evaluation started")
        try:
            logger.info("Calling do_evaluation method.")
            self.do_evaluate(assessment_type, metrics, input_data_path, evaluation_input_format, ground_truth_path, evaluation_path, properties)
            self.ready()
        except Exception as ex: #pylint: disable=broad-except
            logger.exception("Error running do_evaluation")
            self.fail(str(ex))
        logger.debug("_do_evaluation complete")
    
    @abstractmethod    
    def do_evaluate(self, assessment_type, metrics, input_data_format, evaluation_input_format, ground_truth_path, evaluation_path, properties):  # noqa: E501
        """
    Performs metrics' evaluation using the predictions and ground truth files provided.
    Stored the assessment results as a JSON file in the evaluation_path
    
    :param assessment_type: The evaluation type. One of {'BinaryClassification', 
        'MultilabelClassification', 'MulticlassClassification', 'Regression'}
    :param metrics: Specific metrics to evaluate against instead of all metrics defined by assessment_type
    :param input_data_path: Path to input data for the evaluation
    :param evaluation_input_format: The format of the input data
    :param ground_truth_path: The directory path where the ground_truth.csv file is located
    :param evaluation_path: A directory path to where the evaluation.json output file will be stored
    :param properties: A dictionary of key value pairs for evaluation plugin arguments. 
    """
        pass
    
    
