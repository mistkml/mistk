# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from mistk.orchestrator.server.models.base_model_ import Model
from mistk.orchestrator.server import util


class MetricDataParameters(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, prediction_labels: str=None, truth_labels: str=None, prediction_scores: str=None, truth_bounds: str=None, prediction_bounds: str=None):  # noqa: E501
        """MetricDataParameters - a model defined in Swagger

        :param prediction_labels: The prediction_labels of this MetricDataParameters.  # noqa: E501
        :type prediction_labels: str
        :param truth_labels: The truth_labels of this MetricDataParameters.  # noqa: E501
        :type truth_labels: str
        :param prediction_scores: The prediction_scores of this MetricDataParameters.  # noqa: E501
        :type prediction_scores: str
        :param truth_bounds: The truth_bounds of this MetricDataParameters.  # noqa: E501
        :type truth_bounds: str
        :param prediction_bounds: The prediction_bounds of this MetricDataParameters.  # noqa: E501
        :type prediction_bounds: str
        """
        self.swagger_types = {
            'prediction_labels': str,
            'truth_labels': str,
            'prediction_scores': str,
            'truth_bounds': str,
            'prediction_bounds': str
        }

        self.attribute_map = {
            'prediction_labels': 'predictionLabels',
            'truth_labels': 'truthLabels',
            'prediction_scores': 'predictionScores',
            'truth_bounds': 'truthBounds',
            'prediction_bounds': 'predictionBounds'
        }

        self._prediction_labels = prediction_labels
        self._truth_labels = truth_labels
        self._prediction_scores = prediction_scores
        self._truth_bounds = truth_bounds
        self._prediction_bounds = prediction_bounds

    @classmethod
    def from_dict(cls, dikt) -> 'MetricDataParameters':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The MetricDataParameters of this MetricDataParameters.  # noqa: E501
        :rtype: MetricDataParameters
        """
        return util.deserialize_model(dikt, cls)

    @property
    def prediction_labels(self) -> str:
        """Gets the prediction_labels of this MetricDataParameters.

        The arg name for prediction labels  # noqa: E501

        :return: The prediction_labels of this MetricDataParameters.
        :rtype: str
        """
        return self._prediction_labels

    @prediction_labels.setter
    def prediction_labels(self, prediction_labels: str):
        """Sets the prediction_labels of this MetricDataParameters.

        The arg name for prediction labels  # noqa: E501

        :param prediction_labels: The prediction_labels of this MetricDataParameters.
        :type prediction_labels: str
        """

        self._prediction_labels = prediction_labels

    @property
    def truth_labels(self) -> str:
        """Gets the truth_labels of this MetricDataParameters.

        The arg name for ground truth labels  # noqa: E501

        :return: The truth_labels of this MetricDataParameters.
        :rtype: str
        """
        return self._truth_labels

    @truth_labels.setter
    def truth_labels(self, truth_labels: str):
        """Sets the truth_labels of this MetricDataParameters.

        The arg name for ground truth labels  # noqa: E501

        :param truth_labels: The truth_labels of this MetricDataParameters.
        :type truth_labels: str
        """

        self._truth_labels = truth_labels

    @property
    def prediction_scores(self) -> str:
        """Gets the prediction_scores of this MetricDataParameters.

        The arg name for prediction scores  # noqa: E501

        :return: The prediction_scores of this MetricDataParameters.
        :rtype: str
        """
        return self._prediction_scores

    @prediction_scores.setter
    def prediction_scores(self, prediction_scores: str):
        """Sets the prediction_scores of this MetricDataParameters.

        The arg name for prediction scores  # noqa: E501

        :param prediction_scores: The prediction_scores of this MetricDataParameters.
        :type prediction_scores: str
        """

        self._prediction_scores = prediction_scores

    @property
    def truth_bounds(self) -> str:
        """Gets the truth_bounds of this MetricDataParameters.

        The arg name for ground truth bounds  # noqa: E501

        :return: The truth_bounds of this MetricDataParameters.
        :rtype: str
        """
        return self._truth_bounds

    @truth_bounds.setter
    def truth_bounds(self, truth_bounds: str):
        """Sets the truth_bounds of this MetricDataParameters.

        The arg name for ground truth bounds  # noqa: E501

        :param truth_bounds: The truth_bounds of this MetricDataParameters.
        :type truth_bounds: str
        """

        self._truth_bounds = truth_bounds

    @property
    def prediction_bounds(self) -> str:
        """Gets the prediction_bounds of this MetricDataParameters.

        The arg name for prediction bounds  # noqa: E501

        :return: The prediction_bounds of this MetricDataParameters.
        :rtype: str
        """
        return self._prediction_bounds

    @prediction_bounds.setter
    def prediction_bounds(self, prediction_bounds: str):
        """Sets the prediction_bounds of this MetricDataParameters.

        The arg name for prediction bounds  # noqa: E501

        :param prediction_bounds: The prediction_bounds of this MetricDataParameters.
        :type prediction_bounds: str
        """

        self._prediction_bounds = prediction_bounds
