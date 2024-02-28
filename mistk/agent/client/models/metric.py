# coding: utf-8

"""
    Model Integration Software ToolKit - Agent

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: 1.3.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from mistk.agent.client.models.metric_data_parameters import MetricDataParameters  # noqa: F401,E501
from mistk.agent.client.models.object_info import ObjectInfo  # noqa: F401,E501
from mistk.agent.client.models.object_reference import ObjectReference  # noqa: F401,E501


class Metric(object):
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
        'implementation_reference': 'ObjectReference',
        'package': 'str',
        'method': 'str',
        'default_args': 'object',
        'data_parameters': 'MetricDataParameters',
        'assessment_types': 'list[str]',
        'properties': 'object',
        'version': 'str'
    }

    attribute_map = {
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

    def __init__(self, object_info=None, implementation_reference=None, package=None, method=None, default_args=None, data_parameters=None, assessment_types=None, properties=None, version=None):  # noqa: E501
        """Metric - a model defined in Swagger"""  # noqa: E501

        self._object_info = None
        self._implementation_reference = None
        self._package = None
        self._method = None
        self._default_args = None
        self._data_parameters = None
        self._assessment_types = None
        self._properties = None
        self._version = None
        self.discriminator = None

        self.object_info = object_info
        if implementation_reference is not None:
            self.implementation_reference = implementation_reference
        if package is not None:
            self.package = package
        if method is not None:
            self.method = method
        if default_args is not None:
            self.default_args = default_args
        if data_parameters is not None:
            self.data_parameters = data_parameters
        if assessment_types is not None:
            self.assessment_types = assessment_types
        if properties is not None:
            self.properties = properties
        if version is not None:
            self.version = version

    @property
    def object_info(self):
        """Gets the object_info of this Metric.  # noqa: E501


        :return: The object_info of this Metric.  # noqa: E501
        :rtype: ObjectInfo
        """
        return self._object_info

    @object_info.setter
    def object_info(self, object_info):
        """Sets the object_info of this Metric.


        :param object_info: The object_info of this Metric.  # noqa: E501
        :type: ObjectInfo
        """
        if object_info is None:
            raise ValueError("Invalid value for `object_info`, must not be `None`")  # noqa: E501

        self._object_info = object_info

    @property
    def implementation_reference(self):
        """Gets the implementation_reference of this Metric.  # noqa: E501


        :return: The implementation_reference of this Metric.  # noqa: E501
        :rtype: ObjectReference
        """
        return self._implementation_reference

    @implementation_reference.setter
    def implementation_reference(self, implementation_reference):
        """Sets the implementation_reference of this Metric.


        :param implementation_reference: The implementation_reference of this Metric.  # noqa: E501
        :type: ObjectReference
        """

        self._implementation_reference = implementation_reference

    @property
    def package(self):
        """Gets the package of this Metric.  # noqa: E501

        The name of the package containing the implementation of this metric.   # noqa: E501

        :return: The package of this Metric.  # noqa: E501
        :rtype: str
        """
        return self._package

    @package.setter
    def package(self, package):
        """Sets the package of this Metric.

        The name of the package containing the implementation of this metric.   # noqa: E501

        :param package: The package of this Metric.  # noqa: E501
        :type: str
        """

        self._package = package

    @property
    def method(self):
        """Gets the method of this Metric.  # noqa: E501

        The name of the method to be called when applying the metric.   # noqa: E501

        :return: The method of this Metric.  # noqa: E501
        :rtype: str
        """
        return self._method

    @method.setter
    def method(self, method):
        """Sets the method of this Metric.

        The name of the method to be called when applying the metric.   # noqa: E501

        :param method: The method of this Metric.  # noqa: E501
        :type: str
        """

        self._method = method

    @property
    def default_args(self):
        """Gets the default_args of this Metric.  # noqa: E501

        The default arguments passed to the method when the metric is called.  These can be overwritten when the metric is associated with an assessment.   # noqa: E501

        :return: The default_args of this Metric.  # noqa: E501
        :rtype: object
        """
        return self._default_args

    @default_args.setter
    def default_args(self, default_args):
        """Sets the default_args of this Metric.

        The default arguments passed to the method when the metric is called.  These can be overwritten when the metric is associated with an assessment.   # noqa: E501

        :param default_args: The default_args of this Metric.  # noqa: E501
        :type: object
        """

        self._default_args = default_args

    @property
    def data_parameters(self):
        """Gets the data_parameters of this Metric.  # noqa: E501


        :return: The data_parameters of this Metric.  # noqa: E501
        :rtype: MetricDataParameters
        """
        return self._data_parameters

    @data_parameters.setter
    def data_parameters(self, data_parameters):
        """Sets the data_parameters of this Metric.


        :param data_parameters: The data_parameters of this Metric.  # noqa: E501
        :type: MetricDataParameters
        """

        self._data_parameters = data_parameters

    @property
    def assessment_types(self):
        """Gets the assessment_types of this Metric.  # noqa: E501

        The types of assessments this metric can be used for.   # noqa: E501

        :return: The assessment_types of this Metric.  # noqa: E501
        :rtype: list[str]
        """
        return self._assessment_types

    @assessment_types.setter
    def assessment_types(self, assessment_types):
        """Sets the assessment_types of this Metric.

        The types of assessments this metric can be used for.   # noqa: E501

        :param assessment_types: The assessment_types of this Metric.  # noqa: E501
        :type: list[str]
        """

        self._assessment_types = assessment_types

    @property
    def properties(self):
        """Gets the properties of this Metric.  # noqa: E501

        The optional properties which set values for the ParameterSpecs associated with this metric's implementation that will be sent to  the instantiated evaluation metric.   # noqa: E501

        :return: The properties of this Metric.  # noqa: E501
        :rtype: object
        """
        return self._properties

    @properties.setter
    def properties(self, properties):
        """Sets the properties of this Metric.

        The optional properties which set values for the ParameterSpecs associated with this metric's implementation that will be sent to  the instantiated evaluation metric.   # noqa: E501

        :param properties: The properties of this Metric.  # noqa: E501
        :type: object
        """

        self._properties = properties

    @property
    def version(self):
        """Gets the version of this Metric.  # noqa: E501

        The version of this metric  # noqa: E501

        :return: The version of this Metric.  # noqa: E501
        :rtype: str
        """
        return self._version

    @version.setter
    def version(self, version):
        """Sets the version of this Metric.

        The version of this metric  # noqa: E501

        :param version: The version of this Metric.  # noqa: E501
        :type: str
        """

        self._version = version

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
        if issubclass(Metric, dict):
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
        if not isinstance(other, Metric):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
