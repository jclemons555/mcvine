#!/usr/bin/env python
# Jiao Lin Copyright (c) 2006 All rights reserved

__doc__ = """
provides a model instrument that can be used to create tests

  - NAME: Instrument_CylindricalDetectorSystem
  - PURPOSE: provides a model instrument that can be used to create tests
  - DESCRIPTION: 

  This instrument contains 10 detector packs, each contains 10 detectors.
  All detectors are in the same distance from the sample, and form
  a cylinder. Each detector is 1 meter long.
  Each detector has 80 pixels. Each pixel is 2.5cm high.
  
  - RELATED: 
  - TODOs:
"""


import instrument.elements as elements
import instrument.geometers as geometers


from math import sqrt, acos, atan, pi, cos, sin
from numpy import array, dot


import journal
debug = journal.debug("Instrument_CylindricalDetectorSystem")

# number of detectors per pack
numdets = 100
# number of pixels per detector
numpxls = 80


# distance from sample to detector pixel
from . import units
atm = units.pressure.atm
meter = units.length.meter
mm = units.length.mm
inch = units.length.inch

R = 3000.0 * mm
mod2sample = 10000.0 * mm
tubeRadius = inch / 2.
tubeLength = 1 * meter
pixelSolidAngle = 1.0
pixelHeight = tubeLength/numpxls


pressure = 10 * atm


class InstrumentFactory( object):

    """A fake instrument that has 100 detectors, each of which has 80 pixels.

    Detectors form a partial cylinder from -10degree to 90 degree.
    """

    def construct( self):
        fake = elements.instrument( "CylinderDetectors")

        #instrument local geometer
        geometer = geometers.geometer(
            fake, registry_coordinate_system = 'InstrumentScientist' )
        self.local_geometers = [geometer]

        # make monitors: adds elements to arcs & geometer
        # self.makeMonitors( arcs, geometer)

        # make detector array: adds elements to arcs & geometer
        self.makeDetectorSystem( fake, geometer )

        # make Moderator
        self.makeModerator( fake, geometer)

        #make sample
        sample = elements.sample('sample')
        fake.addElement( sample )
        # sample is placed at origin to simplify computation
        geometer.register( sample, (0*mm,0*mm,0*mm), (0,0,0) ) 

        # set up guid registry
        fake.guidRegistry.registerAll( fake )

        # instrument global geometer
        instrumentGeometer = geometers.arcs(
            fake, self.local_geometers,
            registry_coordinate_system = 'InstrumentScientist' )

        fake.geometer = instrumentGeometer

        self._check( fake, instrumentGeometer )

        return fake, instrumentGeometer


    distMod2Sample = mod2sample
    def makeModerator( self, instrument, geometer):
        modXSize = 100.0*mm; modYSize = 100.0*mm; modZSize = 100.0*mm
        position = [-self.distMod2Sample, 0*mm, 0*mm]
        orientation = [0.0, 0.0, 0.0]
        modID = instrument.getUniqueID()
        moderator = elements.moderator(
            'moderator', 
            modXSize, modYSize, modZSize,
            type = "non-existant",
            guid = modID,
            )
        geometer.register( moderator, position, orientation )
        instrument.addElement( moderator )
        return
    

    def makeDetectorSystem( self, instrument, geometer):
        #detector system
        detSystem = elements.detectorSystem( 'detSystem' )
        instrument.addElement( detSystem )
        geometer.register( detSystem, (0*mm,0*mm,0*mm), (0,0,0) )

        detSystemGeometer = geometers.geometer(
            detSystem, registry_coordinate_system = 'InstrumentScientist' )
        self.local_geometers.append( detSystemGeometer )

        for detInd in range(numdets):
            
            detGuid = instrument.getUniqueID()

            name = 'detector%s' % detInd
            
            detector = self.makeDetector(
                name, detInd, instrument, 
                pressure, numpxls, tubeRadius, tubeLength)
            
            detSystem.addElement( detector)

            angle = detInd - 10.
            angle1 = angle * pi/180.
            x = R * cos( angle1 )
            y = R * sin( angle1 )
            position = (x,y,R*0)
            detSystemGeometer.register( detector, position, (0,0,0) )

            continue
        return 


    def makeDetector(self, name, id, instrument, 
                     pressure, npixels, radius, height):
        key = pressure, npixels, radius, height
        detectorModules = self._getDetectorModules()
        for key1 in detectorModules.keys():
            if _equal(key, key1):
                detM = detectorModules[ key1 ]
                debug.log( 'detM=%s' % detM )
                new = elements.copy(
                    name, detM.guid(),
                    id = id, guid = instrument.getUniqueID() )
                return new
            continue
        detector = self._makeDetector(
            name, id,
            instrument, pressure, npixels, radius, height )
        self._detectorModules[ key ] = detector
        return detector
    
        
    def _getDetectorModules(self):
        try: return self._detectorModules
        except:
            self._detectorModules = {}
            return self._detectorModules
        raise RuntimeError("Should not reach here")
        
        
    def _makeDetector(self, name, id, instrument, 
                      pressure, npixels, radius, height):
        from .LPSDFactory import create
        detector, geometer = create(
            name, id, 
            pressure, radius, height, npixels,
            pixelSolidAngle,
            instrument)

        self.local_geometers.append( geometer )
        return detector
    
        
    def _check(self, instrument, geometer):
        from instrument.elements.DetectorVisitor import DetectorVisitor
        class Checker(DetectorVisitor) :
            
            def onDetector(self, detector):
                dist = self._geometer.distanceToSample( self.elementSignature() )
                assert abs((dist - R)/R) < 1.e-7,\
                       'detector-sample-distance = %s, R = %s' % (dist, R)
                self.onElementContainer( detector )
                return
            

            def onPixel(self, pixel):
                geometer = self._geometer
                r =  geometer.distanceToSample( self.elementSignature() )
                assert r>= R or abs(r-R)/R<1e-7, "%s < %s" % (r,R)

                maxZ = numpxls/2.*pixelHeight
                maxDiff = ( maxZ**2 + R**2 )**0.5 - R
                assert r-R < maxDiff*1.1, \
                       "distance from pixel to sample too large: %s" % (
                    r, )
                return

            pass # end of Checker

        checker = Checker( )
        checker.render( instrument, geometer )
        return


    def __init__( self, **kwds):
        return


    pass #end of Instrument_CylindricalDetectorSystem


def _equal( key, key1 ):
    for a, b in zip(key, key1):
        if isinstance( a, int ):
            if a!=b: return False
        else:
            if abs(a-b) > 1.e-8*max(abs(a),abs(b)): return False
            pass
        continue
    return True


def main():
    debug.activate()
    factory = InstrumentFactory()
    fake, geometer = factory.construct()
    return fake, geometer


if __name__ =='__main__' : main()
    

# version
__id__ = "$Id: Instrument_CylindricalDetectorSystem.py 1216 2007-06-04 17:39:46Z linjiao $"

# End of file
