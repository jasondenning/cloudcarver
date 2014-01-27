__author__ = 'jdenning'

valid_request_kw = {
            "request_type" : "Update",
            "stack_id" : "arn:aws:cloudformation:us-east-1:287482246495:stack/test-custom03/92cb9a50-56d0-11e3-b2de-500150b34cb4",
            "request_id" : "de8d6e36-8b45-46a0-a47e-bb7e6a9640ec",
            "logical_resource_id" : "MyCustomResourceTest",
            "physical_resource_id" : "test-custom03-MyCustomResourceTest-Y39E4LV9QT44",
            "resource_type" : "Custom::MyResource",
            "response_url" : "https://cloudformation-custom-resource-response-useast1.s3.amazonaws.com/arn:aws:cloudformation:us-east-1:287482246495:stack/test-custom03/92cb9a50-56d0-11e3-b2de-500150b34cb4|MyCustomResourceTest|de8d6e36-8b45-46a0-a47e-bb7e6a9640ec?Expires=1387250657&AWSAccessKeyId=AKIAJNXHFR7P7YGKLDPQ&Signature=m87YeA+eAttIwtS+dBtkJkiT8wM=",
            "properties" : {"ServiceToken":"arn:aws:sns:us-east-1:287482246495:test-customresource"},
            "old_properties" : {}
            }

valid_request_json = '{"request_type": "Update", "physical_resource_id": "test-custom03-MyCustomResourceTest-Y39E4LV9QT44", "request_id": "de8d6e36-8b45-46a0-a47e-bb7e6a9640ec", "stack_id": "arn:aws:cloudformation:us-east-1:287482246495:stack/test-custom03/92cb9a50-56d0-11e3-b2de-500150b34cb4", "logical_resource_id": "MyCustomResourceTest", "old_properties": {}, "response_url": "https://cloudformation-custom-resource-response-useast1.s3.amazonaws.com/arn:aws:cloudformation:us-east-1:287482246495:stack/test-custom03/92cb9a50-56d0-11e3-b2de-500150b34cb4|MyCustomResourceTest|de8d6e36-8b45-46a0-a47e-bb7e6a9640ec?Expires=1387250657&AWSAccessKeyId=AKIAJNXHFR7P7YGKLDPQ&Signature=m87YeA+eAttIwtS+dBtkJkiT8wM=", "resource_type": "Custom::MyResource", "properties": {"ServiceToken": "arn:aws:sns:us-east-1:287482246495:test-customresource"}}'


class MockRequestMessage(object):
    def __init__(self):
        self.request_type = valid_request_kw['request_type']
        self.stack_id = valid_request_kw['stack_id']
        self.request_id = valid_request_kw['request_id']
        self.logical_resource_id = valid_request_kw['logical_resource_id']
        self.physical_resource_id = valid_request_kw['physical_resource_id']
        self.resource_type = valid_request_kw['resource_type']
        self.response_url = valid_request_kw['response_url']
        self.properties = valid_request_kw['properties']
        self.old_properties = valid_request_kw['old_properties']



"""
        valid_kw_args = {
            'RequestType' : 'request_type',
            'StackId' : 'stack_id',
            'RequestId' : 'request_id',
            'LogicalResourceId' : 'logical_resource_id',
            'ResourceType' : 'resource_type',
            'ResponseURL' : 'response_url',
            'PhysicalResourceId' : 'physical_resource_id',
            'ResourceProperties' : 'resource_properties',
            'OldResourceProperties' : 'old_resource_properties',
        }
        for key, value in kwargs.items():
            if key in valid_kw_args.values():
                setattr(self, key, value)
            elif key in valid_kw_args.keys():
                # Non-pythonic AWS key was used, translate to pythonic version
                setattr(self, valid_kw_args[key], value)
                """