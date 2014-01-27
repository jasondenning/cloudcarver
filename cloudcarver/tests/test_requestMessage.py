from unittest import TestCase
from cloudcarver.message import RequestMessage
from cloudcarver.tests import valid_request_kw, valid_request_json


__author__ = 'jdenning'


class TestRequestMessage(TestCase):
    def setUp(self):
        self._valid_kw = {
            "request_type" : valid_request_kw['request_type'],
            "stack_id" : valid_request_kw['stack_id'],
            "request_id" : valid_request_kw['request_id'],
            "logical_resource_id" : valid_request_kw['logical_resource_id'],
            "physical_resource_id" : valid_request_kw['physical_resource_id'],
            "resource_type" : valid_request_kw['resource_type'],
            "response_url" : valid_request_kw['response_url'],
            "properties" : valid_request_kw['properties'],
            "old_properties" : valid_request_kw['old_properties'],
            }

        self._valid_json = valid_request_json

    def test_from_AWS_json_returns_RequestMessage_object(self):
        req = RequestMessage.from_AWS_json(self._valid_json)
        assert type(req) is RequestMessage

    def test_init_kwarg(self):
        """
        Test that all params in self_valid_kw are accepted by __init__
        """
        req = RequestMessage(**self._valid_kw)

    def test_has_stack_id(self):
        req = RequestMessage(**self._valid_kw)
        assert req.stack_id == self._valid_kw['stack_id']
    
    def test_has_request_id(self):
        req = RequestMessage(**self._valid_kw)
        assert req.request_id == self._valid_kw['request_id']
        
    def test_has_logical_resource_id(self):
        req = RequestMessage(**self._valid_kw)
        assert req.logical_resource_id == self._valid_kw['logical_resource_id']
        
    def test_has_physical_resource_id(self):
        req = RequestMessage(**self._valid_kw)
        assert req.physical_resource_id == self._valid_kw['physical_resource_id']
    
    def test_has_resource_type(self):
        req = RequestMessage(**self._valid_kw)
        assert req.resource_type == self._valid_kw['resource_type']    

    def test_has_response_url(self):
        req = RequestMessage(**self._valid_kw)
        assert req.response_url == self._valid_kw['response_url']
           
    def test_has_request_type(self):
        req = RequestMessage(**self._valid_kw)
        assert req.request_type == self._valid_kw['request_type'] 
           
    def test_has_properties(self):
        req = RequestMessage(**self._valid_kw)
        assert req.properties == self._valid_kw['properties']    
   
    def test_has_old_properties(self):
        req = RequestMessage(**self._valid_kw)
        assert req.old_properties == self._valid_kw['old_properties']    

        


    
    