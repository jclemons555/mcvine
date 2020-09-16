#!/usr/bin/env python
# Timothy M. Kelley Copyright (c) 2005 All rights reserved

class DetPackFactory( object):
    """Constructor of DetectorArray graph object"""

    def construct( self, detectorPackDict, instrument, **kwds):
        """Construct detector packs from dictionaries, add to array"""
        msg = "%s must override construct() method" % self.__class__.__name__
        raise NotImplementedError(msg)
    

    def __init__( self, *args, **kwds):
        # keyz = ['detFactory', 'pixelFactory']

        detFactory = kwds['detFactory']
        pixelFactory = kwds['pixelFactory']

        self._detFactory = detFactory
        self._pixelFactory = pixelFactory
        
        return


# version
__id__ = "$Id$"

# End of file
