#!/usr/bin/env python
#
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 
#                               Michael A.G. Aivazis
#                        California Institute of Technology
#                        (C) 1998-2005 All Rights Reserved
# 
#  <LicenseText>
# 
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

import instrument.geometry.shapes as shapes
from pyre.geometry.pml.parser.AbstractNode import AbstractNode


class RectTube(AbstractNode):

    tag = "rectTube"


    def notify(self, parent):
        rectTube = shapes.rectTube(
            self._front, self._length, self._back)
        parent.onRectTube(rectTube)
        return


    def __init__(self, document, attributes):
        AbstractNode.__init__(self, attributes)
        self._front = self._parse(attributes["front"])
        self._back = self._parse(attributes["back"])
        self._length = self._parse(attributes["length"])
        return


# version
__id__ = "$Id: RectTube.py,v 1.1.1.1 2005/03/08 16:13:45 aivazis Exp $"

# End of file
