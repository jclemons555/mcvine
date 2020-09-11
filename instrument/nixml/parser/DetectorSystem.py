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


class DetectorSystem(AbstractNode):


    tag = "DetectorSystem"
    
    from instrument.elements.DetectorSystem import DetectorSystem as ElementFactory

    onCopy = onDetector = onDetectorPack = onDetectorArray = AbstractNode.onElement

    pass # end of DetectorSystem
    


# version
__id__ = "$Id: DetectorSystem.py,v 1.1.1.1 2005/03/08 16:13:43 linjiao Exp $"

# End of file 
