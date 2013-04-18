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


from instrument.factories.ARCSBootstrap_mantid_idf import *


import unittest

class ARCSBootstrap_TestCase(unittest.TestCase):


    def test(self):
        """instrument.factories.ARCSBootstrap_mantid_idf
        """
        f = 'arcs-mantid-idf.xml'
        factory = InstrumentFactory()
        instrument, geometer = factory.construct(f)
        return


    pass # end of ARCSBootstrap_TestCase


import unittest
if __name__ == '__main__': unittest.main()



# version
__id__ = "$Id$"

# End of file 
