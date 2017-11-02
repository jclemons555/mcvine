from pyre.geometry.pml.parser.Dilation import Dilation as base
from .CompositionExtension import CompositionExtension


class Dilation(base, CompositionExtension):

    def notify(self, parent):
        import instrument.geometry.operations as ops
        dilation = ops.dilate(self._body, scale=self._scale)
        parent.onDilation(dilation)
        return

    def __init__(self, document, attributes):
        super(Dilation, self).__init__(document, attributes)
        self._scale = self._parse(attributes["scale"])
        return

