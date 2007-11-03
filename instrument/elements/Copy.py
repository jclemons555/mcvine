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

class DereferenceError(Exception): pass

class Copy( Element ):

    '''Copy of an existing element
    '''

    class Attributes(Element.Attributes):
        
        import Attribute
        reference = Attribute.int( "reference", default = -1)
        reference.meta['tip'] = "guid of the element to be copied" 

        pass # end of Attributes


    def reference(self):
        if self._reference is None:
            instrument = self._getRoot( )
            guid = self.attributes.reference
            try:
                element = instrument.guidRegistry.guid2element( guid )
            except KeyError, err:
                msg = "%s: Unable to dereference guid %r\n" %(
                    self.name, guid)
                msg += "My parent: %s" % self.parent()
                #msg += '%s: %s' % (err.__class__.__name__, err)
                raise DereferenceError, msg
            self._reference = element
            pass
        return self._reference
    

    def __init__( self, name, shape=None, **attributes):
        Element.__init__( self, name, shape=shape, **attributes)
        self._reference = None
        # delete this attribute so that the __getattribute__
        # trick will work. otherwise self.shape will return this
        # copy's shape which is None
        del self._shape
        return


    def __getattribute__(self, name):
        try: return object.__getattribute__( self, name )
        except AttributeError :
            return self.reference().__getattribute__(name)
        raise RuntimeError , "should not reach here"
    

    def identifyAsReferredElement( self, visitor):
        t = self.reference().__class__.__name__
        name = 'on%s' % t
        handler = getattr(visitor, name)
        return handler(self)


    def identify(self, visitor):
        return visitor.onCopy(self)


    def __str__(self): return "copy of element whose guid is %s" % (
        self.attributes.reference, )


    def __iter__(self): return self.reference().__iter__()


    def _setReferenceElement(self, element):
        self._reference = element
        return

    pass # end of Copy


def createCopy( name, reference, **kwds ):
    return Copy( name, reference = reference, **kwds )


def test():
    from Detector import Detector
    det = Detector( 'det', guid = 10 )
    from Copy import Copy
    c = Copy( 'det2', shape = None, reference = 10, guid = 11 )
    c._setReferenceElement( det )
    from DetectorSystem import DetectorSystem
    ds = DetectorSystem( 'ds' )
    ds.addElement( det )
    assert isinstance(c, Copy)
    ds.addElement( c )
    assert det.id() == 0
    assert c.id() == 1
    assert det.guid() == 10
    assert c.guid() == 11
    assert c.shape() is det.shape()
    assert c.elements() is det.elements()
    import units
    atm = units.pressure.atm
    c.pressure() + atm
    return


def test2():
    from Detector import Detector
    det = Detector( 'det', guid = 10 )
    from Copy import Copy
    c = Copy( 'det2', shape = None, reference = 10, guid = 11 )
    c._setReferenceElement( det )
    from DetectorSystem import DetectorSystem
    ds = DetectorSystem( 'ds' )
    ds.addElement( det )
    assert isinstance(c, Copy)
    ds.addElement( c )

    class Printer:

        def render(self, target):
            return target.identify(self)

        def onElementContainer(self, c):
            self.onElement(c)
            for e in c:
                e.identify(self)
                continue
            return

        onDetector = onDetectorSystem = onElementContainer

        def onElement(self, e):
            print e
            print 'guid=%s, id=%s' % (e.guid(), e.id())
            return

        def onCopy(self, copy):
            return copy.identifyAsReferredElement(self)

        pass # end of Printer

    Printer().render( ds )
    return
    
    

def main():
    createCopy( 'detector2', 301 )
    createCopy( 'detector2', 301, guid = 1000 )
    test()
    test2()
    return

if __name__ == '__main__': main()

    
# version
__id__ = "$Id: Copy.py 1238 2007-09-20 11:50:47Z linjiao $"

# End of file
