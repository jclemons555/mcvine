#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                 Jiao Lin   
#                      California Institute of Technology
#                      (C)   2007    All Rights Reserved
#
# <LicenseText>
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from pyre.xml.Node import Node


class InstrumentGeometer(Node):

    tag = "InstrumentGeometer"
     
    def __init__(self, document, attributes):
        Node.__init__(self, document)
        self._coord_system = attributes.get('registry-coordinate-system')
        self._type = attributes.get('type')
        return


    def notify(self, parent):
        #parent is a xml node. parent.element is an instrument
        #that the geometer should attach to
        target = parent.element

        instrument = target

        #instrument geometer
        #ctor of instrument geometer inferred from attribute 'type'
        import instrument.geometers as igs
        try:
            ctor = getattr(igs, self._type)
        except:
            #default ctor
            ctor = igs.instrumentGeometer

        document = self.document
        geometers = document.geometers
        
        coordinatesystem = self._coord_system
        #if coordinatesystem is not specified in the xml
        #try to see if any local geometers specified it.
        #in this implementation, we are assuming that
        #all geometers have the same registry coordinatesystem.
        #if not, we don't know what to do.
        if not coordinatesystem and len(geometers):
            coordinatesystem = geometers[0].registry_coordinate_system().name
            pass
        instrument.geometer = ctor(
            instrument, geometers,
            registry_coordinate_system = coordinatesystem )
        
        return instrument.geometer

    pass # end of InstrumentGeometer
    


# version
__id__ = "$Id: Geometer.py,v 1.1.1.1 2005/03/08 16:13:43 linjiao Exp $"

# End of file 
