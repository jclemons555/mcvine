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
class parser_TestCase(TestCase):


    def test(self):
        """
        instrument.geometer.pml.parser
        """
        from instrument.geometry.pml import parse_file
        shape = parse_file( 'test.xml' )
        print shape
        return


    pass # end of parser_TestCase


import unittest

def pysuite():
    suite1 = unittest.makeSuite(parser_TestCase)
    return unittest.TestSuite( (suite1,) )



def main():
    import journal
    pytests = pysuite()
    alltests = unittest.TestSuite( (pytests, ) )
    unittest.TextTestRunner(verbosity=2).run(alltests)
    return


if __name__ == '__main__': main()
    

# version
__id__ = "$Id: parser_TestCase.py 1264 2007-06-04 17:56:50Z linjiao $"

# End of file 
