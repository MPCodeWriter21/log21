# StreamHandler.py

import os as _os
import re as _re
from logging import StreamHandler as _StreamHandler

__all__ = ['IS_WINDOWS', 'ColorizingStreamHandler']

IS_WINDOWS = _os.name == 'nt'

if IS_WINDOWS:
    import ctypes


# A stream handler that supports colorizing.
class ColorizingStreamHandler(_StreamHandler):
    terminator = ''

    # logging.StreamHandler's emit function overload
    def emit(self, record):
        try:
            msg = self.format(record)
            if IS_WINDOWS:
                self.convert_and_write(msg)
                self.convert_and_write(self.terminator)
            else:
                self.write(msg)
                self.write(self.terminator)
            self.flush()
        except Exception:
            self.handleError(record)

    # Writes colorized text to the Windows console.
    def convert_and_write(self, message):
        # Regex pattern to find ansi colors in message
        ansi_esc = _re.compile(r'\x1b\[((?:\d+)(?:;(?:\d+))*)m')

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

        parts = ansi_esc.split(message)
        win_handle = None
        file_descriptor = getattr(self.stream, 'fileno', None)

        if file_descriptor is not None:
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

                    for p in params:
                        if p in nt_color_map:
                            color |= nt_color_map[p]
                        else:
                            pass  # error condition ignored

                    ctypes.windll.kernel32.SetConsoleTextAttribute(win_handle, color)

    # Writes the message to the console.
    def write(self, message):
        self.stream.write(message)
        self.flush()
