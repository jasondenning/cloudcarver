__author__ = 'jason'

from cloudcarver.error import HandlerError

import logging

__author__ = 'jdenning'

log = logging.getLogger("cloudcarver")

#def determine_handler_cls(request_msg, routes):
#    """
#    Figure out which handler class to use in order to process the request_msg
#
#    :param request_msg: RequestMessage to process
#    :trequest_msguest: RequestMessage
#    :param routes: Dictionary of routes
#    :type routes: dict
#    :return: Handler instance
#    """
#    # FIXME - move to message.RequestMessage?
#    resource_type_arr = request_msg.resource_type.split("::")
#    # If the first component of the resource_type is 'Custom', delete it
#    if resource_type_arr[0].lower() == "custom":
#        del resource_type_arr[0]
#
#    resource_type = "::".join(resource_type_arr)
#    print("Looking up handler class for resource type `%s`"% resource_type)
#    print(routes)
#    handler_cls = routes.get(resource_type, None)
#    print("Looking up handler class `%s`"% handler_cls)
#
#    if not handler_cls:
#        handler_not_found(resource_type)
#        raise HandlerError("Can't find handler class for %s!"% resource_type)
#    else:
#        # Handler class found, initialize it
#        handler = handler_cls(request_msg)
#        return(handler)

def determine_handler_cls(request_msg, routes):
    """
    Figure out which handler class to use in order to process the request_msg

    :param request_msg: RequestMessage to process
    :type request_msg: RequestMessage
    :param routes: Dictionary of routes
    :type routes: dict
    :return: Handler class
    """
    resource_type = request_msg.resource_type
    log.debug("Determining handler class for resource type %s" % resource_type)
    handler_cls = routes.get(resource_type, None)
    if not handler_cls:
        error_msg = "No handler registered for resource type %s" % resource_type
        log.error(error_msg)
        raise HandlerError(error_msg)
    else:
        return handler_cls




def get_handler(request, routes):
    handler = _get_handler_instance(request, routes)
    log.debug("Got handler instance")
    method_name = request.request_type.lower()
    log.debug("Getting method `%s`"% method_name)
    handler_method = getattr(handler, method_name, None)
    if handler_method is None:
        error = "Handler class `%` does not have a method `%s`"% (handler.__name__, handler_method)
        log.exception(error)
        raise HandlerError(error)
    else:
        return(handler_method)