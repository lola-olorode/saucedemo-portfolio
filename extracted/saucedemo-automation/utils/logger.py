"""Custom logging wrapper.

Wraps the standard logging module so every test run produces a
timestamped log file (useful for debugging CI failures after the fact)
in addition to console output during local runs.
"""

import logging
import os
from datetime import datetime

LOG_DIR = "reports/logs"


def get_logger(name: str) -> logging.Logger:
    os.makedirs(LOG_DIR, exist_ok=True)

    logger = logging.getLogger(name)
    if logger.handlers:
        # Avoid attaching duplicate handlers if get_logger() is called
        # more than once for the same name (e.g. across test modules).
        return logger

    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%H:%M:%S",
    )

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    run_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_handler = logging.FileHandler(f"{LOG_DIR}/run_{run_timestamp}.log")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger
