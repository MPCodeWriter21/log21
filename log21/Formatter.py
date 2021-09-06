# Formatter.py

from logging import Formatter as _Formatter
from typing import Dict as _Dict, Tuple as _Tuple
from log21.Colors import get_colors
from log21.Levels import *

__all__ = ['ColorizingFormatter']


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
    name_color = pathname_color = filename_color = module_color = lineno_color = func_name_color = \
        created_color = msecs_color = relative_created_color = thread_color = thread_name_color = \
        process_color = message_color = tuple()

    def __init__(self, fmt: str = None, datefmt: str = None, style: str = '%', level_colors: _Dict[int, _Tuple[str]] = None,
                 time_color: _Tuple[str, ...] = None, name_color: _Tuple[str, ...] = None,
                 pathname_color: _Tuple[str, ...] = None, filename_color: _Tuple[str, ...] = None,
                 module_color: _Tuple[str, ...] = None, lineno_color: _Tuple[str, ...] = None,
                 func_name_color: _Tuple[str, ...] = None, created_color: _Tuple[str, ...] = None,
                 msecs_color: _Tuple[str, ...] = None, relative_created_color: _Tuple[str, ...] = None,
                 thread_color: _Tuple[str, ...] = None, thread_name_color: _Tuple[str, ...] = None,
                 process_color: _Tuple[str, ...] = None, message_color: _Tuple[str, ...] = None):
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
        if lineno_color:
            if type(lineno_color) is not tuple:
                raise TypeError('`lineno_color` must be a tuple!')
            self.lineno_color = lineno_color
        if func_name_color:
            if type(func_name_color) is not tuple:
                raise TypeError('`func_name_color` must be a tuple!')
            self.func_name_color = func_name_color
        if created_color:
            if type(created_color) is not tuple:
                raise TypeError('`created_color` must be a tuple!')
            self.created_color = created_color
        if msecs_color:
            if type(msecs_color) is not tuple:
                raise TypeError('`msecs_color` must be a tuple!')
            self.msecs_color = msecs_color
        if relative_created_color:
            if type(relative_created_color) is not tuple:
                raise TypeError('`relative_created_color` must be a tuple!')
            self.relative_created_color = relative_created_color
        if thread_color:
            if type(thread_color) is not tuple:
                raise TypeError('`thread_color` must be a tuple!')
            self.thread_color = thread_color
        if thread_name_color:
            if type(thread_name_color) is not tuple:
                raise TypeError('`thread_name_color` must be a tuple!')
            self.thread_name_color = thread_name_color
        if process_color:
            if type(process_color) is not tuple:
                raise TypeError('`process_color` must be a tuple!')
            self.process_color = process_color
        if message_color:
            if type(message_color) is not tuple:
                raise TypeError('`message_color` must be a tuple!')
            self.funcName_color = message_color

    def format(self, record) -> str:
        """
        Colorizes the the record and returns the formatted message.

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
        record.levelname = get_colors(*self.level_colors[record.levelno]) + record.levelname + reset
        record.levelno = get_colors(*self.level_colors[record.levelno]) + str(record.levelno) + reset
        record.name = get_colors(*self.name_color) + str(record.name) + reset
        record.pathname = get_colors(*self.pathname_color) + record.pathname + reset
        record.filename = get_colors(*self.filename_color) + record.filename + reset
        record.module = get_colors(*self.module_color) + record.module + reset
        record.funcName = get_colors(*self.func_name_color) + record.funcName + reset
        record.lineno = get_colors(*self.lineno_color) + str(record.lineno) + reset
        record.created = get_colors(*self.created_color) + str(record.created) + reset
        record.msecs = get_colors(*self.msecs_color) + str(record.msecs) + reset
        record.relativeCreated = get_colors(*self.relative_created_color) + str(record.relativeCreated) + reset
        record.thread = get_colors(*self.thread_color) + str(record.thread) + reset
        record.threadName = get_colors(*self.thread_name_color) + record.threadName + reset
        record.process = get_colors(*self.process_color) + str(record.process) + reset
        record.message = get_colors(*self.message_color) + record.message + reset

        return record
