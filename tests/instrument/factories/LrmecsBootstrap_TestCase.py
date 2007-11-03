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


from instrument.factories.LrmecsBootstrap import *


import unittest, unittestX

class LrmecsBootstrap_TestCase(unittestX.TestCase):


    def test(self):
        """instrument.factories.LrmecsBootstrap
        """
        f = '../ins-data/Lrmecs/4849'
        factory = InstrumentFactory( )
        instrument, geometer = factory.construct( f )
        return


    def test1(self):
        """instrument.factories.LrmecsBootstrap: geometer
        """
        f = '../ins-data/Lrmecs/4849'
        factory = InstrumentFactory( )
        instrument, geometer = factory.construct( f )
        print geometer.position('detSystem/detector144/pixel0' )
        return


    pass # end of LrmecsBootstrap_TestCase


import unittest

def pysuite():
    suite1 = unittest.makeSuite(LrmecsBootstrap_TestCase)
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
