# log21.helper_types.py
# CodeWriter21
"""A collection of useful types meant for using with argument parser to parse CLI
arguments to more usable formats.

+ FileSize: Can take `str` and `int` values. Will convert human inputs such as "121 KB",
  "21MiB", or "4.56 GB" to bytes. Can also be used to represent bytes value in more
  human-readable formats.
"""

# yapf: disable

import re as _re
from math import log as _log
from typing import Union as _Union, SupportsInt as _SupportsInt

# yapf: enable

__all__ = ["FileSize"]

POWERS = "KMGTPEZYRQ"
FILE_SIZE_PATTERN = _re.compile(rf"^([+-]?[0-9]+(?:\.[0-9]+)?)\s*(|[{POWERS}])(i?)B$")


class FileSize:

    def __init__(self, value: _Union[int, str]) -> None:
        """An interface for converting different inputs to file-size (bytes).

        :param value: int value in bytes or a string such as "100 KB", "20MiB", or "1.23
            GB"
        :raises TypeError: If the value is not of type int or str
        :raises ValueError: If the str value does not match the file-size pattern:
            ^([+-]?[0-9]+(?:\\.[0-9]+)?)\\s*(|[KMGTPEZYRQ])(i?)B$
        """
        if isinstance(value, int):
            self.bytes = value
        elif isinstance(value, str):
            match = FILE_SIZE_PATTERN.match(value)
            if not match:
                raise ValueError(f"Input does not match the file-size pattern: {value}")
            val, prefix, binary = match.groups()
            power = POWERS.index(prefix) + 1
            assert power is not None
            self.bytes = int(float(val) * (1024 if binary else 1000)**power)
        else:
            raise TypeError(f"Input to FileSize() can be int or str, not {type(value)}")

    def humanize(
        self,
        binary: bool = False,
        gnu: bool = False,
        fmt: str = "%.2f",
    ) -> str:
        """Returns the size in a human readable way."""
        base = 1024 if (gnu or binary) else 1000
        abs_bytes = abs(self.bytes)

        if abs_bytes == 1 and not gnu:
            return f"{self.bytes} Byte"

        if abs_bytes < base:
            return f"{self.bytes}B" if gnu else f"{self.bytes} Bytes"

        power = int(min(_log(abs_bytes, base), len(POWERS)))
        result: str = fmt % (self.bytes / (base**power))
        if gnu:
            return result + POWERS[power - 1]
        result += " " + POWERS[power - 1]
        if binary:
            result += "i"
        result += "B"
        return result

    @property
    def KB(self) -> float:
        return self.bytes / 1000

    @property
    def MB(self) -> float:
        return self.bytes / 1000_000

    @property
    def GB(self) -> float:
        return self.bytes / 1000_000_000

    @property
    def KiB(self) -> float:
        return self.bytes / 1024

    @property
    def MiB(self) -> float:
        return self.bytes / 1048576

    @property
    def GiB(self) -> float:
        return self.bytes / 1073741824

    def __int__(self) -> int:
        return self.bytes

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, _SupportsInt):
            return False
        return self.bytes == int(value)

    def __lt__(self, value: _SupportsInt) -> bool:
        return self.bytes < int(value)

    def __le__(self, value: _SupportsInt) -> bool:
        return self.bytes <= int(value)

    def __gt__(self, value: _SupportsInt) -> bool:
        return int(value) < self.bytes

    def __ge__(self, value: _SupportsInt) -> bool:
        return int(value) <= self.bytes

    def __add__(self, value: _SupportsInt) -> "FileSize":
        return FileSize(self.bytes + int(value))

    def __str__(self) -> str:
        return self.humanize(binary=True)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: '{self!s}'>"
