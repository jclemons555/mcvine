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


import unittest


from unittestX import TestCase
class xml_TestCase(TestCase):


    def test(self):
        """
        instrument xml file from LRMECS data file
        """
        print "This test must be run after the test cases in 'factories' directory"
        from instrument.nixml import parse_file
        instrument = parse_file( '4849.xml' )
        return


    pass # end of xml_TestCase


import unittest

def pysuite():
    suite1 = unittest.makeSuite(xml_TestCase)
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
__id__ = "$Id: xml_TestCase.py 1264 2007-06-04 17:56:50Z linjiao $"

# End of file 
