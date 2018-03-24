#!/usr/bin/env python
#
# Jiao Lin <jiao.lin@gmail.com>
#

from pyre.geometry.solids.Sphere import Sphere as Base


class Sphere(Base):

    '''Sphere

  Attributes:
    - radius
  '''

    def identify(self, visitor):
        return visitor.onSphere( self )

    pass # end of Sphere


# End of file 
