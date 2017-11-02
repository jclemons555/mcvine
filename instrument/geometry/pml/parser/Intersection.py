
from pyre.geometry.pml.parser.Intersection import Intersection as base
from .CompositionExtension import CompositionExtension

class Intersection(base, CompositionExtension):

    def notify(self, parent):
        if not self._b1 or not self._b2:
            raise ValueError("'%s' requires exactly two children" % self.tag)

        import instrument.geometry.operations as ops
        intersection = ops.intersect(self._b1, self._b2)
        parent.onIntersection(intersection)
        return
    
