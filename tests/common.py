from __future__ import print_function
from os.path import join, dirname, normpath
import sys

top_level = normpath(join(dirname(__file__), '..'))
sys.path[0:0] = [top_level]
