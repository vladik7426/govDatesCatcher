"""
The main start file of the project. This will start all the threads and control them.

Codes:
    201 - there are not clients to regiser in database
"""
import asyncio
import threading
from datetime import datetime
from queue import Queue
from time import sleep

import gdc_bot
from app.Controller import Controller
from app.DateCatchDriver import DateCatchDriver
from app.logger import MyLogger

"""
ГКУ в Торонто:
    Оформлення закордонного паспорта
    Оформлення закордонного паспорта дитині віком до 16 років
"""


async def main():
    MyLogger.init_logger()

    try:
        queue = Queue()

        Controller.init(queue)

        MyLogger.logger().info("Waiting for minutes to be equal 28 or 58")

        while True:
            minutes_str = datetime.now().time().strftime('%M')

            if minutes_str == '28' or minutes_str == '58':
                Controller.start_dates_catching()

            Controller.join_all()

            await asyncio.sleep(1)

    except Exception as e:
        MyLogger.logger().error(str(e))
        gdc_bot.send_error(str(e))

    finally:
        Controller.kill_all_processes()


if __name__ == '__main__':
    threading.Thread.name = 'Main'

    loop = asyncio.get_event_loop()
    loop.create_task(gdc_bot.start_telegram_log_bot())
    loop.run_until_complete(main())
