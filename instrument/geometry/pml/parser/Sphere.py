#!/usr/bin/env python
#
# Jiao Lin <jiao.lin@gmail.com>
#

from pyre.geometry.pml.parser.Sphere import Sphere as base
import instrument.geometry.shapes as shapes

class Sphere( base ):

    def notify(self, parent):
        sphere = shapes.sphere(radius=self._radius)
        parent.onSphere(sphere)
        return


# End of file 
