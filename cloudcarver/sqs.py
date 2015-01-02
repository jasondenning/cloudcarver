__author__ = 'jason'


from cloudcarver.message import ResponseMessage, RequestMessage

import boto

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
    return(RequestMessage.from_AWS_json(message.get_body()))



def get_queue(name):
    try:
        log.debug("Connecting to SQS")
        conn = boto.connect_sqs()
        log.debug("Getting queue - `%s`"% name)
        queue = conn.get_queue(name)
        return(queue)
    except Exception, e:
        raise AWSError("Unable to connect to SQS queue `%s` - %s"% e.message)

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

def process_request_message(sqs_message, config):
    """

    :param sqs_message:
    :type sqs_message: boto.sqs.Message
    :param config:
    :return:
    """
    #handle_request(sqs_message, config)
    sqs_message.delete()