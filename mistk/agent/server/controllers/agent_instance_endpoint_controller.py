import connexion
import six

from mistk.agent.server.models.agent_instance_init_params import AgentInstanceInitParams  # noqa: E501
from mistk.agent.server.models.agent_instance_status import AgentInstanceStatus  # noqa: E501
from mistk.agent.server.models.service_error import ServiceError  # noqa: E501
from mistk.agent.server import util


def agent_registered(agentCfg=None):  # noqa: E501
    """Agent registered

    Agent has been registered to a orchestrator # noqa: E501

    :param agentCfg: A dictionary for the agent configuration from the orchestrator 
    :type agentCfg: 

    :rtype: None
    """
    return 'do some magic!'


def build_model(modelPath=None):  # noqa: E501
    """Build the model

    Instructs the container to construct the model # noqa: E501

    :param modelPath: A path pointing to the directory where the model can be loaded from. 
    :type modelPath: str

    :rtype: None
    """
    return 'do some magic!'


def episode_started(episodeCfg=None):  # noqa: E501
    """Episode started

    Instructs the agent that the episode has started # noqa: E501

    :param episodeCfg: A dict for the episode config from the orchestrator. One key must be &#x60;obs&#x60;. 
    :type episodeCfg: 

    :rtype: None
    """
    return 'do some magic!'


def episode_stopped():  # noqa: E501
    """Episode stopped

    Instructs the agent that the episode has stopped # noqa: E501


    :rtype: None
    """
    return 'do some magic!'


def get_action(obs):  # noqa: E501
    """Get action(s) from agent

    Gives the agent the observations to perform some action(s) # noqa: E501

    :param obs: A dict for each agent&#39;s environmental observations it has observed 
    :type obs: 

    :rtype: object
    """
    return 'do some magic!'


def get_api_version():  # noqa: E501
    """Returns the version of the MISTK API

    Returns the version of the MISTK API # noqa: E501


    :rtype: str
    """
    return 'do some magic!'


def get_status(watch=None, resourceVersion=None):  # noqa: E501
    """Get the status of the model

    Retrieves the current status of the model # noqa: E501

    :param watch: Watch for changes to the described resources and return them as a stream of add, update, and remove notifications. Specify resourceVersion. 
    :type watch: bool
    :param resourceVersion: When specified with a watch call, shows changes that occur after that particular version of a resource. Defaults to changes from the beginning of history. 
    :type resourceVersion: int

    :rtype: AgentInstanceStatus
    """
    return 'do some magic!'


def initialize_agent(initializationParameters):  # noqa: E501
    """Initialize the model

    Instructs the model instance to initialize. # noqa: E501

    :param initializationParameters: Initialization parameters for the agent including properties, and hparams. Properties are a dictionary of properties for this agent instance. Hparams are a dictionary of hyperparameters for this agent instance. 
    :type initializationParameters: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        initializationParameters = AgentInstanceInitParams.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def replay_action(obs):  # noqa: E501
    """Replay an action from agent

    Gives the agent the observations to replay an action for learning # noqa: E501

    :param obs: A dictionary with the keys for prev_obs, rewards, actions, &amp; new_obs 
    :type obs: 

    :rtype: None
    """
    return 'do some magic!'


def reset(unloadModel):  # noqa: E501
    """Resets the model

    Resets the model # noqa: E501

    :param unloadModel: Unload (reset) the built model or keep the current built model 
    :type unloadModel: bool

    :rtype: None
    """
    return 'do some magic!'


def save_model(modelPath):  # noqa: E501
    """Save the model snapshot

    Instructs the container to serialize the model to the specified path  # noqa: E501

    :param modelPath: A path pointing to the directory where the model is to be saved. 
    :type modelPath: str

    :rtype: None
    """
    return 'do some magic!'


def terminate():  # noqa: E501
    """Shut down the agent

    Shuts down the agent # noqa: E501


    :rtype: None
    """
    return 'do some magic!'
