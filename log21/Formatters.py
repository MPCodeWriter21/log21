# Formatter.py

import time as _time
from logging import Formatter as _Formatter
from typing import Dict as _Dict, Tuple as _Tuple
from log21.Colors import get_colors, ansi_esc
from log21.Levels import *

__all__ = ['ColorizingFormatter', 'DecolorizingFormatter']


class ColorizingFormatter(_Formatter):
    # Default color values
    level_colors = {
        DEBUG: ('lightblue',),
        INFO: ('green',),
        WARNING: ('lightyellow',),
        ERROR: ('light red',),
        CRITICAL: ('background red', 'white')
    }
    time_color = ('lightblue',)
    name_color = pathname_color = filename_color = module_color = func_name_color = thread_name_color = \
        message_color = tuple()

    def __init__(self, fmt: str = None, datefmt: str = None, style: str = '%',
                 level_colors: _Dict[int, _Tuple[str]] = None,
                 time_color: _Tuple[str, ...] = None, name_color: _Tuple[str, ...] = None,
                 pathname_color: _Tuple[str, ...] = None, filename_color: _Tuple[str, ...] = None,
                 module_color: _Tuple[str, ...] = None, func_name_color: _Tuple[str, ...] = None,
                 thread_name_color: _Tuple[str, ...] = None, message_color: _Tuple[str, ...] = None):
        super().__init__(fmt=fmt, datefmt=datefmt, style=style)
        # Checks and sets colors
        if level_colors:
            if type(level_colors) is not dict:
                raise TypeError('`level_colors` must be a dictionary!')
            for key in level_colors:
                self.level_colors[key] = level_colors[key]
        if time_color:
            if type(time_color) is not tuple:
                raise TypeError('`time_color` must be a tuple!')
            self.time_color = time_color
        if name_color:
            if type(name_color) is not tuple:
                raise TypeError('`name_color` must be a tuple!')
            self.name_color = name_color
        if pathname_color:
            if type(pathname_color) is not tuple:
                raise TypeError('`pathname_color` must be a tuple!')
            self.pathname_color = pathname_color
        if filename_color:
            if type(filename_color) is not tuple:
                raise TypeError('`filename_color` must be a tuple!')
            self.filename_color = filename_color
        if module_color:
            if type(module_color) is not tuple:
                raise TypeError('`module_color` must be a tuple!')
            self.module_color = module_color
        if func_name_color:
            if type(func_name_color) is not tuple:
                raise TypeError('`func_name_color` must be a tuple!')
            self.func_name_color = func_name_color
        if thread_name_color:
            if type(thread_name_color) is not tuple:
                raise TypeError('`thread_name_color` must be a tuple!')
            self.thread_name_color = thread_name_color
        if message_color:
            if type(message_color) is not tuple:
                raise TypeError('`message_color` must be a tuple!')
            self.funcName_color = message_color

    def format(self, record) -> str:
        """
        Colorizes the record and returns the formatted message.

        :param record:
        :return: str
        """
        record.message = record.getMessage()
        if self.usesTime():
            record.asctime = self.formatTime(record, self.datefmt)

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

        record.asctime = get_colors(*self.time_color) + record.asctime + reset
        record.levelname = get_colors(*self.level_colors[int(record.levelno)]) + record.levelname + reset
        record.name = get_colors(*self.name_color) + str(record.name) + reset
        record.pathname = get_colors(*self.pathname_color) + record.pathname + reset
        record.filename = get_colors(*self.filename_color) + record.filename + reset
        record.module = get_colors(*self.module_color) + record.module + reset
        record.funcName = get_colors(*self.func_name_color) + record.funcName + reset
        record.threadName = get_colors(*self.thread_name_color) + record.threadName + reset
        record.message = get_colors(*self.message_color) + record.message + reset

        return record


class DecolorizingFormatter(_Formatter):
    def formatTime(self, record, datefmt=None):
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

        return ansi_esc.subn('', text)[0]
