#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2006  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from Element import Element, debug


class Monitor( Element):

    class Attributes(Element.Attributes):
        import Attribute
        mode = Attribute.str("mode", default = "monitor")
        mode.meta['tip'] = "monitor mode: either 'monitor' or 'timer'"
        
        sampledFraction = Attribute.float(
            "sampledFraction", default = 0.01)
        mode.meta['tip'] = "sampled fraction of neutron beam"
        pass # end of Attributes


    def identify( self, visitor):
        return visitor.onMonitor( self)


    def __init__( self, name, shape = None,
                  **attributes):
        if shape is None: shape = defaultShape
        Element.__init__( self, name, shape = shape, **attributes)
        return

    pass # end of Monitor



import instrument.geometry.shapes as shapes

import units
cm = units.length.cm
defaultShape = shapes.block( 10*cm,10*cm, 1*cm )

def createNormalMonitor(
    name, width, height, thickness, mode = 'monitor',
    sampledFraction = 0.01, **kwds):
    shape = shapes.block( width, height, thickness )
    return Monitor( name, shape = shape, mode = mode,
                    sampledFraction = sampledFraction, **kwds)


def main():
    m = createNormalMonitor( 'monitor', 10, 10, 0.1, 'abc', 1.0 )
    assert m.attributes.mode == 'abc'
    assert m.attributes.sampledFraction == 1
    
    m = createNormalMonitor( 'monitor', 10, 10, 0.1, 'abc', 1.0, guid=100 )
    return

if __name__ == '__main__': main()


# version
__id__ = "$Id$"

# End of file
