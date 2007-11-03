#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2007 All Rights Reserved  
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from instrument.geometry import shapes
from Sample import Sample


def vanadiumPlate( width, height, thickness ):
    '''create a vanadium plate sample

    all inputs must have units attached
    '''
    plate = shapes.plate( width, height, thickness )
    ret = Sample( name='vanadium', shape = plate )
    return ret


# version
__id__ = "$Id$"

# End of file 
