
from pyre.geometry.pml.parser.Difference import Difference as base
from .CompositionExtension import CompositionExtension

class Difference(base, CompositionExtension):

    def notify(self, parent):
        if not self._b1 or not self._b2:
            raise ValueError("'%s' requires exactly two children" % self.tag)

        import instrument.geometry.operations as ops
        difference = ops.subtract(self._b1, self._b2)
        parent.onDifference(difference)
        return
    
