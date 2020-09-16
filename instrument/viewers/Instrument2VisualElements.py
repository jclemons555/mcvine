#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2006 All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


import journal
warning = journal.warning("instrument.visitors.Instrument2VisualElements")
debug = journal.debug("instrument.visitors.Instrument2VisualElements")


class Instrument2VisualElements:

    """Renderer to render an instrument to a collection of visual
    elements.

    This class renders an instrument to a list of visual elements so
    a renderer can take that list and render a visual representation.

    An instrument should be a graph consisting of instrument elements.

    The result would be an instance of VisualElements.

    To use this, be sure to overload "visual_properties" and
    visitor hooks ("onSth" methods) when necessary.
    
    """

    #overload 'visual_properties' to change visual properities of
    #variuos types of components
    visual_properties = {
        "Guide": {'color': (1,1,1), 'opacity': 1},
        "Moderator" : {'color': (1,0,0), 'opacity': 1},
        "DetectorBank" : {'color': (0,0,1), 'opacity': 1},
        "Detector" : {'color':(0,1,0), 'opacity':0.5},
        }
    
    
    def __init__(self, coordinate_system):
        self.coordinate_system = coordinate_system
        return


    def render(self, instrument, geometer):
        coordinate_system = self.coordinate_system
        
        #make sure geometer will return coodinates in desired coordinate system
        print("make sure geometer will return coodinates in desired coordinate system")
        geometer.changeCoordinateSystem( coordinate_system )
        #keep reference to geometer
        print("#keep reference to geometer")
        self._geometer  = geometer

        #create things to be computed
        print("#create things to be computed")
        from .VisualElements import VisualElements
        self._visual_elements = VisualElements(coordinate_system)

        #
        self._currentPath = ''
        
        #render
        print("render")
        instrument.identify(self)

        #clean up and return
        self._geometer = None
        rt = self._visual_elements; self._visual_elements = None
        return rt
    

    def onElementContainer(self, elementContainer):
        save = self._currentPath
        debug.log( "entering container %s:%s" % (save,elementContainer) )
        print("entering container %s:%s" % (save,elementContainer)) 
        self.onElement( elementContainer )

        print("childrens %s" % (elementContainer.childIdentifiers() ))
        
        for identifier in elementContainer.childIdentifiers():
            self._currentPath = '/'.join( [save, identifier] )
            print("currentPath = %s" % self._currentPath)
            element = elementContainer.getChild( identifier )
            print("element = %s" % element)
            element.identify(self)
            continue
        self._currentPath = save
        return


    def onElement(self, element):
        path = self._currentPath
        debug.log( "entering element %s:%s" % (path, element) )
        print("entering element %s:%s" % (path, element)) 
        
        self.makeVisualElement( path, element )
        return


    def getVisualProperties(self, element):
        return self.visual_properties[ element.__class__.__name__ ]


    def getGeometricProperties(self, path, element):
        elementShape = element.shape()
        print("element %s, type %s, shape: %s" % (
            element, element.__class__.__name__, elementShape ))
        if elementShape is None:
            try: name = element.name
            except: name = element
            warning.log("Cannot get shape of '%s'." % (name, ))
            return
        position, orientation = self._getCoords( path )
        return position, orientation, elementShape


    def makeVisualElement(self, path, element):
        t = self.getGeometricProperties(path, element)
        print("geometric properties: %s" % (t,))
        if t is None: return
        pos, ori, shape = t

        visualProperties = self.getVisualProperties( element )
        color = visualProperties['color']
        opacity = visualProperties['opacity']

        from .VisualElement import VisualElement
        ve = VisualElement(pos, ori, shape, color, opacity)
        self._visual_elements.add( ve )
        return
        
    
    onGuide = onElement
    onInstrument = onElementContainer


    def doNothing(self, node): return

    #overload the following methods to provide visual representations
    #for those neutron components
    onT0Chopper = onModerator = onMonitor = onFermiChopper = onElement


    def _getCoords(self, path):
        geometer = self._geometer
        return geometer.position(path), geometer.orientation(path)
 
    pass # end of Instrument2VisualElements
    

# version
__id__ = "$Id: Instrument2VisualElements.py 11 2006-04-18 08:07:50Z jiao $"

# End of file 
