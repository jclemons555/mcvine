
class CompositionExtension:

    def _onBody(self, body):
        self._setOperand(body)
        return

    onHollowCylinder = onSphereShell = _onBody
