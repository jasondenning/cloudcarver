from unittest import TestCase, skip
from cloudcarver.tests import MockRequestMessage

from cloudcarver.message import ResponseMessage

import json

__author__ = 'jdenning'


class TestResponseMessage(TestCase):

    def setUp(self):
        self.request = MockRequestMessage()


    def test_to_dict_has_key_Status(self):
        resp = ResponseMessage(self.request)
        resp_dict = resp.to_dict()
        assert 'Status' in resp_dict.keys()

    def test_to_dict_has_key_StackId(self):
        resp = ResponseMessage(self.request)
        resp_dict = resp.to_dict()
        assert 'StackId' in resp_dict.keys()

    def test_to_dict_has_key_RequestId(self):
        resp = ResponseMessage(self.request)
        resp_dict = resp.to_dict()
        assert 'RequestId' in resp_dict.keys()

    def test_to_dict_has_key_LogicalResourceId(self):
        resp = ResponseMessage(self.request)
        resp_dict = resp.to_dict()
        assert 'LogicalResourceId' in resp_dict.keys()

    def test_to_dict_has_key_PhysicalResourceId(self):
        resp = ResponseMessage(self.request)
        resp_dict = resp.to_dict()
        assert 'PhysicalResourceId' in resp_dict.keys()


    def test_to_dict_StackId_same_as_request(self):
        resp = ResponseMessage(self.request)
        resp_dict = resp.to_dict()
        assert resp_dict['StackId'] == self.request.stack_id

    def test_to_dict_RequestId_same_as_request(self):
        resp = ResponseMessage(self.request)
        resp_dict = resp.to_dict()
        assert resp_dict['RequestId'] == self.request.request_id

    def test_to_dict_LogicalResourceId_same_as_request(self):
        resp = ResponseMessage(self.request)
        resp_dict = resp.to_dict()
        assert resp_dict['LogicalResourceId'] == self.request.logical_resource_id


    def test_default_status_is_SUCCESS(self):
        resp = ResponseMessage(self.request)
        assert resp.status == "SUCCESS"

    def test_status_is_FAILED_if_error(self):
        resp = ResponseMessage(self.request)
        resp.error = True
        assert resp.status == "FAILED"

    def test_to_json_StackId_same_as_request(self):
        resp = ResponseMessage(self.request)
        resp_json = resp.to_json()
        resp_dict = json.loads(resp_json)
        assert resp_dict['StackId'] == self.request.stack_id

    def test_to_json_RequestId_same_as_request(self):
        resp = ResponseMessage(self.request)
        resp_json = resp.to_json()
        resp_dict = json.loads(resp_json)
        assert resp_dict['RequestId'] == self.request.request_id

    def test_to_json_LogicalResourceId_same_as_request(self):
        resp = ResponseMessage(self.request)
        resp_json = resp.to_json()
        resp_dict = json.loads(resp_json)
        assert resp_dict['LogicalResourceId'] == self.request.logical_resource_id

        
