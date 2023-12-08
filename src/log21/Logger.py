# log21.Logger.py
# CodeWriter21

import re as _re
import logging as _logging
from types import MethodType as _MethodType
from typing import (Union as _Union, Literal as _Literal, Mapping,
                    Callable as _Callable, Optional as _Optional, Sequence as _Sequence)
from getpass import getpass as _getpass
from logging import raiseExceptions as _raiseExceptions

import log21 as _log21
from log21.Levels import INFO, DEBUG, ERROR, INPUT, PRINT, NOTSET, WARNING, CRITICAL

__all__ = ['Logger']


class Logger(_logging.Logger):
    """A Logger that can print to the console and log to a file."""

    def __init__(
        self,
        name,
        level: _Union[int, str] = NOTSET,
        handlers: _Optional[_Union[_Sequence[_logging.Handler],
                                   _logging.Handler]] = None
    ):
        """Initialize a Logger object.

        :param name: The name of the logger.
        :param level: The level of the logger.
        :param handlers: The handlers to add to the logger.
        """
        super().__init__(name, level)
        self.setLevel(level)
        self._progress_bar = None
        if handlers:
            if not isinstance(handlers, _Sequence):
                if isinstance(handlers, _logging.Handler):
                    handlers = [handlers]
                else:
                    raise TypeError(
                        "handlers must be a list of logging.Handler objects"
                    )
            for handler in handlers:
                self.addHandler(handler)

    def isEnabledFor(self, level):
        """Is this logger enabled for level 'level'?"""

        return (self.level <= level) or (level in (PRINT, INPUT))

    def log(self, level: int, *msg, args: tuple = (), end='\n', **kwargs):
        """Log 'msg % args' with the integer severity 'level'.

        To pass exception information, use the keyword argument exc_info with a true
        value, e.g.

        logger.log(level, "We have a %s", args=("mysterious problem",), exc_info=1)
        """
        msg = ' '.join([str(m) for m in msg]) + end
        if not isinstance(level, int):
            if _raiseExceptions:
                raise TypeError("level must be an integer")
            return
        if self.isEnabledFor(level):
            self._log(level, msg, args, **kwargs)

    def debug(self, *msg, args: tuple = (), end='\n', **kwargs):
        """Log 'msg % args' with severity 'DEBUG'.

        To pass exception information, use the keyword argument exc_info with a true
        value, e.g.

        logger.debug("Houston, we have a %s", args=("thorny problem",), exc_info=1)
        """
        if self.isEnabledFor(DEBUG):
            msg = ' '.join([str(m) for m in msg]) + end
            self._log(DEBUG, msg, args, **kwargs)

    def info(self, *msg, args: tuple = (), end='\n', **kwargs):
        """Log 'msg % args' with severity 'INFO'.

        To pass exception information, use the keyword argument exc_info with a true
        value, e.g.

        logger.info("Houston, we have an %s", args=("interesting problem",), exc_info=1)
        """
        if self.isEnabledFor(INFO):
            msg = ' '.join([str(m) for m in msg]) + end
            self._log(INFO, msg, args, **kwargs)

    def warning(self, *msg, args: tuple = (), end='\n', **kwargs):
        """Log 'msg % args' with severity 'WARNING'.

        To pass exception information, use the keyword argument exc_info with a true
        value, e.g.

        logger.warning("Houston, we have a %s", args=("bit of a problem",), exc_info=1)
        """
        if self.isEnabledFor(WARNING):
            msg = ' '.join([str(m) for m in msg]) + end
            self._log(WARNING, msg, args, **kwargs)

    warn = warning

    def write(self, *msg, args: tuple = (), end='', **kwargs):
        """Log 'msg % args' with severity 'WARNING'.

        To pass exception information, use the keyword argument exc_info with a true
        value, e.g.

        logger.write("Houston, we have a %s", args=("bit of a problem",), exc_info=1)
        """
        if self.isEnabledFor(WARNING):
            msg = ' '.join([str(m) for m in msg]) + end
            self._log(WARNING, msg, args, **kwargs)

    def error(self, *msg, args: tuple = (), end='\n', **kwargs):
        """Log 'msg % args' with severity 'ERROR'.

        To pass exception information, use the keyword argument exc_info with a true
        value, e.g.

        logger.error("Houston, we have a %s", args=("major problem",), exc_info=1)
        """
        if self.isEnabledFor(ERROR):
            msg = ' '.join([str(m) for m in msg]) + end
            self._log(ERROR, msg, args, **kwargs)

    def exception(self, *msg, args: tuple = (), exc_info=True, **kwargs):
        """Convenience method for logging an ERROR with exception information."""
        self.error(*msg, args=args, exc_info=exc_info, **kwargs)

    def critical(self, *msg, args: tuple = (), end='\n', **kwargs):
        """Log 'msg % args' with severity 'CRITICAL'.

        To pass exception information, use the keyword argument exc_info with a true
        value, e.g.

        logger.critical("Houston, we have a %s", args=("major disaster",), exc_info=1)
        """
        if self.isEnabledFor(CRITICAL):
            msg = ' '.join([str(m) for m in msg]) + end
            self._log(CRITICAL, msg, args, **kwargs)

    fatal = critical

    def print(self, *msg, args: tuple = (), end='\n', **kwargs):
        """Log 'msg % args'.

        To pass exception information, use the keyword argument exc_info with a true
        value, e.g.

        logger.print("Houston, we have a %s", args=("major disaster",), exc_info=1)
        """
        msg = ' '.join([str(m) for m in msg]) + end
        self._log(PRINT, msg, args, **kwargs)

    def input(self, *msg, args: tuple = (), end='', **kwargs):
        """Log 'msg % args'.

        To pass exception information, use the keyword argument exc_info with a true
        value, e.g.

        age = logger.input("Enter your age: ")
        """
        msg = ' '.join([str(m) for m in msg]) + end
        self._log(INPUT, msg, args, **kwargs)
        return input()

    def getpass(self, *msg, args: tuple = (), end='', **kwargs):
        """


        :return:
        """
        msg = ' '.join([str(m) for m in msg]) + end
        self._log(self.level if self.level >= NOTSET else NOTSET, msg, args, **kwargs)
        return _getpass('')

    def print_progress(self, progress: float, total: float, **kwargs):
        """Log progress."""
        self.progress_bar(progress, total, **kwargs)

    @property
    def progress_bar(self):
        """Return a progress bar instance.

        If not exists, create a new one.
        """
        if not self._progress_bar:
            # avoid circular import; pylint: disable=import-outside-toplevel
            from log21.ProgressBar import ProgressBar
            self._progress_bar = ProgressBar(logger=self)
        return self._progress_bar

    @progress_bar.setter
    def progress_bar(self, value: '_log21.ProgressBar'):
        self._progress_bar = value

    def clear_line(self, length: _Optional[int] = None):
        """Clear the current line.

        :param length: The length of the line to clear.
        :return:
        """
        for handler in self.handlers:
            if isinstance(getattr(handler, 'clear_line', None), _Callable):
                handler.clear_line(length)  # type: ignore

    def add_level(
        self,
        level: int,
        name: str,
        errors: _Literal["raise", "ignore", "handle", "force"] = "raise"
    ) -> str:
        """Adds a new method to the logger with a specific level and name.

        :param level: The level of the new method.
        :param name: The name of the new method.
        :param errors: The action to take if the level already exists.
            + ``raise`` (default): Raise an exception if anything goes wrong.
            + ``ignore``: Do nothing.
            + ``handle``: Handle the situation if a method with the same ``name``
              already exists. Adds a number to the name to avoid the conflict.
            + ``force``: Add the new level with the specified level even if a
              method with the same ``name`` already exists.
        :raises TypeError: If ``level`` is not an integer.
        :raises TypeError: If ``name`` is not a string.
        :raises ValueError: If ``errors`` is not one of "raise", "ignore", "handle",
            or "force".
        :raises ValueError: If ``name`` starts with a number.
        :raises ValueError: If ``name`` is not a valid identifier.
        :raises AttributeError: If ``errors`` is "raise" and a method with the
            same ``name`` already exists.
        :return: The name of the new method.
        """

        def raise_(error: BaseException):
            if errors == 'ignore':
                return
            raise error

        if not isinstance(level, int):
            raise_(TypeError('level must be an integer'))
        if not isinstance(name, str):
            raise_(TypeError('name must be a string'))
        if errors not in ('raise', 'ignore', 'handle', 'force'):
            raise_(
                ValueError(
                    'errors must be one of "raise", "ignore", "handle", "force"'
                )
            )

        name = _re.sub(r'\s', '_', name)
        if _re.match(r'[0-9].*', name):
            raise_(ValueError(f'level name cannot start with a number: "{name}"'))
        if not _re.fullmatch(r'[a-zA-Z_][a-zA-Z0-9_]*', name):
            raise_(ValueError(f'level name must be a valid identifier: "{name}"'))

        if hasattr(self, name):
            if errors == 'raise':
                raise AttributeError(f'level "{name}" already exists')
            if errors == 'ignore':
                return name
            if errors == 'handle':
                return self.add_level(level, _add_one(name), errors)

        def log_for_level(self, *msg, args: tuple = (), end='\n', **kwargs):
            self.log(level, *msg, args=args, end=end, **kwargs)

        setattr(self, name, _MethodType(log_for_level, self))
        return name

    def add_levels(
        self,
        level_names: Mapping[int, str],
        errors: _Literal["raise", "ignore", "handle", "force"] = "raise"
    ) -> None:
        """Adds new methods to the logger with specific levels and names.

        :param level_names: A mapping of levels to names.
        :param errors: The action to take if the level already exists
        :return:
        """
        for level, name in level_names.items():
            self.add_level(level, name, errors)


def _add_one(name: str) -> str:
    """Add one to the end of a string.

    :param name: The string to add one to.
    :return: The string with one added to the end.
    """
    match = _re.match(r'([\S]+)_([0-9]+)', name)
    if not match:
        return name + '_1'
    return f'{match.group(1)}{int(match.group(2)) + 1}'
