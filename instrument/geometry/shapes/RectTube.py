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


class RectTube(Primitive):

    """
    a shape that represents a tube with rectangular openinngs.
    It is useful to describe a neutron guide.
    """

    def __init__(self, front, length, back):
        self._fr_width, self._fr_height = front
        self._length = length
        self._bk_width, self._bk_height = back
        return


    def frontVertexes(self):
        w,h = self._fr_width, self._fr_height
        hw = w/2.
        hh = h/2.
        leftup = hw, hh, 0
        rightup = -hw, hh, 0
        leftdown = hw, -hh, 0
        rightdown = -hw, -hh, 0
        return leftup, rightup, leftdown, rightdown
        

    def backVertexes(self):
        w,h = self._bk_width, self._bk_height
        l = self._length
        hw = w/2.
        hh = h/2.
        leftup = hw, hh, l
        rightup = -hw, hh, l
        leftdown = hw, -hh, l
        rightdown = -hw, -hh, l
        return leftup, rightup, leftdown, rightdown


    def identify(self, visitor, *args, **kwds):
        return visitor.onRectTube( self, *args, **kwds )
        

    pass # end of RectTube


#from geometry.shapes.RectTube import RectTube as base
base = RectTube


class RectTube(base):

    '''Rectangular tube

 Its axis lies in the neutron beam.

 It is a tube that is rectangular at both ends.

 The attributes 'front' and 'back' give the
 width and height of the front opening and back opening.

 'Front' is hit by neutrons earlier than 'back'.

 The length of the tube is given the attribute 'length'.
 '''

    def identify(self, visitor):
        return visitor.onRectTube( self )

    pass # end of RectTube


# version
__id__ = "$Id$"

# Generated automatically by PythonMill on Wed Sep 26 13:07:18 2007

# End of file 
