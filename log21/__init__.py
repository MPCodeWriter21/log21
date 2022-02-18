# log21.__init__.py
# CodeWriter21

import io as _io

from typing import Union as _Union, Dict as _Dict

from log21.Levels import *
from log21.Logger import Logger
from log21.Manager import Manager
from log21.PPrint import PrettyPrinter, pformat
from log21.TreePrint import TreePrint, tree_format
from log21.Argparse import ColorizingArgumentParser
from log21.FileHandler import DecolorizingFileHandler
from log21.StreamHandler import ColorizingStreamHandler, StreamHandler
from log21.Formatters import ColorizingFormatter, DecolorizingFormatter
from log21.Colors import Colors, get_color, get_colors, ansi_esc, get_color_name, closest_color

__version__ = "1.5.8"
__author__ = "CodeWriter21 (Mehrad Pooryoussof)"
__github__ = "Https://GitHub.com/MPCodeWriter21/log21"
__all__ = ['ColorizingStreamHandler', 'DecolorizingFileHandler', 'ColorizingFormatter', 'DecolorizingFormatter',
           'get_logger', 'Logger', 'Colors', 'get_color', 'get_colors', 'CRITICAL', 'FATAL', 'ERROR', 'WARNING', 'WARN',
           'INFO', 'DEBUG', 'NOTSET', 'StreamHandler', 'ColorizingArgumentParser', 'PrettyPrinter', 'pformat',
           'pprint', 'pretty_print']

_manager = Manager()


def get_logger(name: str = '', level: _Union[int, str] = NOTSET, show_time: bool = True,
               show_level: bool = True, colorize_time_and_level: bool = True, fmt: str = None,
               datefmt: str = "%H:%M:%S", style: str = '%', handle_carriage_return: bool = True,
               handle_new_line: bool = True, override=False, level_names: _Dict[int, str] = None) -> Logger:
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
    :param level_names: Dict[int, str] = None: You can specify custom level names.
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
        formatter = ColorizingFormatter(fmt, datefmt, style=style, level_names=level_names)
        if not colorize_time_and_level:
            for key in formatter.level_colors:
                formatter.level_colors[key] = tuple()
            formatter.time_color = tuple()

        # Defines the handler
        handler = ColorizingStreamHandler(handle_carriage_return=handle_carriage_return,
                                          handle_new_line=handle_new_line)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        _manager.addLogger(name, logger)
    return logger


getLogger = get_logger


def print(*msg, args: tuple = (), end='\033[0m\n', **kwargs):
    logger = get_logger('log21.print', level=DEBUG, show_time=False, show_level=False)
    logger.print(*msg, args=args, end=end, **kwargs)


def pprint(obj, indent=1, width=80, depth=None, signs_colors: _Dict[str, str] = None, *, compact=False, sort_dicts=True,
           underscore_numbers=False, end='\033[0m\n', **kwargs):
    logger = get_logger('log21.pprint', level=DEBUG, show_time=False, show_level=False)
    logger.print(pformat(obj=obj, indent=indent, width=width, depth=depth, signs_colors=signs_colors, compact=compact,
                         sort_dicts=sort_dicts, underscore_numbers=underscore_numbers), end=end, **kwargs)


pretty_print = pprint


def tree_print(obj, indent: int = 4, mode='-', colors: _Dict[str, str] = None, end='\033[0m\n', **kwargs):
    logger = get_logger('log21.tree_print', level=DEBUG, show_time=False, show_level=False)
    logger.print(tree_format(obj, indent=indent, mode=mode, colors=colors), end=end, **kwargs)


tprint = tree_print

root = Logger('root-logger', INFO)


def basic_config(**kwargs):
    """
    Do basic configuration for the logging system.

    This function does nothing if the root logger already has handlers
    configured, unless the keyword argument *force* is set to ``True``.
    It is a convenience method intended for use by simple scripts
    to do one-shot configuration of the logging package.

    The default behaviour is to create a ColorizingStreamHandler which writes to
    sys.stderr, set a formatter using the BASIC_FORMAT format string, and
    add the handler to the root logger.

    A number of optional keyword arguments may be specified, which can alter
    the default behaviour.

    filename  Specifies that a FileHandler be created, using the specified
              filename, rather than a StreamHandler.
    filemode  Specifies the mode to open the file, if filename is specified
              (if filemode is unspecified, it defaults to 'a').
    format    Use the specified format string for the handler.
    datefmt   Use the specified date/time format.
    style     If a format string is specified, use this to specify the
              type of format string (possible values '%', '{', '$', for
              %-formatting, :meth:`str.format` and :class:`string.Template`
              - defaults to '%').
    level     Set the root logger level to the specified level.
    stream    Use the specified stream to initialize the StreamHandler. Note
              that this argument is incompatible with 'filename' - if both
              are present, 'stream' is ignored.
    handlers  If specified, this should be an iterable of already created
              handlers, which will be added to the root handler. Any handler
              in the list which does not have a formatter assigned will be
              assigned the formatter created in this function.
    force     If this keyword  is specified as true, any existing handlers
              attached to the root logger are removed and closed, before
              carrying out the configuration as specified by the other
              arguments.
    encoding  If specified together with a filename, this encoding is passed to
              the created FileHandler, causing it to be used when the file is
              opened.
    errors    If specified together with a filename, this value is passed to the
              created FileHandler, causing it to be used when the file is
              opened in text mode. If not specified, the default value is
              `backslashreplace`.

    Note that you could specify a stream created using open(filename, mode)
    rather than passing the filename and mode in. However, it should be
    remembered that StreamHandler does not close its stream (since it may be
    using sys.stdout or sys.stderr), whereas FileHandler closes its stream
    when the handler is closed.
    """
    force = kwargs.pop('force', False)
    encoding = kwargs.pop('encoding', None)
    errors = kwargs.pop('errors', 'backslashreplace')
    if force:
        for handler in root.handlers[:]:
            root.removeHandler(handler)
            handler.close()
    if len(root.handlers) == 0:
        handlers = kwargs.pop("handlers", None)
        if handlers is None:
            if "stream" in kwargs and "filename" in kwargs:
                raise ValueError("'stream' and 'filename' should not be specified together")
        else:
            if "stream" in kwargs or "filename" in kwargs:
                raise ValueError("'stream' or 'filename' should not be specified together with 'handlers'")
        if handlers is None:
            filename = kwargs.pop("filename", None)
            mode = kwargs.pop("filemode", 'a')
            if filename:
                if 'b' in mode:
                    errors = None
                else:
                    encoding = _io.text_encoding(encoding)
                handler = DecolorizingFileHandler(filename, mode, encoding=encoding, errors=errors)
            else:
                stream = kwargs.pop("stream", None)
                handler = ColorizingStreamHandler(stream=stream)
            handlers = [handler]
        date_format = kwargs.pop("datefmt", "%H:%M:%S")
        style = kwargs.pop("style", '%')
        if style not in '%{$':
            raise ValueError('Style must be one of: %, {, $')
        format_ = kwargs.pop("format", {'%': '[%(asctime)s] [%(levelname)s] %(message)s',
                                        '{': '[{asctime}] [{levelname}] {message}',
                                        '$': '[${asctime}] [${levelname}] ${message}'}[style])
        formatter = ColorizingFormatter(format_, date_format, style=style)
        for handler in handlers:
            if handler.formatter is None:
                handler.setFormatter(formatter)
            root.addHandler(handler)
        level = kwargs.pop("level", None)
        if level is not None:
            root.setLevel(level)
        if kwargs:
            keys = ', '.join(kwargs.keys())
            raise ValueError('Unrecognised argument(s): %s' % keys)


basicConfig = basic_config


def critical(*msg, args=(), **kwargs):
    """
    Log a message with severity 'CRITICAL' on the root logger. If the logger has no handlers, call basicConfig() to add
    a console handler with a pre-defined format.
    """
    if len(root.handlers) == 0:
        basic_config()
    root.critical(*msg, args=args, **kwargs)


def fatal(*msg, args=(), **kwargs):
    """
    Don't use this function, use critical() instead.
    """
    critical(*msg, args=args, **kwargs)


def error(*msg, args=(), **kwargs):
    """
    Log a message with severity 'ERROR' on the root logger. If the logger has no handlers, call basicConfig() to add a
    console handler with a pre-defined format.
    """
    if len(root.handlers) == 0:
        basic_config()
    root.error(*msg, args=args, **kwargs)


def exception(*msg, args=(), exc_info=True, **kwargs):
    """
    Log a message with severity 'ERROR' on the root logger, with exception information. If the logger has no handlers,
    basicConfig() is called to add a console handler with a pre-defined format.
    """
    error(*msg, args=args, exc_info=exc_info, **kwargs)


def warning(*msg, args=(), **kwargs):
    """
    Log a message with severity 'WARNING' on the root logger. If the logger has no handlers, call basicConfig() to add
    a console handler with a pre-defined format.
    """
    if len(root.handlers) == 0:
        basic_config()
    root.warning(*msg, args=args, **kwargs)


def warn(*msg, args=(), **kwargs):
    warning(*msg, args=args, **kwargs)


def info(*msg, args=(), **kwargs):
    """
    Log a message with severity 'INFO' on the root logger. If the logger has no handlers, call basicConfig() to add a
    console handler with a pre-defined format.
    """
    if len(root.handlers) == 0:
        basic_config()
    root.info(*msg, args=args, **kwargs)


def debug(*msg, args=(), **kwargs):
    """
    Log a message with severity 'DEBUG' on the root logger. If the logger has no handlers, call basicConfig() to add a
    console handler with a pre-defined format.
    """
    if len(root.handlers) == 0:
        basic_config()
    root.debug(*msg, args=args, **kwargs)


def log(level, *msg, args=(), **kwargs):
    """
    Log 'msg % args' with the integer severity 'level' on the root logger. If the logger has no handlers, call
    basicConfig() to add a console handler with a pre-defined format.
    """
    if len(root.handlers) == 0:
        basic_config()
    root.log(level, *msg, args=args, **kwargs)
