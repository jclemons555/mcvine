from pyre.geometry.pml.parser.Rotation import Rotation as base
from .CompositionExtension import CompositionExtension


class Rotation(base, CompositionExtension):

    def notify(self, parent):
        import instrument.geometry.operations as ops
        rotation = ops.rotate(self._body, angles=self._angles)
        parent.onRotation(rotation)
        return

    def __init__(self, document, attributes):
        super(Rotation, self).__init__(document, attributes)
        self._angles = self._parse(attributes["angles"])
        return

