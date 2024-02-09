# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from mistk.agent.server.models.agent_instance_init_params import AgentInstanceInitParams  # noqa: E501
from mistk.agent.server.models.agent_instance_status import AgentInstanceStatus  # noqa: E501
from mistk.agent.server.models.service_error import ServiceError  # noqa: E501
from mistk.agent.server.test import BaseTestCase


class TestAgentInstanceEndpointController(BaseTestCase):
    """AgentInstanceEndpointController integration test stubs"""

    def test_agent_registered(self):
        """Test case for agent_registered

        Agent registered
        """
        agentCfg = None
        response = self.client.open(
            '/v1/mistk/agent/agentRegistered',
            method='POST',
            data=json.dumps(agentCfg),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_build_model(self):
        """Test case for build_model

        Build the model
        """
        query_string = [('modelPath', 'modelPath_example')]
        response = self.client.open(
            '/v1/mistk/agent/buildModel',
            method='POST',
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_episode_started(self):
        """Test case for episode_started

        Episode started
        """
        episodeCfg = None
        response = self.client.open(
            '/v1/mistk/agent/episodeStarted',
            method='POST',
            data=json.dumps(episodeCfg),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_episode_stopped(self):
        """Test case for episode_stopped

        Episode stopped
        """
        response = self.client.open(
            '/v1/mistk/agent/episodeStopped',
            method='POST',
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_action(self):
        """Test case for get_action

        Get action(s) from agent
        """
        obs = None
        response = self.client.open(
            '/v1/mistk/agent/getAction',
            method='POST',
            data=json.dumps(obs),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_api_version(self):
        """Test case for get_api_version

        Returns the version of the MISTK API
        """
        response = self.client.open(
            '/v1/mistk/agent/apiVersion',
            method='GET',
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_status(self):
        """Test case for get_status

        Get the status of the model
        """
        query_string = [('watch', False),
                        ('resourceVersion', 56)]
        response = self.client.open(
            '/v1/mistk/agent/status',
            method='GET',
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_initialize_agent(self):
        """Test case for initialize_agent

        Initialize the model
        """
        initializationParameters = AgentInstanceInitParams()
        response = self.client.open(
            '/v1/mistk/agent/initialize',
            method='POST',
            data=json.dumps(initializationParameters),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_replay_action(self):
        """Test case for replay_action

        Replay an action from agent
        """
        obs = None
        response = self.client.open(
            '/v1/mistk/agent/replayAction',
            method='POST',
            data=json.dumps(obs),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_reset(self):
        """Test case for reset

        Resets the model
        """
        query_string = [('unloadModel', True)]
        response = self.client.open(
            '/v1/mistk/agent/reset',
            method='POST',
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_save_model(self):
        """Test case for save_model

        Save the model snapshot
        """
        query_string = [('modelPath', 'modelPath_example')]
        response = self.client.open(
            '/v1/mistk/agent/saveModel',
            method='POST',
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_terminate(self):
        """Test case for terminate

        Shut down the agent
        """
        response = self.client.open(
            '/v1/mistk/agent/shutdown',
            method='POST',
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
