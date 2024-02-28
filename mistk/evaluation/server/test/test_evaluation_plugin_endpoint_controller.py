# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from mistk.evaluation.server.models.evaluation_instance_status import EvaluationInstanceStatus  # noqa: E501
from mistk.evaluation.server.models.evaluation_specification_init_params import EvaluationSpecificationInitParams  # noqa: E501
from mistk.evaluation.server.models.mistk_metric import MistkMetric  # noqa: E501
from mistk.evaluation.server.models.service_error import ServiceError  # noqa: E501
from mistk.evaluation.server.test import BaseTestCase


class TestEvaluationPluginEndpointController(BaseTestCase):
    """EvaluationPluginEndpointController integration test stubs"""

    def test_evaluate(self):
        """Test case for evaluate

        Performs the evaluation defined for this plugin
        """
        initParams = EvaluationSpecificationInitParams()
        response = self.client.open(
            '/v1/mistk/evaluation/evaluate',
            method='POST',
            data=json.dumps(initParams),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_api_version(self):
        """Test case for get_api_version

        Returns the version of the MISTK API
        """
        response = self.client.open(
            '/v1/mistk/evaluation/apiVersion',
            method='GET',
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_metrics(self):
        """Test case for get_metrics

        Retrieves the metrics available to perform for the evaluation plugin
        """
        response = self.client.open(
            '/v1/mistk/evaluation/metrics',
            method='GET',
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_status(self):
        """Test case for get_status

        Retrieves the status of the evaluation plugin
        """
        query_string = [('watch', true),
                        ('resourceVersion', 8.14)]
        response = self.client.open(
            '/v1/mistk/evaluation/status',
            method='GET',
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_terminate(self):
        """Test case for terminate

        Shutdowns the evaluation plugin and cleans up any resources.
        """
        response = self.client.open(
            '/v1/mistk/evaluation/shutdown',
            method='POST',
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
