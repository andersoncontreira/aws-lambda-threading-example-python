import logging
import os
import sys

# vendor
ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) + '/'
sys.path.insert(0, ROOT_DIR + 'vendor/')

from services.request_manager import RequestManager

APP_NAME = 'aws-lambda-threading-example-python'
log_level = logging.DEBUG
log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(format=log_format, level=log_level)
logger = logging.getLogger(APP_NAME)

profile_request_list = [
    'https://dog.ceo/api/breeds/image/random',
    'https://dog.ceo/api/breeds/list/all',
    'https://date.nager.at/Api/v2/CountryInfo?countryCode=AR',
    # 'https://date.nager.at/Api/v2/CountryInfo?countryCode=BR'
]


def execute(mode, requests=None):
    manager = RequestManager(logger, mode)
    if not requests:
        requests = profile_request_list
    manager.add_request_list(requests)
    manager.execute()
    return manager.get_response_list()


def thread_handler(event, context):
    logger.info('Handler event {}'.format(event))
    result = execute(RequestManager.MODE_THREADS)
    print('result', result)
    return result


def process_handler(event, context):
    logger.info('Handler event {}'.format(event))
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
    result = execute(RequestManager.MODE_PROCESS, request_list)
    print('result', result)
    return result


def process_pool_handler(event, context):
    logger.info('Handler event {}'.format(event))
    result = execute(RequestManager.MODE_POOL, profile_request_list)
    print('result', result)
    return result
