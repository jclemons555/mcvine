
from .Multiary import Multiary

class Union(Multiary):

    tag = 'union'
    
    def notify(self, parent):
        if len(self._shapes)<2:
            raise ValueError("'%s' requires at least two children" % self.tag)

        import instrument.geometry.operations as ops
        union = ops.unite(*self._shapes)
        parent.onUnion(union)
        return

    pass
