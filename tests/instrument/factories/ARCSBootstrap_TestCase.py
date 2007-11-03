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


from instrument.factories.ARCSBootstrap import *


import unittest, unittestX

class ARCSBootstrap_TestCase(unittestX.TestCase):


    def test(self):
        """instrument.factories.ARCSBootstrap
        """
        f = 'arcs1810ds0001xls.txt'
        factory = InstrumentFactory( )
        
        from pyre.units.length import meter, inch
        from pyre.units.pressure import atm
        
        long = 10*atm, 128, 0.5*inch, 1.*meter, 0.08*inch
        short = 10*atm, 32, 0.5*inch, 0.25*meter, 0.08*inch
        instrument, geometer = factory.construct(
            f, long, short )
        return


    pass # end of ARCSBootstrap_TestCase


import unittest

def pysuite():
    suite1 = unittest.makeSuite(ARCSBootstrap_TestCase)
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
