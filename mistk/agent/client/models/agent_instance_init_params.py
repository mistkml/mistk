# coding: utf-8

"""
    Model Integration Software ToolKit - Agent

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: 1.4.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six


class AgentInstanceInitParams(object):
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
        'model_properties': 'object',
        'hyperparameters': 'object'
    }

    attribute_map = {
        'model_properties': 'modelProperties',
        'hyperparameters': 'hyperparameters'
    }

    def __init__(self, model_properties=None, hyperparameters=None):  # noqa: E501
        """AgentInstanceInitParams - a model defined in Swagger"""  # noqa: E501

        self._model_properties = None
        self._hyperparameters = None
        self.discriminator = None

        if model_properties is not None:
            self.model_properties = model_properties
        if hyperparameters is not None:
            self.hyperparameters = hyperparameters

    @property
    def model_properties(self):
        """Gets the model_properties of this AgentInstanceInitParams.  # noqa: E501

        A dictionary of settings or configuration values that are passed from the ecosystem, but are not considered model hyperparameters. Model properties are typically defined by a specific implementation of an algorithm (ie. a PyTorch implementation of Densenet may have different properties than a Tensorflow implementation).   # noqa: E501

        :return: The model_properties of this AgentInstanceInitParams.  # noqa: E501
        :rtype: object
        """
        return self._model_properties

    @model_properties.setter
    def model_properties(self, model_properties):
        """Sets the model_properties of this AgentInstanceInitParams.

        A dictionary of settings or configuration values that are passed from the ecosystem, but are not considered model hyperparameters. Model properties are typically defined by a specific implementation of an algorithm (ie. a PyTorch implementation of Densenet may have different properties than a Tensorflow implementation).   # noqa: E501

        :param model_properties: The model_properties of this AgentInstanceInitParams.  # noqa: E501
        :type: object
        """

        self._model_properties = model_properties

    @property
    def hyperparameters(self):
        """Gets the hyperparameters of this AgentInstanceInitParams.  # noqa: E501

        A dictionary of hyperparameters that are used by the model. Hyperparameters are typically defined by the algorithm that a model is based on.   # noqa: E501

        :return: The hyperparameters of this AgentInstanceInitParams.  # noqa: E501
        :rtype: object
        """
        return self._hyperparameters

    @hyperparameters.setter
    def hyperparameters(self, hyperparameters):
        """Sets the hyperparameters of this AgentInstanceInitParams.

        A dictionary of hyperparameters that are used by the model. Hyperparameters are typically defined by the algorithm that a model is based on.   # noqa: E501

        :param hyperparameters: The hyperparameters of this AgentInstanceInitParams.  # noqa: E501
        :type: object
        """

        self._hyperparameters = hyperparameters

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
        if issubclass(AgentInstanceInitParams, dict):
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
        if not isinstance(other, AgentInstanceInitParams):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other