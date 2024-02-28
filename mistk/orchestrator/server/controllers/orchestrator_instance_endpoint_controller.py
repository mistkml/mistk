import connexion
import six

from mistk.orchestrator.server.models.model_instance_init_params import ModelInstanceInitParams  # noqa: E501
from mistk.orchestrator.server.models.orchestrator_instance_status import OrchestratorInstanceStatus  # noqa: E501
from mistk.orchestrator.server.models.service_error import ServiceError  # noqa: E501
from mistk.orchestrator.server import util


def get_status(watch=None, resourceVersion=None):  # noqa: E501
    """Get the status of the orchestrator

    Retrieves the current status of the orchestrator # noqa: E501

    :param watch: Watch for changes to the described resources and return them as a stream of add, update, and remove notifications. Specify resourceVersion. 
    :type watch: bool
    :param resourceVersion: When specified with a watch call, shows changes that occur after that particular version of a resource. Defaults to changes from the beginning of history. 
    :type resourceVersion: int

    :rtype: OrchestratorInstanceStatus
    """
    return 'do some magic!'


def initialize(initializationParameters):  # noqa: E501
    """Initialize the orchestrator

    Instructs the orchestrator instance to initialize. # noqa: E501

    :param initializationParameters: Initialization parameters for the orchestrator including the objectives, properties, and hparams. Objectives are a list of objectives for this orchestrator instance. Properties are a dictionary of properties for this orchestrator instance. Hparams are a dictionary of hyperparameters for this orchestrator instance. 
    :type initializationParameters: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        initializationParameters = ModelInstanceInitParams.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def register_agent(agentName, agentUrl):  # noqa: E501
    """Registers an agent to the orchestrator

    Connects an agent, which should have been initialized, to the orchestrator # noqa: E501

    :param agentName: The name of this agent
    :type agentName: str
    :param agentUrl: The URL to this agent
    :type agentUrl: str

    :rtype: None
    """
    return 'do some magic!'


def reset():  # noqa: E501
    """Resets the orchestrator

    Resets the orchestrator # noqa: E501


    :rtype: None
    """
    return 'do some magic!'


def start_episode(episodeCfg):  # noqa: E501
    """Starts an episode

    Instructs the container to have the orchestrator play an episode # noqa: E501

    :param episodeCfg: Configuration parameters needed to be used by that episode
    :type episodeCfg: 

    :rtype: None
    """
    return 'do some magic!'


def stop_episode():  # noqa: E501
    """Stops the episode that the orchestrator is currently playing

    Stops the episode that the orchestrator is currently playing # noqa: E501


    :rtype: None
    """
    return 'do some magic!'
