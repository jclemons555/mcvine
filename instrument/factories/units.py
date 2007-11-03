#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2007  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

from pyre.units import *
from pyre.units import length, energy, angle, pressure, time


def isdimensional( candidate ):
    'test if the candidate is a quantity with units'
    from pyre.units.unit import unit
    return isinstance( candidate, unit )

# version
__id__ = "$Id$"

# End of file 
