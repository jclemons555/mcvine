
from pyre.geometry.pml.parser.AbstractNode import AbstractNode

class Vector(AbstractNode):

    tag = "vector"
    unit = 'meter'

    def notify(self, parent):
        vector = self._vector
        parent.onVector(vector)
        return


    def __init__(self, document, attributes):
        AbstractNode.__init__(self, attributes)
        vector = dict()
        for a in 'beam transversal vertical'.split():
            if a in attributes:
                v = self._parse(attributes[a])
            else:
                v = 0*self._parse(self.unit)
            vector[a] = v
        self._vector = vector
        return

