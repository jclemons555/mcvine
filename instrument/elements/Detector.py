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


from ElementContainer import ElementContainer
import journal
debug = journal.debug("instrument")


class Detector( ElementContainer):
    
    """The common part of the interface for detectors"""

    allowed_item_types = [
        'Pixel',
        'Copy',
        ]    

    class Attributes(ElementContainer.Attributes):

        import Attribute

        import units
        pressure = Attribute.dimensional(
            'pressure', default = 10*units.pressure.atm )

        type = Attribute.str( 'type', default = 'He3 LPSD' )
        type.meta['tip'] = 'type of detector'

        deadTime = Attribute.dimensional(
            'deadTime', default = 10 * units.time.microsecond )

        holdOff = Attribute.dimensional(
            'holdOff', default = units.time.microsecond )
        holdOff.meta['tip'] = "Delay for this detector to register an event (microsec)"

        pass # end of Attributes


    def __init__( self, name, shape = None, **attributes):
        """Detector( name, shape,
          gasPressure = 10.*atm,
          type = "He3 LPSD",
          deadTime = 1.* microsecond,
          )
        """
        if shape is None: shape = defaultShape
        ElementContainer.__init__( self, name, shape = shape, **attributes)
        return


    # visitor
    def identify( self, visitor):
        return visitor.onDetector( self)


    pass # end of Detector



import instrument.geometry.shapes as shapes
import units
cm = units.length.cm

defaultShape = shapes.cylinder( 1.25*cm, 100.*cm )  #unit: cm # should we put unit in there?

def createDetector( name, radius = 1.25*cm, height = 100.*cm, **attributes):
    shape = shapes.cylinder( radius, height )
    return Detector( name, shape, **attributes )



def test():
    d = createDetector("detector", 2.5, 100 )
    assert d.guid() == -1
    
    d = createDetector("detector", 2.5, 100, guid = 10 )
    assert d.guid() == 10

    d = Detector( 'det', guid = 100 )
    assert d.guid() == 100
    import instrument.geometry.shapes as shapes
    assert shapes.isshape( d.shape() )
    return
    
if __name__ == "__main__": test()



# comments from Tim's code
# Note: Nexus items "input" was excluded because I do not
# know what it is meant to mean.
# "calibration_data" and "calibration_method" were excluded because they are
# not properties of the detector per se.


# version
__id__ = "$Id$"

# End of file
