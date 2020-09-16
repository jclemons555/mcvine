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


from unittest import TestCase
class renderer_TestCase(TestCase):


    def test(self):
        """
        instrument.geometry.pml.render
        """
        from instrument.geometry.pml import render, parse_file
        shapes = parse_file( 'test1.xml' )
        text = render( shapes[0], print_docs=False )
        print('\n'.join(text), file=open('test1.xml.rendered','w')) 
        return


    pass # end of renderer_TestCase


import unittest

def pysuite():
    suite1 = unittest.makeSuite(renderer_TestCase)
    return unittest.TestSuite( (suite1,) )


def main():
    import journal
    pytests = pysuite()
    alltests = unittest.TestSuite( (pytests, ) )
    unittest.TextTestRunner(verbosity=2).run(alltests)
    return


if __name__ == '__main__': main()
    

# version
__id__ = "$Id: renderer_TestCase.py 1264 2007-06-04 17:56:50Z linjiao $"

# End of file 
