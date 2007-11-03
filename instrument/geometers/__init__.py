#!/usr/bin/env python
# Timothy M. Kelley Copyright (c) 2005 All rights reserved


## \namespace instrument::geometers
## This subpackage collects geometers
##
## All geometers are subclasses of Geometer.Geometer. They are responsible
## for keeping track of positions and orientations of elements in an instrument,
## and measurements of displacements between elements.

def instrumentGeometer(
    target, local_geometers,
    registry_coordinate_system = "InstrumentScientist",
    **kwds ):
    
    cs = _name2cs( registry_coordinate_system )
    from InstrumentGeometer import InstrumentGeometer
    return InstrumentGeometer(
        target, local_geometers, registry_coordinate_system = cs, **kwds )


def geometer( target, registry_coordinate_system = 'InstrumentScientist',
              **kwds ):
    cs = _name2cs( registry_coordinate_system )
    from Geometer import Geometer
    return Geometer( target, registry_coordinate_system = cs, **kwds )


# following are specific instrument geometers
# they must have a name that match to the class name
# arcs -- ARCSGeometer
# <something> -- <something>Geometer
def arcs( target, local_geometers = [],
          registry_coordinate_system = 'InstrumentScientist',
          **kwds ):
    cs = _name2cs( registry_coordinate_system )
    from ARCSGeometer import ARCSGeometer
    return ARCSGeometer(
        target, local_geometers, registry_coordinate_system = cs, **kwds )


def coordinateSystem( name ):
    '''coordinateSystem(name) --> prebuilt coordinate system of given name
    '''
    return _name2cs( name )


def _name2cs( name ):
    from CoordinateSystem import coordinateSystem
    return coordinateSystem( name )

from _journal import debug

# version
__id__ = "$Id$"

# End of file

