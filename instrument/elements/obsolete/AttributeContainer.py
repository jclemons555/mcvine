#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2007  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


#implementation similar to pyre.inventory.Notary

class AttributeNotary(type):
    
    def __init__(klass, name, bases, dict):
        type.__init__(name, bases, dict)

        attributes = []
        
        bases = list(bases)
        bases.reverse()
        for base in bases:
            try:
                attributes += base._attributes
            except AttributeError:
                pass

            continue
        
        attributes += collectAttributes( klass )
        klass._attributes = attributes
        
        return

    pass #end of AttributeNotary


#helper for Notary
def collectAttributes( klass ):
    from Attribute import Attribute
    ret = []
    for key,value in klass.__dict__.items():
        if not isinstance( value, Attribute ):continue
        ret.append( key )
        continue
    return ret



from AbstractAttributeContainer import AbstractAttributeContainer
from future.utils import with_metaclass

class AttributeContainer(with_metaclass(AttributeNotary, AbstractAttributeContainer)):

    from Attribute import Attribute
    name = Attribute( 'name' )
    

    def set(self, name, value):
        exec("self.%s = value" % name)
        return


    def get(self, name):
        exec("value = self.%s" % name)
        return value


    def __iter__(self):
        attributes = list(self.__dict__.keys())
        return attributes.__iter__()


    def copy(self):
        ret = self.__class__( self.name )
        for k in self: ret.set( k, self.get( k ) )
        return ret
    

    def __setattr__(self, name, value):
        if name not in self._attributes :
            raise AttributeError("Unknown attribute %s" % name)
        return object.__setattr__(self, name, value)

        pass


def test():

    from AbstractAttributeContainer import TestCase as TC

    class TestCase(TC):

        def setUp(self):
            class AC(AttributeContainer):
                from Attribute import Attribute
                hello = Attribute( 'hello' )
                pass

            self.attributeContainer = AC( 'test' )
            return

        pass

    import unittest as ut
    suite = ut.makeSuite( TestCase )
    alltests = ut.TestSuite( (suite, ) )
    ut.TextTestRunner(verbosity=2).run(alltests)
    return


if __name__ == "__main__": test()


# version
__id__ = "$Id$"

# End of file 

