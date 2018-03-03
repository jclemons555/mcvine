#!/usr/bin/env python
#
# Jiao Lin <jiao.lin@gmail.com>
#


from pyre.geometry.pml.parser.AbstractNode import AbstractNode
import instrument.geometry.shapes as shapes

class Pyramid( AbstractNode ):

    tag = "pyramid"
    
    def notify(self, parent):
        pyramid = shapes.pyramid(
            thickness=self._thickness,
            width = self._width,
            height = self._height
            )
        parent.onPyramid(pyramid)
        return


    def __init__(self, document, attributes):
        AbstractNode.__init__(self, attributes)
        self._thickness = self._parse(attributes["thickness"])
        self._width = self._parse(attributes["width"])
        self._height = self._parse(attributes["height"])
        return

# End of file 
