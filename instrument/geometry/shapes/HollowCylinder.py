#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2007  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from pyre.geometry.solids.Body import Body as Base


#hollow cylinder is quite common in shapes of instrument components
#so I give it a place here, although it is not a primitive.

class HollowCylinder(Base):

    '''HollowCylinder

  Its axis is vertical.

  It is actually a "difference" of two cylinders.

  Attributes:
    - in_radius: inside radius
    - out_radius: outer radius
    - height
  '''

    def __init__(self, in_radius, out_radius, height ):
        self.in_radius = in_radius
        self.out_radius = out_radius
        self.height = height
        return

    def identify(self, visitor):
        return visitor.onHollowCylinder( self )

    pass # end of Cylinder


# version
__id__ = "$Id$"

# Generated automatically by PythonMill on Wed Sep 26 13:07:18 2007

# End of file 
