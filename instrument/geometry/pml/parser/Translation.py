from pyre.geometry.pml.parser.Translation import Translation as base
from .CompositionExtension import CompositionExtension


class Translation(base, CompositionExtension):

    def notify(self, parent):
        import instrument.geometry.operations as ops
        translation = ops.translate(self._body, vector=self._vector)
        parent.onTranslation(translation)
        return

    def __init__(self, document, attributes):
        super(Translation, self).__init__(document, attributes)
        self._vector = self._parse(attributes["vector"])
        return

