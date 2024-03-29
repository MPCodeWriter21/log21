# log21.StreamHandler.py
# CodeWriter21

import os as _os
import re as _re
import shutil as _shutil
from typing import Optional as _Optional
from logging import StreamHandler as _StreamHandler

from log21.Colors import (get_colors as _gc, hex_escape as _hex_escape,
                          ansi_escape as _ansi_escape)

__all__ = ['IS_WINDOWS', 'ColorizingStreamHandler', 'StreamHandler']

IS_WINDOWS = _os.name == 'nt'

if IS_WINDOWS:
    import ctypes


class StreamHandler(_StreamHandler):
    """A StreamHandler that can handle carriage returns and new lines."""
    terminator = ''

    def __init__(
        self,
        handle_carriage_return: bool = True,
        handle_new_line: bool = True,
        stream=None,
        formatter=None,
        level=None
    ):
        """Initialize the StreamHandler.

        :param handle_carriage_return: Whether to handle carriage
            returns.
        :param handle_new_line: Whether to handle new lines.
        :param stream: The stream to write to.
        :param formatter: The formatter to use.
        :param level: The level to log at.
        """
        self.HandleCR = handle_carriage_return
        self.HandleNL = handle_new_line
        super().__init__(stream=stream)
        if formatter is not None:
            self.setFormatter(formatter)
        if level is not None:
            self.setLevel(level)

    def check_cr(self, record):
        """Check if the record contains a carriage return and handle it."""
        if record.msg:
            msg = _hex_escape.sub(
                '', _ansi_escape.sub('', record.msg.strip(' \t\n\x0b\x0c'))
            )
            if '\r' == msg[:1]:
                file_descriptor = getattr(self.stream, 'fileno', None)
                if file_descriptor:
                    file_descriptor = file_descriptor()
                    if file_descriptor in (1, 2):  # stdout or stderr
                        self.stream.write(
                            '\r' + (
                                ' ' * (
                                    _shutil.get_terminal_size(file_descriptor).columns -
                                    1
                                )
                            ) + '\r'
                        )
                        index = record.msg.rfind('\r')
                        find = _re.compile(r'(\x1b\[(?:\d+(?:;(?:\d+))*)m)')
                        record.msg = _gc(*find.split(record.msg[:index])
                                         ) + record.msg[index + 1:]

    def check_nl(self, record):
        """Check if the record contains a newline and handle it."""
        while record.msg and record.msg[0] == '\n':
            file_descriptor = getattr(self.stream, 'fileno', None)
            if file_descriptor:
                file_descriptor = file_descriptor()
                if file_descriptor in (1, 2):  # stdout or stderr
                    self.stream.write('\n')
                    record.msg = record.msg[1:]

    def emit(self, record):
        if self.HandleCR:
            self.check_cr(record)
        if self.HandleNL:
            self.check_nl(record)
        super().emit(record)

    def clear_line(self, length: _Optional[int] = None):
        """Clear the current line.

        :param length: The length of the line to clear.
        :return:
        """
        file_descriptor = getattr(self.stream, 'fileno', None)
        if file_descriptor:
            file_descriptor = file_descriptor()
            if file_descriptor in (1, 2):
                if length is None:
                    length = _shutil.get_terminal_size(file_descriptor).columns
                self.stream.write('\r' + (' ' * (length - 1)) + '\r')


# A stream handler that supports colorizing.
class ColorizingStreamHandler(StreamHandler):
    """A stream handler that supports colorizing even in Windows."""

    def emit(self, record):
        try:
            if self.HandleCR:
                self.check_cr(record)
            if self.HandleNL:
                self.check_nl(record)
            msg = self.format(record)
            if IS_WINDOWS:
                self.convert_and_write(msg)
                self.convert_and_write(self.terminator)
            else:
                self.write(msg)
                self.write(self.terminator)
            self.flush()
        except Exception:  # pylint: disable=broad-except
            self.handleError(record)

    # Writes colorized text to the Windows console.
    def convert_and_write(self, message):
        """Convert the message to a Windows console colorized message and write
        it to the stream."""
        nt_color_map = {
            30: 0,  # foreground: black   - 0b00000000
            31: 4,  # foreground: red     - 0b00000100
            32: 2,  # foreground: green   - 0b00000010
            33: 6,  # foreground: yellow  - 0b00000110
            34: 1,  # foreground: blue    - 0b00000001
            35: 5,  # foreground: magenta - 0b00000101
            36: 3,  # foreground: cyan    - 0b00000011
            37: 7,  # foreground: white   - 0b00000111
            40: 0,  # background: black   - 0b00000000 = 0 << 4
            41: 64,  # background: red     - 0b01000000 = 4 << 4
            42: 32,  # background: green   - 0b00100000 = 2 << 4
            43: 96,  # background: yellow  - 0b01100000 = 6 << 4
            44: 16,  # background: blue    - 0b00010000 = 1 << 4
            45: 80,  # background: magenta - 0b01010000 = 5 << 4
            46: 48,  # background: cyan    - 0b00110000 = 3 << 4
            47: 112,  # background: white   - 0b01110000 = 7 << 4
            90: 8,  # foreground: gray          - 0b00001000
            91: 12,  # foreground: light red     - 0b00001100
            92: 10,  # foreground: light green   - 0b00001010
            93: 14,  # foreground: light yellow  - 0b00001110
            94: 9,  # foreground: light blue    - 0b00001001
            95: 13,  # foreground: light magenta - 0b00001101
            96: 11,  # foreground: light cyan    - 0b00001011
            97: 15,  # foreground: light white   - 0b00001111
            100: 128,  # background: gray          - 0b10000000 = 8  << 4
            101: 192,  # background: light red     - 0b11000000 = 12 << 4
            102: 160,  # background: light green   - 0b10100000 = 10 << 4
            103: 224,  # background: light yellow  - 0b11100000 = 14 << 4
            104: 144,  # background: light blue    - 0b10010000 = 9  << 4
            105: 208,  # background: light magenta - 0b11010000 = 13 << 4
            106: 176,  # background: light cyan    - 0b10110000 = 11 << 4
            107: 240,  # background: light white   - 0b11110000 = 15 << 4
            2: 8,
            0: 7
        }

        parts = _ansi_escape.split(message)
        win_handle = None
        file_descriptor = getattr(self.stream, 'fileno', None)

        if file_descriptor:
            file_descriptor = file_descriptor()

            if file_descriptor in (1, 2):  # stdout or stderr
                win_handle = ctypes.windll.kernel32.GetStdHandle(-10 - file_descriptor)

        while parts:
            text = parts.pop(0)

            if text:
                self.write(text)

            if parts:
                params = parts.pop(0)

                if win_handle is not None:
                    params = [int(p) for p in params.split(';')]
                    color = 0

                    for param in params:
                        if param in nt_color_map:
                            color |= nt_color_map[param]
                        else:
                            pass  # error condition ignored

                    ctypes.windll.kernel32.SetConsoleTextAttribute(win_handle, color)

    # Writes the message to the console.
    def write(self, message):
        """Write the message to the stream."""
        self.stream.write(message)
        self.flush()
