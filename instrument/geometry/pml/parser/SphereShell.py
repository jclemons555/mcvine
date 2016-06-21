#!/usr/bin/env python
#
# Jiao Lin <jiao.lin@gmail.com>
#

import instrument.geometry.shapes as shapes
from pyre.geometry.pml.parser.AbstractNode import AbstractNode


class SphereShell(AbstractNode):

    tag = "sphereShell"


    def notify(self, parent):
        sphereShell = shapes.sphereShell(
            self._in_radius, self._out_radius, self._height)
        parent.onSphereShell(sphereShell)
        return


    def __init__(self, document, attributes):
        AbstractNode.__init__(self, attributes)
        self._in_radius = self._parse(attributes["in_radius"])
        self._out_radius = self._parse(attributes["out_radius"])
        self._height = self._parse(attributes["height"])
        return


# version
__id__ = "$Id: RectTube.py,v 1.1.1.1 2005/03/08 16:13:45 aivazis Exp $"

# End of file
