#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#              (C) 2006 All Rights Reserved  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


#!!! needs revisions to match new Base.py

"""
renderer of shapes that are typical of neutron components.
This renderer uses vtk.

The convention that is concerned by this module is normal convention
adopted by reduction codes.

In reduction,

  x -> neutron beam
  z -> inverse gravity

"""


import journal
debug = journal.debug('VTKShapeRenderer')


from .Base import VTKShapeRenderer as Base, ModelCoordinator as MCBase
class VTKShapeRenderer(Base):

    def __init__(self, modelCoordinator = None):
        if modelCoordinator == None: modelCoordinator = ModelCoordinator()
        Base.__init__(self, modelCoordinator)
        return


    def _toVTKconvention(self, position, orientation):
        return position, orientation


    pass # end of VTKShapeRenderer
        


class ModelCoordinator(MCBase):

    pass # end of ModelCoordinator


# version
__id__ = "$Id: SimuRedConvention.py 3 2006-01-10 08:43:46Z linjiao $"

# End of file 
