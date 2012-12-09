from __future__ import print_function
from path import path
from tempfile import gettempdir
from ichiko.common import *
from types import MethodType
import re
import sys
import logging, logging.handlers
INFO = logging.INFO
DEBUG = logging.DEBUG
WARN  = logging.WARN

def _patch_logging():
    global TRACE, STDIO_HANDLER, TRC_HANDLER
    if hasattr(logging, '_patched'):
        return
    TRACE = logging.TRACE = 5
    STDIO_HANDLER = logging.StreamHandler(sys.stderr)
    STDIO_HANDLER.setFormatter(default_formatter)
    TRC_HANDLER = logging.handlers.RotatingFileHandler(path(gettempdir()) / 'root.log', 
                                              maxBytes=2**25, backupCount=5)
    TRC_HANDLER.setFormatter(default_formatter)
    logging.addLevelName(TRACE, 'TRACE')
    logging._patched = True

def _unpatch_logging(force=False):
    global TRACE, STDIO_HANDLER
    if not hasattr(logging, '_patched') and not forced:
        return
    del logging._levelNames['TRACE']
    del logging._levelNames[logging.TRACE]
    del TRACE
    del logging.TRACE
    del STDIO_HANDLER
    del TRC_HANDLER
    del logging._patched 
    
_defaultfmt = '[%(levelname)-5s %(name)s (%(relativeCreated)d)] %(message)s'
default_formatter = logging.Formatter(_defaultfmt)
default_level     = logging.DEBUG

def log_fn(level, levelname):
    def fn(self, fmt, *args):
        return self.log(level, fmt, *args)
    fn.__name__ = levelname
    return fn

format_re = re.compile('%[rscdoxXeEfFgG]')
class Logger(object):
    def __init__(self, logger):
        self._logger = logger
        self.indent_level = 0
        for (level, levelname) in logging._levelNames.iteritems():
            if isinstance(level, str):
                continue
            levelname = levelname.lower()
            fn = log_fn(level, levelname)
            setattr(self, levelname, MethodType(fn, self, self.__class__))

    def indent(self):
        self.indent_level += 1

    def dedent(self):
        self.indent_level -= 1

    @property
    def pre(self):
        return '    ' * self.indent_level

    def log(self, level, fmt, *args):
        fmt = self.pre + str(fmt)
        try:
            out = fmt % args
        except TypeError:
            fmt_cnt = fmt.replace('%%', '').count('%')
            diff = len(args) - fmt_cnt
            if diff > 0:
                fmt = fmt + (' %s' * diff)
            out = fmt % args
        self._logger.log(level, out)

    def __getattr__(self, attr):
        return getattr(self._logger, attr)

def getlogger(name=None, stdio=True):
    if name is None:
        name = getcaller().module
    logpath = path(gettempdir()) / name + '.log'
    logger = Logger(logging.getLogger(name))
    if stdio:
        root.addHandler(STDIO_HANDLER)
        root.addHandler(TRC_HANDLER)
    return logger

def get_stdiohandler():
    return STDIO_HANDLER
    
_patch_logging()
root = logging.getLogger()
root.setLevel(TRACE)
