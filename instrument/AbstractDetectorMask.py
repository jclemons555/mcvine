#!/usr/bin/env python
# 
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 
#                                    Jiao Lin
#                        California Institute of Technology
#                        (C) 2004-2007  All Rights Reserved
# 
#  <LicenseText>
# 
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#



class AbstractDetectorMask:

    """holder of mask information
    """

    def include( self, *args):
        """does the pixel specified by the 'args' included
        in this mask?
        """
        raise NotImplementedError
        
    pass # end of DetectorMask


# version
__id__ = "$Id$"

#  End of file 
