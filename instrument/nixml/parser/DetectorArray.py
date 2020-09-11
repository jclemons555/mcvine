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


class DetectorArray(AbstractNode):


    tag = "DetectorArray"
    
    from instrument.elements.DetectorArray import DetectorArray \
         as ElementFactory

    onCopy = onDetector = onDetectorPack = AbstractNode.onElement

    pass # end of DetectorArray
    


# version
__id__ = "$Id: DetectorArray.py,v 1.1.1.1 2005/03/08 16:13:43 linjiao Exp $"

# End of file 

