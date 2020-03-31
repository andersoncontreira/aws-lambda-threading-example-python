import concurrent
from concurrent.futures.thread import ThreadPoolExecutor


class ThreadExecutor:
    def __init__(self, queue, logger):
        self._results = []
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

            # total de threads a serem executadas
            futures_count = self.queue.qsize()
            futures = []
            self._executing = True

            with ThreadPoolExecutor(max_workers=self._max_workers) as executor:
                try:
                    for i in range(futures_count):
                        futures.append(executor.submit(future_fn))
                    finished = concurrent.futures.wait(futures, return_when=concurrent.futures.ALL_COMPLETED)
                    if finished:
                        self._executing = False

                        for future in futures:
                            future_result = future.result()
                            self._results.append(future_result)

                        finish_callback(self._results)

                except Exception as err:
                    self._logger.error(err)
                finally:
                    executor.shutdown(wait=True)
                    self._executing = False
        else:
            self._logger.debug('not processing queue...')