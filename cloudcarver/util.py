__author__ = 'Jason Denning'

"""
Utility functions for common tasks
"""

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
    import uuid

    uuid_str = str(uuid.uuid4())
    first_slice_index = int(length / 2)
    last_slice_index = int(length - first_slice_index)
    last_slice_index = -1 * last_slice_index
    short_uuid = uuid_str[:first_slice_index] + uuid_str[last_slice_index:]
    return short_uuid