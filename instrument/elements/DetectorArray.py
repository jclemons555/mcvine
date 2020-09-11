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


from .ElementContainer import ElementContainer

import journal
debug = journal.debug("instrument.elements")


class DetectorArray( ElementContainer ):
    
    """Container for detector pack objects"""

    allowed_item_types = [
        'DetectorPack',
        'Detector',
        'Copy',
        ]

    def __init__( self, name, shape = None, **attributes):
        ElementContainer.__init__( self, name, shape=shape, **attributes)
        return


    def identify( self, visitor):
        return visitor.onDetectorArray( self)
        return

    pass # end of DetectorArray


# version
__id__ = "$Id$"

# End of file
