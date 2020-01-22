# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from mistk.model.server.models.model_instance_init_params import ModelInstanceInitParams  # noqa: E501
from mistk.model.server.models.model_instance_status import ModelInstanceStatus  # noqa: E501
from mistk.model.server.models.service_error import ServiceError  # noqa: E501
from mistk.model.server.test import BaseTestCase


class TestModelInstanceEndpointController(BaseTestCase):
    """ModelInstanceEndpointController integration test stubs"""

    def test_build_model(self):
        """Test case for build_model

        Build the model
        """
        query_string = [('modelPath', 'modelPath_example')]
        response = self.client.open(
            '/v1/mistk/buildModel',
            method='POST',
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_api_version(self):
        """Test case for get_api_version

        Returns the version of the MISTK API
        """
        response = self.client.open(
            '/v1/mistk/apiVersion',
            method='GET',
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_status(self):
        """Test case for get_status

        Get the status of the model
        """
        query_string = [('watch', false),
                        ('resourceVersion', 56)]
        response = self.client.open(
            '/v1/mistk/status',
            method='GET',
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_initialize_model(self):
        """Test case for initialize_model

        Initialize the model
        """
        initializationParameters = ModelInstanceInitParams()
        response = self.client.open(
            '/v1/mistk/initialize',
            method='POST',
            data=json.dumps(initializationParameters),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_load_data(self):
        """Test case for load_data

        Loads data for the model
        """
        datasets = None
        response = self.client.open(
            '/v1/mistk/loadData',
            method='POST',
            data=json.dumps(datasets),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_pause(self):
        """Test case for pause

        Pause the model
        """
        response = self.client.open(
            '/v1/mistk/pause',
            method='POST',
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_predict(self):
        """Test case for predict

        Perform predictions with the model
        """
        response = self.client.open(
            '/v1/mistk/predict',
            method='POST',
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_reset(self):
        """Test case for reset

        Resets the model
        """
        response = self.client.open(
            '/v1/mistk/reset',
            method='POST',
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_resume_predict(self):
        """Test case for resume_predict

        Resume predicitons on a paused model
        """
        response = self.client.open(
            '/v1/mistk/resumePredict',
            method='POST',
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_resume_training(self):
        """Test case for resume_training

        Resume training on a paused model
        """
        response = self.client.open(
            '/v1/mistk/resumeTraining',
            method='POST',
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_save_model(self):
        """Test case for save_model

        Save the model snapshot
        """
        query_string = [('modelPath', 'modelPath_example')]
        response = self.client.open(
            '/v1/mistk/saveModel',
            method='POST',
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_save_predictions(self):
        """Test case for save_predictions

        Save the model's predictions
        """
        query_string = [('dataPath', 'dataPath_example')]
        response = self.client.open(
            '/v1/mistk/savePredictions',
            method='POST',
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_stream_predict(self):
        """Test case for stream_predict

        Perform streaming predictions with the model
        """
        dataMap = None
        response = self.client.open(
            '/v1/mistk/streamPredict',
            method='POST',
            data=json.dumps(dataMap),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_terminate(self):
        """Test case for terminate

        Shut down the model
        """
        response = self.client.open(
            '/v1/mistk/shutdown',
            method='POST',
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_train(self):
        """Test case for train

        Train the model
        """
        response = self.client.open(
            '/v1/mistk/train',
            method='POST',
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
