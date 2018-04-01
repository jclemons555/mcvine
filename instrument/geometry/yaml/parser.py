#!/usr/bin/env python
#
# Jiao Lin <jiao.lin@gmail.com>
#

from .. import operations, shapes
from pyre.units import parser
parser = parser()

class Parser:

    def parse(self, d):
        assert len(d) == 1
        name, value = list(d.items())[0]
        return self._toObj(name, value)

    def _toObj(self, name, value):
        method = 'on%s' % name.capitalize()
        method = getattr(self, method)
        return method(value)

    def _parseDict(self, d):
        o = dict()
        for k, v in d.items():
            o[k] = parser.parse(v)
            continue
        return o        

    def onBlock(self, d):
        d = self._parseDict(d)
        return shapes.block(**d)

    def onRotation(self, d):
        o = dict()
        for k, v in d.items():
            obj = self._toObj(k, v)
            if k not in ['angle', 'axis']:
                k = 'body'
            o[k] = obj
            continue
        return operations.rotate(o['body'], angle=o['angle'], **o['axis'])

    def onAngle(self, v):
        return parser.parse(v)

    def onAxis(self, d):
        return d

            
# End of file 
