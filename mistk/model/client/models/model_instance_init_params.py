# coding: utf-8

"""
    Model Integration Software ToolKit

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: 1.0.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six


class ModelInstanceInitParams(object):
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
        'objectives': 'list[str]',
        'model_properties': 'object',
        'hyperparameters': 'object'
    }

    attribute_map = {
        'objectives': 'objectives',
        'model_properties': 'modelProperties',
        'hyperparameters': 'hyperparameters'
    }

    def __init__(self, objectives=None, model_properties=None, hyperparameters=None):  # noqa: E501
        """ModelInstanceInitParams - a model defined in Swagger"""  # noqa: E501

        self._objectives = None
        self._model_properties = None
        self._hyperparameters = None
        self.discriminator = None

        if objectives is not None:
            self.objectives = objectives
        if model_properties is not None:
            self.model_properties = model_properties
        if hyperparameters is not None:
            self.hyperparameters = hyperparameters

    @property
    def objectives(self):
        """Gets the objectives of this ModelInstanceInitParams.  # noqa: E501

        The objectives inform the model how it will be used while running   # noqa: E501

        :return: The objectives of this ModelInstanceInitParams.  # noqa: E501
        :rtype: list[str]
        """
        return self._objectives

    @objectives.setter
    def objectives(self, objectives):
        """Sets the objectives of this ModelInstanceInitParams.

        The objectives inform the model how it will be used while running   # noqa: E501

        :param objectives: The objectives of this ModelInstanceInitParams.  # noqa: E501
        :type: list[str]
        """
        allowed_values = ["training", "prediction", "streaming_prediction", "transfer_learning", "generation"]  # noqa: E501
        if not set(objectives).issubset(set(allowed_values)):
            raise ValueError(
                "Invalid values for `objectives` [{0}], must be a subset of [{1}]"  # noqa: E501
                .format(", ".join(map(str, set(objectives) - set(allowed_values))),  # noqa: E501
                        ", ".join(map(str, allowed_values)))
            )

        self._objectives = objectives

    @property
    def model_properties(self):
        """Gets the model_properties of this ModelInstanceInitParams.  # noqa: E501

        A dictionary of settings or configuration values that are passed from the ecosystem, but are not considered model hyperparameters. Model  properties are typically defined by a specific implementation of an  algorithm (ie. a PyTorch implementation of Densenet may have different  properties than a Tensorflow implementation).    # noqa: E501

        :return: The model_properties of this ModelInstanceInitParams.  # noqa: E501
        :rtype: object
        """
        return self._model_properties

    @model_properties.setter
    def model_properties(self, model_properties):
        """Sets the model_properties of this ModelInstanceInitParams.

        A dictionary of settings or configuration values that are passed from the ecosystem, but are not considered model hyperparameters. Model  properties are typically defined by a specific implementation of an  algorithm (ie. a PyTorch implementation of Densenet may have different  properties than a Tensorflow implementation).    # noqa: E501

        :param model_properties: The model_properties of this ModelInstanceInitParams.  # noqa: E501
        :type: object
        """

        self._model_properties = model_properties

    @property
    def hyperparameters(self):
        """Gets the hyperparameters of this ModelInstanceInitParams.  # noqa: E501

        A dictionary of hyperparameters that are used by the model. Hyperparameters are typically defined by the algorithm that a model is based on.    # noqa: E501

        :return: The hyperparameters of this ModelInstanceInitParams.  # noqa: E501
        :rtype: object
        """
        return self._hyperparameters

    @hyperparameters.setter
    def hyperparameters(self, hyperparameters):
        """Sets the hyperparameters of this ModelInstanceInitParams.

        A dictionary of hyperparameters that are used by the model. Hyperparameters are typically defined by the algorithm that a model is based on.    # noqa: E501

        :param hyperparameters: The hyperparameters of this ModelInstanceInitParams.  # noqa: E501
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

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, ModelInstanceInitParams):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
