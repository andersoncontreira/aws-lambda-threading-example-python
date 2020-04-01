import concurrent
from concurrent.futures.thread import ThreadPoolExecutor

import requests

request_list = [
    'https://dog.ceo/api/breeds/image/random',
    'https://dog.ceo/api/breeds/list/all',
    'https://date.nager.at/Api/v2/CountryInfo?countryCode=AR',
    'https://dog.ceo/api/breeds/image/random',
    'https://dog.ceo/api/breeds/list/all',
    'https://date.nager.at/Api/v2/CountryInfo?countryCode=US',
    'https://dog.ceo/api/breeds/image/random',
    'https://dog.ceo/api/breeds/list/all',
    'https://date.nager.at/Api/v2/CountryInfo?countryCode=BR',
]

# total de threads a serem executadas
futures_count = len(request_list)
futures = []
max_workers = 3
results = []


def my_function(rid):
    url = request_list.pop()
    print('my fn: %s %s' % (rid, url))

    # self.logger.info('Executing a request')
    result = None
    response = requests.get(url)
    print('my fn: %s %s' % (rid, url))

    return {
        'url': url,
        'response': {
            'status_code': response.status_code,
            'text': response.text}
    }


def finished_callback(results):
    print('fim')
    for r in results:
        print('Result: {}'.format(r))


with ThreadPoolExecutor(max_workers=max_workers) as executor:
    try:
        for i in range(futures_count):
            futures.append(executor.submit(my_function, i))

        finished = concurrent.futures.wait(futures, return_when=concurrent.futures.ALL_COMPLETED)
        if finished:

            for future in futures:
                future_result = future.result()
                results.append(future_result)

            finished_callback(results)

    except Exception as err:
        # self._logger.error(err)
        print(err)
    finally:
        executor.shutdown(wait=True)
        # self._executing = False
