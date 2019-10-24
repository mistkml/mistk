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


class WatchEvent(object):
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
        'payload': 'object',
        'event_type': 'str'
    }

    attribute_map = {
        'payload': 'payload',
        'event_type': 'eventType'
    }

    def __init__(self, payload=None, event_type=None):  # noqa: E501
        """WatchEvent - a model defined in Swagger"""  # noqa: E501

        self._payload = None
        self._event_type = None
        self.discriminator = None

        self.payload = payload
        self.event_type = event_type

    @property
    def payload(self):
        """Gets the payload of this WatchEvent.  # noqa: E501

        The object/resource which was changed. If the type of the event was *added* or *modified*, then this field is the new state of the resource.  If the field is *deleted* then the value is the state just before deletion.   # noqa: E501

        :return: The payload of this WatchEvent.  # noqa: E501
        :rtype: object
        """
        return self._payload

    @payload.setter
    def payload(self, payload):
        """Sets the payload of this WatchEvent.

        The object/resource which was changed. If the type of the event was *added* or *modified*, then this field is the new state of the resource.  If the field is *deleted* then the value is the state just before deletion.   # noqa: E501

        :param payload: The payload of this WatchEvent.  # noqa: E501
        :type: object
        """
        if payload is None:
            raise ValueError("Invalid value for `payload`, must not be `None`")  # noqa: E501

        self._payload = payload

    @property
    def event_type(self):
        """Gets the event_type of this WatchEvent.  # noqa: E501


        :return: The event_type of this WatchEvent.  # noqa: E501
        :rtype: str
        """
        return self._event_type

    @event_type.setter
    def event_type(self, event_type):
        """Sets the event_type of this WatchEvent.


        :param event_type: The event_type of this WatchEvent.  # noqa: E501
        :type: str
        """
        if event_type is None:
            raise ValueError("Invalid value for `event_type`, must not be `None`")  # noqa: E501
        allowed_values = ["added", "modified", "deleted"]  # noqa: E501
        if event_type not in allowed_values:
            raise ValueError(
                "Invalid value for `event_type` ({0}), must be one of {1}"  # noqa: E501
                .format(event_type, allowed_values)
            )

        self._event_type = event_type

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
        if not isinstance(other, WatchEvent):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
