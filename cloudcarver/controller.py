import requests

from cloudcarver.error import HandlerError, AWSError

from cloudcarver.message import ResponseMessage, RequestMessage

import time
import logging

__author__ = 'jdenning'

log = logging.getLogger("cloudcarver")


def send_response(request_msg, data=None, error=None):
    """
    Send response message to S3 URL


    :param request_msg:
    :type request_msg: RequestMessage
    :param data: Data to be included in SUCCESS response
    :type data: dict
    :param error: Error message - setting this will cause a FAILED response
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


def handle_request(request, config):
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






