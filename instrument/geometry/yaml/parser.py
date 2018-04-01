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

    def onPrimitive(self, name, d):
        d = self._parseDict(d)
        return getattr(shapes, name)(**d)
    
    def onBlock(self, d): return self.onPrimitive('block', d)
    def onSphere(self, d): return self.onPrimitive('sphere', d)
    def onCylinder(self, d): return self.onPrimitive('cylinder', d)
    def onPyramid(self, d): return self.onPrimitive('pyramid', d)

    def onUnion(self, d):
        l = [self._toObj(k,v) for k, v in d.items()]
        return operations.unite(*l)
    
    def onIntersection(self, d):
        l = [self._toObj(k,v) for k, v in d.items()]
        return operations.intersect(*l)
    
    def onDifference(self, d):
        l = [self._toObj(k,v) for k, v in d.items()]
        assert len(l)==2
        return operations.subtract(*l)
    
    def onRotation(self, d):
        o = dict()
        for k, v in d.items():
            obj = self._toObj(k, v)
            if k not in ['angle', 'axis']:
                k = 'body'
            o[k] = obj
            continue
        return operations.rotate(o['body'], angle=o['angle'], **o['axis'])

    def onTranslation(self, d):
        o = dict()
        for k, v in d.items():
            obj = self._toObj(k, v)
            if k not in ['vector']:
                k = 'body'
            o[k] = obj
            continue
        return operations.translate(o['body'], **o['vector'])

    def onAngle(self, v):
        return parser.parse(v)

    def onAxis(self, d):
        return d

    def onVector(self, d):
        return self._parseDict(d)

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

            
# End of file 
