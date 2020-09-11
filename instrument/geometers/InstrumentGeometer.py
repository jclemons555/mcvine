#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2006  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from ._journal import debug


from .AbstractInstrumentGeometer import AbstractInstrumentGeometer
from .GlobalGeometer import GlobalGeometer


class InstrumentGeometer(  GlobalGeometer, AbstractInstrumentGeometer ):


    def __init__(self, target, local_geometers = [],
                 registry_coordinate_system = None,
                 request_coordinate_system = None):
        GlobalGeometer.__init__(
            self, target, local_geometers,
            registry_coordinate_system = registry_coordinate_system,
            request_coordinate_system = request_coordinate_system)
        self._positionRelativeToSampleRegistry = {}
        return


    def distanceToSample(self, element ):
        p = self.positionRelativeToSample( element )
        from .utils import length
        return length(p/meter) * meter
    

    def scatteringAngle( self, element ):
        'this method is tricky and it depends on instrument'
        self._abstract( "scatteringAngle" )


    def positionRelativeToSample( self, element ):
        t = self._positionRelativeToSampleRegistry.get( element )
        if t is None: t = self._calcPositionRelativeToSample( element )
        return t
    
        
    def _calcPositionRelativeToSample( self, element ):
        instrument = self.target
        sample = instrument.getSample()
        result = self.displacement( sample, element )
        self._positionRelativeToSampleRegistry[element] = result
        return result 

    pass # end of InstrumentGeometer


    
import unittest

from unittest import TestCase
class InstrumentGeometer_TestCase(TestCase):

    def test4(self):
        "InstrumentGeometer: instrument with layers"
        import instrument.elements as ies
        from .Geometer import Geometer
        from instrument.elements.Element import Element
        from instrument.elements.ElementContainer import ElementContainer
        
        instrument = ies.instrument( "instrument" )
        
        moderator = ies.moderator( "moderator", 100., 100., 10. ) 
        instrument.addElement( moderator ) 
        
        monitor1 = ies.monitor( "monitor1", 100., 100., 10. ) 
        instrument.addElement( monitor1 )
        
        sample = ies.sample( "sample", None )
        instrument.addElement( sample)
        
        detectorSystem = ElementContainer( "detectorSystem" )
        instrument.addElement( detectorSystem )

        local_geometers = []
        
        detectorSystem_geometer = Geometer( detectorSystem )
        local_geometers.append( detectorSystem_geometer )
        
        #add 8X10 detectors by brute force
        for i in range(10):
            
            detpack = ElementContainer(
                "detpack%s" % i, guid = instrument.getUniqueID())
            detpack_geometer = Geometer( detpack )

            for j in range(8):
                name = "det%s"%j
                det = Element(name, guid = instrument.getUniqueID())
                exec('det_%s_%s = det' % (i,j))
                detpack.addElement( det )
                detpack_geometer.register( det, (j-3.5, 0, 0 ), (0,0,0) )
                continue
            
            detpack_geometer.finishRegistration()
            
            detectorSystem.addElement( detpack)
            local_geometers.append( detpack_geometer )
            
            detectorSystem_geometer.register( detpack, (10*i, 0, 0), (0,0,0) )
            continue

        detectorSystem_geometer.finishRegistration()

        instrument_geometer = Geometer( instrument )
        instrument_geometer.register( moderator, (0,0,-5), (0,0,0) )
        instrument_geometer.register( sample, (0,0,0), (0,0,0) )
        instrument_geometer.register( detectorSystem, (0,0,0), (0,0,0) )
        instrument_geometer.register( monitor1, (0,0,-3), (0,0,0) )
        instrument_geometer.finishRegistration()

        local_geometers.append( instrument_geometer )

        global_instrument_geometer = InstrumentGeometer( instrument, local_geometers )
        
        moderator_pos = global_instrument_geometer.position( "moderator" )/meter
        self.assertAlmostEqual( moderator_pos[0], 0 )
        self.assertAlmostEqual( moderator_pos[1], 0 )
        self.assertAlmostEqual( moderator_pos[2], -5 )

        detector00_pos = global_instrument_geometer.position( "detectorSystem/detpack0/det0" ) / meter
        self.assertAlmostEqual( detector00_pos[0], -3.5 )
        self.assertAlmostEqual( detector00_pos[1], 0 )
        self.assertAlmostEqual( detector00_pos[2], 0 )

        detector00_dist2sample = global_instrument_geometer.distanceToSample( "detectorSystem/detpack0/det0") / meter
        self.assertAlmostEqual( 3.5, detector00_dist2sample )
        return

    pass # end of InstrumentGeometer_TestCase
from . import units
meter = units.length.meter

    
def pysuite():
    suite1 = unittest.makeSuite(InstrumentGeometer_TestCase)
    return unittest.TestSuite( (suite1,) )

def main():
    pytests = pysuite()
    unittest.TextTestRunner(verbosity=2).run(pytests)
    return


if __name__ == '__main__': main()
    

# version
__id__ = "$Id: InstrumentGeometer.py 1208 2007-01-12 17:11:01Z linjiao $"

# End of file
