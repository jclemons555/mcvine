#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2005 All Rights Reserved 
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#



from .Visitor import Visitor


class DetectorVisitor(Visitor):

    def render(self, instrument, geometer):
        self._IDs = []
        Visitor.render(self, instrument, geometer)
        del self._IDs
        return


    def elementSignature(self):
        '''return a tuple of IDs pointing to the current element.
        It is the signature of the current element that is being visited.
        In each layer of the instrument hierarchy, the "ID" is unique
        for each subelements.
        Signature (3, 5, 2) means, for example, element #3 (the detector system)
        has a subelement, a detector pack with ID=5. The pack #5 has
        a subelement, a detector tube with ID=2. The signature (3,5,2)
        refers to that particular tube.
        '''
        return tuple( self._IDs )


    def detectorElementSignature(self):
        '''return a tuple of IDs inside the detector system, pointing to the current
        detector element.

        This is almost the same as the method "elementSignature".
        The only difference is this signature is only unique inside the
        detectorSystem.
        '''
        return self.elementSignature()[1:] # remove the ID for detSystem


    def onCopy(self, copy):
        return copy.identifyAsReferredElement(self)


    def onElementContainer(self, container):
        for element in container.elements():
            self._IDs.append( element.id() )
            element.identify(self)
            self._IDs.pop()
            continue
        return


    onInstrument = onDetectorSystem = onDetectorArray \
                   = onDetectorPack = onElementContainer


    #we are only concerned with detectors, so all other elements are ignored
    def doNothing(self, element): return

    onModerator = onMonitor = onGuide = onSample = doNothing


    def onDetector(self, detector): raise NotImplementedError("%s should handle 'onDetector'" % self.__class__.__name__)


    pass # end of DetectorVisitor



class DetectorSubsystemVisitor(DetectorVisitor):

    '''This visitor only visits a portion of the detector system

    The detector subsystem to be visited is specified by its "path".
    '''
    
    def render(self, instrument, geometer, detectorSubSystemPath):
        detSys = instrument.getDetectorSystem()
        path = '%s/%s' % (detSys.name, detectorSubSystemPath)
        self._IDs = list( instrument._indexTupleFromPath( path ) )
        subSystem = instrument._getDescendent( path )
        Visitor.render(self, subSystem, geometer)
        del self._IDs
        return

    pass # end of DetectorSubsystemVisitor



# a trivial detector visitor
class DetectorCounter(DetectorVisitor):

    def render(self, instrument):
        geometer = None
        self._result = 0
        DetectorVisitor.render(self, instrument, geometer)
        ret = self._result
        del self._result
        return ret
    

    def onDetector(self, detector):
        self._result += 1
        return

    pass



# version
__id__ = "$Id: LoopUtils.py 1414 2007-09-26 22:35:04Z linjiao $"

# End of file 
