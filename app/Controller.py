"""
Here are thread controlling functional
"""
import asyncio
import sys
from multiprocessing import Process
from queue import Queue
from threading import Thread

import gdc_bot
from app.DateCatchDriver import DateCatchDriver
from app.logger import MyLogger
from gdc_database import db_clients
from gdc_database.db_clients import DataClient


class Controller:
    __dates_catcher_processes: list[Process] = []
    __drivers: list[DateCatchDriver] = []

    @classmethod
    def init(cls, queue: Queue):
        cls.queue = queue

    @classmethod
    def start_dates_catching(cls):
        dates_catcher_process = Process(target=cls._dates_catcher_process_handler)
        dates_catcher_process.name = f"DatesCatcherProcess-{len(cls.__dates_catcher_processes)}"

        cls.__dates_catcher_processes.append(dates_catcher_process)

        dates_catcher_process.start()

    @classmethod
    def _dates_catcher_process_handler(cls):
        unreg_clients = db_clients.get_unreg_clients()
        if len(unreg_clients) > 0:
            driver = DateCatchDriver()
            cls.__drivers.append(driver)

            for client in unreg_clients:
                if cls.__start_catching_for_client(client, driver):
                    continue
                else:
                    break
        else:
            sys.exit(201)

    @classmethod
    def __start_catching_for_client(cls, client: DataClient, driver: DateCatchDriver) -> bool:
        driver.set_basic_inputs_values(client.consulate)

        gdc_bot.send_info(f"Ловимо дату для {client.name}({client.consulate}, {client.category})")

        if driver.catch_date_for_client(client):
            gdc_bot.send_alert(f"Підтвердіть злапану дату для {client.name}({client.consulate}, {client.category})!\n"
                               f"Пошта: {client.email}")
            return True
        else:
            gdc_bot.send_info(f"Не вийшло злапати дату для {client.name}({client.consulate}, {client.category}) :(")
            return False

    @classmethod
    def join_all(cls):
        if len(cls.__dates_catcher_processes) > 0:
            for process in cls.__dates_catcher_processes:
                process.join()

            # return cls.join_all()

    @classmethod
    def kill_all_processes(cls):
        MyLogger.logger().info("Killing all processes.")

        for driver in cls.__drivers:
            driver.quit()

        for process in cls.__dates_catcher_processes:
            process.kill()
