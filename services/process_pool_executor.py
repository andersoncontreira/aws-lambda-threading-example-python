import multiprocessing
from multiprocessing import Pool
from multiprocessing import Queue
from multiprocessing.context import Process


class ProcessPoolExecutor:
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

    def execute(self, future_fn, finish_callback):
        if not self._executing:
            self._logger.debug('processing queue...')

            if self.queue.qsize() == 0:
                return True

            self.handle_pool(future_fn, finish_callback)

    def handle_pool(self, future_fn, finish_callback):
        # total de threads a serem executadas
        process_count = self.queue.qsize()
        self._executing = True
        processes = []

        pool = Pool(multiprocessing.cpu_count())

        for i in range(process_count):
            self._process_results.put(pool.apply_async(future_fn))

        pool.close()
        pool.join()

        while self._process_results.qsize() > 0:
            future_result = self._process_results.get()
            self._results.append(future_result.get())

        finish_callback(self._results)





