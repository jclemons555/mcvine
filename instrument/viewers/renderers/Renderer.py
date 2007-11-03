#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                       (C) 2006 All Rights Reserved  
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

"""
renderer of shapes that are typical of neutron components.

The target that can be rendered by this renderer will be
a list of 'visual elements'. 

This renderer create visual representation of shapes.
"""


import journal
debug = journal.debug('Renderer')


from geometry.Visitor import Visitor

class Renderer(Visitor):


    def render(self, visual_elements, canvas):
        """render shapes and show them on a canvas"""
        self.coordinate_system = visual_elements.coordinate_system
        self.canvas = canvas
        for ve in visual_elements.elements: self.add(ve)
        return
    
    
    #handles shapes
    def onBox(self, box): self._abstract( "onBox" )


    def onCylinder(self, cylinder): self._abstract( "onCylinder" )
    
    
    # add visual element 
    def add(self, visual_element): self._abstract("add" )
    
    
    def _abstract(self, method):
        raise NotImplementedError , "%s must provide method '%s'" % method
    
    
    pass # end of Renderer


# version
__id__ = "$Id: ShapeRenderer.py 11 2006-04-18 08:07:50Z jiao $"

# End of file 
