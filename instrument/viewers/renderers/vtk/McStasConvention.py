#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2006 All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

"""
renderer of shapes that are typical of neutron components.
This renderer uses vtk.

This renderer concerns with McStas convention.
"""


import journal
debug = journal.debug('instrument.viewers.renderers.McStasConvention')


from .Base import VTKRenderer as Base, ModelConventionAdaptor as MCBase
class VTKRenderer(Base):


    def __init__(self, modelConventionAdaptor = None):
        if modelConventionAdaptor == None: modelConventionAdaptor = ModelConventionAdaptor()
        Base.__init__(self, modelConventionAdaptor)
        return


    #In McStas convention, orientations are specified by 
    # rotate x degree by mcstas x axis
    # rotate y degree by mcstas y axis
    # rotate z degree by mcstas z axis
    def _addRotations( self, actor, orientation ):
        x,y,z = orientation
        actor.RotateX( x )
        actor.RotateY( y )
        actor.RotateZ( z )
        return


    def _toVTKconvention(self, position, orientation):
        from .mcstasRotation import toAngles
        rotations = toAngles( orientation, unit = 'deg')
        return position, rotations


    pass # end of VTKRenderer
        


class ModelConventionAdaptor(MCBase):

    def onSphereShell(self, sphereShell):
        #in vtk z is the direction out of plane. x is horizontal in the plane.
        #y point up.
        #in vtk a sphere is defined with z pointing to north pole
        #we need to rotate the sphere to match mcstas convention, in which mcstas y
        #is north pole.
        #rotate around x by 90 deg will bring z to y, and y to -z.

        #x should be in the opposite direction of original z
        #so we need to rotate 90 deg by the new z
        return [ ('x',-90), ('z',90) ]

    pass # end of ModelConventionAdaptor


# version
__id__ = "$Id: McStasConvention.py 7 2006-04-14 16:57:01Z jiao $"

# End of file 
