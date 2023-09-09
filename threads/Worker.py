"""
Here are working functional, and creating thread
"""
from queue import Queue
from threading import Thread

from GovDriver import GovDriver
from logger import logger


class Worker(Thread):
    def __init__(self, queue: Queue):
        super().__init__(target=self.life_loop)

        self.queue = queue

    def life_loop(self):
        logger().info("Worker started.")

        driver = GovDriver()

        while True:
            ...
