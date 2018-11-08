#!/usr/bin/env python
#
# Jiao Lin <jiao.lin@gmail.com>
#


from pyre.geometry.pml.parser.AbstractNode import AbstractNode
import instrument.geometry.shapes as shapes

class Cone( AbstractNode ):

    tag = "cone"
    
    def notify(self, parent):
        cone = shapes.cone(
            radius=self._radius,
            height = self._height
            )
        parent.onCone(cone)
        return


    def __init__(self, document, attributes):
        AbstractNode.__init__(self, attributes)
        self._radius = self._parse(attributes["radius"])
        self._height = self._parse(attributes["height"])
        return

# End of file 
