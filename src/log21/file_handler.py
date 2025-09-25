# log21.file_handler.py
# CodeWriter21

from logging import FileHandler

from log21.formatters import DecolorizingFormatter


class FileHandler(FileHandler):
    """A subclass of logging.FileHandler that allows you to specify a formatter and a
    level when you initialize it."""

    def __init__(
        self,
        filename,
        mode='a',
        encoding=None,
        delay=False,
        errors=None,
        formatter=None,
        level=None
    ):
        """Initialize the handler.

        :param filename: The filename of the log file.
        :param mode: The mode to open the file in.
        :param encoding: The encoding to use when opening the file.
        :param delay: Whether to delay opening the file.
        :param errors: The error handling scheme to use.
        :param formatter: The formatter to use.
        :param level: The level to use.
        """
        super().__init__(filename, mode, encoding, delay, errors)
        if formatter is not None:
            self.setFormatter(formatter)
        if level is not None:
            self.setLevel(level)


class DecolorizingFileHandler(FileHandler):
    """A subclass of FileHandler that removes ANSI colors from the log messages before
    writing them to the file."""
    terminator = ''

    def emit(self, record):
        """Emit a record."""
        if self.stream is None:
            self.stream = self._open()
        try:
            msg = self.format(record)
            msg = DecolorizingFormatter.decolorize(msg)
            stream = self.stream
            stream.write(msg + self.terminator)
            self.flush()
        except Exception:  # pylint: disable=broad-except
            self.handleError(record)
