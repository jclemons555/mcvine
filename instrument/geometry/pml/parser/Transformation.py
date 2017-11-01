from pyre.geometry.pml.parser.AbstractNode import AbstractNode


class Transformation(AbstractNode):


    def onBody(self, body):
        self._body = body
        return

    onBlock = onCylinder = onSphere \
            = onHollowCylinder = onSphereShell \
            = onUnion = onDifference = onIntersection \
            = onDilation = onReflection = onReversal = onRotation = onTranslation \
            = onBody
