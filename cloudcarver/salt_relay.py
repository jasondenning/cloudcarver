from cloudcarver.errors import HandlerError

__author__ = 'jdenning'
import logging


log = logging.getLogger()
try:
    import salt.client
    fire_local = salt.client.Caller().sminion.functions['event.fire']
    fire_master = salt.client.Caller().sminion.functions['event.fire_master']
except:
    log.error("Unable to import salt.client!")
    raise HandlerError("Unable to import salt libraries!")


class SaltHandler(object):

    def __init__(self, request):
        fire_master({"data": "Initialized SaltHandler"}, "MyCustomResource")
        self.request = request
        self.request.physical_resource_id = "Foo1234"


    def set_physical_id(self, id=None):
        if self.request.physical_resource_id:
            # Use the resource_physical_id on the request
            pass
        elif id:
            # Use the id passed into this function
            self.request.physical_resource_id = id
        else:
            # Generate a new id
            self.request.physical_resource_id = self.generate_physical_id()


    def relay_request(self, req_type):
        tag = "sns/%s/%s"% (self.request.resource_type, self.request.request_id, req_type)
        fire_master(self.request.to_dict(), tag)

    def wait_for_response(self, maxwait=30):
        pass



    def relay_request(self, req_type):
        print("Got %s request!"% req_type)
        print("Request: %s"% self.request)

    def create(self):
        self.relay_request("CREATE")

    def update(self):
        self.relay_request("UPDATE")

    def delete(self):
        self.relay_request("DELETE")


if __name__ == "__main__":
    print("Starting the loop!")
    import sys
    from cloudcarver.controller import watch_sqs_queue
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logfile_path = '/tmp/cloudcarver.log'
    logfile_handler = logging.FileHandler(logfile_path)
    logfile_handler.setLevel(logging.DEBUG)
    logfile_handler.setFormatter(formatter)
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging.DEBUG)
    stdout_handler.setFormatter(formatter)
    log.addHandler(stdout_handler)


    config = {
        'sqs' : {
            'num_messages': 1,
            'visibility_timeout' : 5,
            'wait_time' : 5,
            'sleep_time' : 10,
            },
        'routes' : {
            'MyResource' : SaltHandler,
        }
    }
    print(config)
    queue_name = "test-custom-resource-queue"
    log.debug("Beginning watch_sqs_queue loop")
    watch_sqs_queue(queue_name, config)
