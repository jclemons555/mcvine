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


# Every directory containing neutron data files must have a
# text file stating the number of neutrons in each neutron data
# file.
packetsizefile = 'packetsize'


from mcni.neutron_storage import ndblsperneutron

from mcni.pyre_support.AbstractComponent import AbstractComponent

class NeutronToStorage( AbstractComponent ):


    class Inventory( AbstractComponent.Inventory ):
        import pyre.inventory as pinv
        path = pinv.str( 'path', default = '' )
        append = pinv.bool( 'append', default = False )
        pass
    

    def process(self, neutrons):
        return self.engine.process( neutrons )
    
    
    def _configure(self):
        AbstractComponent._configure(self)
        self.path = self.inventory.path
        self.append = self.inventory.append
        return


    def _init(self):
        AbstractComponent._init(self)
        from mcni.components.NeutronToStorage import NeutronToStorage
        self.engine = NeutronToStorage( self.name, self.path, self.append )
        return

    pass # end of Source


def filesize( n ):
    '''calculate neutron file size given number of neutrons
    '''
    return titlesize + versionsize + commentsize + nsize + n * neutronsize


import os, math, numpy


# version
__id__ = "$Id$"

# End of file 
