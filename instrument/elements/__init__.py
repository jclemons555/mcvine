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


def instrument( *args, **kwds ):
    from .Instrument import createInstrument
    return createInstrument( *args, **kwds )

def moderator( *args, **kwds ):
    from .Moderator import createNormalModerator
    return createNormalModerator( *args, **kwds )

def monitor( *args, **kwds ):
    from .Monitor import createNormalMonitor
    return createNormalMonitor( *args, **kwds )

def guide(*args, **kwds):
    from .Guide import createRectangularGuide
    return createRectangularGuide( *args, **kwds )

def detectorSystem(*args, **kwds):
    from .DetectorSystem import DetectorSystem
    return DetectorSystem( *args, **kwds )

def detectorArray(*args, **kwds):
    from .DetectorArray import DetectorArray
    return DetectorArray( *args, **kwds )

def detectorPack(*args, **kwds):
    from .DetectorPack import DetectorPack
    return DetectorPack( *args, **kwds )

def detector(*args, **kwds):
    from .Detector import createDetector
    return createDetector(*args, **kwds)

def pixel(*args, **kwds):
    from .Pixel import createPixel
    return createPixel( *args, **kwds )

def sample(*args, **kwds):
    from .Sample import Sample
    return Sample( *args, **kwds )


def copy(name, reference, **kwds):
    from .Copy import createCopy
    return createCopy(name, reference, **kwds)


from ._journal import debug

# version
__id__ = "$Id$"

# End of file 
