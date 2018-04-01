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


from pyre.geometry.solids.Cylinder import Cylinder as Base


class Cylinder(Base):

    '''Cylinder

  Its axis is vertical.

  Attributes:
    - radius
    - height
  '''

    def identify(self, visitor):
        return visitor.onCylinder( self )

    def todict(self):
        return dict(cylinder=dict(radius=str(self.radius), height=str(self.height)))

    pass # end of Cylinder


# version
__id__ = "$Id$"

# Generated automatically by PythonMill on Wed Sep 26 13:07:18 2007

# End of file 
