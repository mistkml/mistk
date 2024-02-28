# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from mistk.evaluation.server.models.base_model_ import Model
from mistk.evaluation.server.models.metric_data_parameters import MetricDataParameters  # noqa: F401,E501
from mistk.evaluation.server.models.object_info import ObjectInfo  # noqa: F401,E501
from mistk.evaluation.server.models.object_reference import ObjectReference  # noqa: F401,E501
from mistk.evaluation.server import util


class Metric(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, object_info: ObjectInfo=None, implementation_reference: ObjectReference=None, package: str=None, method: str=None, default_args: object=None, data_parameters: MetricDataParameters=None, assessment_types: List[str]=None, properties: object=None, version: str=None):  # noqa: E501
        """Metric - a model defined in Swagger

        :param object_info: The object_info of this Metric.  # noqa: E501
        :type object_info: ObjectInfo
        :param implementation_reference: The implementation_reference of this Metric.  # noqa: E501
        :type implementation_reference: ObjectReference
        :param package: The package of this Metric.  # noqa: E501
        :type package: str
        :param method: The method of this Metric.  # noqa: E501
        :type method: str
        :param default_args: The default_args of this Metric.  # noqa: E501
        :type default_args: object
        :param data_parameters: The data_parameters of this Metric.  # noqa: E501
        :type data_parameters: MetricDataParameters
        :param assessment_types: The assessment_types of this Metric.  # noqa: E501
        :type assessment_types: List[str]
        :param properties: The properties of this Metric.  # noqa: E501
        :type properties: object
        :param version: The version of this Metric.  # noqa: E501
        :type version: str
        """
        self.swagger_types = {
            'object_info': ObjectInfo,
            'implementation_reference': ObjectReference,
            'package': str,
            'method': str,
            'default_args': object,
            'data_parameters': MetricDataParameters,
            'assessment_types': List[str],
            'properties': object,
            'version': str
        }

        self.attribute_map = {
            'object_info': 'objectInfo',
            'implementation_reference': 'implementationReference',
            'package': 'package',
            'method': 'method',
            'default_args': 'defaultArgs',
            'data_parameters': 'dataParameters',
            'assessment_types': 'assessmentTypes',
            'properties': 'properties',
            'version': 'version'
        }

        self._object_info = object_info
        self._implementation_reference = implementation_reference
        self._package = package
        self._method = method
        self._default_args = default_args
        self._data_parameters = data_parameters
        self._assessment_types = assessment_types
        self._properties = properties
        self._version = version

    @classmethod
    def from_dict(cls, dikt) -> 'Metric':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Metric of this Metric.  # noqa: E501
        :rtype: Metric
        """
        return util.deserialize_model(dikt, cls)

    @property
    def object_info(self) -> ObjectInfo:
        """Gets the object_info of this Metric.


        :return: The object_info of this Metric.
        :rtype: ObjectInfo
        """
        return self._object_info

    @object_info.setter
    def object_info(self, object_info: ObjectInfo):
        """Sets the object_info of this Metric.


        :param object_info: The object_info of this Metric.
        :type object_info: ObjectInfo
        """
        if object_info is None:
            raise ValueError("Invalid value for `object_info`, must not be `None`")  # noqa: E501

        self._object_info = object_info

    @property
    def implementation_reference(self) -> ObjectReference:
        """Gets the implementation_reference of this Metric.


        :return: The implementation_reference of this Metric.
        :rtype: ObjectReference
        """
        return self._implementation_reference

    @implementation_reference.setter
    def implementation_reference(self, implementation_reference: ObjectReference):
        """Sets the implementation_reference of this Metric.


        :param implementation_reference: The implementation_reference of this Metric.
        :type implementation_reference: ObjectReference
        """

        self._implementation_reference = implementation_reference

    @property
    def package(self) -> str:
        """Gets the package of this Metric.

        The name of the package containing the implementation of this metric.   # noqa: E501

        :return: The package of this Metric.
        :rtype: str
        """
        return self._package

    @package.setter
    def package(self, package: str):
        """Sets the package of this Metric.

        The name of the package containing the implementation of this metric.   # noqa: E501

        :param package: The package of this Metric.
        :type package: str
        """

        self._package = package

    @property
    def method(self) -> str:
        """Gets the method of this Metric.

        The name of the method to be called when applying the metric.   # noqa: E501

        :return: The method of this Metric.
        :rtype: str
        """
        return self._method

    @method.setter
    def method(self, method: str):
        """Sets the method of this Metric.

        The name of the method to be called when applying the metric.   # noqa: E501

        :param method: The method of this Metric.
        :type method: str
        """

        self._method = method

    @property
    def default_args(self) -> object:
        """Gets the default_args of this Metric.

        The default arguments passed to the method when the metric is called.  These can be overwritten when the metric is associated with an assessment.   # noqa: E501

        :return: The default_args of this Metric.
        :rtype: object
        """
        return self._default_args

    @default_args.setter
    def default_args(self, default_args: object):
        """Sets the default_args of this Metric.

        The default arguments passed to the method when the metric is called.  These can be overwritten when the metric is associated with an assessment.   # noqa: E501

        :param default_args: The default_args of this Metric.
        :type default_args: object
        """

        self._default_args = default_args

    @property
    def data_parameters(self) -> MetricDataParameters:
        """Gets the data_parameters of this Metric.


        :return: The data_parameters of this Metric.
        :rtype: MetricDataParameters
        """
        return self._data_parameters

    @data_parameters.setter
    def data_parameters(self, data_parameters: MetricDataParameters):
        """Sets the data_parameters of this Metric.


        :param data_parameters: The data_parameters of this Metric.
        :type data_parameters: MetricDataParameters
        """

        self._data_parameters = data_parameters

    @property
    def assessment_types(self) -> List[str]:
        """Gets the assessment_types of this Metric.

        The types of assessments this metric can be used for.   # noqa: E501

        :return: The assessment_types of this Metric.
        :rtype: List[str]
        """
        return self._assessment_types

    @assessment_types.setter
    def assessment_types(self, assessment_types: List[str]):
        """Sets the assessment_types of this Metric.

        The types of assessments this metric can be used for.   # noqa: E501

        :param assessment_types: The assessment_types of this Metric.
        :type assessment_types: List[str]
        """

        self._assessment_types = assessment_types

    @property
    def properties(self) -> object:
        """Gets the properties of this Metric.

        The optional properties which set values for the ParameterSpecs associated with this metric's implementation that will be sent to  the instantiated evaluation metric.   # noqa: E501

        :return: The properties of this Metric.
        :rtype: object
        """
        return self._properties

    @properties.setter
    def properties(self, properties: object):
        """Sets the properties of this Metric.

        The optional properties which set values for the ParameterSpecs associated with this metric's implementation that will be sent to  the instantiated evaluation metric.   # noqa: E501

        :param properties: The properties of this Metric.
        :type properties: object
        """

        self._properties = properties

    @property
    def version(self) -> str:
        """Gets the version of this Metric.

        The version of this metric  # noqa: E501

        :return: The version of this Metric.
        :rtype: str
        """
        return self._version

    @version.setter
    def version(self, version: str):
        """Sets the version of this Metric.

        The version of this metric  # noqa: E501

        :param version: The version of this Metric.
        :type version: str
        """

        self._version = version
