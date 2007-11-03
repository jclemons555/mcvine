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


from ElementContainer import ElementContainer, debug, typeFromName


class Instrument( ElementContainer ):
    
    """Top level container of things instrumental"""

    allowed_item_types = [
        'Moderator',
        'Guide',
        'Sample',
        'Monitor',
        'Element',
        'DetectorSystem',
        'Copy',
        ]

    def __init__( self, name, children = None, **attributes):
        """Instrument( name, children = [])
        Create a new Insturment instanc
        """
        ElementContainer.__init__(
            self, name,
            children = children,
            **attributes )
        
        from GuidGenerator import GuidGenerator
        self._guidGenerator = GuidGenerator()
        
        from GuidRegistry import GuidRegistry
        self.guidRegistry = GuidRegistry()
        return


    def getUniqueID(self): return self._guidGenerator.getUniqueID()


    def addElement(self, element):
        '''addElement( element ) --> None

        add an element.
        
        The difference between the instrument and the general
        element container is that the instrument is also
        a guid generator and it can assign the element a guid
        if necessary.
        '''
        ElementContainer.addElement( self, element )

        guid = element.guid()
        if guid == -1:
            #need guid
            guid = self.getUniqueID()
            debug.log( element.parent() )
            element._setGuid( guid )
            pass
        return


    def getModerator(self): return self._getSingleComponent( 'Moderator' )
    def getSample(self): return self._getSingleComponent( 'Sample' )
    def getDetectorSystem(self): return self._getSingleComponent( 'DetectorSystem' )
    def getMonitors(self):
        '''getMonitors() --> a list of monitors
        '''
        return self._getComponents( 'Monitor' )


    def changeSample(self, new):
        'change sample'
        try:
            sample = self.getSample()
        except:
            sample = None
            pass

        if sample is None:
            # no previous sample
            self.addElement( new )
        else:
            self.replace( sample, new )
        return


    _singlecomponenttypes = [
        'Moderator',
        'Sample',
        'DetectorSystem',
        ]
    def _getSingleComponent(self, name):
        '''Some components can only have one instance in
        an instrument, for example:

          - Moderator
          - Sample
          - Detector System

        This method returns the only component given its
        name.
        '''
        if name not in self._singlecomponenttypes:
            raise ValueError , "Component %s is not unique" % name
        t = typeFromName( name )
        for e in self.elements():
            if isinstance( e, t ): return e
            continue
        raise "Cannot find %s component" % name


    def _getComponents(self, typename):
        '''return components of given type who are direct chidren of
        this instrument. The components buried in deep hierarchy
        are not reported.
        '''
        t = typeFromName( typename )
        ret = []
        for e in self.elements():
            if isinstance( e, t ): ret.append( e )
            continue
        return ret
        

    def identify( self, visitor):
        return visitor.onInstrument( self)


    def _setGuid(self, guid):
        self.attributes.guid = guid
        assert self.attributes.guid == -1 , "guid for instrument has to be -1"
        return


    pass # end of Instrument


def createInstrument( name, guid = -1, **attributes ):
    return Instrument( name, guid = guid, **attributes )



import unittest

from unittest import TestCase
class Instrument_TestCase(TestCase):


    def test(self):
        instrument = createInstrument('test')
        return


    def test_addElement(self):
        'instrument: addElement'
        instrument = createInstrument('test')
        self.assertEqual( instrument.guid(), -1 )
        
        from Moderator import createNormalModerator
        moderator = createNormalModerator('moderator', 10, 10, 2 )
        self.assertEqual( moderator.guid(), -1 )
        instrument.addElement( moderator )

        self.assert_( moderator.guid() >= 0 )
        return
        
    def test_getModerator(self):
        'instrument: getModerator'
        instrument = createInstrument('test')
        
        from Moderator import createNormalModerator
        moderator = createNormalModerator('moderator', 10, 10, 2 )
        instrument.addElement( moderator )

        moderator1 = instrument.getModerator()

        self.assertEqual( moderator, moderator1 )
        return

    
    def test_getSample(self):
        'instrument: getSample'
        instrument = createInstrument('test')
        from Sample import Sample
        instrument.addElement( Sample('aluminum') )
        instrument.getSample()
        return


    def test_changeSample(self):
        'instrument: changeSample'
        instrument = createInstrument('test')
        from Sample import Sample
        instrument.addElement( Sample('aluminum') )
        instrument.changeSample( Sample('vanadium') )
        return

    
    def test_getDetectorSystem(self):
        'instrument: getDetectorSystem'
        return

    
    def test_getMonitors(self):
        'instrument: getMonitors'
        instrument = createInstrument('test')
        
        from Monitor import createNormalMonitor
        monitor1 = createNormalMonitor('monitor1', 10, 10, 2 )
        instrument.addElement( monitor1 )
        
        monitor2 = createNormalMonitor('monitor2', 10, 10, 2 )
        instrument.addElement( monitor2 )

        monitors = instrument.getMonitors()

        self.assertEqual( monitors, [monitor1, monitor2] )
        return


    def test_registerAll(self):
        instrument = createInstrument( 'test' )
        from DetectorSystem import DetectorSystem
        ds = DetectorSystem( 'ds', guid  = instrument.getUniqueID() )
        from Detector import Detector
        det = Detector( 'det', guid = instrument.getUniqueID() )
        ds.addElement( det )
        instrument.addElement( ds )

        self.assertRaises(
            KeyError, 
            instrument.guidRegistry.guid2element,
            det.guid(),
            )

        instrument.guidRegistry.registerAll( instrument )
        self.assertEqual(
            instrument.guidRegistry.guid2element(det.guid()), det )
        return
        
    pass # end of Instrument_TestCase

    
def pysuite():
    suite1 = unittest.makeSuite(Instrument_TestCase)
    return unittest.TestSuite( (suite1,) )

def main():
    debug.activate()
    pytests = pysuite()
    unittest.TextTestRunner(verbosity=2).run(pytests)
    return

if __name__ == '__main__': main()


# version
__id__ = "$Id$"

# End of file
