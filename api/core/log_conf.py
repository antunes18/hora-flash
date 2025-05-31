import logging
import sys, os
from logging.handlers import RotatingFileHandler
from datetime import datetime, timezone

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)


logger = logging.getLogger()

formatter = logging.Formatter(
    fmt=f"{datetime.strftime(datetime.now(timezone.utc), '%d/%m/%Y %H:%M:%S')} UTC - %(levelname)s - %(message)s"
)

stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(formatter)

file_handler = logging.FileHandler("app.log")
file_handler.setFormatter(formatter)

## ERROR  Logger
error_handler = RotatingFileHandler(
    f"{LOG_DIR}/error.log", maxBytes=5_000_000, backupCount=5
)
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(formatter)


# Add Handler to the logger
logger.handlers = [stream_handler, file_handler, error_handler]


# set logger level
logger.setLevel(logging.INFO)
