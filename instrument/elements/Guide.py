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
import units
angstrom = units.length.angstrom


class Reflectivity:

    def __init__( self, 
                  low_angle_reflectivity = 1.,
                  critical_scattering_vector = 0.0219 / angstrom,
                  slope_of_reflectivity = 6.49 * angstrom ):
        self.low_angle_reflectivity = low_angle_reflectivity
        
        try: critical_scattering_vector + 1./angstrom
        except: raise ValueError, \
                "critical_scattering_vector %s has wrong unit" % critical_scattering_vector
        self.critical_scattering_vector = critical_scattering_vector

        try: slope_of_reflectivity + angstrom
        except: raise ValueError, \
                "slope_of_reflectivity %s has wrong unit" % slope_of_reflectivity
        
        self.slope_of_reflectivity = slope_of_reflectivity
        return

    pass # end of Reflectivity


def _convertToReflectivity( l ):
    parser = units.parser()
    l = tuple(l)
    assert len(l)==3
    
    low_angle_reflectivity = int(l[0])
    
    if isstr(l[1]): critical_scattering_vector = parser.parse( l[1] )
    else: critical_scattering_vector = l[1]

    if isstr(l[2]): slope_of_reflectivity = parser.parse( l[2] )
    else: slope_of_reflectivity = l[2]

    Reflectivity( low_angle_reflectivity, critical_scattering_vector, slope_of_reflectivity )
    
    return low_angle_reflectivity, critical_scattering_vector, slope_of_reflectivity


def isstr(s): return isinstance(s, basestring )


defaultReflectivity = [1., 0.0219 / angstrom,6.49 * angstrom]

class Guide( Element ):

    class Attributes(Element.Attributes):

        import Attribute

        reflectivity = Attribute.list(
            "reflectivity", default = defaultReflectivity,
            validator = _convertToReflectivity )
        reflectivity.meta['tip'] = \
            "reflectivity parameters: a list of 3 values: "\
            "low_angle_reflectivity, "\
            "critical_scattering_vector, "\
            "and slope_of_reflectivity. "
        
        m = Attribute.float( "m", default = 2. )
        m.meta['tip'] = "m-value. Zero means completely absorbing."
        
        W = Attribute.dimensional( "W", default = 0.003/angstrom)
        W.meta['tip'] = "Width of supermirror cut-off"
        pass
        

    def __init__( self, name, shape = None, **attributes):
        """
        Guide ctor
        reflectivity: reflectivity property. an instance of Reflectivity
        m: m-value of material. Zero means completely absorbing.
        W: Width of supermirror cut-off
        """
        if shape is None: shape = defaultShape
        Element.__init__(
            self, name, shape = shape, **attributes)
        return


    def identify( self, visitor):
        return visitor.onGuide( self)

    pass # end of Guide



import instrument.geometry.shapes as shapes

cm = units.length.cm
defaultShape = shapes.rectTube( (10*cm,10*cm), 100*cm, (8*cm,8*cm) )  #unit: cm # should we put unit in there?

def createRectangularGuide( name, front, length, back,
                            reflectivity = defaultReflectivity,
                            m = 2., W = 0.003/angstrom, **attributes):
    shape = shapes.rectTube( front, length, back )
    return Guide( name, shape, reflectivity=reflectivity,
                  m = m, W = W, **attributes)

def test():
    createRectangularGuide("guide", (10,10), 100, (9,9) )
    createRectangularGuide("guide", (10,10), 100, (9,9), guid = 3 )
    return

if __name__ == "__main__": test()

# version
__id__ = "$Id: Moderator.py 487 2005-06-22 22:52:09Z tim $"

# End of file
