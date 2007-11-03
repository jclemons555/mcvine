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


from instrument.elements.DetectorVisitor import *
import instrument.elements as ie


import instrument.elements.units as units
degree = units.angle.degree

import unittest, unittestX

class DetectorVisitor_TestCase(unittestX.TestCase):


    def test(self):
        """instrument.elements.DetectorVisitor
        """
        #create an instrument with layers and copies
        i = ie.instrument('test')
        ds = ie.detectorSystem('detSystem', guid = i.getUniqueID())
        dp1 = ie.detectorPack( 'detPack1', guid = i.getUniqueID() )
        det1 = ie.detector( 'detector1', guid = i.getUniqueID() )
        det2 = ie.copy( 'detector2', det1.guid(), guid = i.getUniqueID() )
        dp1.addElement( det1 ); dp1.addElement( det2 )
        
        dp2 = ie.copy( 'detPack2', dp1.guid(), guid = i.getUniqueID() )

        ds.addElement( dp1 ); ds.addElement(dp2)

        i.addElement( ds )
        i.guidRegistry.registerAll( i )
        
        counter = DetectorCounter( )
        self.assertEqual( counter.render( i ), 4 )
        return


    def test2(self):
        """instrument.elements.DetectorVisitor: method 'elementSignature'
        """
        print """
You should see indexes are increasing from the last (highest) index to
the lower index, one by one.
Copies are printed out twice.
"""
        #create an instrument with layers and copies
        i = ie.instrument('test')
        sample = ie.sample('sample')
        i.addElement( sample )
        
        ds = ie.detectorSystem('detSystem', guid = i.getUniqueID())
        dp1 = ie.detectorPack( 'detPack1', guid = i.getUniqueID() )
        det1 = ie.detector( 'detector1', guid = i.getUniqueID() )
        det2 = ie.copy( 'detector2', det1.guid(), guid = i.getUniqueID() )
        dp1.addElement( det1 ); dp1.addElement( det2 )
        
        dp2 = ie.copy( 'detPack2', dp1.guid(), guid = i.getUniqueID() )

        ds.addElement( dp1 ); ds.addElement(dp2)

        i.addElement( ds )
        i.guidRegistry.registerAll( i )

        import instrument.geometers as ig
        g = ig.arcs( i, registry_coordinate_system = 'McStas' )
        g.register( sample, (0,0,0), (0,0,0) )
        g.register( ds, (0,0,0), (0,0,0) )
        g.register( dp1, (1,0,0), (0,90,0), relative = ds )
        g.register( det1, (0.1,0,0), (90,0,0), relative = dp1 )
        g.register( det2, (-0.1, 0, 0), (90,0,0), relative = dp1 )
        g.register( dp2, (-1,0,0), (0,90,0), relative = ds )
        g.finishRegistration()
        self.assertAlmostEqual( g.scatteringAngle( 'detSystem/detPack1' )/degree, 90 )

        class Visitor(DetectorVisitor):

            def onDetectorPack(self, pack):
                print pack.name, self.elementSignature()
                self.onElementContainer(pack)
                return

            def onDetector(self, detector):
                print detector.name, self.elementSignature()
                return

            def onCopy(self, copy):
                print copy.name, self.elementSignature()
                DetectorVisitor.onCopy(self, copy)
                return

            pass # end of Visitor

        Visitor().render( i, g )
        return


    def test3(self):
        """instrument.elements.DetectorVisitor.DetectorSubsystemVisitor: method 'elementSignature'
        """
        print """
You should see indexes are increasing from the last (highest) index to
the lower index, one by one.
Copies are printed out twice.
"""
        #create an instrument with layers and copies
        i = ie.instrument('test')
        sample = ie.sample('sample')
        i.addElement( sample )
        
        ds = ie.detectorSystem('detSystem', guid = i.getUniqueID())
        da = ie.detectorArray('detArray', guid = i.getUniqueID() )
        ds.addElement( da )
        dp1 = ie.detectorPack( 'detPack1', guid = i.getUniqueID() )
        da.addElement( dp1 )
        det1 = ie.detector( 'detector1', guid = i.getUniqueID() )
        det2 = ie.copy( 'detector2', det1.guid(), guid = i.getUniqueID() )
        dp1.addElement( det1 ); dp1.addElement( det2 )
        
        dp2 = ie.copy( 'detPack2', dp1.guid(), guid = i.getUniqueID() )
        da.addElement(dp2 )

        i.addElement( ds )
        i.guidRegistry.registerAll( i )

        import instrument.geometers as ig
        g = ig.arcs( i, registry_coordinate_system = 'McStas' )
        g.register( sample, (0,0,0), (0,0,0) )
        g.register( ds, (0,0,0), (0,0,0) )
        g.register( dp1, (1,0,0), (0,90,0), relative = da )
        g.register( det1, (0.1,0,0), (90,0,0), relative = dp1 )
        g.register( det2, (-0.1, 0, 0), (90,0,0), relative = dp1 )
        g.register( dp2, (-1,0,0), (0,90,0), relative = da )
        g.register( da, (0,0,0), (0,0,0), relative = ds )
        g.finishRegistration()
        self.assertAlmostEqual( g.scatteringAngle( 'detSystem/detArray/detPack1' )/degree, 90 )

        class Visitor(DetectorSubsystemVisitor):

            def onDetectorPack(self, pack):
                print pack.name, self.detectorElementSignature()
                self.onElementContainer(pack)
                return

            def onDetector(self, detector):
                print detector.name, self.detectorElementSignature()
                return

            def onCopy(self, copy):
                print copy.name, self.detectorElementSignature()
                DetectorVisitor.onCopy(self, copy)
                return

            pass # end of Visitor

        Visitor().render( i, g, 'detArray' )
        return


    pass # end of DetectorVisitor_TestCase


import unittest

def pysuite():
    suite1 = unittest.makeSuite(DetectorVisitor_TestCase)
    return unittest.TestSuite( (suite1,) )



def main():
    import journal
    pytests = pysuite()
    alltests = unittest.TestSuite( (pytests, ) )
    unittest.TextTestRunner(verbosity=2).run(alltests)
    return


if __name__ == '__main__': main()



# version
__id__ = "$Id$"

# End of file 
