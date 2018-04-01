#!/usr/bin/env python
#
#


import unittest

class renderer_TestCase(unittest.TestCase):


    def test(self):
        """
        instrument.geometer.yaml.render_file
        """
        from instrument.geometry.yaml import render_file, parse_file
        shape = parse_file( 'test.yaml' )
        # print shape.todict()
        render_file(shape, 'output.yaml')
        import os
        rt = os.system('diff output.yaml expected-render-output.yaml')
        assert not rt
        return

    pass 


if __name__ == '__main__': unittest.main()
    

# End of file 
