from StringIO import StringIO
import common
import sys

str_stdout = StringIO()
sys.stdout = str_stdout

sys.stdout = sys.__stdout__
import ichiko.ichilog as ichilog


ichilog._unpatch_logging()
ichilog._patch_logging()
ichilog._unpatch_logging()
ichilog._patch_logging()

log = ichilog.getlogger()
log.info('hi')
log.trace('wa')
