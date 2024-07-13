import logging
import sys


def setup_logger(level: str = "INFO"):
    # Remove any existing handlers to avoid duplicates
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    # Set up root logger
    logger = logging.getLogger()
    logger.setLevel(level)
    ch = logging.StreamHandler(stream=sys.stdout)
    ch.setLevel(level)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    # Configure uvicorn loggers separately
    uvicorn_logger = logging.getLogger("uvicorn")
    uvicorn_logger.handlers = [ch]
    uvicorn_logger.propagate = False

    return logger
