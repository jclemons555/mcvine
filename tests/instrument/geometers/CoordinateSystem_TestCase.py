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


from instrument.geometers.CoordinateSystem import *

degree = 1.


import unittest, unittestX

class CoordinateSystem_TestCase(unittestX.TestCase):


    def test(self):
        """instrument.geometers.CoordinateSystem: InstrumentScientistCS2McStasCS
        """
        p, r = InstrumentScientistCS2McStasCS( (0,0,0), (0,0,0) )
        self.assertVectorAlmostEqual( p, (0,0,0) )
        self.assertVectorAlmostEqual( r, (0*degree,0*degree,0*degree) )
        
        p, r = InstrumentScientistCS2McStasCS( (0,0,33), (0,0,0) )
        self.assertVectorAlmostEqual( p, (0,33,0) )
        self.assertVectorAlmostEqual( r, (0*degree,0*degree,0*degree) )

        p, r = InstrumentScientistCS2McStasCS( (0,33,0), (0,0,0) )
        self.assertVectorAlmostEqual( p, (33,0,0) )
        self.assertVectorAlmostEqual( r, (0*degree,0*degree,0*degree) )

        p, r = InstrumentScientistCS2McStasCS( (33,0,0), (0,0,0) )
        self.assertVectorAlmostEqual( p, (0,0,33) )
        self.assertVectorAlmostEqual( r, (0*degree,0*degree,0*degree) )

        p, r = InstrumentScientistCS2McStasCS( (0,0,0), (33*degree,0,0) )
        self.assertVectorAlmostEqual( p, (0,0,0) )
        self.assertVectorAlmostEqual( r, (0*degree,0*degree,33*degree) )

        p, r = InstrumentScientistCS2McStasCS( (0,0,0), (0,33*degree,0) )
        self.assertVectorAlmostEqual( p, (0,0,0) )
        self.assertVectorAlmostEqual( r, (33*degree,0*degree,0*degree) )

        p, r = InstrumentScientistCS2McStasCS( (0,0,0), (0,0,33*degree) )
        self.assertVectorAlmostEqual( p, (0,0,0) )
        self.assertVectorAlmostEqual( r, (0*degree,33*degree,0*degree) )

        p, r = InstrumentScientistCS2McStasCS( (0,0,0), (0,44*degree,33*degree) )
        self.assertVectorAlmostEqual( p, (0,0,0) )
        self.assertVectorAlmostEqual( r, (44*degree,33*degree,0*degree) )
        
        p, r = InstrumentScientistCS2McStasCS( (0,0,0), (90*degree,90*degree,0) )
        self.assertVectorAlmostEqual( p, (0,0,0) )
        self.assertVectorAlmostEqual( r, (0*degree,-90*degree,90*degree) )

        p, r = InstrumentScientistCS2McStasCS( (0,0,0), (90*degree,0,90*degree) )
        self.assertVectorAlmostEqual( p, (0,0,0) )
        self.assertVectorAlmostEqual( r, (90*degree,0*degree,90*degree) )
        
        p, r = InstrumentScientistCS2McStasCS( (0,0,0), (0,90*degree,90*degree) )
        self.assertVectorAlmostEqual( p, (0,0,0) )
        self.assertVectorAlmostEqual( r, (0*degree,90*degree,-90*degree) )
        
        return


    pass # end of CoordinateSystem_TestCase


import unittest

def pysuite():
    suite1 = unittest.makeSuite(CoordinateSystem_TestCase)
    return unittest.TestSuite( (suite1,) )



def main():
    import journal
    pytests = pysuite()
    alltests = unittest.TestSuite( (pytests, ) )
    unittest.TextTestRunner(verbosity=2).run(alltests)
    return


if __name__ == '__main__': main()



# version
__id__ = "$Id$"

# End of file 

