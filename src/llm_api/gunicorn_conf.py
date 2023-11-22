# ruff: noqa
"""Define Gunicorn config."""

import logging
import multiprocessing
import sys

from loguru import logger

bind = "0.0.0.0:8000"

# Worker class
worker_class = "uvicorn.workers.UvicornWorker"

# Number of workers recommended by Gunicorn docs
workers = multiprocessing.cpu_count() * 2 + 1

# threads per worker
threads = 1

logging_level = "INFO"


class InterceptHandler(logging.Handler):
    def emit(self, record):
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame = logging.currentframe()
        depth = 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


# Replace Gunicorn loggers with Loguru logger
gunicorn_logger = logging.getLogger("gunicorn.error")
gunicorn_logger.handlers = [InterceptHandler()]
gunicorn_logger.propagate = False

access_logger = logging.getLogger("gunicorn.access")
access_logger.handlers = [InterceptHandler()]
access_logger.propagate = False

# Remove any other loggers handled by loguru to eliminate duplicate logging
logger.remove()
# Add the desired logs in the desired format, at the desired level
logger.add(sys.stderr, format="{time} {level} {message}", level=logging_level)


def when_ready(server):
    logger.info("Server ready. Spawning workers.")


def on_starting(server):
    logger.info("Starting Gunicorn.")


def on_exit(server):
    logger.info("Server shutting down.")
