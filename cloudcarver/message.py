import json

import requests

__author__ = 'jdenning'


class RequestMessage(object):
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
    
    def to_dict(self):
        request_dict = {
            'RequestType' : self.request_type,
            'StackId' : self.stack_id,
            'RequestId' : self.request_id,
            'LogicalResourceId' : self.logical_resource_id,
            'ResourceType' : self.resource_type,
            'ResponseURL' : self.response_url,
            'PhysicalResourceId' : self.physical_resource_id,
            'ResourceProperties' : self.properties,
            'OldResourceProperties' : self.old_properties,
        }
        return(request_dict)

    @classmethod
    def from_AWS_format(cls, **kwargs):
        print(kwargs)
        valid_kw_args = {
            'RequestType' : 'request_type',
            'StackId' : 'stack_id',
            'RequestId' : 'request_id',
            'LogicalResourceId' : 'logical_resource_id',
            'ResourceType' : 'resource_type',
            'ResponseURL' : 'response_url',
            'PhysicalResourceId' : 'physical_resource_id',
            'ResourceProperties' : 'properties',
            'OldResourceProperties' : 'old_properties',
        }
        parsed_kw_args = {}
        for key, value in kwargs.items():
            if key in valid_kw_args.values():
                parsed_kw_args[key] = value
            elif key in valid_kw_args.keys():
                # Non-pythonic AWS key was used, translate to pythonic version
                parsed_kw_args[valid_kw_args[key]] = value
            else:
                pass
        print(parsed_kw_args)
        return(RequestMessage(**parsed_kw_args))

    @classmethod
    def from_AWS_json(cls, json_str):
        """
        Alternate constructor for use with JSON data
        :param json_str: String of JSON data
        :return: RequestMessage instance
        """
        params = json.loads(json_str)
        return(cls.from_AWS_format(**params))

    def __str__(self):
        return "RequestMessage - %s"% self.request_id


class ResponseMessage(object):

    @property
    def status(self):
        if not self.error:
            return("SUCCESS")
        else:
            return("FAILED")


    def __init__(self, request):
        self.stack_id = request.stack_id
        self.request_id = request.request_id
        self.logical_resource_id = request.logical_resource_id
        self.error = None
        self.data = None
        if getattr(request, 'physical_resource_id', None):
            physical_resource_id = request.physical_resource_id
        else:
            physical_resource_id = self.generate_physical_id()
        self.physical_resource_id = physical_resource_id

    def generate_physical_id(self):
        return "FOO54321"


    def to_dict(self):
        response_dict = {
            'Status' : self.status,
            'StackId' : self.stack_id,
            'RequestId' : self.request_id,
            'LogicalResourceId' : self.logical_resource_id,
            'PhysicalResourceId' : self.physical_resource_id,
        }
        # Include reason if there's an error
        if self.error:
            response_dict['Reason'] = self.error
        # Include output data, if it exists
        if self.data:
            response_dict['Data'] = self.data

        return(response_dict)

    def to_json(self):
        return(json.dumps(self.to_dict()))



