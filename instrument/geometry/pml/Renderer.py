#!/usr/bin/env python
#
# Jiao Lin <jiao.lin@gmail.com>
#



from pyre.geometry.pml.Renderer import Renderer as base 


class Renderer(base):

    def onHollowCylinder(self, hollowCylinder):
        self._printDocs( hollowCylinder)
        s  = '<hollowCylinder in_radius="%s" out_radius="%s" height="%s"/>' %(
            hollowCylinder.in_radius, hollowCylinder.out_radius,
            hollowCylinder.height)
        self._write(s )
        return
    

    def onCylinder(self, cylinder):
        self._printDocs( cylinder)
        base.onCylinder(self, cylinder)
        return
    

    def onSphereShell(self, sphereShell):
        self._printDocs( sphereShell)
        s  = '<sphereShell in_radius="%s" out_radius="%s" />' %(
            sphereShell.in_radius, sphereShell.out_radius,
            )
        self._write(s )
        return
    

    def onSphere(self, sphere):
        self._printDocs( sphere)
        base.onSphere(self, sphere)
        return
    

    def onBlock(self, block):
        self._printDocs( block)
        s  = '<block width="%s" height="%s" thickness="%s"/>' %(
            block.width, block.height, block.thickness)
        self._write(s )
        return
    

    def onPyramid(self, pyramid):
        self._printDocs( pyramid)
        s  = '<pyramid thickness="%s" width="%s" height="%s"/>' %(
            pyramid.width, pyramid.height, pyramid.thickness)
        self._write(s )
        return
    

    def onRectTube(self, rectTube):
        self._printDocs( rectTube )
        s = '<rectTube front="%s,%s" back="%s,%s" length="%s"/>' %(
            rectTube._fr_width, rectTube._fr_height,
            rectTube._bk_width, rectTube._bk_height,
            rectTube._length,
            )
        self._write( s )
        return


    def onMultiary(self, mul, tag):
        self._write("<%s>" % tag)

        self._indent()
        for s in mul.shapes:
            s.identify(self)
        self._outdent()

        self._write("</%s>" % tag)
        return

    def onUnion(self, u):
        return self.onMultiary(u, 'union')

    def onIntersection(self, i):
        return self.onMultiary(i, 'intersection')


    def _printDocs(self, element):
        self._write('<!--')
        self._write(element.__class__.__doc__)
        self._write('-->')
        return

    pass # end of Renderer


# End of file 
