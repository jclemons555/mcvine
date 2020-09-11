#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2007  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from ._journal import debug

from .InstrumentGeometer import InstrumentGeometer

class ARCSGeometer(InstrumentGeometer):

    '''A geometer that is most useful for inelastic direct-geometry
chopper spectrometer.
'''

    def scatteringAngle( self, element ):
        """scatteringAngle( element) -> scattering angle in degrees
        Compute the scattering angle of the specified element in degrees.
        Inputs:
            element: The element or the element signature
        Output:
            scattering angle, in radian
        Exceptions: KeyError
        Notes: scattering angle means angle from moderator to sample to
        element."""
        from numpy import array, dot, arccos, pi
        
        x = self.positionRelativeToSample( element )
        x = array(x)
        
        #remove unit if necessary
        from . import units
        m = units.length.meter
        try:
            x + m
            x /= m
        except: pass

        lx = vlen( x )

        beam = self.request_coordinate_system().neutronBeamDirection
        lbeam = vlen( array(beam) )
        
        cost = dot(x, beam)
        cost /= lx * lbeam
        
        return arccos( cost ) * radian


    def phi(self, element):
        """phi( detector ) -> angle phi in degrees
        !!! Please note this angle phi is not the scattering angle.
        !!! In many conventioins, scattering angle are called 'phi',
        !!! but that is not true here.
        !!! Please call scatteringAngle method to get scattering angle
        
        Compute the phi angle of the specified detector element in degrees.
        Inputs:
            element: the element or the element signature
        Output:
            phi angle, in radian
        Exceptions: KeyError
        Notes: phi angle is the horizontal angle of scattering
        """
        from numpy import array, dot, arctan2, pi, cross

        x = self.positionRelativeToSample( element )
        x = array(x)
        
        #remove unit if necessary
        from . import units
        m = units.length.meter
        try:
            x + m
            x /= m
        except: pass

        #lx = vlen( x )
        #x/=lx

        beam = self.request_coordinate_system().neutronBeamDirection
        up = -array(self.request_coordinate_system().gravityDirection)
        hor = cross( up, beam )

        cosp = dot(x, beam)
        sinp = dot(x, hor)
        
        return arctan2( sinp, cosp ) * radian

    pass # end of ARCSGeometer


from . import units
radian = units.angle.radian
degree = units.angle.degree


def vlen( v ):
    from numpy import array, sum, sqrt, conjugate, real
    l = sqrt(sum( v*v ))
    return l

    
import unittest

from unittest import TestCase
class ARCSGeometer_TestCase(TestCase):

    def test4(self):
        "ARCSGeometer: instrument with layers"
        import instrument.elements as ies
        
        instrument = ies.instrument( "instrument" )
        
        sample = ies.sample( 'sample' )
        instrument.addElement( sample)

        detSystem = ies.detectorSystem( 'detSystem')
        instrument.addElement( detSystem )

        det1 = ies.detector( 'det1', guid = instrument.getUniqueID() )
        detSystem.addElement( det1 )
        
        pixel1 = ies.pixel( 'pixel1', guid = instrument.getUniqueID() )
        det1.addElement( pixel1 )

        from .CoordinateSystem import McStasCS
        geometer = ARCSGeometer(
            instrument, registry_coordinate_system = McStasCS )

        geometer.register( sample, (0,0,0), (0,0,0) )
        geometer.register( detSystem, (0,0,0), (0,0,0) )
        geometer.register( det1, (1,0,0), (0,90,0), relative = detSystem )
        geometer.register( pixel1, (0,1,0), (0,0,0), relative = det1 )
        geometer.finishRegistration()

        self.assertAlmostEqual( geometer.scatteringAngle(
            'detSystem/det1/pixel1'), 90*degree )
        self.assertAlmostEqual( geometer.phi(
            'detSystem/det1/pixel1'), 90*degree )
        return

    pass # end of ARCSGeometer_TestCase

    
def pysuite():
    suite1 = unittest.makeSuite(ARCSGeometer_TestCase)
    return unittest.TestSuite( (suite1,) )

def main():
    pytests = pysuite()
    unittest.TextTestRunner(verbosity=2).run(pytests)
    return


if __name__ == '__main__': main()
    

# version
__id__ = "$Id: ARCSGeometer.py 1208 2007-01-12 17:11:01Z linjiao $"

# End of file
