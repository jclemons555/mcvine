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


class Moderator( Element ):

    class Attributes(Element.Attributes):
        
        from . import Attribute
        type = Attribute.str( "type", default = "")
        type.meta['tip'] = "moderator type" 

        pass # end of Attributes
    

    def __init__( self, name, shape=None, **attributes):
        if shape is None: shape = defaultShape

        Element.__init__( self, name, shape=shape, **attributes)
        return


    def identify( self, visitor):
        return visitor.onModerator( self)

    pass # end of Moderator


import instrument.geometry.shapes as shapes

from . import units
cm = units.length.cm
defaultShape = shapes.block( 10*cm,10*cm,2*cm )

def createNormalModerator( name, width, height, thickness, type = "", **attributes):
    shape = shapes.block( width, height, thickness )
    return Moderator( name, shape = shape, type = type, **attributes )


def main():
    createNormalModerator( 'moderator', 10, 10, 2 )
    createNormalModerator( 'moderator', 10, 10, 2, guid = 3 )
    return

if __name__ == '__main__': main()

    
# version
__id__ = "$Id$"

# End of file
