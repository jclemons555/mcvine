#!/usr/bin/env python
# Timothy M. Kelley Copyright (c) 2005 All rights reserved

from PharosDetCSVParser import Parser
from math import sqrt, acos, atan, pi, cos, sin

import units
atm = units.pressure.atm
meter = units.length.meter
mm = units.length.mm
inch = units.length.inch


import instrument.elements as elements
import instrument.geometers as geometers


from _journal import debug


# number of detectors per pack
numdets = 8

# number of pixels per 1m tube
numPixels1m = 40

#number of pixels per short tube
## Not applicable at present:
## numPixels32cm = 16

# radius of detector
tubeRadius = 0.5 *inch

# pixel solid angle. hard coded. should be calcuated
pixelSolidAngle = 1.

#monitor positions: relative to the sample, in spherical coordinates.
monitorPositions = [
    [-2300.0*mm, 0.0*mm, 0.0*mm],
    [-1700.0*mm, 0.0*mm, 0.0*mm],
    [+4900.0*mm, 0.0*mm, 0.0*mm]
    ]

monitorNames = [
    "monitor1",
    "monitor2",
    "monitor3"
    ]

monitorIDs = [1,2,3]

monSizes = [
    [30.0*mm, 120.0*mm, 120.0*mm],
    [30.0*mm, 120.0*mm, 120.0*mm],
    [30.0*mm, 120.0*mm, 120.0*mm],
    ]


class InstrumentFactory( object):
    """Use a combination of hard-coded and CSV data files to construct an
    Instrument object and a geometer for ARCS"""


    distMod2Sample = 20. * meter
        
    def construct( self, detPackFilename):
        pharos = elements.instrument( "Pharos")

        #instrument local geometer
        geometer = geometers.geometer(
            pharos, registry_coordinate_system = 'InstrumentScientist' )
        self.local_geometers = [geometer]

        # Pharos currently don't have monitors. The following are commented out
        # make monitors: adds elements to pharos & geometer
        # self.makeMonitors( pharos, geometer)

        # make detector array: adds elements to pharos & geometer
        import os
        if not os.path.exists(detPackFilename):
            raise RuntimeError ,"Cannot find file %s" % detPackFilename
        self.makeDetectorSystem( pharos, geometer, detPackFilename)

        # make Moderator
        self.makeModerator( pharos, geometer)

        # make sample
        sample = elements.sample( 'sample' )
        pharos.addElement( sample )
        geometer.register( sample, (0,0,0), (0,0,0) )

        # set up guid registry
        pharos.guidRegistry.registerAll( pharos )

        # instrument global geometer
        instrumentGeometer = geometers.arcs(
            pharos, self.local_geometers,
            registry_coordinate_system = 'InstrumentScientist' )

        pharos.geometer = instrumentGeometer

        del self.local_geometers

        # save the xml description
        from instrument.nixml import weave
        import os
        f = '%s.xml' % (os.path.basename(detPackFilename),)
        print 'write pharos instrument to %s' % f
        weave( pharos, open(f, 'w') )
        return pharos, instrumentGeometer


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
        
        instrument.addElement( moderator)
        geometer.register( moderator, position, orientation)
        return
    

    def makeMonitors( self, instrument, geometer):
        # this is not used yet
        i = 1
        for position, name, monid, monSize in zip(
            monitorPositions, monitorNames,
            monitorIDs, monSizes):
            
            debug.log("monitor position: %s, monitor name: '%s', id: %s" %
                      (position, name, monid))
            monID = instrument.getUniqueID()
            thickness, width, height = monSize
            monitor = elements.monitor(
                name, width, height, thickness,
                guid = monID, 
                id = monid,
                type="watchful"
                )
            instrument.addElement( monitor )
            i += 1
            
            geometer.register( monitor, position, orientation=[0.0,0.0,0.0])
            continue

        return
    
        
    def makeDetectorSystem( self, instrument, geometer, detPackFilename):
        instrument.detIDs = [] #keep the list of detector IDs
        
        # detector array
        did = instrument.getUniqueID()
        detSystem = elements.detectorSystem( 'detSystem', guid = did )
        instrument.addElement( detSystem )
        geometer.register( detSystem, (0*mm,0*mm,0*mm), (0,0,0) )

        # geometer for tubes
        detSystemGeometer = geometers.geometer(
            detSystem, registry_coordinate_system = 'InstrumentScientist' )
        self.local_geometers.append( detSystemGeometer )

        # detectorPacks
        # get detector pack info records
        parser = Parser( detPackFilename)
        instrument.raw_detector_records = records = parser.parse()

        # make detectors
        for i, record in enumerate( records ):
            if 'short' in record['type']['value']: continue
            detGuid = instrument.getUniqueID()
            
            detID = record['tubeNo'] ['value']
            
            instrument.detIDs.append( detID )
            
            detDescr = record[ 'type']['value']

            # properties of the detector
            pressure = 0.0
            if '6atm' in detDescr:
                pressure = 6.0 * atm
            elif '10atm' in detDescr:
                pressure = 10.0 * atm
            else:
                raise ValueError, "unknown detector pressure"
            
            height = record['length']['value'] * _todimensional( record['length']['unit'] )
            radius = tubeRadius
            
            if height/mm > 999.0:
                numPixels = numPixels1m
            elif height/mm < 330.0 and height > 310.0:
                numPixels = numPixels32cm
                raise ValueError, "did not expect short detectors yet!"

            name = 'detector%s' % detID

            # create detector element
            detector = self.makeDetector(
                name, detID, instrument, 
                pressure, numPixels, radius, height)
            
            rho = record['distance']['value']*_todimensional( record['distance']['unit'] )
            phi = record['angle']['value']*_todimensional( record['angle']['unit'] )
            phi *= -1.0

            # convert from polar to cartesian coordinates. Note theta = 90 (in
            # other words, the detector centers all lie in the scattering plane).
            x = rho*cos( phi)
            y = rho*sin( phi)
            position = [x,y,0.*mm]
            
            orientation = [0.0, 0.0, 0.0]

            detSystem.addElement( detector )
            detSystemGeometer.register(
                detector, position, orientation)

            continue
                    
        return # detSystem # arcs, geometer


    def makeDetector(self, name, id, instrument, 
                     pressure, npixels, radius, height):
        
        key = pressure, npixels, radius, height
        detectorModules = self._getDetectorModules()
        
        for key1 in detectorModules.iterkeys():
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
        raise RuntimeError , "Should not reach here"
        
        
    def _makeDetector(self, name, id, instrument, 
                      pressure, npixels, radius, height):
        
        from LPSDFactory import create
        detector, geometer = create(
            name, id, 
            pressure, radius, height, npixels,
            pixelSolidAngle,
            instrument)

        self.local_geometers.append( geometer )
        return detector
    

    pass # end of  InstrumentFactory



#helpers 
def _equal( key, key1 ):
    for a, b in zip(key, key1):
        if isinstance( a, int ):
            if a!=b: return False
        else:
            if abs(a-b) > 1.e-8*max(abs(a),abs(b)): return False
            pass
        continue
    return True


import units
def _todimensional( candidate ):
    if isinstance( candidate, basestring ):
        parser = units.parser()
        return parser.parse( candidate )
    if not units.isdimensional( unit ) and not isinstance( candidate, int )\
           and not isinstance( candidate, float ):
        raise ValueError , "Cannot convert %s to a dimensional" % (
            candidate, )
    return candidate


# version
__id__ = "$Id$"

# End of file
