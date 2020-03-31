import queue
import requests

from services.process_executor import ProcessExecutor
from services.thread_executor import ThreadExecutor


class RequestManager:
    MODE_PROCESS = 'process'
    MODE_THREADS = 'threads'

    def __init__(self, logger, mode):
        self.queue = queue.Queue()
        self.logger = logger
        self.responses = []
        if mode == self.MODE_PROCESS:
            self.mode = self.MODE_PROCESS
        else:
            self.mode = self.MODE_THREADS

    def get_response_list(self):
        return self.responses

    def add_request_list(self, request_list):
        # map(self.queue.put, request_list)
        for req in request_list:
            self.queue.put(req)

    def add_request(self, request):
        self.queue.put(request)

    def execute(self):
        result = True
        self.logger.info('Executing a requests...')
        if self.queue.qsize() == 0:
            self.logger.info('Empty queue...')
            result = False
        else:
            if self.mode == self.MODE_PROCESS:
                executor = ProcessExecutor(self.queue, self.logger)
                executor.execute(self._do_request, self.on_finish)

            else:
                executor = ThreadExecutor(self.queue, self.logger)
                executor.execute(self._do_request, self.on_finish)

        return result

    def _do_request(self):
        self.logger.info('Executing a request')
        result = None
        if not self.queue.empty():
            url = self.queue.get()
            response = requests.get(url)
            result = {
                'url': url,
                'response': {
                    'status_code': response.status_code,
                    'text': response.text}
            }
        return result

    def on_finish(self, responses):
        self.logger.info('finished with responses')
        self.responses = responses
