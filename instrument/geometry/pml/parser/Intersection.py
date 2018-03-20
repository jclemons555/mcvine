
from .Multiary import Multiary

class Intersection(Multiary):

    tag = 'intersection'
    
    def notify(self, parent):
        if len(self._shapes)<2:
            raise ValueError("'%s' requires at least two children" % self.tag)

        import instrument.geometry.operations as ops
        intersection = ops.intersect(*self._shapes)
        parent.onIntersection(intersection)
        return

    pass
