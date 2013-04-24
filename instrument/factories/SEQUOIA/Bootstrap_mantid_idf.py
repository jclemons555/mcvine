# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                      (C) 2005-2013  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


"""
Compose SEQUOIA instrument from mantid IDF xml file.

This implementation only uses the detector packs information
from mantid IDF. 

XXX: should consider reading other information like moderator
XXX: and monitors from IDF as well.

XXX: coordinate system is now hard coded.

      <along-beam axis="z"/>
      <pointing-up axis="y"/>
      <handedness axis="right"/>

"""

from .BootstrapBase import InstrumentFactory as base, PackInfo, units
class InstrumentFactory(base):
    
    tube_orientation = (0,0,0) # overwrite to match mantid convention
    
    def construct( 
        self, idfpath,
        mod2sample = 20.0254*units.length.meter,
        pressure=10 * units.pressure.atm, 
        tuberadius=0.5 * units.length.inch, 
        tubegap = 0.08 * units.length.inch,
        xmloutput = None ):
        
        # default output file
        if not xmloutput:
            import os
            base = os.path.basename(idfpath)
            fn = os.path.splitext(base)[0]
            xmloutput = '%s-danse.xml' % (fn,)
            
        # get packs from nexus file
        self.pressure = pressure/units.pressure.atm
        self.tuberadius = tuberadius/units.length.mm
        self.tubegap = tubegap/units.length.mm        
        packs = self._readPacks(idfpath)
        
        return super(InstrumentFactory, self).construct(
            packs, mod2sample=mod2sample, xmloutput=xmloutput)


    def _readPacks(self, idfpath):
        from ...mantid import parse_file
        inst = parse_file(idfpath)
        
        import operator as op
        rows = inst.detectors
        getpacks = lambda row: row.getType().components
        packs = [getpacks(row) for row in rows]
        packs = reduce(op.add, packs)
        
        for pkno, pkinfo in enumerate(packs):
            
            eightpack = pkinfo.getType().components[0]
            eightpack_type = eightpack.getType()
            ntubes = getNTubes(eightpack_type)
            npixels = getNPixelsPerTube(eightpack_type)
            position, orientation = getPositionAndOrientation(eightpack)
            tubelen = getTubeLength(eightpack_type)
            
            pack = PackInfo()
            pack.id = pkno
            pack.position = position 
            pack.orientation = orientation
            pack.pressure = self.pressure 
            pack.ntubes = ntubes
            pack.npixelspertube = npixels
            pack.tubelength = tubelen * 1000
            
            pack.tuberadius = self.tuberadius
            pack.tubegap = self.tubegap
            
            yield pack
            continue
        
        return


def getTubeLength(eightpack_type):
    tube = eightpack_type.components[0]
    tube_type = tube.getType()
    pixels = tube_type.components[0]
    locations = pixels.getChildren('location')
    y0 = float(locations[0].y)
    y_1 = float(locations[-1].y)
    n = len(locations)
    return (y_1-y0)/(n-1)*n


def getNTubes(eightpack_type):
    tube = eightpack_type.components[0]
    locations = tube.getChildren('location')
    return len(locations)


def getNPixelsPerTube(eightpack_type):
    tubes = eightpack_type.components[0]
    tube_type = tubes.getType()
    pixels = tube_type.components[0]
    locations = pixels.getChildren('location')
    return len(locations)


def getPositionAndOrientation(eightpack):
    location = eightpack.getChildren('location')[0]
    x = float(location.x); y = float(location.y); z = float(location.z)
    # pos = x,y,z
    # unit: mm
    pos = z*1000, x*1000, y*1000
    
    rot1 = location.getChildren('rot')[0]
    rot1 = getRotation(rot1)
    assert rot1[0] == [0., 1., 0.]
    rot = 0,0,rot1[1]-180
    return pos,rot


def getRotation(rot):
    axis = rot['axis-x'], rot['axis-y'], rot['axis-z']
    axis = map(float, axis)
    angle = float(rot['val'])
    return axis, angle


# version
__id__ = "$Id$"

# End of file
