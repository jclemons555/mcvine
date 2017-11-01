from .Transformation import Transformation
import instrument.geometry.operations as ops


class Translation(Transformation):


    tag = "translation"


    def notify(self, parent):
        translation = ops.translate(self._body, vector=self._vector)
        parent.onTranslation(translation)
        return


    def __init__(self, document, attributes):
        super(Translation, self).__init__(attributes)
        self._vector = self._parse(attributes["vector"])
        return

