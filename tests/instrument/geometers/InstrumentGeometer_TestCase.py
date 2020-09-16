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


import unittest, unittestX

class InstrumentGeometer_TestCase(unittestX.TestCase):


    def test1(self):
        """instrument.geometers.InstrumentGeometer: layered structure. check rotations on vector
        """
        from instrument.nixml import parse_file
        instrument = parse_file( 'InstrumentGeometer-test1.xml' )

        geometer = instrument.geometer

        det1position = geometer.position( 'detectorSystem/detPack1/det1' )

        from numpy import array, sqrt
        from pyre.units.length import meter
        det1position/=meter

        packCenter = array( [ sqrt(3)/2, 1./2, 0 ] )
        det1offset = array( [ -1./2, sqrt(3)/2, 0] ) * 0.3
        expected = packCenter+det1offset

        print(det1position, expected)
        self.assertVectorAlmostEqual( det1position, expected )
        return


    def test2(self):
        'instrument.geometer.InstrumentGeometer: layered structure. check orientation'
        from instrument.nixml import parse_file
        instrument = parse_file( 'InstrumentGeometer-test2.xml' )

        geometer = instrument.geometer

        self.assertVectorAlmostEqual(
            geometer.orientation('detectorSystem'),
            (0*degree,0*degree,90*degree) 
            )
        self.assertVectorAlmostEqual(
            geometer.orientation('detectorSystem/detPack1'),
            (0*degree,90*degree,90*degree) 
            )
        print(geometer.orientation('detectorSystem/detPack1/det1'))
        self.assertVectorAlmostEqual(
            geometer.orientation('detectorSystem/detPack1/det1'),
            (-90*degree,0*degree,180*degree) 
            )
        return


    pass # end of InstrumentGeometer_TestCase


from pyre.units.angle import degree

import unittest

def pysuite():
    suite1 = unittest.makeSuite(InstrumentGeometer_TestCase)
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
