#!/usr/bin/env python
#


import unittest


from unittest import TestCase
class renderer_TestCase(TestCase):


    def test(self):
        """
        instrument.geometry.pml.render
        """
        from instrument.geometry.pml import render
        from instrument.geometry import shapes, operations
        cyl = shapes.cylinder(radius="1.*cm", height="5.*cm")
        sphere = shapes.sphere(radius="2.*cm")
        block = shapes.block(width="5*cm", height="4.*cm", thickness="1.*mm")
        u = operations.unite(cyl, sphere, block)
        t = operations.translate(u, vertical="0.2*cm")
        r = operations.rotate(t, vertical=1., angle = 90.)
        pyramid = shapes.pyramid(width="4.*cm", height="2.*cm", thickness="1.*cm")
        i = operations.intersect(r, pyramid)
        cone = shapes.cone(radius="2.*cm", height="2.*cm")
        u = operations.unite(i, cone)
        sphere2 = shapes.sphere(radius="3.*cm")
        s = operations.subtract(sphere2, u)
        text = render( s, print_docs = False )
        print >> open('test2.xml.rendered','w'),  '\n'.join(text) 
        return


    pass # end of renderer_TestCase


def main():
    import journal
    unittest.main()
    return


if __name__ == '__main__': main()
    
# End of file 
