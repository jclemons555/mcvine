#!/usr/bin/env python
#
# Jiao Lin <jiao.lin@gmail.com>
#

#! needs revisions to match Base.py

"""
renderer of shapes that are typical of neutron components.
This renderer uses vtk.

The convention that is concerned by this module is the simulated data
go through reduction code. The simulated data follows McStas convention,
so the orientations of the banks and tubes are specified by three rotation
angles around x,y,z.

When data goes through reduction package, the coordinate
system changes.

In McStas,

  z -> neutron beam
  y -> inverse gravity

In reduction,

  x -> neutron beam
  z -> inverse gravity

The positions are specified in the reduction coords system. The orientations
are specified in the reduction coords system too, but rotation sequence
is tricky. Please take a look at method _addRotations
"""


import journal
debug = journal.debug('VTKShapeRenderer')


from Base import VTKShapeRenderer as Base, ModelCoordinator as MCBase
class VTKShapeRenderer(Base):

    def __init__(self, modelCoordinator = None):
        if modelCoordinator == None: modelCoordinator = ModelCoordinator()
        Base.__init__(self, modelCoordinator)
        return


    # the rotation sequence was specified using McStas convention, which is
    # rotate x degree by mcstas x axis
    # rotate y degree by mcstas y axis
    # rotate z degree by mcstas z axis
    # now that the coordinate system has changed, we better be careful here.
    # the coordinate system now is
    # x - mcstas z
    # y - mcstas x
    # z - mcstas y
    def _addRotations( self, actor, orientation ):
        x,y,z = orientation
        actor.RotateY( y )
        actor.RotateZ( z )
        actor.RotateX( x )
        return


    def _toVTKconvention(self, position, orientation):
        return position, orientation


    pass # end of VTKShapeRenderer
        


class ModelCoordinator(MCBase):

    #cylinder in vtk has an axis along y. but we want the cylinder to be along z
    #rotation of 90 degrees by x axis will solve this problem
    def onCylinder(self, cylinder):
        return [('x',90)]

    pass # end of ModelCoordinator


# version
__id__ = "$Id: SimuRedConvention.py 3 2006-01-10 08:43:46Z linjiao $"

# End of file 
