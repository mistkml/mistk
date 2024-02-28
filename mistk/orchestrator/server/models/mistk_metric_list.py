# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from mistk.orchestrator.server.models.base_model_ import Model
from mistk.orchestrator.server.models.mistk_metric import MistkMetric  # noqa: F401,E501
from mistk.orchestrator.server import util


class MistkMetricList(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, items: List[MistkMetric]=None, continue_token: str=None):  # noqa: E501
        """MistkMetricList - a model defined in Swagger

        :param items: The items of this MistkMetricList.  # noqa: E501
        :type items: List[MistkMetric]
        :param continue_token: The continue_token of this MistkMetricList.  # noqa: E501
        :type continue_token: str
        """
        self.swagger_types = {
            'items': List[MistkMetric],
            'continue_token': str
        }

        self.attribute_map = {
            'items': 'items',
            'continue_token': 'continueToken'
        }

        self._items = items
        self._continue_token = continue_token

    @classmethod
    def from_dict(cls, dikt) -> 'MistkMetricList':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The MistkMetricList of this MistkMetricList.  # noqa: E501
        :rtype: MistkMetricList
        """
        return util.deserialize_model(dikt, cls)

    @property
    def items(self) -> List[MistkMetric]:
        """Gets the items of this MistkMetricList.


        :return: The items of this MistkMetricList.
        :rtype: List[MistkMetric]
        """
        return self._items

    @items.setter
    def items(self, items: List[MistkMetric]):
        """Sets the items of this MistkMetricList.


        :param items: The items of this MistkMetricList.
        :type items: List[MistkMetric]
        """

        self._items = items

    @property
    def continue_token(self) -> str:
        """Gets the continue_token of this MistkMetricList.


        :return: The continue_token of this MistkMetricList.
        :rtype: str
        """
        return self._continue_token

    @continue_token.setter
    def continue_token(self, continue_token: str):
        """Sets the continue_token of this MistkMetricList.


        :param continue_token: The continue_token of this MistkMetricList.
        :type continue_token: str
        """

        self._continue_token = continue_token
