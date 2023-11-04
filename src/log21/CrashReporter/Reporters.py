# log21.CrashReporter.Reporters.py
# CodeWriter21

from __future__ import annotations

import ssl as _ssl
import smtplib as _smtplib  # This module is used to send emails.
from os import PathLike as _PathLike
from typing import (IO as _IO, Any as _Any, Set as _Set, Type as _Type, Union as _Union,
                    Callable as _Callable, Iterable as _Iterable, Optional as _Optional)
from functools import wraps as _wraps
from email.mime.text import MIMEText as _MIMEText
from email.mime.multipart import MIMEMultipart as _MIMEMultipart

import log21 as _log21

from .Formatters import (FILE_REPORTER_FORMAT as _FILE_REPORTER_FORMAT,
                         EMAIL_REPORTER_FORMAT as _EMAIL_REPORTER_FORMAT,
                         CONSOLE_REPORTER_FORMAT as _CONSOLE_REPORTER_FORMAT)

__all__ = ['Reporter', 'ConsoleReporter', 'FileReporter', 'EmailReporter']


# pylint: disable=redefined-builtin
def print(*msg, args: tuple = (), end='\033[0m\n', **kwargs):
    """Prints a message to the console using the log21.Logger."""
    logger = _log21.get_logger(
        'log21.print', level='DEBUG', show_time=False, show_level=False
    )
    logger.print(*msg, args=args, end=end, **kwargs)


class Reporter:
    """Reporter is a decorator that wraps a function and calls a function when
    an exception is raised.

    Usage Example:
        >>>
        >>> # Define a function that gets an exception and somehow reports it to you
        >>> def report_function(exception):
        ...     print(exception)
        ...
        >>>
        >>> # Create a Reporter object and pass the reporter function you defined to it
        >>> reporter_object = Reporter(report_function, False)
        >>>
        >>> # Define the function you want to wrap
        >>> # This function might raise an exception
        >>> # You can wrap your main function, so that you get notified whenever your
        >>> # app crashes
        >>> @reporter_object.reporter
        ... def divide(a, b):
        ...     return a / b
        ...
        >>>
        >>> divide(21, 3)
        7.0
        >>> divide(10, 0)
        division by zero
        >>>
        >>> # You also can wrap a function like this
        >>> import math
        >>> wrapped_sqrt = reporter_object.reporter(math.sqrt)
        >>> wrapped_sqrt(121)
        11.0
        >>> wrapped_sqrt(-1)
        math domain error
        >>>
    """

    _reporter_function: _Callable[[
        BaseException
    ], _Any]  # A function that will be called when an exception is raised.
    _exceptions_to_catch: _Set = None
    _exceptions_to_ignore: _Set = None
    raise_after_report: bool

    def __init__(
        self,
        report_function: _Optional[_Callable[[BaseException], _Any]],
        raise_after_report: bool = False,
        formatter: _Optional[_log21.CrashReporter.Formatter] = None,
        exceptions_to_catch: _Optional[_Iterable[BaseException]] = None,
        exceptions_to_ignore: _Optional[_Iterable[BaseException]] = None
    ):
        """
        :param report_function: Function to call when an exception is raised.
        :param raise_after_report: If True, the exception will be raised after the
            report_function is called.
        """
        self._reporter_function = report_function
        self.raise_after_report = raise_after_report
        self.formatter = formatter
        self._exceptions_to_catch = set(
            exceptions_to_catch
        ) if exceptions_to_catch else None
        self._exceptions_to_ignore = set(
            exceptions_to_ignore
        ) if exceptions_to_ignore else None

    def reporter(self, func):
        """It will wrap the function and call the report_function when an
        exception is raised.

        :param func: Function to wrap.
        :return: Wrapped function.
        """

        exceptions_to_catch = tuple(
            self._exceptions_to_catch
        ) if self._exceptions_to_catch else BaseException
        exceptions_to_ignore = tuple(self._exceptions_to_ignore
                                     ) if self._exceptions_to_ignore else tuple()

        @_wraps(func)
        def wrap(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except BaseException as e:
                if isinstance(e, exceptions_to_catch) and not isinstance(
                        e, exceptions_to_ignore):
                    self._reporter_function(e)
                    if self.raise_after_report:
                        raise e
                else:
                    raise e

        return wrap

    def catch(self, exception: _Type[BaseException]):
        """Add an exception to the list of exceptions to catch.

        :param exception: Exception to catch.
        """
        if not issubclass(exception, BaseException):
            raise TypeError('`exception` must be a subclass of BaseException.')
        if self._exceptions_to_catch is None:
            self._exceptions_to_catch = set()
        if exception not in self._exceptions_to_catch:
            self._exceptions_to_catch.add(exception)
        else:
            raise ValueError('exception is already in the list of exceptions to catch')

    def ignore(self, exception: _Type[BaseException]):
        """Add an exception to the list of exceptions to ignore.

        :param exception: Exception to ignore.
        """
        if not issubclass(exception, BaseException):
            raise TypeError('`exception` must be a subclass of BaseException.')
        if self._exceptions_to_ignore is None:
            self._exceptions_to_ignore = set()
        if exception not in self._exceptions_to_ignore:
            self._exceptions_to_ignore.add(exception)
        else:
            raise ValueError('exception is already in the list of exceptions to ignore')

    def __call__(self, func):
        return self.reporter(func)


class ConsoleReporter(Reporter):
    """ConsoleReporter is a Reporter that prints the exception to the console.

    Usage Example:
        >>>
        >>> # Define a ConsoleReporter object
        >>> console_reporter = ConsoleReporter()
        >>>
        >>> # Define a function that raises an exception
        >>> @console_reporter.reporter
        ... def divide(a, b):
        ...     return a / b
        ...
        >>>
        >>> divide(21, 3)
        7.0
        >>> divide(10, 0)
        ZeroDivisionError: division by zero
            File: "<stdin>"
            Line: 3
        >>>
        >>> # You can also use costume formatters
        >>> import log21
        >>> BLUE = log21.get_color('Light Blue')
        >>> RED = log21.get_color('Light Red')
        >>> YELLOW = log21.get_color('LIGHT YELLOW')
        >>> RESET = log21.get_color('reset')
        >>> formatter = log21.CrashReporter.Formatter(
        ...     format_='[' + BLUE + '%(asctime)s' + RESET + '] ' +
        ...             YELLOW + '%(function)s' + RED + ': ' +
        ...             RESET + 'Line ' + RED + '%(lineno)d: %(name)s:' +
        ...             RESET + ' %(message)s'
        ... )
        >>> console_reporter = log21.CrashReporter.ConsoleReporter(formatter=formatter)
        >>>
        >>> @console_reporter.reporter
        ... def divide(a, b):
        ...     return a / b
        ...
        >>>
        >>> divide(21, 3)
        7.0
        >>> divide(10, 0)
        [2121-12-21 21:21:21] divide: Line 3: ZeroDivisionError: division by zero
        >>>
    """

    def __init__(
        self,
        raise_after_report: bool = False,
        formatter: _Optional[_log21.CrashReporter.Formatter] = None,
        print_function: _Optional[_Callable] = print,
        exceptions_to_catch: _Optional[_Iterable[BaseException]] = None,
        exceptions_to_ignore: _Optional[_Iterable[BaseException]] = None
    ):
        """
        :param raise_after_report: If True, the exception will be raised after the
            report_function is called.
        :param print_function: Function to use to print the message.
        """
        super().__init__(
            self._report, raise_after_report, formatter, exceptions_to_catch,
            exceptions_to_ignore
        )

        if formatter:
            if isinstance(formatter, _log21.CrashReporter.Formatter):
                self.formatter = formatter
            else:
                raise ValueError('formatter must be a log21.CrashReporter.Formatter')
        else:
            self.formatter = _log21.CrashReporter.Formatters.Formatter(
                **_CONSOLE_REPORTER_FORMAT
            )

        self.print = print_function

    def _report(self, exception: BaseException):
        """Prints the exception to the console.

        :param exception: Exception to print.
        :return:
        """

        self.print(self.formatter.format(exception))


class FileReporter(Reporter):
    """FileReporter is a Reporter that writes the exception to a file."""

    def __init__(
        self,
        *,
        file: _Union[str, _PathLike, _IO],
        encoding: str = 'utf-8',
        raise_after_report: bool = True,
        formatter: _Optional[_log21.CrashReporter.Formatter] = None,
        exceptions_to_catch: _Optional[_Iterable[BaseException]] = None,
        exceptions_to_ignore: _Optional[_Iterable[BaseException]] = None
    ):
        super().__init__(
            self._report, raise_after_report, formatter, exceptions_to_catch,
            exceptions_to_ignore
        )
        # pylint: disable=consider-using-with
        if isinstance(file, str):
            self.file = open(file, 'a', encoding=encoding)
        elif isinstance(file, _PathLike):
            self.file = open(file, 'a', encoding=encoding)
        elif isinstance(file, _IO):
            if file.writable():
                self.file = file
            else:
                raise ValueError('file must be writable')
        else:
            raise ValueError('file must be a string, PathLike, or IO object')

        if formatter:
            if isinstance(formatter, _log21.CrashReporter.Formatter):
                self.formatter = formatter
            else:
                raise ValueError('formatter must be a log21.CrashReporter.Formatter')
        else:
            self.formatter = _log21.CrashReporter.Formatters.Formatter(
                **_FILE_REPORTER_FORMAT
            )

    def _report(self, exception: BaseException):
        """Writes the exception to the file.

        :param exception: Exception to write.
        :return:
        """

        self.file.write(self.formatter.format(exception))
        self.file.flush()


class EmailReporter(Reporter):  # pylint: disable=too-many-instance-attributes
    """EmailReporter is a Reporter that sends an email with the exception.

    Usage Example:
        >>>
        >>> # Define a EmailReporter object
        >>> email_reporter = EmailReporter(
        ...     mail_host='smtp.yandex.ru',
        ...     port=465,
        ...     from_address='MyEmail@yandex.ru',
        ...     to_address='CodeWriter21@gmail.com',
        ...     password='My$up3rStr0ngP@assw0rd XD'
        ... )
        ...
        >>> # Define the function you want to wrap
        >>> @email_reporter.reporter
        ... def divide(a, b):
        ...     return a / b
        ...
        >>>
        >>> divide(21, 3)
        7.0
        >>> divide(10, 0)
        Traceback (most recent call last):
          File "<stdin>", line 1, in <module>
          File ".../site-packages/log21/CrashReporter/Reporters.py",
           line 81, in wrap
            raise e
          File ".../site-packages/log21/CrashReporter/Reporters.py",
           line 77, in wrap
            return func(*args, **kwargs)
          File "<stdin>", line 3, in divide
        ZeroDivisionError: division by zero
        >>> # At this point a Crash Report is sent to my email: CodeWriter21@gmail.com
        >>>
    """

    def __init__(
        self,
        mail_host: str,
        port: int,
        from_address: str,
        to_address: str,
        password: str,
        username: str = '',
        tls: bool = True,
        raise_after_report: bool = True,
        formatter: _Optional[_log21.CrashReporter.Formatter] = None,
        exceptions_to_catch: _Optional[_Iterable[BaseException]] = None,
        exceptions_to_ignore: _Optional[_Iterable[BaseException]] = None
    ):
        super().__init__(
            self._report, raise_after_report, formatter, exceptions_to_catch,
            exceptions_to_ignore
        )
        self.mail_host = mail_host
        self.port = port
        self.from_address = from_address
        self.to_address = to_address
        self.password = password
        if username:
            self.username = username
        else:
            self.username = self.from_address
        self.tls = tls

        # Checks if the sender email is accessible
        try:
            if self.tls:
                context = _ssl.create_default_context()
                with _smtplib.SMTP_SSL(self.mail_host, port, context=context) as server:
                    server.ehlo()
                    server.login(self.username, self.password)
            else:
                with _smtplib.SMTP(self.mail_host, port) as server:
                    server.ehlo()
                    server.login(self.username, self.password)
                    server.ehlo()
        except Exception as ex:  # pylint: disable=broad-except
            raise ex

        if formatter:
            if isinstance(formatter, _log21.CrashReporter.Formatter):
                self.formatter = formatter
            else:
                raise ValueError('formatter must be a log21.CrashReporter.Formatter')
        else:
            self.formatter = _log21.CrashReporter.Formatters.Formatter(
                **_EMAIL_REPORTER_FORMAT
            )

    def _report(self, exception: BaseException):
        """Sends an email with the exception.

        :param exception: Exception to send.
        :return:
        """
        message = _MIMEMultipart()
        message['From'] = self.from_address  # Sender
        message['To'] = self.to_address  # Receiver
        message['Subject'] = f'Crash Report: {exception.__class__.__name__}'  # Subject
        message.attach(_MIMEText(self.formatter.format(exception), 'html'))
        if self.tls:
            context = _ssl.create_default_context()
            with _smtplib.SMTP_SSL(self.mail_host, port=self.port,
                                   context=context) as server:
                server.login(self.username, self.password)
                server.sendmail(self.from_address, self.to_address, message.as_string())
        else:
            with _smtplib.SMTP(self.username, port=self.port) as server:
                server.login(self.from_address, self.password)
                server.sendmail(self.from_address, self.to_address, message.as_string())
