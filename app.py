import logging

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


def execute(mode):
    manager = RequestManager(logger, mode)
    manager.add_request_list(profile_request_list)
    manager.execute()
    return manager.get_response_list()


def thread_handler(event, context):
    logger.info('Handler event {}'.format(event))
    result = execute(RequestManager.MODE_THREADS)
    print('result', result)
    return result


def process_handler(event, context):
    logger.info('Handler event {}'.format(event))
    result = execute(RequestManager.MODE_PROCESS)
    print('result', result)
    return result


# if __name__ == "__main__":
#     # thread_handler({}, {})
#     process_handler({}, {})
