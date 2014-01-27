__author__ = 'jdenning'
import logging

log = logging.getLogger()

class PrintHandler(object):

    def __init__(self, request):
        self.request = request
        self.request.physical_resource_id = "Foo1234"

    def print_handler(self, req_type):
        print("Got %s request!"% req_type)
        print("Request: %s"% self.request)

    def create(self):
        self.print_handler("CREATE")

    def update(self):
        self.print_handler("UPDATE")

    def delete(self):
        self.print_handler("DELETE")

    def Delete(self):
        log.debug("Called the wrong handler!")
        self.delete()


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
            'MyResource' : PrintHandler,
        }
    }
    print(config)
    queue_name = "test-custom-resource-queue"
    log.debug("Beginning watch_sqs_queue loop")
    watch_sqs_queue(queue_name, config)
