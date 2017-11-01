from .Transformation import Transformation
import instrument.geometry.operations as ops


class Rotation(Transformation):


    tag = "rotation"


    def notify(self, parent):
        rotation = ops.rotate(self._body, angles=self._angles)
        parent.onRotation(rotation)
        return


    def __init__(self, document, attributes):
        super(Rotation, self).__init__(attributes)
        self._angles = self._parse(attributes["angles"])
        return

