import os

from loguru import logger

log_file = os.path.join(os.path.dirname(__file__), "../../log/app_{time}.log")
logger.add(log_file, enqueue=True, rotation="12 hours", level="DEBUG", format="{time} - {level} - {message} - "
                                                                              "in function: {function} - File: {file}")