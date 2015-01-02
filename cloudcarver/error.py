__author__ = 'jdenning'

class CloudCarverError(Exception):
    pass

class HandlerError(CloudCarverError):
    pass

class HandlerActionError(HandlerError):
    pass


class AWSError(CloudCarverError):
    pass
