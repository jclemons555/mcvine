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


def create(name, id, 
           pressure, radius, height, npixels,
           pixelSolidAngle,
           guidGenerator,
           detectorFactory = None,
           pixelFactory = None,
           geometerFactory = None):
    '''make a unique detector module

all physical parameters must have units attached.
'''
    if detectorFactory is None:
        from instrument.elements import detector as detectorFactory
        pass

    if pixelFactory is None:
        from instrument.elements import pixel as pixelFactory
        pass

    if geometerFactory is None:
        from instrument.geometers import geometer as geometerFactory
        pass
    
    guid = guidGenerator.getUniqueID()

    # create detector itself
    detector = detectorFactory(
        name, 
        radius = radius, height = height, pressure = pressure,
        guid = guid, id = id,
        )

    # geometer for pixels in the detector
    detectorGeometer = geometerFactory( detector )

    # now pixels
    #  first pixel
    #   pixel height
    pixelht = height / npixels
    # pixel must from down to up. this is a requirement from
    # instrument simulation
    bottom = (-(npixels)/2.0 + 0.5)*pixelht
    pixel0 = pixelFactory(
        'pixel0',
        radius = radius, height = pixelht, solidAngle = pixelSolidAngle,
        guid = guidGenerator.getUniqueID(),
        )
    detector.addElement( pixel0 )
    detectorGeometer.register( pixel0, (0*pixelht,0*pixelht,bottom), (0,0,0) )

    #  all other pixels are copies of the first pixel
    from instrument.elements import copy
    for i in range(1, npixels):
        pixel = copy( 'pixel%s' % i, reference = pixel0.guid(),
                      guid = guidGenerator.getUniqueID() )
        z = bottom + i*pixelht
        detector.addElement( pixel )
        detectorGeometer.register( pixel, (0*pixelht,0*pixelht,z), (0,0,0) )
        continue
    
    return detector, detectorGeometer



# version
__id__ = "$Id$"

# End of file 
