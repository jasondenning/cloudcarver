import requests

import boto

from cloudcarver.errors import HandlerError, AWSError

from cloudcarver.message import ResponseMessage, RequestMessage

import time
import logging

__author__ = 'jdenning'

log = logging.getLogger("cloudcarver")

def get_message_from_sqs(sqs_queue):
    """
    Get message from sqs_queue, and return a RequestMessage object
    :param sqs_queue:
    :param num_messages:
    :param visibility_timeout:
    :param wait_time_seconds:
    :return:
    """
    result_set = sqs_queue.get_messages(num_messages=1, visibility_timeout=5, wait_time_seconds=5)
    if len(result_set) > 0:
        sqs_msg = result_set[0]
        req_msg = parse_sqs_message(sqs_msg)
        sqs_msg.delete()
        return(req_msg)

def parse_sqs_message(message):
    return(RequestMessage.from_AWS_json(sqs_msg.get_body()))



def send_response(request_msg, data=None, error=None):
    """
    Send response message to S3 url
    :param request:
    :param data:
    :param error:
    :return:
    """
    response = ResponseMessage(request_msg)
    if data:
        response.data = data

    if error:
        response.error = error
    try:
        # PUT the response file to the S3 pre-signed URL
        requests.put(url=request_msg.response_url,
                     data=response.to_json(),
                     headers={"Content-Type": ""},
                     verify=True
                    ).raise_for_status()
        log.debug((response.to_json()))
        log.info("Successfully send response %s for RequestID:%s"% (request_msg.response_url, request_msg.request_id))
    except Exception, e:
        print("Got Error! - %s"% e.message)
        log.exception("Failed sending response %s for RequestID:%s"% (request_msg.response_url, request_msg.request_id))
        log.exception("Error: %s"% e.message)
        raise AWSError("Unable to send response!")

def handler_not_found(resource_type):
    """
    Handle the error case, when a route is not found for a request
    :param request:
    :return:
    """
    error_msg = "Handler not found for resource type '%s'"% resource_type
    log.error(error_msg)
    raise HandlerError(error_msg)

def _get_handler_instance(request, routes):
    """
    Figure out which handler to use for the message
    :param request: RequestMessage to process
    :type request: RequestMessage
    :param routes: Dictionary of routes
    :type routes: dict
    :return: Handler instance
    """
    resource_type_arr = request.resource_type.split("::")
    # If the first component of the resource_type is 'Custom', delete it
    if resource_type_arr[0].lower() == "custom":
        del resource_type_arr[0]

    resource_type = "::".join(resource_type_arr)
    print("Looking up handler class for resource type `%s`"% resource_type)
    print(routes)
    handler_cls = routes.get(resource_type, None)
    print("Looking up handler class `%s`"% handler_cls)

    if not handler_cls:
        handler_not_found(resource_type)
        raise HandlerError("Can't find handler class for %s!"% resource_type)
    else:
        # Handler class found, initialize it
        handler = handler_cls(request)
        return(handler)


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


def error_handling_sqs_request(request, exception=None, error_msg=None):
    log.debug("Error handling request!")
    log.debug("Request: %s"% request)
    AWS_error = "Unable to handle request!"
    if exception:
        log.error("Caught exception handling message!")
        log.exception(exception.message)
    if error_msg:
        log.error(error_msg)
        AWS_error = error_msg
    log.info("Sending FAILED response")
    send_response(request, error=AWS_error)


def handle_sqs_request(request, config):
    req_msg = RequestMessage.from_AWS_json(request.get_body())
    try:
        handler = get_handler(req_msg, config['routes'])
        data = handler()
        error = getattr(handler, 'error', None)
        send_response(req_msg, data=data, error=error)

    except HandlerError, e:
        error_handling_sqs_request(req_msg, exception=e)

    except AWSError, e:
        # AWS Connection error or other unknown error connecting to SQS
        log.error("Unable to process Request!")
        log.exception(e.message)
        raise e

    except Exception, e:
        print(e)
        error_handling_sqs_request(req_msg, exception=e)


def get_queue(name):
    try:
        log.debug("Connecting to SQS")
        conn = boto.connect_sqs()
        log.debug("Getting queue - `%s`"% name)
        queue = conn.get_queue(name)
        return(queue)
    except Exception, e:
        raise AWSError("Unable to connect to SQS queue `%s` - %s"% e.message)


def process_request_message(sqs_message, config):
    """

    :param sqs_message:
    :type sqs_message: boto.sqs.Message
    :param config:
    :return:
    """
    handle_sqs_request(sqs_message, config)
    sqs_message.delete()


def watch_sqs_queue(name, config):
    """
    Watch an SQS queue, and handle messages according to routes

    :param name:
    :return:
    """
    log.debug("Watching SQS queue named `%s`"% name)
    log.debug("Config: %s"% config)
    queue = get_queue(name)
    sqs_config = config['sqs']
    while 1:
        messages = queue.get_messages(num_messages=sqs_config['num_messages'],
                                      visibility_timeout=sqs_config['visibility_timeout'],
                                      wait_time_seconds=sqs_config['wait_time'])
        if messages:
            for m in messages:
                process_request_message(m, config)
        log.debug("Waiting for %s seconds"% sqs_config['sleep_time'])
        time.sleep(sqs_config['sleep_time'])
