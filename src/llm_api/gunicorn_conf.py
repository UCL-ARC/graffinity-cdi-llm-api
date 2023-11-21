"""Define Gunicorn config."""
bind = "0.0.0.0:8000"

# Worker class
worker_class = "uvicorn.workers.UvicornWorker"

# Number of workers
workers = 4

# threads per worker
threads = 1

enable_stdio_inheritance = True

logconfig_dict = {
    "version": 1,
    "disable_existing_loggers": False,
    "loggers": {
        "root": {
            "level": "INFO",
            "handlers": ["console"],
        },
        "gunicorn": {
            "level": "INFO",
            "handlers": ["console"],
            "propagate": False,
        },
    },
}
