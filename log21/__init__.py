# __init__.py

import logging as _logging
from typing import Union as _Union
from log21.Levels import *
from log21.StreamHandler import ColorizingStreamHandler
from log21.Formatter import ColorizingFormatter
from log21.Logger import Logger
from log21.Colors import Colors, get_color, get_colors

__version__ = "1.2.0"
__all__ = ['ColorizingStreamHandler', 'get_logger', 'Logger', 'Colors', 'get_color', 'get_colors', 'CRITICAL', 'FATAL', 'ERROR',
           'WARNING', 'WARN', 'INFO', 'DEBUG', 'NOTSET', '__version__']


def get_logger(name: str = None, level: _Union[int, str] = NOTSET, show_time: bool = True,
               show_level: bool = True, colorize_time_and_level: bool = True, fmt: str = None) -> _logging.Logger:
    """
    Returns a logging.Logger with colorizing support.

    :param name: Optional[str]: The name of the logger
    :param level: Union[int, str] = logging.NOTSET: The logging level of the logger
    :param show_time: bool = True: Show the time in the log
    :param show_level: bool = True: Show the level of logging in the log
    :param fmt: Optional[str]: Custom formatting for the logger - overrides the default(show_time & show_level)
    :param colorize_time_and_level: bool = True: Colorizes the time and level using the default colors
    :return: logging.Logger

    """
    # Prepares a formatting if the fmt was None
    if not fmt:
        fmt = "%(message)s"
        if show_level:
            fmt = "[%(levelname)s] " + fmt
        if show_time:
            fmt = "[%(asctime)s] " + fmt
        fmt = '\r' + fmt
    # Defines the formatter
    if colorize_time_and_level:
        formatter = ColorizingFormatter(fmt, "%H:%M:%S")
    else:
        formatter = _logging.Formatter(fmt, "%H:%M:%S")
    # Defines the handler
    handler = ColorizingStreamHandler()
    handler.setFormatter(formatter)
    logger = Logger(name, level)
    logger.addHandler(handler)
    return logger
