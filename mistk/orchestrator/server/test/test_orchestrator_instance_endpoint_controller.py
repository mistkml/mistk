# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from mistk.orchestrator.server.models.model_instance_init_params import ModelInstanceInitParams  # noqa: E501
from mistk.orchestrator.server.models.orchestrator_instance_status import OrchestratorInstanceStatus  # noqa: E501
from mistk.orchestrator.server.models.service_error import ServiceError  # noqa: E501
from mistk.orchestrator.server.test import BaseTestCase


class TestOrchestratorInstanceEndpointController(BaseTestCase):
    """OrchestratorInstanceEndpointController integration test stubs"""

    def test_get_status(self):
        """Test case for get_status

        Get the status of the orchestrator
        """
        query_string = [('watch', False),
                        ('resourceVersion', 56)]
        response = self.client.open(
            '/v1/mistk/orchestrator/status',
            method='GET',
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_initialize(self):
        """Test case for initialize

        Initialize the orchestrator
        """
        initializationParameters = ModelInstanceInitParams()
        response = self.client.open(
            '/v1/mistk/orchestrator/initialize',
            method='POST',
            data=json.dumps(initializationParameters),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_register_agent(self):
        """Test case for register_agent

        Registers an agent to the orchestrator
        """
        query_string = [('agentName', 'agentName_example'),
                        ('agentUrl', 'agentUrl_example')]
        response = self.client.open(
            '/v1/mistk/orchestrator/registerAgent',
            method='POST',
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_reset(self):
        """Test case for reset

        Resets the orchestrator
        """
        response = self.client.open(
            '/v1/mistk/orchestrator/reset',
            method='POST',
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_start_episode(self):
        """Test case for start_episode

        Starts an episode
        """
        episodeCfg = None
        response = self.client.open(
            '/v1/mistk/orchestrator/startEpisode',
            method='POST',
            data=json.dumps(episodeCfg),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_stop_episode(self):
        """Test case for stop_episode

        Stops the episode that the orchestrator is currently playing
        """
        response = self.client.open(
            '/v1/mistk/orchestrator/stopEpisode',
            method='POST',
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
