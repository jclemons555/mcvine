from pyre.geometry.pml.parser.Rotation import Rotation as base
from .CompositionExtension import CompositionExtension


class Rotation(base, CompositionExtension):

    def onAngle(self, angle):
        self._angle = angle
        return


    def onVector(self, vector):
        self._axis = vector
        return


    def notify(self, parent):
        import instrument.geometry.operations as ops
        rotation = ops.rotate(self._body, angle=self._angle, **self._axis)
        parent.onRotation(rotation)
        return

    def __init__(self, document, attributes):
        super(Rotation, self).__init__(document, attributes)
        return

