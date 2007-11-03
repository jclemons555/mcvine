#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                 Jiao Lin   
#                      California Institute of Technology
#                      (C)   2007    All Rights Reserved
#
# <LicenseText>
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from pyre.geometry.pml.parser.AbstractNode import AbstractNode
import instrument.geometry.shapes as shapes


class Block(AbstractNode):

    tag = "block"

    def notify(self, parent):
        block = shapes.block(
            width = self._width,
            height = self._height,
            thickness = self._thickness,
            )
        parent.onBlock(block)
        return


    def __init__(self, document, attributes):
        AbstractNode.__init__(self, attributes)
        self._width = self._parse(attributes["width"])
        self._height = self._parse(attributes["height"])
        self._thickness = self._parse(attributes["thickness"])
        return


# version
__id__ = "$Id: Geometer.py,v 1.1.1.1 2005/03/08 16:13:43 linjiao Exp $"

# End of file 
