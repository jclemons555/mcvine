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


import journal
debug = journal.debug("instrument.geometers")


from AbstractGlobalGeometer import AbstractGlobalGeometer

class AbstractInstrumentGeometer( AbstractGlobalGeometer ):
    
    """Maintain positions and orientations of elements in an instrument;
    measures displacements between elements."""


    def displacement( self, element1, element2):
        """displacement( el1, el2) -> vector from el2 to el1
        """
        self._abstract( "displacement" )


    def orientation( self, element):
        """orientation( element) -> orientation of element rel. to instrument
        coordinate system.
        List of three angles.
        Use changeCoordinateSystem to change the coordinate system 
        Use getCoordinateSystemDescription to get description of the current coordinate
          system.
        """
        self._abstract( "orientation" )
        

    def position( self, element):
        """position( element) -> displacement of element's reference point
        from parent's reference point
        Use changeCoordinateSystem to change the coordinate system 
        Use getCoordinateSystemDescription to get description of the current coordinate
          system.
        """
        self._abstract( "position" )
          

##     def phi(self, detector):
##         msg = "%s must provide method 'phi' to return phi angle of given detector" % (
##             self.__class__.__name__)
##         raise NotImplementedError , msg


    def distanceToSample(self, element ):
        """return distance between the given element and sample position
        """
        self._abstract( "distanceToSample" )
        

    def scatteringAngle( self, element ):
        self._abstract( "scatteringAngle" )
        

    def getCoordinateSystemDescription( self):
        """getCoordinateSystemDescription() -> verbal description of current
        coordinate system"""
        self._abstract( "getCoordinateSystemDescription" )


    pass # end of AbstractInstrumentGeometer


# version
__id__ = "$Id: Geometer.py 1156 2006-10-12 00:51:00Z linjiao $"

# End of file
