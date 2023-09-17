import logging
import logging.handlers
import queue
from datetime import datetime

logger = logging.getLogger('gdc.logging.root')

if not logger.hasHandlers():
    log_queue = queue.Queue(-1)
    queue_handler = logging.handlers.QueueHandler(log_queue)

    logger.setLevel(logging.DEBUG)
    logger.addHandler(queue_handler)

    fullFormatter = logging.Formatter("%(asctime)s %(threadName)s %(levelname)-8s %(message)s")
    simpleFormatter = logging.Formatter("%(levelname)-7s [%(threadName)s] %(message)s")

    fileHandler = logging.FileHandler(f"logs/{datetime.now().strftime('%Y.%m.%d')}.log")
    fileHandler.setFormatter(fullFormatter)
    fileHandler.setLevel(logging.DEBUG)

    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(simpleFormatter)
    consoleHandler.setLevel(logging.DEBUG)

    listener = logging.handlers.QueueListener(log_queue, consoleHandler, fileHandler)
    listener.start()

    logger.debug("Debug mode enabled.")
