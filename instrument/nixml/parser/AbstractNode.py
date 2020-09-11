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

import journal
debug = journal.debug("instrument.xmlparser")


from pyre.xml.Node import Node
import urllib.request, urllib.parse, urllib.error



class XMLFormatError(Exception): pass


class AbstractNode(Node):

    ElementFactory = None # overload this to provide factory method of creating element

    def __init__(self, document, attributes):
        Node.__init__(self, document)

        try:
            name = attributes['name']
        except KeyError:
            print(list(attributes.keys()))
            raise XMLFormatError("Element does not have the 'name' attribute."\
                  "Element type: %s" % (
                self.__class__.__name__ ))
        guid = attributes.get('guid')

        # convert to dictionary
        attrs = {}
        for k,v in list(attributes.items()): attrs[str(k)] = v
        del attrs['name'], attrs['guid']

        # see if we have instrument instance established
        try:
            instrument = document.instrument
        except AttributeError :
            instrument = None
            
        # create guid if necessary and possible
        if guid is None and instrument:
            guid = instrument.getUniqueID()
            pass

        # new element
        self.element = self.ElementFactory(name, guid = guid, **attrs)

        #register guid, element pair
        if instrument is None and isInstrument(self.element):
            #establish instrument instance
            document.instrument = instrument = self.element
            pass
        if instrument is None:
            raise RuntimeError("Instrument is not yet defined")
        #instrument.guidRegistry.register( self.element.guid(), self.element )

        # if new element is a copy, need to establish reference
##         element = self.element
##         if isCopy(element):
##             ref = element.attributes.reference
##             refelement = instrument.guidRegistry.guid2element( ref )
##             element._setReferenceElement( refelement )
##             pass
        return


    def notify(self, parent):
        return self.element.identify( parent )


    def content(self, content):
        debug.log( "content=%s" % content )
        content = content.strip()
        if len(content)==0: return
        self.element.appendContent( urllib.parse.unquote(content).strip() )
        self.locator = self.document.locator
        return


    def onElement(self, element):
        self.element.addElement( element )
        return

    pass



def isCopy( element ):
    from instrument.elements.Copy import Copy
    return isinstance( element, Copy )


def isInstrument( element ):
    from instrument.elements.Instrument import Instrument
    return isinstance( element, Instrument )


# version
__id__ = "$Id: AbstractNode.py,v 1.1.1.1 2005/03/08 16:13:43 linjiao Exp $"

# End of file 
