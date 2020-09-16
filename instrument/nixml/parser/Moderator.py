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


class Moderator(AbstractNode):


    tag = "Moderator"

    from instrument.elements.Moderator import Moderator as ElementFactory 

    pass # end of Moderator
    

# version
__id__ = "$Id: Moderator.py,v 1.1.1.1 2005/03/08 16:13:43 linjiao Exp $"

# End of file 
