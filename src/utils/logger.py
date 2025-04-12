import logging
import sys


def setup_logger(name, level=logging.INFO):
    """
    Configures and returns a logger with a stream handler to stdout.
    """
    inner_logger = logging.getLogger(name)
    inner_logger.setLevel(level)

    if not inner_logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(level)
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%d.%m.%Y %H:%M'
        )
        handler.setFormatter(formatter)
        inner_logger.addHandler(handler)

    return inner_logger


# Create a default logger for the module.
logger = setup_logger(__name__)