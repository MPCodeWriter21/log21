# log21.FileHandler.py
# CodeWriter21

from logging import FileHandler as _FileHandler
from log21.Formatters import DecolorizingFormatter as _DecolorizingFormatter


class FileHandler(_FileHandler):
    def __init__(self, filename, mode='a', encoding=None, delay=False, errors=None, formatter=None, level=None):
        super().__init__(filename, mode, encoding, delay, errors)
        if formatter is not None:
            self.setFormatter(formatter)
        if level is not None:
            self.setLevel(level)


class DecolorizingFileHandler(FileHandler):
    terminator = ''

    def emit(self, record):
        if self.stream is None:
            self.stream = self._open()
        try:
            msg = self.format(record)
            msg = _DecolorizingFormatter.decolorize(msg)
            stream = self.stream
            stream.write(msg + self.terminator)
            self.flush()
        except Exception:
            self.handleError(record)
