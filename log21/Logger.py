# log21.Logger.py
# CodeWriter21

import log21 as _log21
import logging as _logging
from logging import raiseExceptions as _raiseExceptions
from log21.Levels import *

__all__ = ['Logger']


class Logger(_logging.Logger):
    def __init__(self, name, level=NOTSET):
        super().__init__(name, level)
        self.setLevel(level)
        self._progress_bar = None

    def isEnabledFor(self, level):
        """
        Is this logger enabled for level 'level'?
        """

        return self.level <= level

    def log(self, level: int, *msg, args: tuple = (), end='\033[0m\n', **kwargs):
        """
        Log 'msg % args' with the integer severity 'level'.

        To pass exception information, use the keyword argument exc_info with
        a true value, e.g.

        logger.log(level, "We have a %s", args=("mysterious problem",), exc_info=1)
        """
        msg = ' '.join([str(m) for m in msg]) + end
        if not isinstance(level, int):
            if _raiseExceptions:
                raise TypeError("level must be an integer")
            else:
                return
        if self.isEnabledFor(level):
            self._log(level, msg, args, **kwargs)

    def debug(self, *msg, args: tuple = (), end='\033[0m\n', **kwargs):
        """
        Log 'msg % args' with severity 'DEBUG'.

        To pass exception information, use the keyword argument exc_info with
        a true value, e.g.

        logger.debug("Houston, we have a %s", args=("thorny problem",), exc_info=1)
        """
        if self.isEnabledFor(DEBUG):
            msg = ' '.join([str(m) for m in msg]) + end
            self._log(DEBUG, msg, args, **kwargs)

    def info(self, *msg, args: tuple = (), end='\033[0m\n', **kwargs):
        """
        Log 'msg % args' with severity 'INFO'.

        To pass exception information, use the keyword argument exc_info with
        a true value, e.g.

        logger.info("Houston, we have an %s", args=("interesting problem",), exc_info=1)
        """
        if self.isEnabledFor(INFO):
            msg = ' '.join([str(m) for m in msg]) + end
            self._log(INFO, msg, args, **kwargs)

    def warning(self, *msg, args: tuple = (), end='\033[0m\n', **kwargs):
        """
        Log 'msg % args' with severity 'WARNING'.

        To pass exception information, use the keyword argument exc_info with
        a true value, e.g.

        logger.warning("Houston, we have a %s", args=("bit of a problem",), exc_info=1)
        """
        if self.isEnabledFor(WARNING):
            msg = ' '.join([str(m) for m in msg]) + end
            self._log(WARNING, msg, args, **kwargs)

    warn = warning

    def write(self, *msg, args: tuple = (), end='', **kwargs):
        """
        Log 'msg % args' with severity 'WARNING'.

        To pass exception information, use the keyword argument exc_info with
        a true value, e.g.

        logger.write("Houston, we have a %s", args=("bit of a problem",), exc_info=1)
        """
        if self.isEnabledFor(WARNING):
            msg = ' '.join([str(m) for m in msg]) + end
            self._log(WARNING, msg, args, **kwargs)

    def error(self, *msg, args: tuple = (), end='\033[0m\n', **kwargs):
        """
        Log 'msg % args' with severity 'ERROR'.

        To pass exception information, use the keyword argument exc_info with
        a true value, e.g.

        logger.error("Houston, we have a %s", args=("major problem",), exc_info=1)
        """
        if self.isEnabledFor(ERROR):
            msg = ' '.join([str(m) for m in msg]) + end
            self._log(ERROR, msg, args, **kwargs)

    def exception(self, *msg, args, exc_info=True, **kwargs):
        """
        Convenience method for logging an ERROR with exception information.
        """
        self.error(*msg, args=args, exc_info=exc_info, **kwargs)

    def critical(self, *msg, args: tuple = (), end='\033[0m\n', **kwargs):
        """
        Log 'msg % args' with severity 'CRITICAL'.

        To pass exception information, use the keyword argument exc_info with
        a true value, e.g.

        logger.critical("Houston, we have a %s", args=("major disaster",), exc_info=1)
        """
        if self.isEnabledFor(CRITICAL):
            msg = ' '.join([str(m) for m in msg]) + end
            self._log(CRITICAL, msg, args, **kwargs)

    fatal = critical

    def print(self, *msg, args: tuple = (), end='\033[0m\n', **kwargs):
        """
        Log 'msg % args'.

        To pass exception information, use the keyword argument exc_info with
        a true value, e.g.

        logger.print("Houston, we have a %s", args=("major disaster",), exc_info=1)
        """
        msg = ' '.join([str(m) for m in msg]) + end
        self._log(self.level if self.level >= NOTSET else NOTSET, msg, args, **kwargs)

    def input(self, *msg, args: tuple = (), end='\033[0m', **kwargs):
        """
        Log 'msg % args'.

        To pass exception information, use the keyword argument exc_info with
        a true value, e.g.

        age = logger.input("Enter your age: ")
        """
        msg = ' '.join([str(m) for m in msg]) + end
        self._log(self.level if self.level >= NOTSET else NOTSET, msg, args, **kwargs)
        return input()

    def print_progress(self, progress: float, total: float):
        """
        Log progress.
        """
        self.progress_bar(progress, total)

    @property
    def progress_bar(self):
        if not self._progress_bar:
            from log21.ProgressBar import ProgressBar
            self._progress_bar = ProgressBar(logger=self)
        return self._progress_bar

    @progress_bar.setter
    def progress_bar(self, value: '_log21.ProgressBar'):
        self._progress_bar = value
