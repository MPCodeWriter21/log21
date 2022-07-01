# log21.ProgressBar.py
# CodeWriter21

import os as _os

import log21 as _log21
from log21.Logger import Logger as _Logger
from log21.StreamHandler import ColorizingStreamHandler as _ColorizingStreamHandler
from log21.Colors import get_colors as _gc

_logger = _Logger('ProgressBar')
_logger.addHandler(_ColorizingStreamHandler())

__all__ = ['ProgressBar']


class ProgressBar:
    """
    Usage Example:
        >>> pb = ProgressBar(width=20, show_percentage=False, prefix='[', suffix=']', fill='=', empty='-')
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
        |████████████████████████████████████████████████████████████████████████████████████████████| 100%
        >>> # Of course, You should try it yourself to see the progress! XD
        >>>
    """

    def __init__(self, *args, width: int = None, show_percentage: bool = True, prefix: str = '|', suffix: str = '|',
                 fill: str = '█', empty: str = ' ', format_: str = None, style: str = '%',
                 new_line_when_complete: bool = True, colors: dict = None, logger: '_log21.Logger' = _logger):
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
        :param new_line_when_complete: Whether to print a new line when the progress is complete or failed
        :param colors: The colors of the progress bar
        :param logger: The logger to use
        """
        self.width = width if width else _os.get_terminal_size().columns - 1
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
            self.format = '%(prefix)s%(bar)s%(suffix)s %(percentage)s%%' if show_percentage else \
                '%(prefix)s%(bar)s%(suffix)s'
            style = '%'
        self.style = style
        self.new_line_when_complete = new_line_when_complete
        if colors:
            for key, value in colors.items():
                self.colors[key] = value
        self.logger = logger
        self.i = 0

    def get_bar(self, progress: float, total: float):
        if progress == total:
            return self.progress_complete()
        elif progress > total or progress < 0:
            return self.progress_failed(progress, total)
        else:
            return self.progress_in_progress(progress, total)

    def progress_in_progress(self, progress: float, total: float):
        percentage = str(round(progress / total * 100, 2))
        progress_dict = {
            'prefix': self.prefix,
            'bar': '',
            'suffix': self.suffix,
            'percentage': percentage
        }

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
            'prefix': self.colors['prefix-color in-progress'] + self.prefix + self.colors['reset-color'],
            'bar': self.colors['progress in-progress'] +
                   (self.fill * fill_length + spinner_char + self.empty * empty_length) + self.colors['reset-color'],
            'suffix': self.colors['suffix-color in-progress'] + self.suffix + self.colors['reset-color'],
            'percentage': self.colors["percentage in-progress"] + str(percentage) + self.colors['reset-color']
        }

        if self.style == '%':
            bar = self.format % progress_dict
        elif self.style == '{':
            bar = self.format.format(**progress_dict)
        else:
            raise ValueError('`style` must be either `%` or `{`')

        return '\r' + bar + self.colors['reset-color']

    def progress_complete(self):
        progress_dict = {
            'prefix': self.prefix,
            'bar': '',
            'suffix': self.suffix,
            'percentage': '100'
        }

        if self.style == '%':
            bar_length = self.width - len(self.format % progress_dict)
        elif self.style == '{':
            bar_length = self.width - len(self.format.format(**progress_dict))
        else:
            raise ValueError('`style` must be either `%` or `{`')

        progress_dict = {
            'prefix': self.colors['prefix-color complete'] + self.prefix + self.colors['reset-color'],
            'bar': self.colors['progress complete'] + (self.fill * bar_length) + self.colors['reset-color'],
            'suffix': self.colors['suffix-color complete'] + self.suffix + self.colors['reset-color'],
            'percentage': self.colors["percentage complete"] + '100' + self.colors['reset-color']
        }

        if self.style == '%':
            bar = self.format % progress_dict
        elif self.style == '{':
            bar = self.format.format(**progress_dict)
        else:
            raise ValueError('`style` must be either `%` or `{`')

        return '\r' + bar + self.colors['reset-color'] + ('\n' if self.new_line_when_complete else '')

    def progress_failed(self, progress: float, total: float):
        progress_dict = {
            'prefix': self.prefix,
            'bar': '',
            'suffix': self.suffix,
            'percentage': str(round(progress / total * 100, 2))
        }

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
            'prefix': self.colors['prefix-color failed'] + self.prefix + self.colors['reset-color'],
            'bar': self.colors['progress failed'] + (bar_char * bar_length) + self.colors['reset-color'],
            'suffix': self.colors['suffix-color failed'] + self.suffix + self.colors['reset-color'],
            'percentage': self.colors["percentage failed"] + progress_dict['percentage'] + self.colors['reset-color']
        }

        if self.style == '%':
            bar = self.format % progress_dict
        elif self.style == '{':
            bar = self.format.format(**progress_dict)
        else:
            raise ValueError('`style` must be either `%` or `{`')

        return '\r' + bar + self.colors['reset-color'] + ('\n' if self.new_line_when_complete else '')

    def __call__(self, progress: float, total: float, logger: '_log21.Logger' = None):
        if not logger:
            logger = self.logger

        logger.print(self.get_bar(progress, total), end='')

    def update(self, progress: float, total: float, logger: '_log21.Logger' = None):
        self(progress, total, logger)
