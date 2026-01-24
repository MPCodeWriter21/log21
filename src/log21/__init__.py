# log21.__init__.py
# CodeWriter21

# yapf: disable

import os as _os
import sys as _sys
import logging as _logging
from types import ModuleType as _ModuleType
from typing import (Type as _Type, Union as _Union, Literal as _Literal,
                    Mapping as _Mapping, Iterable as _Iterable, Optional as _Optional)

from . import crash_reporter
from .colors import (Colors, get_color, get_colors, ansi_escape, closest_color,
                     get_color_name)
from .levels import INFO, WARN, DEBUG, ERROR, FATAL, INPUT, NOTSET, WARNING, CRITICAL
from .logger import Logger
from .pprint import PrettyPrinter, pformat
from .manager import Manager
from .argparse import ColorizingArgumentParser
from .formatters import ColorizingFormatter, DecolorizingFormatter, _Formatter
from .tree_print import TreePrint, tree_format
from .argumentify import (ArgumentError, TooFewArgumentsError, RequiredArgumentError,
                          IncompatibleArgumentsError, argumentify)
from .file_handler import FileHandler, DecolorizingFileHandler
from .progress_bar import ProgressBar
from ._module_helper import FakeModule as _FakeModule
from .logging_window import LoggingWindow, LoggingWindowHandler
from .stream_handler import StreamHandler, ColorizingStreamHandler

# yapf: enable

__author__ = 'CodeWriter21 (Mehrad Pooryoussof)'
__version__ = '3.0.0'
__github__ = 'https://GitHub.com/MPCodeWriter21/log21'
__all__ = [
    'ColorizingStreamHandler', 'DecolorizingFileHandler', 'ColorizingFormatter',
    'DecolorizingFormatter', 'get_logger', 'Logger', 'Colors', 'get_color',
    'get_colors', 'CRITICAL', 'FATAL', 'ERROR', 'WARNING', 'WARN', 'INFO', 'DEBUG',
    'NOTSET', 'INPUT', 'StreamHandler', 'ColorizingArgumentParser', 'PrettyPrinter',
    'pformat', 'pprint', 'pretty_print', 'tree_format', 'TreePrint', 'Manager',
    'get_color_name', 'closest_color', 'ansi_escape', '__author__', '__github__',
    'debug', 'info', 'warning', 'warn', 'error', 'critical', 'fatal', 'exception',
    'log', 'basic_config', 'basicConfig', 'ProgressBar', 'LoggingWindow',
    'LoggingWindowHandler', 'get_logging_window', 'crash_reporter', 'console_reporter',
    'file_reporter', 'argumentify', 'ArgumentError', 'IncompatibleArgumentsError',
    'RequiredArgumentError', 'TooFewArgumentsError'
]

_manager = Manager()
_logging.setLoggerClass(Logger)


def _prepare_formatter(
    fmt: _Optional[str] = None,
    style: _Literal["%", "{", "$"] = "%",
    datefmt: str = '%H:%M:%S',
    show_level: bool = True,
    show_time: bool = True,
    colorize_time_and_level: bool = True,
    level_names: _Optional[_Mapping[int, str]] = None,
    level_colors: _Optional[_Mapping[int, tuple[str, ...]]] = None,
    formatter_class: _Type[_logging.Formatter] = ColorizingFormatter
) -> _logging.Formatter:
    # Prepares a formatting if the fmt was None
    if not fmt:
        style = '%'
        fmt = '%(message)s'
        if show_level:
            fmt = '[%(levelname)s] ' + fmt
        if show_time:
            fmt = '[%(asctime)s] ' + fmt
        fmt = '\r' + fmt

    if level_colors and not issubclass(formatter_class, ColorizingFormatter):
        warning(
            '`formatter_class` should be a subclass of ColorizingFormatter when used '
            'with level_colors.'
        )
        warning(
            f'Using `{formatter_class.__name__}` might lead to unexpected behaviour!'
        )

    # Defines the formatter
    if level_colors:
        formatter = formatter_class(
            fmt,
            datefmt,
            style=style,
            level_colors=level_colors  # type: ignore
        )
    else:
        formatter = formatter_class(fmt, datefmt, style=style)  # type: ignore

    if isinstance(formatter, _Formatter) and level_names:
        formatter.level_names = level_names
    if not colorize_time_and_level and isinstance(formatter, ColorizingFormatter):
        for key in formatter.level_colors:
            formatter.level_colors[key] = ()
        formatter.time_color = ()

    return formatter


def get_logger(
    name: str = '',
    level: _Union[int, str] = NOTSET,
    show_time: bool = True,
    show_level: bool = True,
    colorize_time_and_level: bool = True,
    fmt: _Optional[str] = None,
    datefmt: str = '%H:%M:%S',
    style: _Literal["%", "{", "$"] = '%',
    handle_carriage_return: bool = True,
    handle_new_line: bool = True,
    override: bool = False,
    level_names: _Optional[_Mapping[int, str]] = None,
    level_colors: _Optional[_Mapping[int, tuple[str, ...]]] = None,
    file: _Optional[_Union[_os.PathLike, str]] = None
) -> Logger:
    """Returns a logging.Logger with colorizing support.

    >>>
    >>> import log21
    >>>
    >>> l = log21.get_logger()
    >>> l.warning('Pretty basic, huh?')
    [14:49:41] [WARNING] Pretty basic, huh?
    >>> l.critical('CONTINUE READING!! please...')
    [14:50:08] [CRITICAL] CONTINUE READING!! please...
    >>>
    >>> my_logger = log21.get_logger(name='CodeWriter21', level=log21.INFO, ... fmt='{asctime} -> [{levelname}]: {message}', style='{', override=True)
    >>>
    >>> my_logger.info('FYI: My name is Mehrad.')
    14:56:12 -> [INFO]: FYI: My name is Mehrad.
    >>> my_logger.error(log21.get_color('LightRed') + 'Oh no! Something went wrong D:')
    14:56:29 -> [ERROR]: Oh no! Something went wrong D:
    >>>
    >>> my_logger.debug(1 ,2 ,3)
    >>> # It prints Nothing because our logger level is INFO and DEBUG level is lower
    >>> # than INFO.
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
    :param fmt: Optional[str]: Custom formatting for the logger - overrides the default
        (show_time & show_level)
    :param datefmt: str = "%H:%M:%S": Custom date-time formatting for the logger
    :param style: str = '%': Use a style parameter of '%', '{' or '$' to specify that
        you want to use one of %-formatting, :meth:`str.format` (``{}``) formatting or
        :class:`string.Template` formatting in your format string.
    :param colorize_time_and_level: bool = True: Colorizes the time and level using the
        default colors
    :param handle_carriage_return: bool = True: Adds a line of space characters to
        remove any text before the CR
    :param handle_new_line: bool = True: Places the NewLine characters at the beginning
        of the text before everything else
    :param override: bool = True: Overrides the logger attributes even if it already
        exists.
    :param level_names: Mapping[int, str] = None: You can specify custom level names.
    :param level_colors: Mapping[int, Tuple[str, ...]] = None: You can specify custom
        level colors.
    :param file: Union[os.PathLike, str] = None: The file to log to
    :return: log21.Logger
    """
    if not isinstance(name, str):
        raise TypeError('A logger name must be a string')
    logger = None
    if name:
        logger = _manager.getLogger(name)
    if (not logger) or override:
        logger = Logger(name, level)
        formatter = _prepare_formatter(
            fmt, style, datefmt, show_level, show_time, colorize_time_and_level,
            level_names, level_colors
        )

        # Defines the handler
        handler = ColorizingStreamHandler(
            handle_carriage_return=handle_carriage_return,
            handle_new_line=handle_new_line
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        if level_names:
            logger.add_levels(level_names, errors='ignore')
        _manager.addLogger(name, logger)

        if file:
            file_handler = FileHandler(file)
            file_formatter = _prepare_formatter(
                fmt,
                style,
                datefmt,
                show_level,
                show_time,
                False,
                level_names,
                formatter_class=DecolorizingFormatter
            )
            file_handler.setFormatter(file_formatter)
            logger.addHandler(file_handler)

    return logger  # ty: ignore[invalid-return-type]


def get_logging_window(
    name: str = '',
    level: _Union[int, str] = NOTSET,
    show_time: bool = True,
    show_level: bool = True,
    colorize_time_and_level: bool = True,
    fmt: _Optional[str] = None,
    datefmt: str = '%H:%M:%S',
    style: _Literal["%", "{", "$"] = '%',
    handle_carriage_return: bool = True,
    handle_new_line: bool = True,
    override: bool = False,
    level_names: _Optional[_Mapping[int, str]] = None,
    width: int = 80,
    height: int = 20,
    allow_shell: bool = False
) -> LoggingWindow:
    """Returns a logging window.

    >>> # Let's see how it works
    >>> # Imports log21 and time modules
    >>> import log21, time
    >>> # Creates a new LoggingWindow object
    >>> window = log21.get_logging_window('Test Window')
    >>> # Now use it without any additional steps to add handlers and formatters!
    >>> # It works just like a normal logger but with some extra features
    >>>
    >>> window.info('This works properly!')
    >>>
    >>> # You can use HEX colors as well as the ANSI colors which are supported by
    >>> # normal loggers
    >>> # ANSI colors usage:
    >>> window.info('This is a \033[91mred\033[0m message.')
    >>> window.info('\033[102mThis is a message with green background.')
    >>> # HEX colors usage:
    >>> window.info('\033#00FFFFhfThis is a message with cyan foreground.')
    >>> window.info('\033#0000FFhbThis is a message with blue background.')
    >>>
    >>> # Progressbar usage:
    >>> for i in range(100):
    ...     window.print_progress(i + 1, 100)
    ...     time.sleep(0.1)
    ...
    >>>
    >>> # Gettig input from the user:
    >>> name: str = window.input('Enter your name: ')
    >>> window.print('Hello, ' + name + '!')
    >>> # Run these lines to see the messages in the window
    >>>

    :param name: Optional[str]: The name of the logger
    :param level: Union[int, str] = logging.NOTSET: The logging level of the logger
    :param show_time: bool = True: Show the time in the log
    :param show_level: bool = True: Show the level of logging in the log
    :param fmt: Optional[str]: Custom formatting for the logger - overrides the default
        (show_time & show_level)
    :param datefmt: str = "%H:%M:%S": Custom date-time formatting for the logger
    :param style: str = '%': Use a style parameter of '%', '{' or '$' to specify that
        you want to use one of %-formatting, :meth:`str.format` (``{}``) formatting or
        :class:`string.Template` formatting in your format string.
    :param colorize_time_and_level: bool = True: Colorizes the time and level using the
        default colors
    :param handle_carriage_return: bool = True: Adds a line of space characters to
        remove any text before the CR
    :param handle_new_line: bool = True: Places the NewLine characters at the beginning
        of the text before everything else
    :param override: bool = True: Overrides the logger attributes even if it already
        exists
    :param level_names: Mapping[int, str] = None: You can specify custom level names.
    :param width: int = 80: The width of the window
    :param height: int = 20: The height of the window
    :param allow_shell: bool = False: Allow the user to use the shell
    :return: log21.LoggingWindow
    """
    if not isinstance(name, str):
        raise TypeError('A logger name must be a string')
    logging_window = None
    if name:
        logging_window = _manager.getLogger(name)
    if (not logging_window) or override:
        logging_window = LoggingWindow(
            name, level=level, width=width, height=height, allow_shell=allow_shell
        )
        formatter = _prepare_formatter(
            fmt, style, datefmt, show_level, show_time, colorize_time_and_level,
            level_names
        )

        # Defines the handler
        handler = LoggingWindowHandler(
            logging_window,
            handle_carriage_return=handle_carriage_return,
            handle_new_line=handle_new_line
        )
        handler.setFormatter(formatter)
        logging_window.addHandler(handler)
        _manager.addLogger(name, logging_window)
    return logging_window  # ty: ignore[invalid-return-type]


getLogger = get_logger


def print(  # pylint: disable=redefined-builtin
    *msg,
    args: tuple = (),
    end: str='\033[0m\n',
    **kwargs
) -> None:
    """Works like the print function but ANSI colors are supported (even on Windows) and
    it ends with a new line and a reset color by default."""
    logger = get_logger('log21.print', level=DEBUG, show_time=False, show_level=False)
    logger.print(*msg, args=args, end=end, **kwargs)


def input(  # pylint: disable=redefined-builtin
    *msg,
    args: tuple = (),
          end: str='',
    **kwargs
) -> str:
    """Works like the input function but ANSI colors are supported (even on Windows)."""
    logger = get_logger('log21.input', level=DEBUG, show_time=False, show_level=False)
    return logger.input(*msg, args=args, end=end, **kwargs)


def getpass(*msg, args: tuple = (), end: str = '', **kwargs) -> str:
    """Works like the getpass.getpass function but ANSI colors are supported (even on
    Windows)."""
    logger = get_logger('log21.getpass', level=DEBUG, show_time=False, show_level=False)
    return logger.getpass(*msg, args=args, end=end, **kwargs)


def pprint(
    obj,  # noqa: ANN001
    indent: int = 1,
    width: int = 80,
    depth: _Optional[int] = None,
    signs_colors: _Optional[_Mapping[str, str]] = None,
    *,
    sort_dicts: bool = True,
    underscore_numbers: bool = False,
    compact: bool = False,
    end: str = '\033[0m\n',
    **kwargs
) -> None:
    """A colorful version of the pprint.pprint function.

    :param obj: The object to print.
    :param indent: The amount of indentation to use.
    :param width: The maximum width in characters of the output.
    :param depth: The maximum depth to print nested structures. None means unlimited.
    :param signs_colors: A mapping that lets you specify the colors of the supported
        signs.
    :param sort_dicts: If True, dictionaries are sorted by key.
    :param underscore_numbers: If True, numbers are printed with an underscore between
        each group of three digits.
    :param compact: If True, lists and tuples are displayed on a single line.
    :param end: The string to append at the end of the output.
    :param kwargs: Additional keyword arguments passed to the Logger.print function.
    """
    logger = get_logger('log21.pprint', level=DEBUG, show_time=False, show_level=False)
    logger.print(
        pformat(
            obj=obj,
            indent=indent,
            width=width,
            depth=depth,
            signs_colors=signs_colors,
            compact=compact,
            sort_dicts=sort_dicts,
            underscore_numbers=underscore_numbers
        ),
        end=end,
        **kwargs
    )


pretty_print = pprint


def tree_print(
    obj,  # noqa: ANN001
    indent: int = 4,
    mode: _Literal['-', '='] = '-',
    colors: _Optional[_Mapping[str, str]] = None,
    end: str = '\033[0m\n',
    **kwargs
) -> None:
    """Prints a tree representation of the given object. (e.g. a dictionary)

    :param obj: The object to print.
    :param indent: The number of spaces to indent each level.
    :param mode: The mode to use for the tree. Can be '-' or '='.
    :param colors: A mapping that lets you customize the colors of branches and fruits.
    :param end: The string to append at the end of the output.
    :param kwargs: Additional keyword arguments passed to the Logger.print function.
    """
    logger = get_logger(
        'log21.tree_print', level=DEBUG, show_time=False, show_level=False
    )
    logger.print(
        tree_format(obj, indent=indent, mode=mode, colors=colors), end=end, **kwargs
    )


tprint = tree_print

root = Logger('root-logger', INFO)


def basic_config(
    force: bool = False,
    encoding: _Optional[str] = None,
    errors: _Optional[str] = 'backslashreplace',
    handlers: _Optional[_Iterable[_logging.Handler]] = None,
    stream=None,  # noqa: ANN001
    filename: _Optional[_Union[str, _os.PathLike]] = None,
    filemode: str = 'a',
    date_format: str = '%H:%M:%S',
    style: str = '%',
    format_: _Optional[str] = None,
    level: _Optional[_Union[int, str]] = None
) -> None:  # pylint: disable=too-many-branches
    """Do basic configuration for the logging system.

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
    if force:
        for handler in root.handlers[:]:
            root.removeHandler(handler)
            handler.close()
    if len(root.handlers) == 0:
        if handlers is None:
            if stream and filename:
                raise ValueError(
                    "'stream' and 'filename' should not be specified together"
                )
        elif stream or filename:
            raise ValueError(
                "'stream' or 'filename' should not be specified together with "
                "'handlers'"
            )
        if handlers is None:
            if filename:
                if 'b' in filemode:
                    errors = None
                else:
                    encoding = encoding or 'utf-8'
                handler = DecolorizingFileHandler(
                    filename, filemode, encoding=encoding, errors=errors
                )
            else:
                handler = ColorizingStreamHandler(stream=stream)
            handlers = [handler]
        if style not in '%{$':
            raise ValueError('Style must be one of: %, {, $')
        if not format_:
            format_ = {
                '%': '[%(asctime)s] [%(levelname)s] %(message)s',
                '{': '[{asctime}] [{levelname}] {message}',
                '$': '[${asctime}] [${levelname}] ${message}'
            }[style]
        formatter = ColorizingFormatter(format_, date_format, style=style)
        for handler in handlers:
            if handler.formatter is None:
                handler.setFormatter(formatter)
            root.addHandler(handler)
    if level is not None:
        root.setLevel(level)


basicConfig = basic_config


def critical(*msg, args: tuple = (), **kwargs) -> None:
    """Log a message with severity 'CRITICAL' on the root logger.

    If the logger has no handlers, call basicConfig() to add a console handler with a
    pre-defined format.
    """
    if len(root.handlers) == 0:
        basic_config()
    root.critical(*msg, args=args, **kwargs)


def fatal(*msg, args: tuple = (), **kwargs) -> None:
    """Don't use this function, use critical() instead."""
    critical(*msg, args=args, **kwargs)


def error(*msg, args: tuple = (), **kwargs) -> None:
    """Log a message with severity 'ERROR' on the root logger.

    If the logger has no handlers, call basicConfig() to add a console handler with a
    pre-defined format.
    """
    if len(root.handlers) == 0:
        basic_config()
    root.error(*msg, args=args, **kwargs)


def exception(*msg, args: tuple = (), exc_info: bool = True, **kwargs) -> None:
    """Log a message with severity 'ERROR' on the root logger, with exception
    information.

    If the logger has no handlers, basicConfig() is called to add a console handler with
    a pre-defined format.
    """
    error(*msg, args=args, exc_info=exc_info, **kwargs)


def warning(*msg, args: tuple = (), **kwargs) -> None:
    """Log a message with severity 'WARNING' on the root logger.

    If the logger has no handlers, call basicConfig() to add a console handler with a
    pre-defined format.
    """
    if len(root.handlers) == 0:
        basic_config()
    root.warning(*msg, args=args, **kwargs)


def warn(*msg, args: tuple = (), **kwargs) -> None:
    """An alias of warning()"""
    warning(*msg, args=args, **kwargs)


def info(*msg, args: tuple = (), **kwargs) -> None:
    """Log a message with severity 'INFO' on the root logger.

    If the logger has no handlers, call basicConfig() to add a console handler with a
    pre-defined format.
    """
    if len(root.handlers) == 0:
        basic_config()
    root.info(*msg, args=args, **kwargs)


def debug(*msg, args: tuple = (), **kwargs) -> None:
    """Log a message with severity 'DEBUG' on the root logger.

    If the logger has no handlers, call basicConfig() to add a console handler with a
    pre-defined format.
    """
    if len(root.handlers) == 0:
        basic_config()
    root.debug(*msg, args=args, **kwargs)


def log(level: int, *msg, args: tuple = (), **kwargs) -> None:
    """Log 'msg % args' with the integer severity 'level' on the root logger.

    If the logger has no handlers, call basicConfig() to add a console handler with a
    pre-defined format.
    """
    if len(root.handlers) == 0:
        basic_config()
    root.log(level, *msg, args=args, **kwargs)


endl = '\n'

console_reporter = crash_reporter.ConsoleReporter()


class _Module(_FakeModule):

    def __init__(self, real_module: _ModuleType) -> None:
        super().__init__(real_module, lambda: None)
        self.__file_reporter: _Optional[crash_reporter.FileReporter] = None

    @property
    def file_reporter(self) -> crash_reporter.FileReporter:
        if self.__file_reporter is None:
            self.__file_reporter = crash_reporter.FileReporter(file='.crash_report.log')
        return self.__file_reporter


_sys.modules[__name__] = _Module(_sys.modules[__name__])
