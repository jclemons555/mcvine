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


class GuidGenerator:


    def __init__(self):
        self._idCounter = 0
        return


    reserved = [ -1, 0 ]
    
    
    def getUniqueID( self):
        """getUniqueID() -> id
        get an identifier that is unique for this generator
        Input:
            None
        Output:
            id: integer
        Exceptions: None
        Notes: Right now, just using integers."""
        # idea is constructer of elements requests id, passes it to element's
        # (subclass) ctor. Alternative: addElement() sets the id when it is
        # set. 
        
        # This breaks at ~2,000,000,000 elements...better?
        self._idCounter += 1
        ret = self._idCounter
        if ret in self.reserved: raise RuntimeError
        return ret
    

# version
__id__ = "$Id: Instrument.py 1234 2007-09-18 18:32:56Z linjiao $"

# End of file
