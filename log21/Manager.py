# log21.Manager.py
# CodeWriter21

import logging as _logging
from log21.Logger import Logger as _loggerClass
from log21.Levels import INFO as _INFO
from typing import Optional as _Optional, Type as _Type

root = _logging.RootLogger(_INFO)


class Manager(_logging.Manager):
    def __init__(self):
        self.root = root
        self.disable = 0
        self.emittedNoHandlerWarning = False
        self.loggerDict = {}
        self.loggerClass = None
        self.logRecordFactory = None

    def getLogger(self, name):
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
        except:
            rv = None
        return rv

    def addLogger(self, name: str, logger):
        if not isinstance(name, str):
            raise TypeError('A logger name must be a string')
        self.loggerDict[name] = logger
