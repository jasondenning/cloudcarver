__author__ = 'Jason Denning'

import logging

log = logging.getLogger(__name__)


class Handler(object):
    """
    Base Handler Class

    Takes care of typical initialization (setting self.request) and physical
    resource id generation.

    You can either override the standard action methods (create, update, delete),
    or implement them as 'do_create()', 'do_update()', and 'do_delete()'; in the
    latter case calls to these methods will be wrapped with logging.

    A physical resource id will be generated in the 'create' case, otherwise the
    physical_resource_id from the request will be used.

    As with create, et. al.,  _set_physical_resource_id() may be defined as
    _set_physical_resource_id or as _do_set_physical_resource_id.
    """

    def __init__(self, request):
        self._request = request
        self._request_type = request.request_type.lower()
        self._set_physical_resource_id()

    @property
    def request(self):
        """
        Request message from AWS - read only property
        """
        return self._request


    @property
    def request_type(self):
        return self._request_type

    def _set_physical_resource_id(self):
        """
        Either generates a new, unique(ish) physical resource id (in the case
        of a create request), or sets self.physical_resource_id (really
        self._physical_resource_id) to whatever is specified in the request.
        """
        if self.request_type == 'create':
            log.debug("Got 'create' request - generating a new pysical_resource_id")
            if hasattr(self, '_do_set_physical_resource_id'):
                self._do_set_physical_resource_id()
                log.info("Generated physical_resource_id: %s " %
                    self.physical_resource_id)
            else:
                physical_resource_id = self.__name__ + ''