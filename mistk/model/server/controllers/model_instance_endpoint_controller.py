import connexion
import six

from mistk.model.server.models.model_instance_init_params import ModelInstanceInitParams  # noqa: E501
from mistk.model.server.models.model_instance_status import ModelInstanceStatus  # noqa: E501
from mistk.model.server.models.service_error import ServiceError  # noqa: E501
from mistk.model.server import util


def build_model(modelPath=None):  # noqa: E501
    """Build the model

    Instructs the container to construct the model # noqa: E501

    :param modelPath: The absolute path to the directory where the model&#39;s checkpoint/snapshot file can be found.  
    :type modelPath: str

    :rtype: None
    """
    return 'do some magic!'


def get_status(watch=None, resourceVersion=None):  # noqa: E501
    """Get the status of the model

    Retrieves the current status of the model # noqa: E501

    :param watch: Watch for changes to the described resources and return them as a stream of add, update, and remove notifications. Specify resourceVersion. 
    :type watch: bool
    :param resourceVersion: When specified with a watch call, shows changes that occur after that particular version of a resource. Defaults to changes from the beginning of history. 
    :type resourceVersion: int

    :rtype: ModelInstanceStatus
    """
    return 'do some magic!'


def initialize_model(initializationParameters):  # noqa: E501
    """Initialize the model

    Instructs the model instance to initialize. # noqa: E501

    :param initializationParameters: Initialization parameters for the model including the objectives, properties, and hparams. Objectives are a list of objectives for this model instance from the following options { train, predict}. Properties are a dictionary of properties for this model instance.  Hparams are a dictionary of hyperparameters for this model instance. 
    :type initializationParameters: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        initializationParameters = ModelInstanceInitParams.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def load_data(datasets):  # noqa: E501
    """Loads data for the model

    Loads data onto a staging area for use by the model # noqa: E501

    :param datasets: A dictionary mapping objectives to MistkDataset objects.  Dictionary keys must be one of the following {train, test} 
    :type datasets: 

    :rtype: None
    """
    return 'do some magic!'


def pause():  # noqa: E501
    """Pause the model

    Instructs the container to pause the current training or  prediction activity  # noqa: E501


    :rtype: None
    """
    return 'do some magic!'


def predict():  # noqa: E501
    """Perform predictions with the model

    Perform predictions with the test dataset previously loaded # noqa: E501


    :rtype: None
    """
    return 'do some magic!'


def reset():  # noqa: E501
    """Resets the model

    Resets the model # noqa: E501


    :rtype: None
    """
    return 'do some magic!'


def resume_predict():  # noqa: E501
    """Resume predicitons on a paused model

    Resumes the training activity  # noqa: E501


    :rtype: None
    """
    return 'do some magic!'


def resume_training():  # noqa: E501
    """Resume training on a paused model

    Resumes the training activity  # noqa: E501


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


def save_predictions(dataPath):  # noqa: E501
    """Save the model&#39;s predictions

    Instructs the container to save the predictions to the specified path  # noqa: E501

    :param dataPath: A path pointing to the directory where the predictions are to be saved. 
    :type dataPath: str

    :rtype: None
    """
    return 'do some magic!'


def stream_predict(dataMap):  # noqa: E501
    """Perform streaming predictions with the model

    Perform predictions with the test dataset previously loaded # noqa: E501

    :param dataMap: Dictionary of IDs to b64 encoded data
    :type dataMap: 

    :rtype: object
    """
    return 'do some magic!'


def terminate():  # noqa: E501
    """Shut down the model

    Shuts down the model # noqa: E501


    :rtype: None
    """
    return 'do some magic!'


def train():  # noqa: E501
    """Train the model

    Trains the model with the training dataset previously loaded # noqa: E501


    :rtype: None
    """
    return 'do some magic!'
