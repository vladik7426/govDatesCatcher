import logging
from datetime import datetime


class MyLogger:
    __logger = logging.Logger('govDatesCatcher')

    @classmethod
    def init_logger(cls):
        logging.getLogger('selenium.webdriver.remote.remote_connection').setLevel(logging.ERROR)
        logging.getLogger('selenium.webdriver.common.service').setLevel(logging.ERROR)
        logging.getLogger('urllib3').setLevel(logging.ERROR)
        logging.getLogger('undetected_chromedriver').setLevel(logging.ERROR)

        logging.basicConfig(format='%(levelname).1s-[%(threadName)s] %(message)s',
                            datefmt='%H:%M:%S')

        file_handler = logging.FileHandler(f'logs/{datetime.now().strftime("%d-%m-%Y")}.log', 'a')
        file_handler.setLevel(logging.NOTSET)

        formatter = logging.Formatter('%(levelname)s::(%(asctime)s)::[%(threadName)s] %(message)s',
                                      datefmt='%H:%M:%S')

        file_handler.setFormatter(formatter)

        cls.__logger.addHandler(file_handler)

    @classmethod
    def logger(cls):
        return cls.__logger
