"""
The main start file of the project. This will start all the threads and control them.

Codes:
    201 - there are not clients to regiser in database
"""
import asyncio
import threading
from datetime import datetime
from queue import Queue

from gdc.Controller import Controller
from gdc.logger import logger

"""
ГКУ в Торонто:
    Оформлення закордонного паспорта
    Оформлення закордонного паспорта дитині віком до 16 років
"""


async def main():
    try:
        Controller.init(Queue())

        logger.debug("Starting main loop..")

        while True:
            # minutes_str = datetime.now().time().strftime('%H:%M')
            minutes_str = datetime.now().time().strftime('%M')

#             if minutes_str == '02:57':
            if minutes_str == '57':
                logger.debug(f"Time: {minutes_str}. Starting driver..")
                Controller.start_dates_catching()

            Controller.join_all()

            await asyncio.sleep(1)

    except Exception as e:
        logger.exception("An error occurred when in main loop:")

    finally:
        Controller.kill_all_processes()


if __name__ == '__main__':
    threading.Thread.name = 'MainThread'

    asyncio.run(main())
