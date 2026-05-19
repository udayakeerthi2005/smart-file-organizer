import os
import logging

from config.settings import LOG_FILE_PATH


def setup_logger():
    log_folder = os.path.dirname(LOG_FILE_PATH)

    if log_folder:
        os.makedirs(log_folder, exist_ok=True)

    logging.basicConfig(
        filename=LOG_FILE_PATH,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )


def log_info(message):
    logging.info(message)


def log_error(message):
    logging.error(message)