"""
The main start file of the project. This will start all the threads and control them.
"""
import threading
from datetime import datetime
from queue import Queue
from time import sleep

from logger import init_logger, logger
from threads.Controller import Controller

if __name__ == '__main__':
    threading.Thread.name = 'Main'

    init_logger()

    try:
        queue = Queue()

        Controller.init(queue)

        while True:
            minutes_str = datetime.now().time().strftime('%M')

            if minutes_str == '29' or minutes_str == '59':
                Controller.start_control_adult_dates()

            Controller.join_all()

            sleep(1)

    except Exception as e:
        logger().error(str(e))

    finally:
        Controller.kill_all_processes()
