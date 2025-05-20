import logging
import sys
from typing import Optional


def get_logger(name: Optional[str] = None, level: int = logging.INFO) -> logging.Logger:
    """
    Returns a configured logger instance with a consistent format.

    Args:
        name (str, optional): Name of the logger. Defaults to root logger.
        level (int): Logging level. Default is logging.INFO.

    Returns:
        logging.Logger: Configured logger.
    """
    logger = logging.getLogger(name)

    # Avoid adding multiple handlers to the same logger
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(level)
        logger.propagate = False

    return logger
