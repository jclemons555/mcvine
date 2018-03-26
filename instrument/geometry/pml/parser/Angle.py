from pyre.geometry.pml.parser.Angle import Angle as base

class Angle(base):

    def notify(self, parent):
        value = self._parse(self._angle.strip())
        parent.onAngle(value)
        return
