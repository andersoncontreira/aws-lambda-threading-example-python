from multiprocessing import Queue
from multiprocessing.context import Process
from time import sleep


class ProcessExecutor:
    def __init__(self, queue, logger):
        self._results = []
        # Other type oueue here
        self._process_results = Queue()
        self.queue = queue
        self._logger = logger
        # número máximo de threads em paralelo
        self._max_workers = 3
        self._executing = False

    def get_results(self):
        return self._results

    def _worker(self, fn):
        self._process_results.put(fn())

    def execute(self, future_fn, finish_callback):
        if not self._executing:
            self._logger.debug('processing queue...')

            if self.queue.qsize() == 0:
                return True

            self.handle_processes(future_fn, finish_callback)

    def handle_processes(self, future_fn, finish_callback):
        # total de threads a serem executadas
        process_count = self.queue.qsize()
        self._executing = True
        processes = []

        # process_loop = math.ceil(process_count/self._max_workers)
        for i in range(process_count):
            processes.append(Process(target=self._worker, args=(future_fn,), ))

        while len(processes) > 0:
            for i in range(self._max_workers):
                process = processes.pop()
                process.start()
                process.join()
            # wait a little space o time to create the new subprocess
            sleep(0.001)
        else:
            self._logger.info('all executed')
            while self._process_results.qsize() > 0:
                future_result = self._process_results.get()
                self._results.append(future_result)

            finish_callback(self._results)




