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


from numpy import array
from pyre.units.length import m


import unittest


from unittestX import TestCase
class parser_TestCase(TestCase):


    def test0(self):
        """
        instrument.nixml.parser
        """
        from instrument.nixml import parse_file
        instrument = parse_file( 'test0.xml' )
        pos = instrument.geometer.position(
            "detectorSystem/det1" )
        print pos
        pos = array(pos)/m
        self.assertVectorAlmostEqual(pos, (0.3, 0., 4) )
        return


    def test(self):
        """
        instrument.nixml.parser
        """
        from instrument.nixml import parse_file
        instrument = parse_file( 'test.xml' )
        from instrument.elements.Instrument import Instrument
        self.assert_( isinstance(instrument, Instrument) )
        pos = instrument.geometer.position(
            "detectorSystem/detArray1/detPack1/det1/pix2" )
        pos = array(pos)/m
        self.assertVectorAlmostEqual(pos, (0.3, 0.1, 9) )
        return


    def test2(self):
        """
        instrument.nixml.parser: Instrument Scientist Coordinate System
        """
        from instrument.nixml import parse_file
        instrument = parse_file( 'test2.xml' )
        return
    

    def test3(self):
        """
        instrument.nixml.parser: Instrument Scientist Coordinate System
        """
        from instrument.nixml import parse_file
        instrument = parse_file( 'test-InstrumentScientistCS.xml' )
        from instrument.elements.Instrument import Instrument
        self.assert_( isinstance(instrument, Instrument) )
        pos = instrument.geometer.position(
            "detectorSystem/detArray1/detPack1/det1/pix2" )
        pos = array(pos)/m
        self.assertVectorAlmostEqual(pos, (9, 0.3, 0.1) )
        return


    pass # end of parser_TestCase


import unittest

def pysuite():
    suite1 = unittest.makeSuite(parser_TestCase)
    return unittest.TestSuite( (suite1,) )



def main():
    import journal
    from instrument.elements import debug
    debug.activate()
    pytests = pysuite()
    alltests = unittest.TestSuite( (pytests, ) )
    unittest.TextTestRunner(verbosity=2).run(alltests)
    return


if __name__ == '__main__': main()
    

# version
__id__ = "$Id: parser_TestCase.py 1264 2007-06-04 17:56:50Z linjiao $"

# End of file 
