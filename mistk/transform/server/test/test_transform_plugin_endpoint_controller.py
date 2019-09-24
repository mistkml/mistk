# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from mistk.transform.server.models.service_error import ServiceError  # noqa: E501
from mistk.transform.server.models.transform_instance_status import TransformInstanceStatus  # noqa: E501
from mistk.transform.server.models.transform_specification_init_params import TransformSpecificationInitParams  # noqa: E501
from mistk.transform.server.test import BaseTestCase


class TestTransformPluginEndpointController(BaseTestCase):
    """TransformPluginEndpointController integration test stubs"""

    def test_get_status(self):
        """Test case for get_status

        Retrieves the status of the transform plugin
        """
        query_string = [('watch', true),
                        ('resourceVersion', 8.14)]
        response = self.client.open(
            '/v1/mistk/transform/status',
            method='GET',
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_terminate(self):
        """Test case for terminate

        Shutdowns the transform plugin and cleans up any resources.
        """
        response = self.client.open(
            '/v1/mistk/transform/shutdown',
            method='POST',
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_transform(self):
        """Test case for transform

        Performs the transforms defined for this plugin
        """
        initParams = TransformSpecificationInitParams()
        response = self.client.open(
            '/v1/mistk/transform/transform',
            method='POST',
            data=json.dumps(initParams),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
