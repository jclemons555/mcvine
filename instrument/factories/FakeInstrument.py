#!/usr/bin/env python
# Jiao Lin Copyright (c) 2006 All rights reserved


# This module probably should be removed. The Instrument_CylindricalDetectorSystem is better.

__doc__ = """
provides a model instrument that can be used to create tests

  - NAME: FakeInstrument
  - PURPOSE: provides a model instrument that can be used to create tests
  - DESCRIPTION: This module combined with FakeMeasurement and FakeGeometer
  provides a base for creating test for reduction procedures.

  This instrument contains 100 detectors.
  Each detector has 10 pixels. All pixel in one detector has exacctly the
  same scattering angle.
  Detector's pressure is correlated with detID: pressure = detID/10+5. (atm)
  Detector's scattering angle is correlated with detID: phi = detID (degree)
  
  - RELATED: measurment.FakeMeasurement, instrument.geoemters.FakeGeometer
  - TODOs:
"""

from instrument.geometers.FakeGeometer import Geometer

import  instrument.elements  as  elements

from math import sqrt, acos, atan, pi, cos, sin


import journal
debug = journal.debug("FakeInstrument")

# number of detectors per pack
numdets = 100
# number of pixels per detector
numpxls = 10


# distance from sample to detector pixel 
from . import units
mm = units.length.mm
R = 3000.0 * mm #mm

#detector radius
detradius = 0.5 * units.length.inch
def detpressure( detID ):
    return (0.5+detID*0.1)*units.pressure.atm

pixelSolidAngle = 1.0
pixelHeight = 0.0

## #monitor positions: all guesses
## monitorPositions = [
##     [2300.0, 90.0, 180.0],
##     [1700.0, 90.0, 180.0],
##     [4900.0, 90.0, 0.0]
##     ]

## monitorNames = [
##     "monitor1",
##     "monitor2",
##     "monitor3"
##     ]

## monitorIDs = [1,2,3]

## monSizes = [30.0, 120.0, 120.0]



class InstrumentFactory( object):

    """A fake instrument that has 10 detectors, each of which has 10 pixels.

    All pixels in a detector has the same scattering angle.
    100 detectors' scattering angles is a list: [0...99]
    """

    maxNumPixelPerDetector = numpxls
        
    def construct( self):
        fake = elements.instrument( "FAKE", version="0.0.0")

        geometer = Geometer()

##         # make monitors: adds elements to arcs & geometer
##         self.makeMonitors( arcs, geometer)

        # make detector array: adds elements to arcs & geometer
        self.makeDetectorSystem( fake, geometer )

        # make Moderator
        self.makeModerator( fake, geometer)

        self._check( fake, geometer )
        fake.maxNumPixelPerDetector = self.maxNumPixelPerDetector
        return fake, geometer


    def makeModerator( self, instrument, geometer):
        
        modXSize = 100.0; modYSize = 100.0; modZSize = 100.0
        modID = instrument.getUniqueID()
        moderator = elements.moderator(
            'moderator',
            modXSize, modYSize, modZSize,
            type = "non-existant",
            guid = modID,
            )
        
        instrument.addElement( moderator)
        geometer.register( moderator, 0.0, 0.00000001 * mm )
        return
    

##     def makeMonitors( self, instrument, geometer):

##         i = 1
##         for position, name, monid in zip( monitorPositions, monitorNames,
##                                           monitorIDs):
##             debug.log("monitor position: %s, monitor name: '%s', id: %s" %
##                       (position, name, monid))
##             monID = instrument.getUniqueID()
##             monitor = Monitor( monID, instrument.guid(),monitorType="watchful",
##                                xLength=monSizes[0], yLength=monSizes[1],
##                                zLength=monSizes[2], monitorNumber=i,
##                                name = name)
##             instrument.addMonitor( monitor, i)
##             i += 1
            
##             geometer.register( monitor, position, orientation=[0.0,0.0,0.0])

##         return
    
        
    def makeDetectorSystem( self, instrument, geometer):

        # detector system
        dguid = instrument.getUniqueID()
        did = 10
        detSystem = elements.detectorSystem(
            'detectorSystem', guid = dguid, id = did )

        instrument.addElement( detSystem )
        
        # detectors
        for detInd in range(numdets):
            detGuid = instrument.getUniqueID()
            detector = elements.detector(
                'detector%s' % detInd, guid = detGuid,  id = detInd,
                pressure = detpressure(detInd),
                radius = detradius,
                )
            detSystem.addElement( detector)

            geometer.register(
                (did, detInd), detInd*units.angle.degree, R)

            # 3 for each detector, make the pixels for that detector
            for pxlInd in range(numpxls):
                pxlGuid = instrument.getUniqueID()
                pixel = elements.pixel(
                    'pixel%s' % pxlInd, guid = pxlGuid, id = pxlInd,
                    solidAngle = pixelSolidAngle,
                    height = pixelHeight, radius = R )

                detector.addElement( pixel)

                geometer.register(
                    (did, detInd, pxlInd), detInd*units.angle.degree, R)
                continue
            continue
        #print ""
        return 


    def _check(self, instrument, geometer):

        from instrument.elements.DetectorVisitor import DetectorVisitor
        
        class Checker(DetectorVisitor):

            onDetector = DetectorVisitor.onElementContainer
            
            def onPixel(self, pixel):
                geometer = self._geometer
                self.phiList.append( geometer.scatteringAngle( self.elementSignature() ) )
                assert geometer.distanceToSample( self.elementSignature() ) == R
                return
            
            def render(self, instrument, geometer):
                self.phiList = []
                DetectorVisitor.render( self, instrument, geometer )
                from numpy import sort
                return sort(self.phiList)

            pass # end of Checker

        phiList = Checker().render( instrument, geometer )
        debug.log("phiList = %s" % phiList)
        return


    def __init__( self, **kwds):
        return


    pass #end of FakeInstrument



def create():
    factory = InstrumentFactory()
    fake, geometer = factory.construct()
    return fake, geometer


def main():
    debug.activate()
    create()
    return

if __name__ =='__main__' : main()
    

# version
__id__ = "$Id$"

# End of file
