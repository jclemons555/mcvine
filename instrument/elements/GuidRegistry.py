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


from ._journal import debug


class GuidRegistry:


    def __init__(self):
        self._registry = {}
        return


    def register(self, guid, element):
        debug.log( 'register element %r, guid=%r' % (
            element, guid ) )
        self._registry[ guid ] = element
        return


    def guid2element(self, guid):
        if guid not in self._registry:
            raise KeyError("guid has not been registered: %r" % guid)
        return self._registry[guid]


    def registerAll(self, instrument):
        instrument.identify(self)
        return


    def onElementContainer(self, container):
        self.onElement( container )
        for element in container:
            element.identify(self)
            continue
        return
    onInstrument = onDetector = onDetectorSystem = onDetectorArray \
                   = onDetectorPack = onElementContainer


    def onElement(self, element):
        self.register( element.guid(), element )
        return

    onSample = onCopy = onPixel = onModerator = onMonitor = onGuide = onElement


    pass # end of GuidRegistry

    

# version
__id__ = "$Id$"

# End of file
