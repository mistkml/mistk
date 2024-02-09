# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from mistk.agent.server.models.base_model_ import Model
from mistk.agent.server.models.object_info import ObjectInfo  # noqa: F401,E501
from mistk.agent.server import util


class AgentInstanceStatus(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, object_info: ObjectInfo=None, state: str=None, payload: object=None):  # noqa: E501
        """AgentInstanceStatus - a model defined in Swagger

        :param object_info: The object_info of this AgentInstanceStatus.  # noqa: E501
        :type object_info: ObjectInfo
        :param state: The state of this AgentInstanceStatus.  # noqa: E501
        :type state: str
        :param payload: The payload of this AgentInstanceStatus.  # noqa: E501
        :type payload: object
        """
        self.swagger_types = {
            'object_info': ObjectInfo,
            'state': str,
            'payload': object
        }

        self.attribute_map = {
            'object_info': 'objectInfo',
            'state': 'state',
            'payload': 'payload'
        }

        self._object_info = object_info
        self._state = state
        self._payload = payload

    @classmethod
    def from_dict(cls, dikt) -> 'AgentInstanceStatus':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The AgentInstanceStatus of this AgentInstanceStatus.  # noqa: E501
        :rtype: AgentInstanceStatus
        """
        return util.deserialize_model(dikt, cls)

    @property
    def object_info(self) -> ObjectInfo:
        """Gets the object_info of this AgentInstanceStatus.


        :return: The object_info of this AgentInstanceStatus.
        :rtype: ObjectInfo
        """
        return self._object_info

    @object_info.setter
    def object_info(self, object_info: ObjectInfo):
        """Sets the object_info of this AgentInstanceStatus.


        :param object_info: The object_info of this AgentInstanceStatus.
        :type object_info: ObjectInfo
        """
        if object_info is None:
            raise ValueError("Invalid value for `object_info`, must not be `None`")  # noqa: E501

        self._object_info = object_info

    @property
    def state(self) -> str:
        """Gets the state of this AgentInstanceStatus.

        The current state of the agent instance  # noqa: E501

        :return: The state of this AgentInstanceStatus.
        :rtype: str
        """
        return self._state

    @state.setter
    def state(self, state: str):
        """Sets the state of this AgentInstanceStatus.

        The current state of the agent instance  # noqa: E501

        :param state: The state of this AgentInstanceStatus.
        :type state: str
        """
        allowed_values = ["started", "initializing", "initialized", "building_model", "saving_model_init", "saving_model_ready", "agent_registering", "ready", "episode_starting", "in_episode", "getting_action", "replaying_action", "episode_stopping", "resetting", "failed", "completed"]  # noqa: E501
        if state not in allowed_values:
            raise ValueError(
                "Invalid value for `state` ({0}), must be one of {1}"
                .format(state, allowed_values)
            )

        self._state = state

    @property
    def payload(self) -> object:
        """Gets the payload of this AgentInstanceStatus.

        Additional arbitrary information relevant to the current state.   # noqa: E501

        :return: The payload of this AgentInstanceStatus.
        :rtype: object
        """
        return self._payload

    @payload.setter
    def payload(self, payload: object):
        """Sets the payload of this AgentInstanceStatus.

        Additional arbitrary information relevant to the current state.   # noqa: E501

        :param payload: The payload of this AgentInstanceStatus.
        :type payload: object
        """

        self._payload = payload