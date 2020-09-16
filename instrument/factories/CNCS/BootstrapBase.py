#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                      (C) 2005-2014  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


## This piece of code create a graph of instrument elements for CNCS.
## modified from ..HYSPEC.BootstrapBase


from ..HYSPEC.BootstrapBase import InstrumentFactory as base, PackInfo, units, elements, geometers, shapes, packType, pixelSolidAngle, m, mm, atm

class InstrumentFactory( base ):
    
    """Use given detector info and
    hard-coded info to construct an
    Instrument object and a geometer for CNCS"""


    def construct( 
        self, packs,
        xmloutput = None ):
        '''construct a new CNCS instrument

Parameters:
  -packs: a list of PackInfo instances
'''
        self._instrument = cncs = elements.instrument(
            "CNCS" )# version="0.0.0")
        
        #instrument local geometer
        geometer = geometers.geometer(
            cncs, registry_coordinate_system = 'InstrumentScientist' )
        self.local_geometers = [geometer]
        
        # make Moderator
        # self.makeModerator( cncs, geometer )
        
        # make monitors: adds elements to cncs & geometer
        # self.makeMonitors( cncs, geometer, monitorRecords)
        
        #make sample
        sample = elements.sample(
            'sample',guid = cncs.getUniqueID() )
        cncs.addElement( sample )
        geometer.register( sample, (0*m,0*m,0*m), (0,0,0) ) 
        
        # make detector array: adds elements to cncs & geometer
        self.makeDetectorSystem(cncs, geometer, packs)
        
        # set up guid registry
        cncs.guidRegistry.registerAll( cncs )
        
        # instrument global geometer
        instrumentGeometer = geometers.arcs(
            cncs, self.local_geometers,
            registry_coordinate_system = 'InstrumentScientist' )
        
        cncs.geometer = instrumentGeometer
        
        # clean up temporary variables
        del self.local_geometers, self._instrument
        
        # save the xml description
        if xmloutput:
            from instrument.nixml import weave
            print('write cncs instrument to %s' % xmloutput)
            weave( cncs, open(xmloutput, 'w') )
        return cncs, instrumentGeometer
    
    
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
        #### not used right now ####
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

        return # detArray # cncs, geometer

    
    # XXX: need more thoughts here
    # 180 degree is an artifact of current limitation of simulation
    # package.
    tube_orientation = (0, 180, 0) 
    def _makePack(self, name, id, instrument,
                  pressure, npixels, radius, height, gap ):
        '''make a unique 8-pack
        
all physical parameters must have units attached.
'''
        from .packSize import getSize
        size = getSize( radius, height, gap )
        shape = shapes.block( **size )
        pack = elements.detectorPack(
            name, shape = shape, guid = instrument.getUniqueID(), id = id )
        packGeometer = geometers.geometer( pack )
        self.local_geometers.append( packGeometer )
        
        det0 = self._makeDetector(
            'det0', 0, instrument, pressure, npixels, radius, height )
        pack.addElement( det0 )
        
        from .tubePositions import getPositions
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
        from ..LPSDFactory import create
        detector, geometer = create(
            name, id, 
            pressure, radius, height, npixels,
            pixelSolidAngle,
            instrument)
        self.local_geometers.append( geometer )
        return detector

    pass # end of InstrumentFactory


# version
__id__ = "$Id$"

# End of file
