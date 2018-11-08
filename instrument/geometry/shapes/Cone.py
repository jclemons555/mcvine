#!/usr/bin/env python
#
# Jiao Lin <jiao.lin@gmail.com>
#


from pyre.geometry.solids.Primitive import Primitive


class Cone(Primitive):

    '''Cone

  Its tip is at origin and is pointing up.

  Its height is its vertical length (parallel to gravity).

  Its base is a circle resting on a horizontal plane.
  '''

    def __init__(self, radius, height):
        self.radius = radius
        self.height = height
        return
    

    def identify(self, visitor):
        return visitor.onCone( self )


    def todict(self):
        b = dict(
            height=str(self.height),
            radius=str(self.radius)
        )
        return dict(cone=b)

    pass # end of Cone


# End of file 
