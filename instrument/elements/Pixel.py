#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2006  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from .Element import Element, debug


class Pixel( Element ):

    class Attributes(Element.Attributes):
        
        from . import Attribute
        solidAngle = Attribute.float( 'solidAngle', default = 1.0 )
        pass # end of Attributes
    

    def __init__( self, name, shape=None, **attributes):
        if shape is None: shape = defaultShape
        Element.__init__( self, name, shape=shape, **attributes)
        return


    def identify( self, visitor):
        return visitor.onPixel( self)

    pass # end of Pixel


import instrument.geometry.shapes as shapes
from . import units
cm = units.length.cm

defaultShape = shapes.cylinder( 1.25*cm, 2.5*cm )  #unit: cm # should we put unit in there?


def createPixel( name, radius = 1.25*cm, height = 2.5*cm, **attributes ):
    shape = shapes.cylinder( radius, height )
    return Pixel( name, shape = shape, **attributes )


def main():
    createPixel( 'pixel', guid = 10, radius=2.5, height = 2 )
    return

if __name__ == '__main__': main()

    
# version
__id__ = "$Id: Pixel.py 1238 2007-09-20 11:50:47Z linjiao $"

# End of file
