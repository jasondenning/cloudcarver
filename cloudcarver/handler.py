__author__ = 'Jason Denning'

from cloudcarver.util import short_uuid
from cloudcarver.error import HandlerActionError

from abc import ABCMeta, abstractmethod

import logging

log = logging.getLogger(__name__)

def handler_instance_factory(cls, config=None):
    """
    Initialize a handler class instance with configuration parameters, if set.

    :param cls: Class to be instantiated and returned
    :type cls: object
    :param config:
    :type config: dict
    :return:
    """
    # Initialize an empty dict if no config is given
    if not config:
        config = dict()
    # Get handler specific configuration, if present; or an empty dict, if not
    handler_config = config.get(cls.RESOURCE_NAME, dict())
    handler = cls(**handler_config)
    return handler




class Handler(object):
    """
    Handler - Base Handler Class

    Takes care of typical initialization (setting self.request) and physical
    resource id generation.

    You can either override the standard action methods (create, update, delete),
    or implement them as '_create()', '_update()', and '_delete()'; in the
    latter case calls to these methods will be wrapped with logging.

    A physical resource id will be generated in the 'create' case, otherwise the
    physical_resource_id from the request will be used.

    As with create(), et. al.,  generate_physical_id() may be defined as
    generate_physical_id or as generate_physical_id.
    """
    __metaclass__ = ABCMeta

    def __init__(self, request, **kwargs):
        self._request = request
        self.config = kwargs
        self._physical_resource_id = None


    def __repr__(self):
        return "%s(%s, **%s)" % (self.__name__, self._request, self.config)


    @property
    def request(self):
        """
        Request message from AWS - read only property
        """
        return self._request


    @property
    def request_type(self):
        """
        Convenience wrapper around self._request.request_type.
        :return: Request type (one of: CREATE, UPDATE, DELETE)
        """
        return self._request.request_type.upper()


    @property
    def physical_resource_id(self):
        if not self._physical_resource_id:
            self._physical_resource_id = self._get_or_generate_physical_id()
        return self._physical_resource_id


    def _get_or_generate_physical_id(self):
        """
        Either generates a new, unique(ish) physical resource id (in the case
        of a create request), or sets self.physical_resource_id (really
        self._physical_resource_id) to whatever is specified in the request.
        """
        if self.request_type == 'CREATE':
            log.debug("Got create request - generating a new " +
                      "physical_resource_id")
            physical_id = self.generate_physical_id()
            log.info("Got generated physical resource id %s" % physical_id)
        else:
            log.debug("Got %s request - using physical resource id from " +
                      "request" % self.request_type)
            physical_id = self.request.physical_resource_id
            log.info("Got physical resource id %s from request" % log.info)
        return physical_id


    def generate_physical_id(self):
        """
        Generates a unique "physical" resource id.  The format of the name may
        be adjusted in the application config. <- FIXME

        If self._generate_physical_id() is defined, that method will be used
        instead.
        :param base_name:
        :return: (String) A semi-unique resource_id
        """
        log.info("Generating physical resource id")
        if hasattr(self, '_generate_physical_id'):
            log.debug("Using _generate_physical_id method")
            physical_id = self._generate_physical_id()
        else:
            physical_id = self.physical_id_base + short_uuid()

        log.debug("Successfuly generated physical resource id: %s " % physical_id)
        return physical_id


    def run_action(self, action_type):
        """
        Logging wrapper around resource actions (create, update, delete)
        :return:
        """
        log.info("Running %s action" % action_type)
        try:
            action = getattr(self, action_type)

            output = action()
            log.info("Successfully ran %s action" % action_type)
            log.debug("%s action output: %s" % (action_type, output))
            return output
        except Exception, e:
            msg = "Create action failed! Caught exception: %s" e.message
            log.exception(msg)
            raise HandlerActionError(e)


    @abstractmethod
    def create(self):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def delete(self):
        pass


