import connexion
import six

from mistk.transform.server.models.service_error import ServiceError  # noqa: E501
from mistk.transform.server.models.transform_instance_status import TransformInstanceStatus  # noqa: E501
from mistk.transform.server.models.transform_specification_init_params import TransformSpecificationInitParams  # noqa: E501
from mistk.transform.server import util


def get_api_version():  # noqa: E501
    """Returns the version of the MISTK API

    Returns the version of the MISTK API # noqa: E501


    :rtype: str
    """
    return 'do some magic!'


def get_status(watch=None, resourceVersion=None):  # noqa: E501
    """Retrieves the status of the transform plugin

     # noqa: E501

    :param watch: Watch for changes to the described resources and return them as a stream of add, update, and remove notifications. Specify resourceVersion. 
    :type watch: bool
    :param resourceVersion: When specified with a watch call, shows changes that occur after that particular version of a resource. Defaults to changes from the beginning of history. 
    :type resourceVersion: 

    :rtype: TransformInstanceStatus
    """
    return 'do some magic!'


def terminate():  # noqa: E501
    """Shutdowns the transform plugin and cleans up any resources.

     # noqa: E501


    :rtype: None
    """
    return 'do some magic!'


def transform(initParams):  # noqa: E501
    """Performs the transforms defined for this plugin

     # noqa: E501

    :param initParams: A list of directory paths where input files can be found.
    :type initParams: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        initParams = TransformSpecificationInitParams.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
