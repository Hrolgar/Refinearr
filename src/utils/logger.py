# utils/logger.py
import logging
import sys
from src.utils.color_formatter import ColorFormatter


def setup_logger(name, level=logging.INFO, service_name="", color: str = None):
    """
    Configures and returns a logger with a stream handler that uses the ColorFormatter.

    :param name: The logger name.
    :param level: The logging level.
    :param service_name: The service name to include in the log output.
    :param color: The color name (e.g., 'red', 'blue') to color the whole log message.
    :return: Configured logger instance.
    """
    inner_logger = logging.getLogger(name)
    inner_logger.setLevel(level)

    # Add handler only once.
    if not inner_logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(level)
        formatter = ColorFormatter(
            datefmt='%d.%m.%Y %H:%M',
            service_name=service_name,
            color=color
        )
        handler.setFormatter(formatter)
        inner_logger.addHandler(handler)

    return inner_logger


# Create a default logger for the module (without service name/color).
logger = setup_logger(__name__)
