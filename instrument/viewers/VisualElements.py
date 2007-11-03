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

class VisualElements:

    """data structure to hold a list of visual elements.
    The information about coordinate system is also kept
    """

    def __init__(self, coordinate_system, elements = None):
        self.coordinate_system = coordinate_system
        if elements is None: elements = []
        self.elements = elements
        return


    def add(self, element):
        self.elements.append( element )
        return


    def __str__(self):
        return "%s:%s" % (self.coordinate_system, self.elements)

    pass # end of VisualElements
        

# version
__id__ = "$Id$"

# End of file 

