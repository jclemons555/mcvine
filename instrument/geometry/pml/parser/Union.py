
from pyre.geometry.pml.parser.Union import Union as base

class Union(base):

    def notify(self, parent):
        if not self._b1 or not self._b2:
            raise ValueError("'%s' requires exactly two children" % self.tag)

        import instrument.geometry.operations as ops
        union = ops.unite(self._b1, self._b2)
        parent.onUnion(union)
        return
    
