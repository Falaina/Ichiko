# -*- coding: utf-8 -*-
from __future__ import print_function, division, unicode_literals
from collections import OrderedDict
import bitstring

class ConstBitStream(bitstring.ConstBitStream):
    def readstring(self, num_bytes, encoding=None):
        str_bytes = self.read('bytes: {}'.format(num_bytes))
        if encoding:
            return str_bytes.decode(encoding)
        return str_bytes

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
        obj = cls()
        obj.parse(ConstBitStream(filename=filename))
        return obj

    def parse(self, s):
        self.s = s
        _start_offset = s.bytepos
        for (name, field) in self.fields.iteritems():
            if field.offset:
                assert (s.bytepos - _start_offset) == field.offset, \
                    'Incorrect offset: Expected %x, Got %x' %(s.bytepos, field.offset)
            setattr(self, name, s.read(field.fmt))
            
    def __repr__(self):
        if self._pprint_fields is None:
            self._pprint_fields = self.fields.keys()

        items = ['%s=%s' % (k, getattr(self, k)) for k in self._pprint_fields]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(items))

        
