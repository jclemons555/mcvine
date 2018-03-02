#!/usr/bin/env python
#
# Jiao Lin <jiao.lin@gmail.com>
#


from pyre.geometry.solids.Primitive import Primitive


class Pyramid(Primitive):

    '''Pyramid

  Its height is its vertical length (parallel to gravity).

  Its base is a rectangle resting on the xy plane.
  '''

    def __init__(self, thickness, width, height):
        self.thickness = thickness
        self.width = width
        self.height = height
        return
    

    def identify(self, visitor):
        return visitor.onPyramid( self )

    pass # end of Pyramid


# End of file 
