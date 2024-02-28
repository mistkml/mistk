# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from mistk.orchestrator.server.models.base_model_ import Model
from mistk.orchestrator.server import util


class DataRecord(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, record_id: str=None, reference_set_project: str=None, referenced_set_id: str=None, values: List[object]=None):  # noqa: E501
        """DataRecord - a model defined in Swagger

        :param record_id: The record_id of this DataRecord.  # noqa: E501
        :type record_id: str
        :param reference_set_project: The reference_set_project of this DataRecord.  # noqa: E501
        :type reference_set_project: str
        :param referenced_set_id: The referenced_set_id of this DataRecord.  # noqa: E501
        :type referenced_set_id: str
        :param values: The values of this DataRecord.  # noqa: E501
        :type values: List[object]
        """
        self.swagger_types = {
            'record_id': str,
            'reference_set_project': str,
            'referenced_set_id': str,
            'values': List[object]
        }

        self.attribute_map = {
            'record_id': 'recordId',
            'reference_set_project': 'referenceSetProject',
            'referenced_set_id': 'referencedSetId',
            'values': 'values'
        }

        self._record_id = record_id
        self._reference_set_project = reference_set_project
        self._referenced_set_id = referenced_set_id
        self._values = values

    @classmethod
    def from_dict(cls, dikt) -> 'DataRecord':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The DataRecord of this DataRecord.  # noqa: E501
        :rtype: DataRecord
        """
        return util.deserialize_model(dikt, cls)

    @property
    def record_id(self) -> str:
        """Gets the record_id of this DataRecord.

        The id of this record  # noqa: E501

        :return: The record_id of this DataRecord.
        :rtype: str
        """
        return self._record_id

    @record_id.setter
    def record_id(self, record_id: str):
        """Sets the record_id of this DataRecord.

        The id of this record  # noqa: E501

        :param record_id: The record_id of this DataRecord.
        :type record_id: str
        """
        if record_id is None:
            raise ValueError("Invalid value for `record_id`, must not be `None`")  # noqa: E501

        self._record_id = record_id

    @property
    def reference_set_project(self) -> str:
        """Gets the reference_set_project of this DataRecord.

        the project associated with the data record set   # noqa: E501

        :return: The reference_set_project of this DataRecord.
        :rtype: str
        """
        return self._reference_set_project

    @reference_set_project.setter
    def reference_set_project(self, reference_set_project: str):
        """Sets the reference_set_project of this DataRecord.

        the project associated with the data record set   # noqa: E501

        :param reference_set_project: The reference_set_project of this DataRecord.
        :type reference_set_project: str
        """

        self._reference_set_project = reference_set_project

    @property
    def referenced_set_id(self) -> str:
        """Gets the referenced_set_id of this DataRecord.

        The UUID of the Data Record Set this record is associated with. This  should be the ObjectId of a GroundTruthSet or PredictionSet   # noqa: E501

        :return: The referenced_set_id of this DataRecord.
        :rtype: str
        """
        return self._referenced_set_id

    @referenced_set_id.setter
    def referenced_set_id(self, referenced_set_id: str):
        """Sets the referenced_set_id of this DataRecord.

        The UUID of the Data Record Set this record is associated with. This  should be the ObjectId of a GroundTruthSet or PredictionSet   # noqa: E501

        :param referenced_set_id: The referenced_set_id of this DataRecord.
        :type referenced_set_id: str
        """

        self._referenced_set_id = referenced_set_id

    @property
    def values(self) -> List[object]:
        """Gets the values of this DataRecord.

        A list of labels, optionally this could be a list of dictionaries instead where  the dictionaries contain the ground truth label plus a bounding box, etc,  this could also include certainty assessments.    # noqa: E501

        :return: The values of this DataRecord.
        :rtype: List[object]
        """
        return self._values

    @values.setter
    def values(self, values: List[object]):
        """Sets the values of this DataRecord.

        A list of labels, optionally this could be a list of dictionaries instead where  the dictionaries contain the ground truth label plus a bounding box, etc,  this could also include certainty assessments.    # noqa: E501

        :param values: The values of this DataRecord.
        :type values: List[object]
        """

        self._values = values
