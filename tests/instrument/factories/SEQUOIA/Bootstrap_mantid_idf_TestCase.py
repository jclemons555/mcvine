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


from instrument.factories.SEQUOIA.Bootstrap_mantid_idf import *


import unittest

class TestCase(unittest.TestCase):
    
    
    def test(self):
        """instrument.factories.SEQUOIA.Bootstrap_mantid_idf
        """
        f = 'sequoia-mantid-idf.xml'
        factory = InstrumentFactory()
        instrument, geometer = factory.construct(f)
        return


    pass # end of TestCase


import unittest
if __name__ == '__main__': unittest.main()



# version
__id__ = "$Id$"

# End of file 
