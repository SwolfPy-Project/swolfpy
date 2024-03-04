import sys

from loguru import logger


def setup_logging(log_level: str = "INFO"):
    """
    Setup logging configuration.
    """
    logger.remove()
    logger.add(sys.stderr, level=log_level)
    logger.add("swolfpy-{time}.log", level=log_level)
    logger.debug("Logging configured")
    return logger
