import logging
import sys

def setup_logger(name, level=logging.INFO):
    """
    Configures and returns a logger with a stream handler to stdout.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(level)
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%d.%m.%Y T %H:%M'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    return logger

# Create a default logger for the module.
logger = setup_logger(__name__)
