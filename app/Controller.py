"""
Here are thread controlling functional
"""
from multiprocessing import Process
from queue import Queue

from app.GovDriver import GovDriver
from app.logger import MyLogger


class Controller:
    __control_processes: list[Process] = []
    __drivers: list[GovDriver] = []

    @classmethod
    def init(cls, queue: Queue):
        cls.queue = queue

    @classmethod
    def start_control_child_dates(cls):
        process = Process(target=cls.start_control_option,
                          args=('Оформлення закордонного паспорта дитині віком до 16 років',))

        process.name = 'ChildDatesController'

        cls.__control_processes.append(process)
        process.start()

    @classmethod
    def start_control_adult_dates(cls):
        process = Process(target=cls.start_control_option,
                          args=('Оформлення закордонного паспорта',))

        process.name = 'AdultDatesController'

        cls.__control_processes.append(process)
        process.start()

    @classmethod
    def start_control_option(cls, option_value: str):
        MyLogger.logger().info(f"Start controlling option: {option_value}")

        driver = GovDriver()

        cls.__drivers.append(driver)

        driver.control_option(option_value)

    @classmethod
    def join_all(cls):
        if len(cls.__control_processes) > 0:
            for process in cls.__control_processes:
                process.join()

            # return cls.join_all()

    @classmethod
    def kill_all_processes(cls):
        MyLogger.logger().info("Killing all processes.")

        for driver in cls.__drivers:
            driver.quit()

        for process in cls.__control_processes:
            process.kill()
