# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from mistk.evaluation.server.models.base_model_ import Model
from mistk.evaluation.server.models.mistk_metric import MistkMetric  # noqa: F401,E501
from mistk.evaluation.server import util


class EvaluationSpecificationInitParams(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, assessment_type: str=None, metrics: List[MistkMetric]=None, input_data_path: str=None, evaluation_input_format: str=None, ground_truth_path: str=None, evaluation_path: str=None, properties: object=None):  # noqa: E501
        """EvaluationSpecificationInitParams - a model defined in Swagger

        :param assessment_type: The assessment_type of this EvaluationSpecificationInitParams.  # noqa: E501
        :type assessment_type: str
        :param metrics: The metrics of this EvaluationSpecificationInitParams.  # noqa: E501
        :type metrics: List[MistkMetric]
        :param input_data_path: The input_data_path of this EvaluationSpecificationInitParams.  # noqa: E501
        :type input_data_path: str
        :param evaluation_input_format: The evaluation_input_format of this EvaluationSpecificationInitParams.  # noqa: E501
        :type evaluation_input_format: str
        :param ground_truth_path: The ground_truth_path of this EvaluationSpecificationInitParams.  # noqa: E501
        :type ground_truth_path: str
        :param evaluation_path: The evaluation_path of this EvaluationSpecificationInitParams.  # noqa: E501
        :type evaluation_path: str
        :param properties: The properties of this EvaluationSpecificationInitParams.  # noqa: E501
        :type properties: object
        """
        self.swagger_types = {
            'assessment_type': str,
            'metrics': List[MistkMetric],
            'input_data_path': str,
            'evaluation_input_format': str,
            'ground_truth_path': str,
            'evaluation_path': str,
            'properties': object
        }

        self.attribute_map = {
            'assessment_type': 'assessment_type',
            'metrics': 'metrics',
            'input_data_path': 'input_data_path',
            'evaluation_input_format': 'evaluation_input_format',
            'ground_truth_path': 'ground_truth_path',
            'evaluation_path': 'evaluation_path',
            'properties': 'properties'
        }

        self._assessment_type = assessment_type
        self._metrics = metrics
        self._input_data_path = input_data_path
        self._evaluation_input_format = evaluation_input_format
        self._ground_truth_path = ground_truth_path
        self._evaluation_path = evaluation_path
        self._properties = properties

    @classmethod
    def from_dict(cls, dikt) -> 'EvaluationSpecificationInitParams':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The EvaluationSpecificationInitParams of this EvaluationSpecificationInitParams.  # noqa: E501
        :rtype: EvaluationSpecificationInitParams
        """
        return util.deserialize_model(dikt, cls)

    @property
    def assessment_type(self) -> str:
        """Gets the assessment_type of this EvaluationSpecificationInitParams.

        Assessment type to use for the evaluation  # noqa: E501

        :return: The assessment_type of this EvaluationSpecificationInitParams.
        :rtype: str
        """
        return self._assessment_type

    @assessment_type.setter
    def assessment_type(self, assessment_type: str):
        """Sets the assessment_type of this EvaluationSpecificationInitParams.

        Assessment type to use for the evaluation  # noqa: E501

        :param assessment_type: The assessment_type of this EvaluationSpecificationInitParams.
        :type assessment_type: str
        """
        if assessment_type is None:
            raise ValueError("Invalid value for `assessment_type`, must not be `None`")  # noqa: E501

        self._assessment_type = assessment_type

    @property
    def metrics(self) -> List[MistkMetric]:
        """Gets the metrics of this EvaluationSpecificationInitParams.

        A list of metrics to use for the evaluation  # noqa: E501

        :return: The metrics of this EvaluationSpecificationInitParams.
        :rtype: List[MistkMetric]
        """
        return self._metrics

    @metrics.setter
    def metrics(self, metrics: List[MistkMetric]):
        """Sets the metrics of this EvaluationSpecificationInitParams.

        A list of metrics to use for the evaluation  # noqa: E501

        :param metrics: The metrics of this EvaluationSpecificationInitParams.
        :type metrics: List[MistkMetric]
        """
        if metrics is None:
            raise ValueError("Invalid value for `metrics`, must not be `None`")  # noqa: E501

        self._metrics = metrics

    @property
    def input_data_path(self) -> str:
        """Gets the input_data_path of this EvaluationSpecificationInitParams.

        Path to input data for the evaluation  # noqa: E501

        :return: The input_data_path of this EvaluationSpecificationInitParams.
        :rtype: str
        """
        return self._input_data_path

    @input_data_path.setter
    def input_data_path(self, input_data_path: str):
        """Sets the input_data_path of this EvaluationSpecificationInitParams.

        Path to input data for the evaluation  # noqa: E501

        :param input_data_path: The input_data_path of this EvaluationSpecificationInitParams.
        :type input_data_path: str
        """
        if input_data_path is None:
            raise ValueError("Invalid value for `input_data_path`, must not be `None`")  # noqa: E501

        self._input_data_path = input_data_path

    @property
    def evaluation_input_format(self) -> str:
        """Gets the evaluation_input_format of this EvaluationSpecificationInitParams.

        The format of the input data  # noqa: E501

        :return: The evaluation_input_format of this EvaluationSpecificationInitParams.
        :rtype: str
        """
        return self._evaluation_input_format

    @evaluation_input_format.setter
    def evaluation_input_format(self, evaluation_input_format: str):
        """Sets the evaluation_input_format of this EvaluationSpecificationInitParams.

        The format of the input data  # noqa: E501

        :param evaluation_input_format: The evaluation_input_format of this EvaluationSpecificationInitParams.
        :type evaluation_input_format: str
        """
        allowed_values = ["predictions", "generations"]  # noqa: E501
        if evaluation_input_format not in allowed_values:
            raise ValueError(
                "Invalid value for `evaluation_input_format` ({0}), must be one of {1}"
                .format(evaluation_input_format, allowed_values)
            )

        self._evaluation_input_format = evaluation_input_format

    @property
    def ground_truth_path(self) -> str:
        """Gets the ground_truth_path of this EvaluationSpecificationInitParams.

        Path to ground_truth.csv file  # noqa: E501

        :return: The ground_truth_path of this EvaluationSpecificationInitParams.
        :rtype: str
        """
        return self._ground_truth_path

    @ground_truth_path.setter
    def ground_truth_path(self, ground_truth_path: str):
        """Sets the ground_truth_path of this EvaluationSpecificationInitParams.

        Path to ground_truth.csv file  # noqa: E501

        :param ground_truth_path: The ground_truth_path of this EvaluationSpecificationInitParams.
        :type ground_truth_path: str
        """
        if ground_truth_path is None:
            raise ValueError("Invalid value for `ground_truth_path`, must not be `None`")  # noqa: E501

        self._ground_truth_path = ground_truth_path

    @property
    def evaluation_path(self) -> str:
        """Gets the evaluation_path of this EvaluationSpecificationInitParams.

        Path for evaluation output file  # noqa: E501

        :return: The evaluation_path of this EvaluationSpecificationInitParams.
        :rtype: str
        """
        return self._evaluation_path

    @evaluation_path.setter
    def evaluation_path(self, evaluation_path: str):
        """Sets the evaluation_path of this EvaluationSpecificationInitParams.

        Path for evaluation output file  # noqa: E501

        :param evaluation_path: The evaluation_path of this EvaluationSpecificationInitParams.
        :type evaluation_path: str
        """

        self._evaluation_path = evaluation_path

    @property
    def properties(self) -> object:
        """Gets the properties of this EvaluationSpecificationInitParams.

        A dictionary of key value pairs for evaluation plugin arguments.  # noqa: E501

        :return: The properties of this EvaluationSpecificationInitParams.
        :rtype: object
        """
        return self._properties

    @properties.setter
    def properties(self, properties: object):
        """Sets the properties of this EvaluationSpecificationInitParams.

        A dictionary of key value pairs for evaluation plugin arguments.  # noqa: E501

        :param properties: The properties of this EvaluationSpecificationInitParams.
        :type properties: object
        """

        self._properties = properties
