"""Define Gunicorn config."""

from loguru import logger
import logging
import sys
import multiprocessing

bind = "0.0.0.0:8000"

# Worker class
worker_class = "uvicorn.workers.UvicornWorker"

# Number of workers recommended by Gunicorn docs
workers = multiprocessing.cpu_count() * 2 + 1

# threads per worker
threads = 1

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

# Replace Gunicorn loggers with Loguru
gunicorn_logger = logging.getLogger('gunicorn.error')
gunicorn_logger.handlers = [InterceptHandler()]
gunicorn_logger.propagate = False

access_logger = logging.getLogger('gunicorn.access')
access_logger.handlers = [InterceptHandler()]
access_logger.propagate = False

logger.add(sys.stderr, format="{time} {level} {message}", level="INFO")

def when_ready(server):
    logger.info("Server ready. Spawning workers.")

def on_starting(server):
    logger.info("Starting Gunicorn.")

def on_exit(server):
    logger.info("Server shutting down.")

raw_env = [
    "GUNICORN_CMD_ARGS=--access-logformat=%(h)s %(l)s %(u)s %(t)s '%(r)s' %(s)s %(b)s '%(f)s' '%(a)s'",
]
