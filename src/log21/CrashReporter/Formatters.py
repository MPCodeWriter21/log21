# log21.CrashReporter.Formatters.py
# CodeWriter21

import traceback

from datetime import datetime as _datetime
from typing import Mapping as _Mapping, Union as _Union, Callable as _Callable, Any as _Any

__all__ = ['Formatter', 'CONSOLE_REPORTER_FORMAT', 'FILE_REPORTER_FORMAT', 'EMAIL_REPORTER_FORMAT']

RESERVED_KEYS = (
    '__name__',
    'type',
    'message',
    'traceback',
    'name',
    'file',
    'lineno',
    'function',
    'asctime'
)


class Formatter:
    def __init__(self, format_: str, style: str = '%', datefmt: str = '%Y-%m-%d %H:%M:%S',
                 extra_values: _Mapping[str, _Union[str, _Callable, _Any]] = None):
        self._format = format_

        if style in ['%', '{']:
            self.__style = style
        else:
            raise ValueError('Invalid style: "' + str(style) + '" Valid styles: %, {')

        self.datefmt = datefmt
        self.extra_values = dict()
        if extra_values:
            for key in extra_values:
                if key in RESERVED_KEYS:
                    raise ValueError(f'`{key}` is a reserved-key and cannot be used in `extra_values`.')
                self.extra_values[key] = extra_values[key]

    def format(self, exception: BaseException):
        exception_dict = {
            '__name__': __name__,
            'type': type(exception),
            'message': exception.args[0],
            'traceback': traceback.format_tb(exception.__traceback__.tb_next),
            'name': exception.__class__.__name__,
            'file': exception.__traceback__.tb_next.tb_frame.f_code.co_filename,
            'lineno': exception.__traceback__.tb_next.tb_lineno,
            'function': exception.__traceback__.tb_next.tb_frame.f_code.co_name,
            'asctime': _datetime.now().strftime(self.datefmt),
        }
        for key, value in self.extra_values.items():
            if callable(value):
                exception_dict[key] = value()
            else:
                exception_dict[key] = value

        if self.__style == '%':
            return self._format % exception_dict
        elif self.__style == '{':
            return self._format.format(**exception_dict)
        else:
            raise ValueError('Invalid style: "' + str(self.__style) + '" Valid styles: %, {')


CONSOLE_REPORTER_FORMAT = dict(
    format_=f'\033[91m%(name)s: %(message)s\033[0m\n'  # Name and message of the exception.
            f'\tFile\033[91m:\033[0m "%(file)s"\n'  # The file that exception was raised in.
            f'\tLine\033[91m:\033[0m %(lineno)d',  # The line that exception was raised on.
    style='%'
)

FILE_REPORTER_FORMAT = dict(
    format_=f'[%(asctime)s] %(name)s: %(message)s'  # Name and message of the exception.
            f'; File: "%(file)s"'  # The file that exception was raised in.
            f'; Line: %(lineno)d\n',  # The line that exception was raised on.
    style='%'
)

EMAIL_REPORTER_FORMAT = dict(
    format_="""
    <html>
        <body>
            <h1>Crash Report: %(__name__)s</h1>
            <h2>%(name)s: %(message)s</h2>
            <p>
                <span style="bold">File:</span> "%(file)s"<br>
                <span style="bold">Line:</span> %(lineno)d<br>
                <span style="center">%(asctime)s</span><br>
            </p>
        <body>
    </html>
    """,
    style='%'
)
