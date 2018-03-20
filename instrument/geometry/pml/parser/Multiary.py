
from pyre.geometry.pml.parser.Composition import Composition as base
from .CompositionExtension import CompositionExtension

class Multiary(base, CompositionExtension):
    
    def __init__(self, document, attributes=None):
        base.__init__(self, attributes)
        self._shapes = []

    def _setOperand(self, body):
        self._shapes.append(body)
        return
