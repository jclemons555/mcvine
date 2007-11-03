#!/usr/bin/env python
# Timothy M. Kelley Copyright (c) 2005 All rights reserved

msgBase = "class %s must override %s" 

class InstrumentVisitor( object):
    """Interface for visitors of Instrument object graphs."""

    def render( self, element, geometer):
        """render( element) -> ??? behavior supplied by subclass"""
        self._geometer = geometer 

        result = element.identify( self)
        
        # do not keep reference to geometer
        del self._geometer

        return result


    def onDetectorArray( self, pack):
        msg = msgBase % ( self.__class__.__name__, "onDetectorArray")
        raise NotImplementedError, msg


    def onDetectorPack( self, pack):
        msg = msgBase % ( self.__class__.__name__, "onDetectorPack")
        raise NotImplementedError, msg


    def onElement( self, element):
        msg = msgBase % ( self.__class__.__name__, "onElement")
        raise NotImplementedError, msg


    def onElementContainer( self, elementContainer):
        msg = msgBase % ( self.__class__.__name__, "onElementContainer")
        raise NotImplementedError, msg


    def onLPSD( self, lpsd):
        msg = msgBase % ( self.__class__.__name__, "onLPSD")
        raise NotImplementedError, msg


    def onLPSDPixel( self, pixel):
        msg = msgBase % ( self.__class__.__name__, "onLPSDPixel")
        raise NotImplementedError, msg


    def onModerator( self, moderator):
        msg = msgBase % ( self.__class__.__name__, "onModerator")
        raise NotImplementedError, msg
        

    def onMonitor( self, monitor):
        msg = msgBase % ( self.__class__.__name__, "onMonitor")
        raise NotImplementedError, msg
        

# version
__id__ = "$Id$"

# End of file
