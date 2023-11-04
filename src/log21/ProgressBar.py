# log21.ProgressBar.py
# CodeWriter21

from __future__ import annotations

import shutil as _shutil
from typing import Any as _Any, Mapping as _Mapping, Optional as _Optional

import log21 as _log21
from log21.Colors import get_colors as _gc
from log21.Logger import Logger as _Logger
from log21.StreamHandler import ColorizingStreamHandler as _ColorizingStreamHandler

_logger = _Logger('ProgressBar')
_logger.addHandler(_ColorizingStreamHandler())

__all__ = ['ProgressBar']


class ProgressBar:  # pylint: disable=too-many-instance-attributes, line-too-long
    """
    Usage Example:
        >>> pb = ProgressBar(width=20, show_percentage=False, prefix='[', suffix=']',
        ... fill='=', empty='-')
        >>> pb(0, 10)
        [/-----------------]
        >>> pb(1, 10)
        [==----------------]
        >>> pb(2, 10)
        [====\\-------------]
        >>>
        >>> # A better example
        >>> import time
        >>> pb = ProgressBar()
        >>> for i in range(500):
        ...     pb(i + 1, 500)
        ...     time.sleep(0.01)
        ...
        |███████████████████████████████████████████████████████████████████| 100%
        >>> # Of course, You should try it yourself to see the progress! XD
        >>>
    """

    def __init__(
        self,
        *,
        width: _Optional[int] = None,
        show_percentage: bool = True,
        prefix: str = '|',
        suffix: str = '|',
        fill: str = '█',
        empty: str = ' ',
        format_: _Optional[str] = None,
        style: str = '%',
        new_line_when_complete: bool = True,
        colors: _Optional[_Mapping[str, str]] = None,
        no_color: bool = False,
        logger: _log21.Logger = _logger,
        additional_variables: _Optional[_Mapping[str, _Any]] = None
    ):  # pylint: disable=too-many-branches, too-many-statements
        """
        :param args: Prevents the use of positional arguments
        :param width: The width of the progress bar
        :param show_percentage: Whether to show the percentage of the progress
        :param prefix: The prefix of the progress bar
        :param suffix: The suffix of the progress bar
        :param fill: The fill character of the progress bar
        :param empty: The empty character of the progress bar
        :param format_: The format of the progress bar
        :param style: The style that is used to format the progress bar
        :param new_line_when_complete: Whether to print a new line when the progress is
            complete or failed
        :param colors: The colors of the progress bar
        :param no_color: If True, removes the colors of the progress bar
        :param logger: The logger to use
        :param additional_variables: Additional variables to use in the format and their
            default values
        """
        # Sets a default value for the width
        if width is None:
            try:
                width = _shutil.get_terminal_size().columns - 1
            except OSError:
                width = 50
            if width < 1:
                width = 50
        self.width = width
        if self.width < 3:
            raise ValueError('`width` must be greater than 1')
        if not isinstance(fill, str):
            raise TypeError('`fill` must be a string')
        if not isinstance(empty, str):
            raise TypeError('`empty` must be a string')
        if not isinstance(prefix, str):
            raise TypeError('`prefix` must be a string')
        if not isinstance(suffix, str):
            raise TypeError('`suffix` must be a string')
        if len(fill) != 1:
            raise ValueError('`fill` must be a single character')
        if len(empty) != 1:
            raise ValueError('`empty` must be a single character')
        if style not in ['%', '{']:
            raise ValueError('`style` must be either `%` or `{`')
        if colors and no_color:
            raise PermissionError(
                'You cannot use `no_color` and `colors` parameters together!'
            )
        if additional_variables:
            if not isinstance(additional_variables, _Mapping):
                raise TypeError(
                    '`additional_variables` must be a dictionary like object.'
                )
            for key, value in additional_variables.items():
                if not isinstance(key, str):
                    raise TypeError('`additional_variables` keys must be strings')
                if not isinstance(value, str):
                    additional_variables[key] = str(value)
        else:
            additional_variables = {}

        self.colors = {
            'progress in-progress': _gc('LightYellow'),
            'progress complete': _gc('LightGreen'),
            'progress failed': _gc('LightRed'),
            'percentage in-progress': _gc('LightBlue'),
            'percentage complete': _gc('LightCyan'),
            'percentage failed': _gc('LightRed'),
            'prefix-color in-progress': _gc('Yellow'),
            'prefix-color complete': _gc('Green'),
            'prefix-color failed': _gc('Red'),
            'suffix-color in-progress': _gc('Yellow'),
            'suffix-color complete': _gc('Green'),
            'suffix-color failed': _gc('Red'),
            'reset-color': _gc('Reset'),
        }
        self.spinner = ['|', '/', '-', '\\']

        self.fill = fill
        self.empty = empty
        self.prefix = prefix
        self.suffix = suffix
        if format_:
            self.format = format_
        else:
            self.format = (
                '%(prefix)s%(bar)s%(suffix)s %(percentage)s%%'
                if show_percentage else '%(prefix)s%(bar)s%(suffix)s'
            )
            style = '%'
        self.style = style
        self.new_line_when_complete = new_line_when_complete
        if colors:
            for key, value in colors.items():
                self.colors[key] = value
        if no_color:
            self.colors = {name: '' for name in self.colors}
        self.logger = logger
        self.additional_variables = additional_variables
        self.i = 0

    def get_bar(self, progress: float, total: float, **kwargs) -> str:
        """Return the progress bar as a string.

        :param progress: The current progress. (e.g. 21)
        :param total: The total progress. (e.g. 100)
        :param kwargs: Additional variables to be used in the format
            string.
        :raises ValueError: If the style is not supported.
            Set the style to one of the following:
            + '%'
            + '{'
            e.g. bar = ProgressBar(style='{')
        :return: The progress bar as a string.
        """
        if progress == total:
            return self.progress_complete(**kwargs)
        if progress > total or progress < 0:
            return self.progress_failed(progress, total, **kwargs)
        return self.progress_in_progress(progress, total, **kwargs)

    def progress_in_progress(self, progress: float, total: float, **kwargs) -> str:
        """Return the progress bar as a string when the progress is in progress.

        :param progress: The current progress. (e.g. 21)
        :param total: The total progress. (e.g. 100)
        :param kwargs: Additional variables to be used in the format
            string.
        :raises ValueError: If the style is not supported. (supported
            styles: '%', '{')
        :return: The progress bar as a string.
        """
        percentage = str(round(progress / total * 100, 2))
        progress_dict = {
            'prefix': self.prefix,
            'bar': '',
            'suffix': self.suffix,
            'percentage': percentage,
            **self.additional_variables
        }
        for key, value in kwargs.items():
            if key in ['prefix', 'bar', 'suffix', 'percentage']:
                raise ValueError(f'`{key}` is a reserved keyword')
            progress_dict[key] = value

        if self.style == '%':
            used_characters = len(self.format % progress_dict)
        elif self.style == '{':
            used_characters = len(self.format.format(**progress_dict))
        else:
            raise ValueError('`style` must be either `%` or `{`')

        fill_length = round(progress / total * (self.width - used_characters))
        empty_length = (self.width - (fill_length + used_characters)) - 1

        if self.i >= 3:
            self.i = 0
        else:
            self.i += 1
        spinner_char = self.spinner[self.i] if empty_length > 0 else ''

        progress_dict = {
            'prefix':
            self.colors['prefix-color in-progress'] + self.prefix +
            self.colors['reset-color'],
            'bar':
            self.colors['progress in-progress'] +
            (self.fill * fill_length + spinner_char + self.empty * empty_length) +
            self.colors['reset-color'],
            'suffix':
            self.colors['suffix-color in-progress'] + self.suffix +
            self.colors['reset-color'],
            'percentage':
            self.colors["percentage in-progress"] + str(percentage) +
            self.colors['reset-color'],
            **self.additional_variables
        }
        for key, value in kwargs.items():
            progress_dict[key] = value

        if self.style == '%':
            return '\r' + self.format % progress_dict + self.colors['reset-color']
        if self.style == '{':
            return '\r' + self.format.format(**progress_dict
                                             ) + self.colors['reset-color']
        raise ValueError('`style` must be either `%` or `{`')

    def progress_complete(self, **kwargs) -> str:
        """Prints the progress bar as complete.

        :param kwargs: Additional variables to be passed to the format string.
        :raises ValueError: If the style is not either `%` or `{`.
        :return: The formatted progress bar.
        """
        progress_dict = {
            'prefix': self.prefix,
            'bar': '',
            'suffix': self.suffix,
            'percentage': '100',
            **self.additional_variables
        }
        for key, value in kwargs.items():
            if key in ['prefix', 'bar', 'suffix', 'percentage']:
                raise ValueError(f'`{key}` is a reserved keyword')
            progress_dict[key] = value

        if self.style == '%':
            bar_length = self.width - len(self.format % progress_dict)
        elif self.style == '{':
            bar_length = self.width - len(self.format.format(**progress_dict))
        else:
            raise ValueError('`style` must be either `%` or `{`')

        progress_dict = {
            'prefix':
            self.colors['prefix-color complete'] + self.prefix +
            self.colors['reset-color'],
            'bar':
            self.colors['progress complete'] + (self.fill * bar_length) +
            self.colors['reset-color'],
            'suffix':
            self.colors['suffix-color complete'] + self.suffix +
            self.colors['reset-color'],
            'percentage':
            self.colors["percentage complete"] + '100' + self.colors['reset-color'],
            **self.additional_variables
        }
        for key, value in kwargs.items():
            progress_dict[key] = value

        if self.style == '%':
            return (
                '\r' + self.format % progress_dict + self.colors['reset-color'] +
                ('\n' if self.new_line_when_complete else '')
            )
        if self.style == '{':
            return (
                '\r' + self.format.format(**progress_dict) +
                self.colors['reset-color'] +
                ('\n' if self.new_line_when_complete else '')
            )
        raise ValueError('`style` must be either `%` or `{`')

    def progress_failed(self, progress: float, total: float, **kwargs):
        """Returns a progress bar with a failed state.

        :param progress: The current progress.
        :param total: The total progress.
        :param kwargs: Additional variables to be passed to the format string.
        :raises ValueError: If the style is not `%` or `{`.
        :return: A progress bar with a failed state.
        """
        progress_dict = {
            'prefix': self.prefix,
            'bar': '',
            'suffix': self.suffix,
            'percentage': str(round(progress / total * 100, 2)),
            **self.additional_variables
        }
        for key, value in kwargs.items():
            if key in ['prefix', 'bar', 'suffix', 'percentage']:
                raise ValueError(f'`{key}` is a reserved keyword')
            progress_dict[key] = value

        if self.style == '%':
            bar_length = self.width - len(self.format % progress_dict)
        elif self.style == '{':
            bar_length = self.width - len(self.format.format(**progress_dict))
        else:
            raise ValueError('`style` must be either `%` or `{`')

        if progress > total:
            bar_char = self.fill
        else:
            bar_char = self.empty

        progress_dict = {
            'prefix':
            self.colors['prefix-color failed'] + self.prefix +
            self.colors['reset-color'],
            'bar':
            self.colors['progress failed'] + (bar_char * bar_length) +
            self.colors['reset-color'],
            'suffix':
            self.colors['suffix-color failed'] + self.suffix +
            self.colors['reset-color'],
            'percentage':
            self.colors["percentage failed"] + progress_dict['percentage'] +
            self.colors['reset-color'],
            **self.additional_variables
        }
        for key, value in kwargs.items():
            progress_dict[key] = value

        if self.style == '%':
            progress_bar = self.format % progress_dict
        elif self.style == '{':
            progress_bar = self.format.format(**progress_dict)
        else:
            raise ValueError('`style` must be either `%` or `{`')

        return '\r' + progress_bar + self.colors['reset-color'] + (
            '\n' if self.new_line_when_complete else ''
        )

    def __call__(
        self,
        progress: float,
        total: float,
        logger: _Optional[_log21.Logger] = None,
        **kwargs
    ):
        if not logger:
            logger = self.logger

        logger.print(self.get_bar(progress, total, **kwargs), end='')

    def update(
        self,
        progress: float,
        total: float,
        logger: _Optional[_log21.Logger] = None,
        **kwargs
    ):
        """Update the progress bar.

        :param progress: The current progress.
        :param total: The total progress.
        :param logger: The logger to use. If not specified, the logger specified in the
            constructor will be used.
        :param kwargs: Additional variables to be used in the format string.
        :raises ValueError: If the style is not `%` or `{`.
        """
        self(progress, total, logger, **kwargs)
