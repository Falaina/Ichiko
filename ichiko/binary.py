# -*- coding: utf-8 -*-
from __future__ import print_function, division, unicode_literals
from collections import OrderedDict
import bitstring

class ConstBitStream(bitstring.ConstBitStream):
    def readstrings(self, num_bytes, num_strings, encoding=None, max_bytes=4096):
        strs = []
        for _ in range(num_strings):
            strs.append(self.readstring(num_bytes, encoding, max_bytes))
        return strs

    def readstring(self, num_bytes, encoding=None, max_bytes=4096):
        if num_bytes > max_bytes:
            raise ValueError('{} bytes exceed max_bytes of {} bytes'.format(num_bytes, max_bytes))
        str_bytes = self.read('bytes: {}'.format(num_bytes))
        if encoding:
            return str_bytes.decode(encoding)
        return str_bytes

    def magicno(self, goal):
        actual = self.read('bytes: {}'.format(len(goal)))
        assert actual == goal, 'Magic No {} does not match goal {}'.format(actual, goal)

class PackedStructField(object):
    def __init__(self, name, fmt, *args):
        self.name   = name
        self.fmt    = fmt
        self.args   = args

        if len(args) > 0:
            self.offset = args[0]
        else:
            self.offset = None

        self.formatter = self.format
            
    @staticmethod
    def format(obj):
        return '%s' % (obj,)

    def __repr__(self):
        return self.formatter(self)

class PackedStruct(object):
    _fields_ = []
    _pprint_fields = None

    def __init__(self):
        self.fields = OrderedDict()
        for tup in self._fields_:
            field = PackedStructField(*tup)
            assert field.name not in self.fields
            self.fields[field.name] = field

    @classmethod
    def fromfile(cls, filename):
        return cls.fromstream(ConstBitStream(filename=filename))
        
    @classmethod
    def fromstream(cls, s, num=1):
        objs = []
        for _ in range(num):
            obj = cls()
            obj.parse(s)
            objs.append(obj)
        if num == 1:
            return objs[0]
        return objs

    def parse(self, s):
        self.s = s
        _start_offset = s.bytepos
        for (name, field) in self.fields.iteritems():
            if field.offset:
                assert (s.bytepos - _start_offset) == field.offset, \
                    'Incorrect offset: Expected %x, Got %x' %(field.offset, s.bytepos - _start_offset)
            setattr(self, name, s.read(field.fmt))
            
    def __repr__(self):
        if self._pprint_fields is None:
            self._pprint_fields = self.fields.keys()

        items = ['%s=%s' % (k, getattr(self, k)) for k in self._pprint_fields]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(items))

        
