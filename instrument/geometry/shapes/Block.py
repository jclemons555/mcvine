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


from pyre.geometry.solids.Primitive import Primitive


class Block(Primitive):

    '''Block

  Its thickness is the length of the dimension that is parallel
  to neutron beam.
  
  Its height is its vertical length (parallel to gravity).

  Its width is the 3rd dimension.
  '''

    def __init__(self, width, height, thickness):
        self.width = width
        self.height = height
        self.thickness = thickness
        return
    

    def identify(self, visitor):
        return visitor.onBlock( self )


    def __str__(self):
        return "block(width=%s, height=%s, thickness=%s)" % (
            self.width, self.height, self.thickness)

    pass # end of Block


# End of file 
