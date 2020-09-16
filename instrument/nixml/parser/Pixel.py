#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                 Jiao Lin   
#                      California Institute of Technology
#                      (C)   2007    All Rights Reserved
#
# <LicenseText>
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from .AbstractNode import AbstractNode


class Pixel(AbstractNode):


    tag = "Pixel"
    
    from instrument.elements.Pixel import Pixel as ElementFactory

    pass # end of Pixel
    


# version
__id__ = "$Id: Pixel.py,v 1.1.1.1 2005/03/08 16:13:43 linjiao Exp $"

# End of file 
