# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                      (C) 2005-2010  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from ARCSBootstrapBase import InstrumentFactory as base, PackInfo, units
class InstrumentFactory(base):

    def construct( 
        self, nxfilename, nxentry='/entry',
        mod2sample = 13.6*units.length.meter,
        pressure=10 * units.pressure.atm, 
        tuberadius=0.5 * units.length.inch, 
        tubegap = 0.08 * units.length.inch,
        xmloutput = None ):
        
        # default output file
        if not xmloutput:
            import os
            xmloutput = '%s.xml' % (os.path.basename(nxfilename),)

        # get packs from nexus file
        self.pressure = pressure/units.pressure.atm
        self.tuberadius = tuberadius/units.length.mm
        self.tubegap = tubegap/units.length.mm        
        packs = self._readPacks(nxfilename, nxentry)
        
        return super(InstrumentFactory, self).construct(
            packs, mod2sample=mod2sample, xmloutput=xmloutput)


    def _readPacks(self, nxfilename, nxentry):
        reader = createReader(nxfilename, nxentry)
        dirs = reader.listdir('instrument')
        bankdirs = filter(lambda d: d.startswith('bank'), dirs)
        banknumbers = [int(s.lstrip('bank')) for s in bankdirs]
        banknumbers.sort()
        
        for bankno in banknumbers:
            bankdir = 'bank' + str(bankno)
            pack = PackInfo()
            pack.id = int(bankdir.lstrip('bank'))

            x,y,z = translation_distance = reader.readArrayFromPath(
                'instrument/%s/origin/translation/distance' % bankdir) * 1000
            pack.position = z,x,y # unit: mm

            ori = reader.readArrayFromPath(
                'instrument/%s/origin/orientation/value' % bankdir)
            x,y,z = nxorientation2angles(ori)
            pack.orientation = z,x,y+180
            
            pack.pressure = self.pressure 

            x_pixel_offset = reader.readArrayFromPath(
                'instrument/%s/x_pixel_offset' % bankdir)
            pack.ntubes = len(x_pixel_offset)

            y_pixel_offset = reader.readArrayFromPath(
                'instrument/%s/y_pixel_offset' % bankdir)
            pack.npixelspertube = n = len(y_pixel_offset)
            ht = (y_pixel_offset[-1] - y_pixel_offset[0])*(n+1)/n
            pack.tubelength = ht * 1000.
            
            pack.tuberadius = self.tuberadius
            pack.tubegap = self.tubegap

            yield pack
            continue
        
        return


def nxorientation2angles(orientation):
    a1 = orientation[:3]
    a2 = orientation[3:]
    a3 = numpy.cross(a1, a2)
    a = numpy.array((a1,a2,a3))
    from instrument.geometers.mcstasRotations import toAngles
    return toAngles(a, epsilon=1e-4)


import numpy

def createReader(filename, entry):
    import nx5.file
    nxfile = nx5.file.file(filename, 'r')
    nxreader = nx5.file.reader()
    return NeXusReader(entry, nxfile, nxreader)


class NeXusReader:

    def __init__(self, nxrootpath, nxfile, nxreader):
        self.nxroot = nxrootpath
        self.reader = nxreader
        self.file = nxfile
        self.selector = nxfile.selector()
        return


    def listdir(self, path):
        if not path.startswith('/'):
            path = '/'.join([self.nxroot, path])

        nxfile = self.file
        h5fs = nxfile.fs()
        h5dir = h5fs.open(path)
        return h5dir.read()
    
    
    def readArrayFromPath( self, path, **kwds):
        if not path.startswith('/'):
            path = '/'.join([self.nxroot, path])
        
        global _readArrayFromPath
        return _readArrayFromPath( path, self.selector, self.reader, **kwds )



def _readArrayFromPath(path, h5selector, h5reader, **kwds):
    h5selector.select( path)
    vector = h5reader.read( h5selector, **kwds )
    return vector.asNumarray()




def test1():
    
    nxorientation = [0.45523414, 0, 0.89037174,
                     0, 1, 0]
    x,y,z = nxorientation2angles(nxorientation)
    
    assert abs(x) < 1e-8
    assert abs(y+62.92) < 1e-2
    assert abs(z) < 1e-8
    return


def main():
    test1()
    return


if __name__ == '__main__': main()


# version
__id__ = "$Id$"

# End of file
