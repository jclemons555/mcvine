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


from instrument.factories.FakeInstrument import *


import unittest, unittestX


class FakeInstrument_TestCase(unittestX.TestCase):


    def test(self):
        """instrument.factories.FakeInstrument
        """
        factory = InstrumentFactory( )
        instrument, geometer = factory.construct( )
        return


    pass # end of FakeInstrument_TestCase


import unittest

def pysuite():
    suite1 = unittest.makeSuite(FakeInstrument_TestCase)
    return unittest.TestSuite( (suite1,) )



def main():
    import journal
    
    from instrument.factories import debug
    debug.activate()
    
    from instrument.elements import debug
    #debug.activate()
    
    pytests = pysuite()
    alltests = unittest.TestSuite( (pytests, ) )
    unittest.TextTestRunner(verbosity=2).run(alltests)
    return


if __name__ == '__main__': main()



# version
__id__ = "$Id$"

# End of file 
