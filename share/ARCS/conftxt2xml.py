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


from pyre.units.length import *

lgstart = '<LocalGeometer registry-coordinate-system="InstrumentScientist">'
lgend = '</LocalGeometer>'


def readConf( conffn ):
    lines = open(conffn).readlines()
    vars = lines[0].split()
    vars = [ var.lower() for var in vars ]

    ret = []
    for line in lines[1:]:
        try:
            cmd = ','.join(vars) + '=' + 'line.split()'
            exec cmd
        except Exception, err:
            print "Warning: the following line is not parsed because of %s:%s" % (err.__class__.__name__, err)
            print line
            continue
        idx = int(idx)
        for a in [ 'radius', 'azimuth', 'polar', 'xrot', 'yrot', 'zrot',
                   'xtrn', 'ytrn', 'ztrn' ]:
            exec '%s=float(%s)' % (a,a)
            continue

        record = [ (xrot, yrot, zrot), (xtrn, ytrn, ztrn) ]
        ret.append(record)
        continue
            
    return ret


def convert(records):
    '''the rotations given in the file is not in the same
    convention used by 'instrument' package. Need to do
    a conversion here'''
    from numpy import array
    for i, r in enumerate( records ):
        rotation, translation = r
        rotation = 0,0,90+rotation[2] 
        translation = tuple(array( translation )/ 1000.)
        records[i] = rotation, translation
        continue
    return records


def packShapeStr(tuberadius, tubelength, tubegap):
    from packSize import getSize
    size = getSize( tuberadius, tubelength, tubegap )
    width = size['width']/inch
    height = size['height']/meter* 1.005 # 1.005 to make the pack a little longer than the tube
    thickness = size['thickness']/inch
    
    return '<block width="%s*inch" height="%s*m" thickness="%s*inch"/>' %(
        width, height, thickness)



def tubeShapeStr(radius, height):
    return '<cylinder radius="%s*inch" height="%s*m"/>' % (
        radius/inch, height/meter)



def tubesStr( radius, gap ):
    n = 8
    
    base = 10000
    tubes = [ '<Copy name="det%s" reference="%s" guid="%s"/>' % (
        i, base, base+i)  for i in range(1,n) ]

    from tubePositions import getPositions
    positions = getPositions( radius, gap )/inch
    # 8 tubes
    assert len(positions)==8
    # must be descending because of the convention used by ARCS:
    # left-top pixel: id 0
    # right-bottom pixel: id 1024
    assert positions[1]-positions[0] < 0

    # 180 rotation: artifact of simulation and ARCS convention
    hint = '''
	<!--
	    180 degree comes from the convention mismatch between how ARCS instrument labels its pixels and how instrument simulation routines handles pixels.
	-->
'''
    registrations = [
        '<Register name="det%s" position="(0*m,%s*inch,0*m)" orientation="(0, 180, 0)"/>' %(i, positions[i] )
        for i in range(n)
        ]
    lines = tubes + [lgstart] + [hint] + registrations + [lgend ]
    return '\n'.join( lines )



def pixelPosition(i, n, tubeLength):
    d = tubeLength*1./n
    return i*d - tubeLength/2. + d/2.
    

def pixelsStr( n, tubeLength ):
    pixels = [ '<Pixel name="pix%s" guid="%s"/>' % (i, 100000+i)
               for i in range(n) ]
    registrations = [
        '<Register name="pix%s" position="(0*m,0*m,%s)" orientation="(0, 0, 0)"/>' %(
        i, pixelPosition(i, n, tubeLength ) )
        for i in range(n)
        ]
    lines = pixels + [lgstart] + registrations + [lgend ]
    return '\n'.join( lines )


def toxmlstr(records):
    """we need sth like this:

    <Copy name='detPack1' reference='1000' guid='1001'/>
    <Copy name='detPack2' reference='1000' guid='1001'/>
    <LocalGeometer registry-coordinate-system='InstrumentScientist'>
      <Register name='detPack0' position='(0,0,0)' orientation='(0,0,0)'/>
      <Register name='detPack1' position='(0,0,0)' orientation='(0,0,0)'/>
      <Register name='detPack2' position='(0,0,0)' orientation='(0,0,0)'/>
    </LocalGeometer>
    """
    copies = []
    copy = '<Copy name="detPack%(i)s" reference="1000" guid="%(guid)s"/>'
    registrations = []
    regstr = '<Register name="detPack%(i)s" position="%(position)s" orientation="%(orientation)s"/>'
    
    for i,record in enumerate(records):
        orientation, position = record
        locals = {
            'i': i,
            'position': position,
            'orientation': orientation,
            'guid': 1000+i,
            }
        registrations.append( regstr % locals )
        if i != 0: copies.append( copy % locals )
        continue
    return '\n'.join( copies + [lgstart] + registrations + [lgend] ) 


def run( conftxtfn, npixelspertube,
         tuberadius, tubelength, tubegap,
         xmltemplate, outputfn ):
    
    formatstr = open(xmltemplate).read()

    records = readConf( conftxtfn )

    records = convert( records )

    packShape = packShapeStr( tuberadius, tubelength, tubegap )

    packs = toxmlstr( records )

    tubeShape = tubeShapeStr( tuberadius, tubelength )

    tubes = tubesStr( tuberadius, tubegap )

    pixels = pixelsStr( npixelspertube, tubelength )

    s = formatstr % {
        'packs': packs, 'pixels': pixels,
        'packshape': packShape, 'tubeshape': tubeShape,
        'tubes': tubes
        }

    open(outputfn, 'w').write( s )
    return


def main():
    import sys
    argv = sys.argv

    conftxt = argv[1]
    npixelspertube = int(argv[2])

    from pyre.units import parser
    parser = parser()
    
    tuberadius = parser.parse(argv[3])
    tubelength = parser.parse(argv[4])
    tubegap = parser.parse(argv[5])
    
    xmltemplate = argv[6]
    output = argv[7]

    run(conftxt, npixelspertube, tuberadius, tubelength, tubegap,
        xmltemplate, output)
    return


if __name__ == '__main__': main()


# version
__id__ = "$Id$"

# End of file 
