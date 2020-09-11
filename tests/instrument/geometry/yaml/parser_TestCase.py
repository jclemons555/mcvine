#!/usr/bin/env python
#
#


import unittest

class parser_TestCase(unittest.TestCase):


    def test(self):
        """
        instrument.geometer.yaml.parse_file
        """
        from instrument.geometry.yaml import parse_file
        shape = parse_file( 'test.yaml' )
        print(shape)
        return


    pass # end of parser_TestCase


if __name__ == '__main__': unittest.main()
    

# End of file 
