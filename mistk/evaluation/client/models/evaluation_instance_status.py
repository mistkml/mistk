# coding: utf-8

"""
    Model Integration Software ToolKit - Metric Evaluation

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: 1.4.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from mistk.evaluation.client.models.object_info import ObjectInfo  # noqa: F401,E501


class EvaluationInstanceStatus(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'object_info': 'ObjectInfo',
        'state': 'str',
        'payload': 'object'
    }

    attribute_map = {
        'object_info': 'objectInfo',
        'state': 'state',
        'payload': 'payload'
    }

    def __init__(self, object_info=None, state=None, payload=None):  # noqa: E501
        """EvaluationInstanceStatus - a model defined in Swagger"""  # noqa: E501

        self._object_info = None
        self._state = None
        self._payload = None
        self.discriminator = None

        self.object_info = object_info
        if state is not None:
            self.state = state
        if payload is not None:
            self.payload = payload

    @property
    def object_info(self):
        """Gets the object_info of this EvaluationInstanceStatus.  # noqa: E501


        :return: The object_info of this EvaluationInstanceStatus.  # noqa: E501
        :rtype: ObjectInfo
        """
        return self._object_info

    @object_info.setter
    def object_info(self, object_info):
        """Sets the object_info of this EvaluationInstanceStatus.


        :param object_info: The object_info of this EvaluationInstanceStatus.  # noqa: E501
        :type: ObjectInfo
        """
        if object_info is None:
            raise ValueError("Invalid value for `object_info`, must not be `None`")  # noqa: E501

        self._object_info = object_info

    @property
    def state(self):
        """Gets the state of this EvaluationInstanceStatus.  # noqa: E501

        The current state of the evaluation instance  # noqa: E501

        :return: The state of this EvaluationInstanceStatus.  # noqa: E501
        :rtype: str
        """
        return self._state

    @state.setter
    def state(self, state):
        """Sets the state of this EvaluationInstanceStatus.

        The current state of the evaluation instance  # noqa: E501

        :param state: The state of this EvaluationInstanceStatus.  # noqa: E501
        :type: str
        """
        allowed_values = ["started", "initializing", "initialized", "failed", "ready", "evaluating", "completed"]  # noqa: E501
        if state not in allowed_values:
            raise ValueError(
                "Invalid value for `state` ({0}), must be one of {1}"  # noqa: E501
                .format(state, allowed_values)
            )

        self._state = state

    @property
    def payload(self):
        """Gets the payload of this EvaluationInstanceStatus.  # noqa: E501

        Additional arbitrary information relevant to the current state.   # noqa: E501

        :return: The payload of this EvaluationInstanceStatus.  # noqa: E501
        :rtype: object
        """
        return self._payload

    @payload.setter
    def payload(self, payload):
        """Sets the payload of this EvaluationInstanceStatus.

        Additional arbitrary information relevant to the current state.   # noqa: E501

        :param payload: The payload of this EvaluationInstanceStatus.  # noqa: E501
        :type: object
        """

        self._payload = payload

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value
        if issubclass(EvaluationInstanceStatus, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, EvaluationInstanceStatus):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other