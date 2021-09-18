# log21.Argparse.py
# CodeWriter21

import sys as _sys
import log21 as _log21
import argparse as _argparse
from log21.Colors import get_colors as _gc
from gettext import gettext as _gettext


class ColorizingArgumentParser(_argparse.ArgumentParser):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.logger = _log21.Logger('ArgumentParser')

    def _print_message(self, message, file=None):
        if message:
            self.logger.handlers.clear()
            handler = _log21.ColorizingStreamHandler(stream=file)
            self.logger.addHandler(handler)
            self.logger.info(message)

    def exit(self, status=0, message=None):
        if message:
            self._print_message(_gc('lr') + message + _gc('rst'), _sys.stderr)
        _sys.exit(status)

    def error(self, message):
        self.print_usage(_sys.stderr)
        args = {'prog': self.prog, 'message': message}
        self.exit(2, _gettext(f'%(prog)s: {_gc("r")}error{_gc("lr")}:{_gc("rst")} %(message)s\n') % args)
