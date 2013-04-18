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


class parser_TestCase(unittest.TestCase):


    def test0(self):
        """
        instrument.mantid.parser
        """
        from instrument.mantid import parse_file
        instrument = parse_file( 'arcs.xml' )
        # print instrument.components
        # print instrument.detectors
        brow = instrument.detectors[0]
        brow_type = brow.getType()
        brow_packs = brow_type.components
        brow_pack0 = brow_packs[0]
        brow_pack0_type = brow_pack0.getType()
        eightpack = brow_pack0_type.components[0]
        eightpack_type = eightpack.getType()
        tubes = eightpack_type.components[0]
        locations = tubes.getChildren('location')
        assert len(locations) == 8
        tube_type = tubes.getType()
        pixels = tube_type.components[0]
        locations = pixels.getChildren('location')
        assert len(locations) == 128
        return


    pass # end of parser_TestCase


import unittest

if __name__ == '__main__': unittest.main()
    

# version
__id__ = "$Id: parser_TestCase.py 1264 2007-06-04 17:56:50Z linjiao $"

# End of file 
