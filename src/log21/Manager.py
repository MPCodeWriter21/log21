# log21.manager.py
# CodeWriter21

import logging
from typing import Union

from log21.levels import INFO
from log21.logger import Logger as loggerClass

root = logging.RootLogger(INFO)


class Manager(logging.Manager):
    """The Manager class is a subclass of the logging.Manager class.

    It overrides the getLogger method to make it more compatible with the log21.Logger
    class. It also overrides the constructor.
    """

    def __init__(self):
        self.root = root
        self.disable = 0
        self.emittedNoHandlerWarning = False
        self.loggerDict = {}
        self.loggerClass = None
        self.logRecordFactory = None

    def getLogger(self, name: str) -> Union[logging.Logger, loggerClass, None]:
        """Takes the name of a logger and if there was a logger with that name in the
        loggerDict it will return the logger otherwise it'll return None.

        :param name: The name of the logger.
        :raises TypeError: A logger name must be a string
        :return:
        """
        if not isinstance(name, str):
            raise TypeError('A logger name must be a string')
        try:
            if name in self.loggerDict:
                rv = self.loggerDict[name]
                if isinstance(rv, logging.PlaceHolder):
                    rv = (self.loggerClass or loggerClass)(name)
                    rv.manager = self
                    self.loggerDict[name] = rv
            else:
                return None
        except Exception:  # pylint: disable=broad-except
            return None
        return rv

    def addLogger(self, name: str, logger) -> None:  # pylint: disable=invalid-name
        """Adds a logger to the loggerDict dictionary.

        :param name: str: The name of the logger.
        :param logger: The logger to save.
        :raises TypeError: A logger name must be a string
        :return: None
        """
        if not isinstance(name, str):
            raise TypeError('A logger name must be a string')
        self.loggerDict[name] = logger
