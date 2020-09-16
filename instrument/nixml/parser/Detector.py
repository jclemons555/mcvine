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


class Detector(AbstractNode):


    tag = "Detector"
    
    from instrument.elements.Detector import Detector as ElementFactory

    onCopy = onPixel = AbstractNode.onElement

    pass # end of Detector
    


# version
__id__ = "$Id: Detector.py,v 1.1.1.1 2005/03/08 16:13:43 linjiao Exp $"

# End of file 
