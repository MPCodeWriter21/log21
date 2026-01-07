# log21.manager.py
# CodeWriter21

import logging as _logging
from typing import Union as _Union

from log21.levels import INFO as _INFO
from log21.logger import Logger as _loggerClass

root = _logging.RootLogger(_INFO)

LoggingType = _Union[_loggerClass, _logging.Logger]


class Manager(_logging.Manager):
    """The Manager class is a subclass of the logging.Manager class.

    It overrides the getLogger method to make it more compatible with the log21.Logger
    class. It also overrides the constructor.
    """

    def __init__(self) -> None:
        self.root = root
        self.disable = 0
        self.emittedNoHandlerWarning = False
        self.loggerDict = {}
        self.loggerClass = None
        self.logRecordFactory = None

    def getLogger(  # ty: ignore[invalid-method-override]
        self, name: str
    ) -> _Union[LoggingType, None]:
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
                if isinstance(rv, _logging.PlaceHolder):
                    rv = (self.loggerClass or _loggerClass)(name)
                    rv.manager = self
                    self.loggerDict[name] = rv
            else:
                return None
        except Exception:  # pylint: disable=broad-except
            return None
        return rv

    def addLogger(self, name: str, logger: LoggingType) -> None:
        """Adds a logger to the loggerDict dictionary.

        :param name: str: The name of the logger.
        :param logger: The logger to save.
        :raises TypeError: A logger name must be a string
        :return: None
        """
        if not isinstance(name, str):
            raise TypeError('A logger name must be a string')
        self.loggerDict[name] = logger

    get_logger = getLogger
    add_logger = addLogger
