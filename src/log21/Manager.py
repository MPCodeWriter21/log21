# log21.Manager.py
# CodeWriter21

import logging as _logging
from typing import Union as _Union
from log21.Logger import Logger as _loggerClass
from log21.Levels import INFO as _INFO

root = _logging.RootLogger(_INFO)


class Manager(_logging.Manager):
    def __init__(self):
        self.root = root
        self.disable = 0
        self.emittedNoHandlerWarning = False
        self.loggerDict = {}
        self.loggerClass = None
        self.logRecordFactory = None

    def getLogger(self, name: str) -> _Union[_logging.Logger, _loggerClass, None]:
        """
        Takes the name of a logger and if there was a logger with that name in the loggerDict it will return the logger
        otherwise it'll return None.

        :param name: The name of the logger.
        :raises TypeError: A logger name must be a string
        :return:
        """
        if not isinstance(name, str):
            raise TypeError('A logger name must be a string')
        try:
            if name in self.loggerDict:
                rv = self.loggerDict[name]
                if isinstance(rv, _logging.PlaceHolder):
                    rv = (self.loggerClass or _loggerClass)(name)
                    rv.manager = self
                    self.loggerDict[name] = rv
            else:
                return None
        except Exception:
            return None
        return rv

    def addLogger(self, name: str, logger) -> None:
        """
        Adds a logger to the loggerDict dictionary.

        :param name: str: The name of the logger.
        :param logger: The logger to save.
        :raises TypeError: A logger name must be a string
        :return: None
        """
        if not isinstance(name, str):
            raise TypeError('A logger name must be a string')
        self.loggerDict[name] = logger
