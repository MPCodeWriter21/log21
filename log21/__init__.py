# log21.__init__.py
# CodeWriter21

import logging as _logging
from typing import Union as _Union
from log21.Levels import *
from log21.Logger import Logger
from log21.Manager import Manager
from log21.Argparse import ColorizingArgumentParser
from log21.FileHandler import DecolorizingFileHandler
from log21.StreamHandler import ColorizingStreamHandler, StreamHandler
from log21.Formatters import ColorizingFormatter, DecolorizingFormatter
from log21.Colors import Colors, get_color, get_colors, ansi_esc, get_color_name, closest_color

__version__ = "1.4.8"
__author__ = "CodeWriter21 (Mehrad Pooryoussof)"
__github__ = "Https://GitHub.com/MPCodeWriter21/log21"
__all__ = ['ColorizingStreamHandler', 'DecolorizingFileHandler', 'ColorizingFormatter', 'DecolorizingFormatter',
           'get_logger', 'Logger', 'Colors', 'get_color', 'get_colors', 'CRITICAL', 'FATAL', 'ERROR', 'WARNING', 'WARN',
           'INFO', 'DEBUG', 'NOTSET', 'StreamHandler', 'ColorizingArgumentParser']

_manager = Manager()


def get_logger(name: str = None, level: _Union[int, str] = NOTSET, show_time: bool = True,
               show_level: bool = True, colorize_time_and_level: bool = True, fmt: str = None,
               handle_carriage_return: bool = True, handle_new_line: bool = True, override=False) -> Logger:
    """
    Returns a logging.Logger with colorizing support.

    :param name: Optional[str]: The name of the logger
    :param level: Union[int, str] = logging.NOTSET: The logging level of the logger
    :param show_time: bool = True: Show the time in the log
    :param show_level: bool = True: Show the level of logging in the log
    :param fmt: Optional[str]: Custom formatting for the logger - overrides the default(show_time & show_level)
    :param colorize_time_and_level: bool = True: Colorizes the time and level using the default colors
    :param handle_carriage_return: bool = True: Adds a line of space characters to remove any text before the CR
    :param handle_new_line: bool = True: Places the NewLine characters at the beginning of the text before everything else
    :param override: bool = True: Overrides the logger attributes even if it already exists
    :return: logging.Logger

    """
    if not isinstance(name, str):
        raise TypeError('A logger name must be a string')
    logger = None
    if name:
        logger = _manager.getLogger(name)
    if (not logger) or override:
        logger = Logger(name, level)
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
        handler = ColorizingStreamHandler(handle_carriage_return=handle_carriage_return,
                                          handle_new_line=handle_new_line)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        _manager.addLogger(name, logger)
    return logger
