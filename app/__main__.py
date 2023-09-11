"""
The main start file of the project. This will start all the threads and control them.
"""
import threading
from datetime import datetime
from queue import Queue
from time import sleep

from app.logger import MyLogger
from app.Controller import Controller

if __name__ == '__main__':
    threading.Thread.name = 'Main'

    MyLogger.init_logger()

    try:
        queue = Queue()

        Controller.init(queue)

        MyLogger.logger().info("Waiting for minutes == 28 or 58")

        while True:
            minutes_str = datetime.now().time().strftime('%M')

            if minutes_str == '28' or minutes_str == '58':
                MyLogger.logger().info('Starting driver..')
                Controller.start_control_adult_dates()

            Controller.join_all()

            sleep(1)

    except Exception as e:
        MyLogger.logger().error(str(e))

    finally:
        Controller.kill_all_processes()
