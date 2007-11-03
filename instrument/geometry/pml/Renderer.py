#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                Jiao Lin
#                      California Institute of Technology
#                      (C)    2007   All Rights Reserved
#
# <LicenseText>
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#



from pyre.geometry.pml.Renderer import Renderer as base 


class Renderer(base):

    def onHollowCylinder(self, hollowCylinder):
        self._printDocs( hollowCylinder)
        s  = '<hollowCylinder in_radius="%s" out_radius="%s" height="%s"/>' %(
            hollowCylinder.in_radius, hollowCylinder.out_radius,
            hollowCylinder.height)
        self._write(s )
        return
    

    def onCylinder(self, cylinder):
        self._printDocs( cylinder)
        base.onCylinder(self, cylinder)
        return
    

    def onBlock(self, block):
        self._printDocs( block)
        s  = '<block width="%s" height="%s" thickness="%s"/>' %(
            block.width, block.height, block.thickness)
        self._write(s )
        return
    

    def onRectTube(self, rectTube):
        self._printDocs( rectTube )
        s = '<rectTube front="%s,%s" back="%s,%s" length="%s"/>' %(
            rectTube._fr_width, rectTube._fr_height,
            rectTube._bk_width, rectTube._bk_height,
            rectTube._length,
            )
        self._write( s )
        return
    

    def _printDocs(self, element):
        self._write('<!--')
        self._write(element.__class__.__doc__)
        self._write('-->')
        return

    pass # end of Renderer


# version
__id__ = "$Id$"

# End of file 
