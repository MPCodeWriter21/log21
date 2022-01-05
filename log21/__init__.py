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

__version__ = "1.5.2"
__author__ = "CodeWriter21 (Mehrad Pooryoussof)"
__github__ = "Https://GitHub.com/MPCodeWriter21/log21"
__all__ = ['ColorizingStreamHandler', 'DecolorizingFileHandler', 'ColorizingFormatter', 'DecolorizingFormatter',
           'get_logger', 'Logger', 'Colors', 'get_color', 'get_colors', 'CRITICAL', 'FATAL', 'ERROR', 'WARNING', 'WARN',
           'INFO', 'DEBUG', 'NOTSET', 'StreamHandler', 'ColorizingArgumentParser']

_manager = Manager()


def get_logger(name: str = '', level: _Union[int, str] = NOTSET, show_time: bool = True,
               show_level: bool = True, colorize_time_and_level: bool = True, fmt: str = None,
               datefmt: str = "%H:%M:%S", style: str = '%', handle_carriage_return: bool = True,
               handle_new_line: bool = True, override=False) -> Logger:
    """
    Returns a logging.Logger with colorizing support.
    >>>
    >>> import log21
    >>>
    >>> l = log21.get_logger()
    >>> l.warning('Pretty basic, huh?')
    [14:49:41] [WARNING] Pretty basic, huh?
    >>> l.critical('CONTINUE READING!! please...')
    [14:50:08] [CRITICAL] CONTINUE READING!! please...
    >>>
    >>> my_logger = log21.get_logger(name='CodeWriter21', level=log21.INFO, fmt='{asctime} -> [{levelname}]: {message}',
    ... style='{', override=True)
    >>>
    >>> my_logger.info('FYI: My name is Mehrad.')
    14:56:12 -> [INFO]: FYI: My name is Mehrad.
    >>> my_logger.error(log21.get_color('LightRed') + 'Oh no! Something went wrong D:')
    14:56:29 -> [ERROR]: Oh no! Something went wrong D:
    >>>
    >>> my_logger.debug(1 ,2 ,3)
    >>> # It prints Nothing because our logger level is INFO and DEBUG level is less than INFO.
    >>> # So let's modify the my_logger's level
    >>> my_logger.setLevel(log21.DEBUG)
    >>> # Now we try again...
    >>> my_logger.debug(1, 2, 3)
    14:57:34 -> [DEBUG]: 1 2 3
    >>> # Well Done. Right?
    >>> # Let's see more
    >>> my_logger.debug('I like %s number!', args=('21', ), end='\033[0m\n\n\n')
    15:01:43 -> [DEBUG]: I like 21 number!


    >>> # Well, I've got a question...
    >>> # Do you know the name of this color?
    >>> # #888888
    >>> # Oh ya! I can use get_color_name
    >>> log21.get_color_name('#888888')
    'gray'
    >>> # Oh thank you dear!
    >>> # Yes I knew that was grey -_- But I wanted to introduce my little friend ☺
    >>> # See you soon!
    >>>

    :param name: Optional[str]: The name of the logger
    :param level: Union[int, str] = logging.NOTSET: The logging level of the logger
    :param show_time: bool = True: Show the time in the log
    :param show_level: bool = True: Show the level of logging in the log
    :param fmt: Optional[str]: Custom formatting for the logger - overrides the default(show_time & show_level)
    :param datefmt: str = "%H:%M:%S": Custom date-time formatting for the logger
    :param style: str = '%': Use a style parameter of '%', '{' or '$' to specify that you want to use one of %-formatting,
        :meth:`str.format` (``{}``) formatting or :class:`string.Template` formatting in your format string.
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
            formatter = ColorizingFormatter(fmt, datefmt, style=style)
        else:
            formatter = _logging.Formatter(fmt, datefmt, style=style)
        # Defines the handler
        handler = ColorizingStreamHandler(handle_carriage_return=handle_carriage_return,
                                          handle_new_line=handle_new_line)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        _manager.addLogger(name, logger)
    return logger


def print(*msg, args: tuple = (), end='\033[0m\n', **kwargs):
    logger = get_logger('log21.print', level=DEBUG, show_time=False, show_level=False)
    logger.print(*msg, args=args, end=end, **kwargs)
