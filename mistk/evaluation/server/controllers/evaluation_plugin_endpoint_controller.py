import connexion
import six

from mistk.evaluation.server.models.evaluation_instance_status import EvaluationInstanceStatus  # noqa: E501
from mistk.evaluation.server.models.evaluation_specification_init_params import EvaluationSpecificationInitParams  # noqa: E501
from mistk.evaluation.server.models.mistk_metric import MistkMetric  # noqa: E501
from mistk.evaluation.server.models.service_error import ServiceError  # noqa: E501
from mistk.evaluation.server import util


def evaluate(initParams):  # noqa: E501
    """Performs the evaluation defined for this plugin

     # noqa: E501

    :param initParams: A list of metrics to run and ground truth and prediction file paths to run the metrics against
    :type initParams: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        initParams = EvaluationSpecificationInitParams.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def get_api_version():  # noqa: E501
    """Returns the version of the MISTK API

    Returns the version of the MISTK API # noqa: E501


    :rtype: None
    """
    return 'do some magic!'


def get_metrics():  # noqa: E501
    """Retrieves the metrics available to perform for the evaluation plugin

     # noqa: E501


    :rtype: List[MistkMetric]
    """
    return 'do some magic!'


def get_status(watch=None, resourceVersion=None):  # noqa: E501
    """Retrieves the status of the evaluation plugin

     # noqa: E501

    :param watch: Watch for changes to the described resources and return them as a stream of add, update, and remove notifications. Specify resourceVersion. 
    :type watch: bool
    :param resourceVersion: When specified with a watch call, shows changes that occur after that particular version of a resource. Defaults to changes from the beginning of history. 
    :type resourceVersion: 

    :rtype: EvaluationInstanceStatus
    """
    return 'do some magic!'


def terminate():  # noqa: E501
    """Shutdowns the evaluation plugin and cleans up any resources.

     # noqa: E501


    :rtype: None
    """
    return 'do some magic!'
