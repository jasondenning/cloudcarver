__author__ = 'Jason Denning'

"""
Utility functions for common tasks
"""
import os
import yaml

import uuid


def short_uuid(self, length=8):
    """
    Generates a shortened (semi-)unique ID string.

    Uses uuid.uuid4() to generate a random UUID, then shortens it by
    combining the first few characters with the last few characters.
    This, when combined with a logical name, should be fairly unique, and
    easier to type than a full UUID.

    :param length: Number of characters for the shortened UUID; defaults to 8
    :return: Shortened UUID string of length `length`
    """

    uuid_str = str(uuid.uuid4())
    first_slice_index = int(length / 2)
    last_slice_index = int(length - first_slice_index)
    last_slice_index = -1 * last_slice_index
    short_uuid = uuid_str[:first_slice_index] + uuid_str[last_slice_index:]
    return short_uuid


def load_config_file(path):
    """
    Load the config file from 'path'

    Returns a string
    """
    ONE_MEGABYTE = 1049000 #one megabyte in bytes
    MAX_FILE_SIZE = 2 * ONE_MEGABYTE
    file_size = os.path.getsize(path)
    if file_size > MAX_FILE_SIZE:
        # File is too big, don't load it
        msg = "Config file %s is too large - %s MB? Seriously?" % file_size / ONE_MEGABYTE
        # log.exception(msg)
        raise Exception(msg)
    with open(path, 'r') as conf_file:
        # This loads the whole file in memory, which is why we care about size
        return conf_file.read()


def parse_config_file(path):
    """
    Loads a config file, parses the yaml, and returns a dict
    """
    conf_yaml = load_config_file(path)
    return yaml.loads(conf_yaml)



def get_dynamo_record(table, id):
    pass

def create_dynamo_record(table, **kwargs):
    pass
