#!/usr/bin/env python
# 
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 
#                               Michael A.G. Aivazis
#                        California Institute of Technology
#                        (C) 1998-2004  All Rights Reserved
# 
#  <LicenseText>
# 
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

## \mainpage Instrument
##
## classes in this package are used to represents an instrument,
## independently of any particular measurement.
## It could be used in several places, such as parsing files derived from engineering
## plans of an instrument (for
## <a href="../../../reduction/reduction/html/"> reduction </a>
## package ), creating a 3d visualization of an instrument, or perhaps
## in setting up a Monte Carlo simulation.
##
## An instrument consists of several instrument elements and form a hierarchial structure.
## All instrument elements are in subpackage instrument.elements.
## In our design, all instrument elements are derived from class
## instrument.elements.Element.Element.
## An instrument object can be built out of those elements and follow the real instrument
## as closely as possible. An example of an instrument can be shown in the following
## diagram:
##
## \image html instrument_TopLevel_UML.jpg
##
## Currently this package is mostly concerned with inelastic direct geometry
## time-of-flight
## instrument. To support more instruments, we just need to find out those elements
## that are not yet supported and add them to the element library.
##
## \section geometers_sec geometers
## Geometers are responsible to measure distances, angles, and other geometric
## quantities. Each instrument should have an geometer (or several geometers)
## associated. Geometers are in subpackage instrument.geometers.
##
## \section factories_sec factories
##
## Three instruments are now supported: LRMECS, PHAROS, and ARCS.
## Factory methods are created for those instruments and a factory method
## can create a representation of a particular instrument by reading
## a text configuration file (for older instruments not using nexus)
## or a nexus file (for ARCS).
##
## Note: Since the nexus format for ARCS is not settled yet, so the support
## for ARCS may not be compatible with nexus standard.
## 
## For more information, try
## <a href="http://wiki.cacr.caltech.edu/danse/index.php/Instrument_and_related_classes">wiki page </href>
##
## To add a new element:
##  - add a new class in directory "elements"; update Make.mm
##  - add a new class in directory "nixml/parsers"; update Make.mm
##  - add a line in class nixml/parsers/Document.py
##  - in nixml/parsers, find the class that corresponds to the parent
##    element of the new lement, add a method "on<new element class name>"
##    to the class.
##  - nixml/Renderer.py, implement on<new element class name>. Usually
##    onElement or onElementContainer will just work. 




def mask( *args, **kwds ):
    from DetectorMask import DetectorMask
    return DetectorMask( *args, **kwds )



def copyright():
    return "instruments pyre module: Copyright (c) 1998-2004 Michael A.G. Aivazis";


# version
__id__ = "$Id$"

#  End of file 

