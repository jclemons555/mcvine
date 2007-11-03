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


from AbstractNode import AbstractNode


class DetectorPack(AbstractNode):


    tag = "DetectorPack"
    
    from instrument.elements.DetectorPack import DetectorPack as ElementFactory

    onCopy = onDetector = AbstractNode.onElement

    pass # end of DetectorPack
    


# version
__id__ = "$Id: DetectorPack.py,v 1.1.1.1 2005/03/08 16:13:43 linjiao Exp $"

# End of file 
