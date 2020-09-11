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


from .AbstractNode import AbstractNode, debug


class Copy(AbstractNode):


    tag = "Copy"

    from instrument.elements.Copy import Copy as ElementFactory 

    pass # end of Copy
    

# version
__id__ = "$Id: Copy.py,v 1.1.1.1 2005/03/08 16:13:43 linjiao Exp $"

# End of file 
