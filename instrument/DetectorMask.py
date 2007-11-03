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


from AbstractDetectorMask import AbstractDetectorMask

class DetectorMask(AbstractDetectorMask):

    """holder of mask information

    Currently, data to hold are:

      - excludedDetectors
      - excludedPixels
      - excludedSingles
     
    """

    def __init__(self, excludedDetectors = [], excludedPixels = [], excludedSingles = []):
        self.excludedSingles = excludedSingles
        self.excludedPixels = excludedPixels
        self.excludedDetectors = excludedDetectors
        return


    def include( self, detectorID = None, pixelID = None):
        """does the pixel specified by the 'kwds' included
        in this mask?
        """
        if detectorID is not None and detectorID in self.excludedDetectors: return True

        if pixelID is not None and pixelID in self.excludedPixels: return True

        if detectorID is not None and pixelID is not None and (detectorID, pixelID) in self.excludedSingles: return True

        return False


    def __add__(self, rhs):
        ret = self.__class__()
        ret.excludedSingles = _addList( self.excludedSingles , rhs.excludedSingles )
        ret.excludedDetectors = _addList( self.excludedDetectors , rhs.excludedDetectors )
        ret.excludedPixels = _addList( self.excludedPixels , rhs.excludedPixels )
        return ret
    

    pass # end of DetectorMask


def _addList( l1, l2 ):
    ret = l1
    for i in l2:
        if i in ret: continue
        ret.append( i )
        continue
    return ret


class ApplyMask:

    def __init__(self):
        self._cache = []
        return


    def __call__(self, mask, something):
        if self._applied( mask, something ): return
        self.apply(mask, something)
        self._remember( mask, something )
        return


    def apply(self, mask, something):
        raise NotImplementedError


    def _applied(self, mask, something):
        for m, s in self._cache:
            if m() == mask and s() == something: return True
            continue
        return False


    def _remember(self, mask, something):
        self._cache.append( (weakref( mask ), weakref(something) ) )
        return


    pass # end of ApplyMask


from weakref import ref as weakref


# version
__id__ = "$Id$"

#  End of file 
