from __future__ import print_function, division, unicode_literals
import __builtin__
import inspect
from os.path import basename, splitext
from collections import namedtuple
from six.moves import reprlib

repr = reprlib.aRepr.repr
InfoTuple = namedtuple('InfoTuple', ['name', 'module', 'module_path'])

def getcaller():
    print(inspect.stack())
    module_path = inspect.stack()[1][1]
    return InfoTuple(inspect.stack()[1][3], splitext(basename(module_path))[0], module_path)

def check_args(args, arg_test, usage):
    assert arg_test(args[1:]), usage
    return args[0], args[1:]

class InvariantError(ValueError):
    pass

def InvariantCheck(b, msg):
    if not b:
        raise InvariantError(msg)

class Invariant(object):
    types = ['pre', 'post']

    def __init__(self, pre=None, post=None):
        if pre is None and post is None:
            raise ValueError('both pre and post can not be null')
        if pre is None:
            pre  = lambda *args, **kwargs: True
        if post is None:
            post = lambda *args, **kwargs: True
        self.pre  = pre
        self.post = post

    def __call__(self, fn):
        self._fn = fn
        inv = self
        class new_fn(object):
            def _fn(self, *args, **kwargs):
                return fn(*args, **kwargs)

            def __call__(self, *args, **kwargs):
                inv.pre(*args, **kwargs)
                result = fn(*args, **kwargs)
                inv.post(result, *args, **kwargs)
                return result
        return new_fn()
        

