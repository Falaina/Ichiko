import inspect
from os.path import basename, splitext
from collections import namedtuple

InfoTuple = namedtuple('InfoTuple', ['name', 'module', 'module_path'])

def getcaller():
    print inspect.stack()
    module_path = inspect.stack()[1][1]
    return InfoTuple(inspect.stack()[1][3], splitext(basename(module_path))[0], module_path)

def test():
    print getcaller()
test()
