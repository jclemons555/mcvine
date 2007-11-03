#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                                  Tim Kelley
#                      California Institute of Technology
#                      (C) 2005-2007  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


msgBase = "class %s must override %s" 


class Visitor( object):
    
    """Interface for visitors of Instrument object graphs."""

    def render( self, element, geometer):
        """render( element) -> ??? behavior supplied by subclass"""
        self._geometer = geometer 

        result = element.identify( self)
        
        # do not keep reference to geometer
        del self._geometer

        return result


    def onDetectorSystem(self, detSystem):
        msg = msgBase % ( self.__class__.__name__, "onDetectorSystem")
        raise NotImplementedError, msg


    def onDetectorArray( self, pack):
        msg = msgBase % ( self.__class__.__name__, "onDetectorArray")
        raise NotImplementedError, msg


    def onDetectorPack( self, pack):
        msg = msgBase % ( self.__class__.__name__, "onDetectorPack")
        raise NotImplementedError, msg


    def onDetector( self, detector):
        msg = msgBase % ( self.__class__.__name__, "onDetector")
        raise NotImplementedError, msg


    def onPixel( self, pixel):
        msg = msgBase % ( self.__class__.__name__, "onPixel")
        raise NotImplementedError, msg


    def onElement( self, element):
        msg = msgBase % ( self.__class__.__name__, "onElement")
        raise NotImplementedError, msg


    def onElementContainer( self, elementContainer):
        msg = msgBase % ( self.__class__.__name__, "onElementContainer")
        raise NotImplementedError, msg


    def onModerator( self, moderator):
        msg = msgBase % ( self.__class__.__name__, "onModerator")
        raise NotImplementedError, msg
        

    def onMonitor( self, monitor):
        msg = msgBase % ( self.__class__.__name__, "onMonitor")
        raise NotImplementedError, msg
        
    pass # end of Visitor


# version
__id__ = "$Id$"

# End of file
