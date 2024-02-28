# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from mistk.agent.server.models.base_model_ import Model
from mistk.agent.server.models.dataset_statistics import DatasetStatistics  # noqa: F401,E501
from mistk.agent.server.models.object_info import ObjectInfo  # noqa: F401,E501
from mistk.agent.server.models.object_reference import ObjectReference  # noqa: F401,E501
from mistk.agent.server import util


class Dataset(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, object_info: ObjectInfo=None, datastash_id: str=None, datastash_sub_dir: str=None, modality: str=None, format: str=None, statistics: DatasetStatistics=None, default_ground_truth_set_reference: ObjectReference=None):  # noqa: E501
        """Dataset - a model defined in Swagger

        :param object_info: The object_info of this Dataset.  # noqa: E501
        :type object_info: ObjectInfo
        :param datastash_id: The datastash_id of this Dataset.  # noqa: E501
        :type datastash_id: str
        :param datastash_sub_dir: The datastash_sub_dir of this Dataset.  # noqa: E501
        :type datastash_sub_dir: str
        :param modality: The modality of this Dataset.  # noqa: E501
        :type modality: str
        :param format: The format of this Dataset.  # noqa: E501
        :type format: str
        :param statistics: The statistics of this Dataset.  # noqa: E501
        :type statistics: DatasetStatistics
        :param default_ground_truth_set_reference: The default_ground_truth_set_reference of this Dataset.  # noqa: E501
        :type default_ground_truth_set_reference: ObjectReference
        """
        self.swagger_types = {
            'object_info': ObjectInfo,
            'datastash_id': str,
            'datastash_sub_dir': str,
            'modality': str,
            'format': str,
            'statistics': DatasetStatistics,
            'default_ground_truth_set_reference': ObjectReference
        }

        self.attribute_map = {
            'object_info': 'objectInfo',
            'datastash_id': 'datastashId',
            'datastash_sub_dir': 'datastashSubDir',
            'modality': 'modality',
            'format': 'format',
            'statistics': 'statistics',
            'default_ground_truth_set_reference': 'defaultGroundTruthSetReference'
        }

        self._object_info = object_info
        self._datastash_id = datastash_id
        self._datastash_sub_dir = datastash_sub_dir
        self._modality = modality
        self._format = format
        self._statistics = statistics
        self._default_ground_truth_set_reference = default_ground_truth_set_reference

    @classmethod
    def from_dict(cls, dikt) -> 'Dataset':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Dataset of this Dataset.  # noqa: E501
        :rtype: Dataset
        """
        return util.deserialize_model(dikt, cls)

    @property
    def object_info(self) -> ObjectInfo:
        """Gets the object_info of this Dataset.


        :return: The object_info of this Dataset.
        :rtype: ObjectInfo
        """
        return self._object_info

    @object_info.setter
    def object_info(self, object_info: ObjectInfo):
        """Sets the object_info of this Dataset.


        :param object_info: The object_info of this Dataset.
        :type object_info: ObjectInfo
        """
        if object_info is None:
            raise ValueError("Invalid value for `object_info`, must not be `None`")  # noqa: E501

        self._object_info = object_info

    @property
    def datastash_id(self) -> str:
        """Gets the datastash_id of this Dataset.

        The id of the datastash associated with this dataset where all of its files will be stored.   # noqa: E501

        :return: The datastash_id of this Dataset.
        :rtype: str
        """
        return self._datastash_id

    @datastash_id.setter
    def datastash_id(self, datastash_id: str):
        """Sets the datastash_id of this Dataset.

        The id of the datastash associated with this dataset where all of its files will be stored.   # noqa: E501

        :param datastash_id: The datastash_id of this Dataset.
        :type datastash_id: str
        """

        self._datastash_id = datastash_id

    @property
    def datastash_sub_dir(self) -> str:
        """Gets the datastash_sub_dir of this Dataset.

        This field denotes the sub path within the datastash where this dataset's data resides.   # noqa: E501

        :return: The datastash_sub_dir of this Dataset.
        :rtype: str
        """
        return self._datastash_sub_dir

    @datastash_sub_dir.setter
    def datastash_sub_dir(self, datastash_sub_dir: str):
        """Sets the datastash_sub_dir of this Dataset.

        This field denotes the sub path within the datastash where this dataset's data resides.   # noqa: E501

        :param datastash_sub_dir: The datastash_sub_dir of this Dataset.
        :type datastash_sub_dir: str
        """

        self._datastash_sub_dir = datastash_sub_dir

    @property
    def modality(self) -> str:
        """Gets the modality of this Dataset.

        The type of the data supported by this implementation, one of image, audio, video, text, etc. This does not specify the format of the data. Available modalities can be found using the \"global/meta/dataModalities\" endpoint   # noqa: E501

        :return: The modality of this Dataset.
        :rtype: str
        """
        return self._modality

    @modality.setter
    def modality(self, modality: str):
        """Sets the modality of this Dataset.

        The type of the data supported by this implementation, one of image, audio, video, text, etc. This does not specify the format of the data. Available modalities can be found using the \"global/meta/dataModalities\" endpoint   # noqa: E501

        :param modality: The modality of this Dataset.
        :type modality: str
        """

        self._modality = modality

    @property
    def format(self) -> str:
        """Gets the format of this Dataset.

        A string representing the name of the format of the dataset. This should be sufficient to ensure that models and transforms  are able to read and parse the data.   # noqa: E501

        :return: The format of this Dataset.
        :rtype: str
        """
        return self._format

    @format.setter
    def format(self, format: str):
        """Sets the format of this Dataset.

        A string representing the name of the format of the dataset. This should be sufficient to ensure that models and transforms  are able to read and parse the data.   # noqa: E501

        :param format: The format of this Dataset.
        :type format: str
        """

        self._format = format

    @property
    def statistics(self) -> DatasetStatistics:
        """Gets the statistics of this Dataset.


        :return: The statistics of this Dataset.
        :rtype: DatasetStatistics
        """
        return self._statistics

    @statistics.setter
    def statistics(self, statistics: DatasetStatistics):
        """Sets the statistics of this Dataset.


        :param statistics: The statistics of this Dataset.
        :type statistics: DatasetStatistics
        """

        self._statistics = statistics

    @property
    def default_ground_truth_set_reference(self) -> ObjectReference:
        """Gets the default_ground_truth_set_reference of this Dataset.

        A reference to the default ground truth set that is associated with this dataset        # noqa: E501

        :return: The default_ground_truth_set_reference of this Dataset.
        :rtype: ObjectReference
        """
        return self._default_ground_truth_set_reference

    @default_ground_truth_set_reference.setter
    def default_ground_truth_set_reference(self, default_ground_truth_set_reference: ObjectReference):
        """Sets the default_ground_truth_set_reference of this Dataset.

        A reference to the default ground truth set that is associated with this dataset        # noqa: E501

        :param default_ground_truth_set_reference: The default_ground_truth_set_reference of this Dataset.
        :type default_ground_truth_set_reference: ObjectReference
        """

        self._default_ground_truth_set_reference = default_ground_truth_set_reference
