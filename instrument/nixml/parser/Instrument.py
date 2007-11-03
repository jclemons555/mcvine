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


from AbstractNode import AbstractNode


class Instrument(AbstractNode):


    tag = "Instrument"
    
    from instrument.elements.Instrument import Instrument as ElementFactory

    onInstrumentGeometer = onSample = onCopy = onDetectorSystem = onGuide = onModerator = onMonitor = AbstractNode.onElement

    def notify(self, parent):
        document = self.document
        assert parent is document
        instrument = document.instrument
        assert self.element is instrument

        #establish guid registry
        instrument.guidRegistry.registerAll( instrument )
        
        return self.element.identify( parent )
        

    pass # end of Instrument
    


# version
__id__ = "$Id: Instrument.py,v 1.1.1.1 2005/03/08 16:13:43 linjiao Exp $"

# End of file 
