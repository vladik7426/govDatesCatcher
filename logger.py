import logging
from datetime import datetime

__logger = logging.getLogger('root')


def init_logger():
    global __logger

    selenium_logger = logging.getLogger('selenium.webdriver.remote.remote_connection')
    selenium_logger.setLevel(logging.WARNING)

    selenium_logger = logging.getLogger('selenium.webdriver.common.service')
    selenium_logger.setLevel(logging.WARNING)

    urllib3_logger = logging.getLogger('urllib3')
    urllib3_logger.setLevel(logging.WARNING)

    urllib3_logger = logging.getLogger('undetected_chromedriver')
    urllib3_logger.setLevel(logging.WARNING)

    logging.basicConfig(level=logging.NOTSET,
                        format='%(levelname).1s-[%(threadName)s] %(message)s',
                        datefmt='%H:%M:%S')

    file_handler = logging.FileHandler(f'logs/{datetime.now().strftime("%d-%m-%Y")}.log', 'a')
    file_handler.setLevel(logging.NOTSET)

    formatter = logging.Formatter('%(levelname)s::(%(asctime)s)::[%(threadName)s] %(message)s',
                                  datefmt='%H:%M:%S')
    file_handler.setFormatter(formatter)

    __logger.addHandler(file_handler)


def logger():
    global __logger
    return __logger
