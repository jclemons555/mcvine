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

class VisualElement:
    
    def __init__(self, position, orientation, shape, color, opacity):
        self.position = position
        self.orientation = orientation
        self.shape = shape
        self.color = color
        self.opacity = opacity
        return

    pass #end of VisualElement


# version
__id__ = "$Id$"

# End of file 
