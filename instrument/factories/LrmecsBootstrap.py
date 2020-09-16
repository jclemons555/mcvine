#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                      (C) 2005-2007  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from math import sqrt, acos, atan, pi, cos, sin
from . import units
atm = units.pressure.atm
m = units.length.m
mm = units.length.mm

import instrument.elements as elements
import instrument.geometers as geometers


from ._journal import debug


# number of pixels per 1m tube
numPixelsPerTube = 1
# pixel solid angle. hard coded. should be calcuated
pixelSolidAngle = 1.
# detector orientation. in "instrument scientist" coordinate syste
detectorOrientation = (0,0,0)


class InstrumentFactory( object):
    
    """Use det info extracted by LrmecsDataFilerParser and
    hard-coded info to construct an
    Instrument object and a geometer for LRMECS"""


    def __init__( self, **kwds):
        if "interpolateData" in kwds: self.interpolateData = kwds['interpolateData']
        else: self.interpolateData = False            
        return
    

    def construct( self, lrmecsDataFilename):
        import os
        if not os.path.exists(lrmecsDataFilename):
            raise RuntimeError("Cannot find file %s" % os.path.abspath(lrmecsDataFilename))

        self._instrument = lrmecs = elements.instrument(
            "Lrmecs" )# version="0.0.0")

        #instrument local geometer
        geometer = geometers.geometer(
            lrmecs, registry_coordinate_system = 'InstrumentScientist' )
        self.local_geometers = [geometer]

        #parse the file and get all tube records and monitor records
        from .LrmecsDataFileParser import Parser
        self.distMod2Sample, monitorRecords, tubeRecords = Parser(
            lrmecsDataFilename, self.interpolateData ).parse()

        # make Moderator
        self.makeModerator( lrmecs, geometer)

        # make monitors: adds elements to lrmecs & geometer
        self.makeMonitors( lrmecs, geometer, monitorRecords)

        #make sample
        sample = elements.sample('sample')
        lrmecs.addElement( sample )
        # sample is placed at origin to simplify computation
        geometer.register( sample, (0*mm,0*mm,0*mm), (0,0,0) ) 

        # make detector array: adds elements to lrmecs & geometer
        self.makeDetectorSystem( lrmecs, geometer, tubeRecords)

        # set up guid registry
        lrmecs.guidRegistry.registerAll( lrmecs )

        # instrument global geometer
        instrumentGeometer = geometers.arcs(
            lrmecs, self.local_geometers,
            registry_coordinate_system = 'InstrumentScientist' )

        lrmecs.geometer = instrumentGeometer

        # clean up temporary variables
        del self._detectorModules, self.distMod2Sample, self.local_geometers
        del self._instrument

        # save the xml description
        from instrument.nixml import weave
        import os
        f = '%s-interp%s.xml' % (
            os.path.basename(lrmecsDataFilename), self.interpolateData)
        print('write lrmecs instrument to %s' % f)
        weave( lrmecs, open(f, 'w') )
        return lrmecs, instrumentGeometer


    def makeModerator( self, instrument, geometer):

        modXSize = 100.0*mm; modYSize = 100.0*mm; modZSize = 100.0*mm
        position = [-self.distMod2Sample * mm, 0*mm, 0*mm]
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
    

    def makeMonitors( self, instrument, geometer, monitorRecords):

        i = 0

        for record in monitorRecords:
            monid = record['id']
            dist2Samp = record['distance']['value'] #unit: mm
            position = [-dist2Samp * mm, 0 * mm, 0 * mm]
            name = "monitor%s" % i
            
            debug.log("monitor position: %s, monitor name: '%s', id: %s" %
                      (position, name, monid))

            geometry = record['geometry']
            width = height = geometry['radius'] * mm
            thickness = geometry['thickness'] * mm

            monitor = elements.monitor(
                name, width, height, thickness,
                guid = instrument.getUniqueID() )
            
            instrument.addElement( monitor )
            i += 1
            
            geometer.register( monitor, position, orientation=[0.0,0.0,0.0])

            continue

        return


    def makeDetector(self, name, id, instrument, 
                     pressure, npixels, radius, height):
        assert instrument == self._instrument
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
        pressure = pressure * atm
        height = height * mm
        radius = radius * mm

        from .LPSDFactory import create
        detector, geometer = create(
            name, id, 
            pressure, radius, height, npixels,
            pixelSolidAngle,
            instrument)

        self.local_geometers.append( geometer )
        return detector
    
        
    def makeDetectorSystem( self, instrument, geometer, tubeRecords):
        #detector system
        detSystem = elements.detectorSystem( 'detSystem' )
        instrument.addElement( detSystem )
        geometer.register( detSystem, (0*mm,0*mm,0*mm), (0,0,0) )

        detSystemGeometer = geometers.geometer(
            detSystem, registry_coordinate_system = 'InstrumentScientist' )
        self.local_geometers.append( detSystemGeometer )

        numTubes = len(tubeRecords )

        for i, record in enumerate( tubeRecords ):

            detID = i #record['id']
            debug.log( 'detID=%s' % detID)
            #debug.log( 'record=%s' % record )

            pressure = 10.0 # ???

            detLength = record['geometry']['height']
            detRadius = record['geometry']['radius']

            name = 'detector%s' % detID
            detector = self.makeDetector(
                name, detID,
                instrument, pressure, numPixelsPerTube,
                detRadius, detLength)
            
            debug.log("LPSD: %s" % detector )
            
            detSystem.addElement( detector)

            rho = record['distance']['value']
            phi = record['angle']['value']
            #phi *= -1.0 #???
                
            # convert from polar to cartesian coordinates. Note theta = 90 (in
            # other words, the detector centers all lie in the scattering plane).
            x = rho*cos( phi*pi/180.0)
            y = rho*sin( phi*pi/180.0)
            z = 0.0
                                    
            detSystemGeometer.register(
                detector, (x*mm,y*mm,z*mm), detectorOrientation )

            continue

        return # detArray # arcs, geometer


def _equal( key, key1 ):
    for a, b in zip(key, key1):
        if isinstance( a, float ):
            if abs(a-b) > 1.e-8*max(abs(a),abs(b)): return False
            pass
        elif isinstance( a, int ):
            if a!=b: return False
            pass
        else:
            raise NotImplementedError
        continue
    return True



# version
__id__ = "$Id: LrmecsBootstrap.py 638 2005-10-20 01:13:19Z linjiao $"

# End of file
