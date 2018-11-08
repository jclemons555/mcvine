#!/usr/bin/env python
#
# Jiao Lin <jiao.lin@gmail.com>
#


#shapes in this directory have slight difference from shapes in
#pyre.geometry.solids. A shape here is placed into neutron beam,
#and its orientation (without any rotation) is defined by its
#orientation about the neutron beam.

def hollowCylinder(*args, **kwds):
    from .HollowCylinder import HollowCylinder
    return HollowCylinder( *args, **kwds )

def sphereShell(*args, **kwds):
    from .SphereShell import SphereShell
    return SphereShell( *args, **kwds )

def cylinder(*args, **kwds):
    from .Cylinder import Cylinder
    return Cylinder( *args, **kwds )

def pyramid(*args, **kwds):
    from .Pyramid import Pyramid
    return Pyramid( *args, **kwds )

def cone(*args, **kwds):
    from .Cone import Cone
    return Cone( *args, **kwds )

def sphere(*args, **kwds):
    from .Sphere import Sphere
    return Sphere( *args, **kwds )

def block(*args, **kwds):
    from .Block import Block
    return Block( *args, **kwds )
plate = block

def rectTube(*args, **kwds):
    from .RectTube import RectTube
    return RectTube( *args, **kwds )


def isshape( candidate ):
    'test if the candidate is a shape'
    from pyre.geometry.solids.Body import Body
    return isinstance( candidate, Body )


# End of file 
