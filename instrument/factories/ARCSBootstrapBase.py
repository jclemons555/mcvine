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


## This piece of code create a graph of instrument elements for ARCS.
## The ARCS instrument has a hierarchy of detectors: three rows of
## 8-packs. Each row has 37-38 packs. Each pack has 8 tubes.
## Theare two kinds of packs, short packs and long packs.
## Short packs have short detectors, while long packs have long
## detectors.
## Long detectors are 1meter long, short detectors are ?? long.
## The key thing in this code is to create the detector system.
## Please note that I will use copies as long as it is possible,
## because this simplifies many things.
## For example, when I build a long 8-pack, I build one long
## detector tube module,
## and then make 7 copies of that module to create a long 8-pack.
## After I build this long 8-pack, all other long packs
## can be build as copies of this pack.



class PackInfo:

    id = None
    position = None # unit: mm
    orientation = None # unit: degree
    pressure = None # unit: atm
    ntubes = None
    tubelength = None # unit: mm
    tuberadius = None # unit: mm
    tubegap = None # unit: mm
    npixelspertube = None


def packType(packinfo):
    return packinfo.pressure, packinfo.ntubes, packinfo.tubelength, packinfo.tuberadius, packinfo.tubegap, packinfo.npixelspertube



from math import sqrt, acos, atan, pi, cos, sin
import units
atm = units.pressure.atm
m = units.length.m
cm = units.length.cm
mm = units.length.mm

import instrument.elements as elements
import instrument.geometers as geometers
import instrument.geometry.shapes as shapes


#hack
#set all solid angle to 1
pixelSolidAngle = 1.


monitorRecords = [
    { 'id': 0,
      'distanceToModerator': 11.831*m,
      #width, height, thickness
      'dimensions': [7.62*cm, 7.62*cm, 3.81*cm],
      },
    { 'id': 1,
      'distanceToModerator': 18.5*m,
      #width, height, thickness
      'dimensions': [7.62*cm, 7.62*cm, 3.81*cm],
      },
    ]      


from _journal import debug


class InstrumentFactory( object):
    
    """Use given detector info and
    hard-coded info to construct an
    Instrument object and a geometer for ARCS"""


    def construct( 
        self, packs,
        mod2sample = 13.6*m, xmloutput = None ):
        '''construct a new ARCS instrument

Parameters:
  -packs: a list of PackInfo instances
  -mod2sample: moderator to sample distance
'''
        self._instrument = arcs = elements.instrument(
            "ARCS" )# version="0.0.0")

        #instrument local geometer
        geometer = geometers.geometer(
            arcs, registry_coordinate_system = 'InstrumentScientist' )
        self.local_geometers = [geometer]

        # make Moderator
        self.makeModerator( arcs, geometer )

        # make monitors: adds elements to arcs & geometer
        self.makeMonitors( arcs, geometer, monitorRecords)

        #make sample
        sample = elements.sample(
            'sample',guid = arcs.getUniqueID() )
        arcs.addElement( sample )
        geometer.register( sample, (mod2sample,0*m,0*m), (0,0,0) ) 

        # make detector array: adds elements to arcs & geometer
        self.makeDetectorSystem(arcs, geometer, packs)

        # set up guid registry
        arcs.guidRegistry.registerAll( arcs )

        # instrument global geometer
        instrumentGeometer = geometers.arcs(
            arcs, self.local_geometers,
            registry_coordinate_system = 'InstrumentScientist' )
        
        arcs.geometer = instrumentGeometer
        
        # clean up temporary variables
        del self.local_geometers, self._instrument
        
        # save the xml description
        if xmloutput:
            from instrument.nixml import weave
            print 'write arcs instrument to %s' % xmloutput
            weave( arcs, open(xmloutput, 'w') )
        return arcs, instrumentGeometer


    def makeModerator( self, instrument, geometer):
        #hard code moderator. this should be ok because
        #it should not change
        modXSize = 100.0*mm; modYSize = 100.0*mm; modZSize = 100.0*mm
        position = [0* mm, 0*mm, 0*mm]
        orientation = [0.0, 0.0, 0.0]
        modID = instrument.getUniqueID()
        moderator = elements.moderator(
            'moderator', 
            modXSize, modYSize, modZSize,
            type = "non-existant",
            guid = modID,
            )
        
        instrument.addElement( moderator )
        geometer.register( moderator, position, orientation)
        return
    

    def makeMonitors( self, instrument, geometer, monitorRecords):

        i = 0

        for record in monitorRecords:
            monid = record['id']
            dist = record['distanceToModerator']
            position = [dist, 0 * mm, 0 * mm]
            name = "monitor%s" % i
            
            debug.log("monitor position: %s, monitor name: '%s', id: %s" %
                      (position, name, monid))

            dimensions = record['dimensions']
            width, height, thickness = dimensions

            monitor = elements.monitor(
                name, width, height, thickness,
                guid = instrument.getUniqueID() )
            
            instrument.addElement( monitor )
            i += 1
            
            geometer.register( monitor, position, orientation=[0.0,0.0,0.0])

            continue

        return


    def makeDetectorSystem( self, instrument, geometer, packs):

        #detector system
        detSystem = elements.detectorSystem(
            'detSystem', guid = instrument.getUniqueID())
        instrument.addElement( detSystem )
        geometer.register( detSystem, (0*m,0*m,0*m), (0,0,0),
                           relative = instrument.getSample() )

        detSystemGeometer = geometers.geometer(
            detSystem, registry_coordinate_system = 'InstrumentScientist' )
        self.local_geometers.append( detSystemGeometer )

        from numpy import array

        cache = {}
        for packinfo in packs:

            rotation = packinfo.orientation
            translation = tuple(array( packinfo.position )*mm)

            packID = packinfo.id
            name = 'pack%s' % packID
            
            packtype = packType(packinfo)
            pack = cache.get(packtype)

            if pack is None:
                pressure, ntubes, height, radius, gap, npixels = \
                    packtype
                
                assert ntubes == 8, "not implemented"
                
                pack = cache[packtype] = self._makePack(
                    name, packID, instrument,
                    pressure*atm, npixels, radius*mm, height*mm, gap*mm)
                
            else:
                copy = elements.copy(
                    'pack%s' % packID, pack.guid(),
                    id = packID,
                    guid = instrument.getUniqueID() )
                pack = copy
                pass
            
            detSystem.addElement( pack )
            detSystemGeometer.register(
                pack, translation, rotation )

            continue

        return # detArray # arcs, geometer

    
    # XXX: need more thoughts here
    # 180 degree is an artifact of current limitation of simulation
    # package.
    tube_orientation = (0, 180, 0) 
    def _makePack(self, name, id, instrument,
                  pressure, npixels, radius, height, gap ):
        '''make a unique 8-pack
        
all physical parameters must have units attached.
'''
        from ARCS.packSize import getSize
        size = getSize( radius, height, gap )
        shape = shapes.block( **size )
        pack = elements.detectorPack(
            name, shape = shape, guid = instrument.getUniqueID(), id = id )
        packGeometer = geometers.geometer( pack )
        self.local_geometers.append( packGeometer )

        det0 = self._makeDetector(
            'det0', 0, instrument, pressure, npixels, radius, height )
        pack.addElement( det0 )

        from ARCS.tubePositions import getPositions
        positions = getPositions( radius, gap )
        packGeometer.register( det0, (0*m,positions[0],0*m), self.tube_orientation)
        
        for i in range(1,8):
            det = elements.copy( 'det%s' % i, det0.guid(),
                                 guid = instrument.getUniqueID() )
            pack.addElement( det )
            packGeometer.register( det, (0*m,positions[i],0*m), self.tube_orientation)
            continue
        return pack
    
    
    def _makeDetector(self, name, id, instrument, 
                      pressure, npixels, radius, height):
        '''make a unique detector module

all physical parameters must have units attached.
'''
        from LPSDFactory import create
        detector, geometer = create(
            name, id, 
            pressure, radius, height, npixels,
            pixelSolidAngle,
            instrument)
        self.local_geometers.append( geometer )
        return detector

    pass # end of InstrumentFactory


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
__id__ = "$Id: ARCSBootstrap.py 1301 2009-03-04 16:40:10Z linjiao $"

# End of file
