#!/usr/bin/env python
#
# Jiao Lin <jiao.lin@gmail.com>
#


from pyre.geometry.solids.Body import Body as Base


class SphereShell(Base):

    '''SphereShell

  It is actually a "difference" of two spheres.

  Attributes:
    - in_radius: inside radius
    - out_radius: outer radius
  '''

    def __init__(self, in_radius, out_radius):
        self.in_radius = in_radius
        self.out_radius = out_radius
        return

    def identify(self, visitor):
        return visitor.onSphereShell( self )

    def todict(self):
        from .Sphere import Sphere
        from ..operations import subtract
        t = subtract(Sphere(self.out_radius), Sphere(self.in_radius))
        return t.todict()

    pass # end of SphereShell

# End of file 
