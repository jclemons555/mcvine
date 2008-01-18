#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                         (C) 2005 All Rights Reserved  
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

from pyre.applications.Script import Script


class MakeARCSxml(Script):

    class Inventory(Script.Inventory):

        import pyre.inventory as pinv

        detconfigfile = pinv.str(
            'detconfigfile', default = "ARCS-detector-configuration.txt ")

        long = pinv.str(
            'long', default = '10*atm, 128, 0.5*inch, 1.*meter, 0.08*inch' )
        long.meta['tip'] = 'info about long detector pack: pressure, npixels, radius, length, gap'
        
        short = pinv.str(
            'short', default = '10*atm, 32, 0.5*inch, 0.25*meter, 0.08*inch' )
        short.meta['tip'] = 'info about short detector: pressure, npixels, radius, length, gap'
        
        pass  # end of Inventory


    def __init__(self, name = 'makeARCSxml'):
        Script.__init__(self, name )
        return


    def main(self):
        filename = self.inventory.detconfigfile
        long = self._parse( self.inventory.long )
        short = self._parse( self.inventory.short )
        
        from instrument.factories.ARCSBootstrap import InstrumentFactory as Factory
        factory = Factory()
        instrument, geometer = factory.construct(
            filename, long, short )

        import os
        xmlfn = '%s.xml' % filename
        os.rename( xmlfn, 'ARCS.xml' )
        print "%s renamed ARCS.xml" % xmlfn
        return


    from pyre.units import parser
    _parser = parser()
    del parser

    def _parse(self, s): return self._parser.parse( s )

    pass # end of MakeARCSxml


def main():
    app = MakeARCSxml()
    app.run()
    return

if __name__ == '__main__': main()

# version
__id__ = "$Id$"

# End of file 
