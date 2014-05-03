__author__ = 'Jason Denning'

from cloudcarver.util import short_uuid

import logging

log = logging.getLogger(__name__)


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
    generate_physical_id or as _generate_physical_id.
    """

    def __init__(self, request):
        self._request = request
        self._physical_resource_id = None
        self._request_type = request.request_type.lower()


    @property
    def request(self):
        """
        Request message from AWS - read only property
        """
        return self._request


    @property
    def request_type(self):
        return self._request_type


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
        if self.request_type == 'create':
            log.debug("Got create request - generating a new physical_resource_id")
            physical_id = self._generate_physical_id()
            log.info("Got generated physical resource id %s" % physical_id)
        else:
            log.debug("Got %s request - using physical resource id from request" %
                self._request_type)
            physical_id = self.request['PhysicalResourceId']
            log.info("Got physical resource id %s from request")

        return physical_id


    def _generate_physical_id(self):
        """
        Generates a unique "physical" resource id.  The format of the name may
        be adjusted in the application config. <- FIXME

        If self._do_generate_physical_id() is defined, that method will be used
        instead.
        :param base_name:
        :return: (String) A semi-unique resource_id
        """
        log.info("Generating physical resource id")
        if hasattr(self, '_do_generate_physical_id'):
            log.debug("Using _do_generate_physical_id method")
            physical_id = self._do_generate_physical_id()
        else:
            base_name = self.__name__
            physical_id = base_name + short_uuid()

        log.debug("Successfuly generated physical resource id: %s " % physical_id)
        return physical_id


    def create(self):
        """
        Wrapper around _create
        :return:
        """
        log.info("Running create action")
        if hasattr(self, '_create'):
            log.debug("Calling %s._create()" % self.__name__)
            self._create()
            
