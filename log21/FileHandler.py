# log21.FileHandler.py
# CodeWriter21

from logging import FileHandler as _FileHandler
from log21.Formatters import DecolorizingFormatter as _DecolorizingFormatter


class DecolorizingFileHandler(_FileHandler):
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
