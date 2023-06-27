# log21.Formatters.py
# CodeWriter21

import time as _time
from logging import Formatter as __Formatter
from typing import Mapping as _Mapping, Tuple as _Tuple, Dict as _Dict, Optional as _Optional
from log21.Colors import get_colors as _gc, ansi_escape
from log21.Levels import INPUT, CRITICAL, ERROR, WARNING, INFO, DEBUG, PRINT

__all__ = ['ColorizingFormatter', 'DecolorizingFormatter']


class _Formatter(__Formatter):
    def __init__(self, fmt: _Optional[str] = None, datefmt: _Optional[str] = None, style: str = '%',
                 level_names: _Optional[_Mapping[int, str]] = None):
        """
        `level_names` usage:
        >>> import log21
        >>> logger = log21.Logger('MyLogger', log21.DEBUG)
        >>> stream_handler = log21.ColorizingStreamHandler()
        >>> formatter = log21.ColorizingFormatter(fmt='[%(levelname)s] %(message)s',
        ...             level_names={log21.DEBUG: ' ', log21.INFO: '+', log21.WARNING: '-', log21.ERROR: '!',
        ...                          log21.CRITICAL: 'X'})
        >>> stream_handler.setFormatter(formatter)
        >>> logger.addHandler(stream_handler)
        >>>
        >>> logger.debug('Just wanna see if this works...')
        [ ] Just wanna see if this works...
        >>> logger.info("FYI: I'm glad somebody read this 8)")
        [+] FYI: I'm glad somebody read this 8)
        >>> logger.warning("Oh no! Something's gonna happen!")
        [-] Oh no! something's gonna happen!
        >>> logger.error('AN ERROR OCCURRED! (told ya ;))')
        [!] AN ERROR OCCURRED! (told ya ;))
        >>> logger.critical('Crashed....')
        [X] Crashed....
        >>>
        >>> # Hope you've enjoyed
        >>>
        """
        super().__init__(fmt=fmt, datefmt=datefmt, style=style)

        self._level_names: _Dict[int, str] = {
            DEBUG: 'DEBUG',
            INFO: 'INFO',
            WARNING: 'WARNING',
            ERROR: 'ERROR',
            CRITICAL: 'CRITICAL',
            PRINT: 'PRINT',
            INPUT: 'INPUT'
        }

        if level_names:
            for level, name in level_names.items():
                self.level_names[level] = name

    @property
    def level_names(self):
        return self._level_names

    @level_names.setter
    def level_names(self, level_names: _Mapping[int, str]):
        if level_names:
            if not isinstance(level_names, _Mapping):
                raise TypeError('`level_names` must be a Mapping, a dictionary like object!')
            self._level_names = level_names
        else:
            self._level_names = dict()

    def format(self, record) -> str:
        record.message = record.getMessage()
        if self.usesTime():
            record.asctime = self.formatTime(record, self.datefmt)

        record.levelname = self.level_names.get(record.levelno, 'NOTSET')

        s = self.formatMessage(record)
        if record.exc_info:
            if not record.exc_text:
                record.exc_text = self.formatException(record.exc_info)
        if record.exc_text:
            if s[-1:] != "\n":
                s = s + "\n"
            s = s + record.exc_text
        if record.stack_info:
            if s[-1:] != "\n":
                s = s + "\n"
            s = s + self.formatStack(record.stack_info)
        return s


class ColorizingFormatter(_Formatter):
    time_color: _Tuple[str, ...] = ('lightblue',)
    name_color = pathname_color = filename_color = module_color = func_name_color = thread_name_color = \
        message_color = tuple()

    def __init__(self, fmt: _Optional[str] = None, datefmt: _Optional[str] = None, style: str = '%',
                 level_names: _Optional[_Mapping[int, str]] = None,
                 level_colors: _Optional[_Mapping[int, _Tuple[str]]] = None,
                 time_color: _Optional[_Tuple[str, ...]] = None, name_color: _Optional[_Tuple[str, ...]] = None,
                 pathname_color: _Optional[_Tuple[str, ...]] = None, filename_color: _Optional[_Tuple[str, ...]] = None,
                 module_color: _Optional[_Tuple[str, ...]] = None, func_name_color: _Optional[_Tuple[str, ...]] = None,
                 thread_name_color: _Optional[_Tuple[str, ...]] = None,
                 message_color: _Optional[_Tuple[str, ...]] = None):
        super().__init__(fmt=fmt, datefmt=datefmt, style=style, level_names=level_names)
        self.level_colors: _Dict[int, _Tuple[str, ...]] = {
            DEBUG: ('lightblue',),
            INFO: ('green',),
            WARNING: ('lightyellow',),
            ERROR: ('light red',),
            CRITICAL: ('background red', 'white'),
            PRINT: ('Cyan',),
            INPUT: ('Magenta',)
        }
        # Checks and sets colors
        if level_colors:
            if not isinstance(level_colors, _Mapping):
                raise TypeError('`level_colors` must be a dictionary like object!')
            for level, color in level_colors.items():
                self.level_colors[level] = (_gc(*color),)
        if time_color:
            if not isinstance(time_color, tuple):
                raise TypeError('`time_color` must be a tuple!')
            self.time_color = time_color
        if name_color:
            if not isinstance(name_color, tuple):
                raise TypeError('`name_color` must be a tuple!')
            self.name_color = name_color
        if pathname_color:
            if not isinstance(pathname_color, tuple):
                raise TypeError('`pathname_color` must be a tuple!')
            self.pathname_color = pathname_color
        if filename_color:
            if not isinstance(filename_color, tuple):
                raise TypeError('`filename_color` must be a tuple!')
            self.filename_color = filename_color
        if module_color:
            if not isinstance(module_color, tuple):
                raise TypeError('`module_color` must be a tuple!')
            self.module_color = module_color
        if func_name_color:
            if not isinstance(func_name_color, tuple):
                raise TypeError('`func_name_color` must be a tuple!')
            self.func_name_color = func_name_color
        if thread_name_color:
            if not isinstance(thread_name_color, tuple):
                raise TypeError('`thread_name_color` must be a tuple!')
            self.thread_name_color = thread_name_color
        if message_color:
            if not isinstance(message_color, tuple):
                raise TypeError('`message_color` must be a tuple!')
            self.message_color = message_color

    def format(self, record) -> str:
        """
        Colorizes the record and returns the formatted message.

        :param record:
        :return: str
        """
        record.message = record.getMessage()
        if self.usesTime():
            record.asctime = self.formatTime(record, self.datefmt)

        record.levelname = self.level_names.get(record.levelno, 'NOTSET')

        record = self.colorize(record)

        s = self.formatMessage(record)
        if record.exc_info:
            # Cache the traceback text to avoid converting it multiple times
            # (it's constant anyway)
            if not record.exc_text:
                record.exc_text = self.formatException(record.exc_info)
        if record.exc_text:
            if s[-1:] != "\n":
                s = s + "\n"
            s = s + record.exc_text
        if record.stack_info:
            if s[-1:] != "\n":
                s = s + "\n"
            s = s + self.formatStack(record.stack_info)
        return s

    def colorize(self, record):
        """
        Colorizes the record attributes.

        :param record:
        :return: colorized record
        """
        reset = '\033[0m'

        if hasattr(record, 'asctime'):
            record.asctime = _gc(*self.time_color) + record.asctime + reset
        if hasattr(record, 'levelno'):
            record.levelname = _gc(*self.level_colors.get(int(record.levelno), ('lw',))) + \
                               getattr(record, 'levelname', 'NOTSET') + reset
        if hasattr(record, 'name'):
            record.name = _gc(*self.name_color) + str(record.name) + reset
        if hasattr(record, 'pathname'):
            record.pathname = _gc(*self.pathname_color) + record.pathname + reset
        if hasattr(record, 'filename'):
            record.filename = _gc(*self.filename_color) + record.filename + reset
        if hasattr(record, 'module'):
            record.module = _gc(*self.module_color) + record.module + reset
        if hasattr(record, 'funcName'):
            record.funcName = _gc(*self.func_name_color) + record.funcName + reset
        if hasattr(record, 'threadName'):
            record.threadName = _gc(*self.thread_name_color) + record.threadName + reset
        if hasattr(record, 'message'):
            record.message = _gc(*self.message_color) + record.message

        return record


class DecolorizingFormatter(_Formatter):
    def formatTime(self, record, datefmt=None):
        """
        Returns the creation time of the specified LogRecord as formatted text.
        """
        ct = self.converter(int(record.created))
        if datefmt:
            s = _time.strftime(datefmt, ct)
        else:
            t = _time.strftime(self.default_time_format, ct)
            s = self.default_msec_format % (t, record.msecs)
        return s

    def format(self, record) -> str:
        """
        Decolorizes the record and returns the formatted message.

        :param record:
        :return: str
        """
        return self.decolorize(super().format(record))

    @staticmethod
    def decolorize(text: str):
        """
        Removes all ansi colors in the text.

        :param text: str: Input text
        :return: str: decolorized text
        """

        return ansi_escape.sub('', text)
