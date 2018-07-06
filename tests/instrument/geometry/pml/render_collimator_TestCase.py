#!/usr/bin/env python
#


import unittest


from unittest import TestCase
class renderer_TestCase(TestCase):


    def test(self):
        """
        instrument.geometry.pml.render
        """
        import numpy as np
        from instrument.geometry.pml import weave
        from instrument.geometry import shapes, operations
        pyramid = shapes.pyramid(thickness="20.*mm", width="20.*mm", height="110.*mm")
        pyramid_along_beam = operations.rotate(pyramid, transversal="1", angle="90.*deg")
        angles = np.arange(-160, 0., 15.)
        pyramids = [operations.rotate(pyramid_along_beam, vertical="1", angle='%s*deg' % a)
                    for a in angles]
        channels = operations.unite(*pyramids)

        hollow_cylinder = operations.subtract(
            shapes.cylinder(radius="55.*mm", height="50.*mm"),
            shapes.cylinder(radius="25.*mm", height="60.*mm"),
            )
        half_cylinder = operations.subtract(
            hollow_cylinder,
            operations.translate(
                shapes.block(height="110*mm", width="110*mm", thickness="110*mm"),
                transversal="-55.*mm",
                )
            )
        all = operations.subtract(half_cylinder, channels)

        # use a special renderer
        from instrument.geometry.pml.Renderer import Renderer as base
        class Renderer(base):
            def _renderDocument(self, body):
                self.onGeometry(body)
                return
            def header(self):
                return []
            def footer(self):
                return []
            def end(self):
                return
        text = weave( all, open('collimator.xml', 'wt'), print_docs = False, renderer=Renderer(), author='')
        return


    pass # end of renderer_TestCase


def main():
    import journal
    unittest.main()
    return


if __name__ == '__main__': main()
    
# End of file 
