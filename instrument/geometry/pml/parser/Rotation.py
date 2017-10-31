from pyre.geometry.pml.parser.AbstractNode import AbstractNode
import instrument.geometry.operations as ops


class Rotation(AbstractNode):


    tag = "rotation"


    def notify(self, parent):
        rotation = ops.rotate(self._body, angles=self._angles)
        parent.onRotation(rotation)
        return


    def __init__(self, document, attributes):
        AbstractNode.__init__(self, attributes)
        self._angles = self._parse(attributes["angles"])
        return


    def onBody(self, body):
        self._body = body
        return

    onBlock = onBody
