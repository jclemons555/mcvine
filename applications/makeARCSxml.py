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
            'long', default = '10*atm, 128, 0.5*inch, 38.06*inch, 0.08*inch' )
        long.meta['tip'] = 'info about long detector pack: pressure, npixels, radius, length, gap'
        
        short1 = pinv.str(
            'short1', default = '10*atm, 128, 0.5*inch, 10.92*inch, 0.08*inch' )
        short1.meta['tip'] = 'info about short detector type 1 (pack 71, shorter): pressure, npixels, radius, length, gap'

        short2 = pinv.str(
            'short2', default = '10*atm, 128, 0.5*inch, 14.86*inch, 0.08*inch' )
        short2.meta['tip'] = 'info about short detector type 2 (pack 70, longer): pressure, npixels, radius, length, gap'

        xmloutput = pinv.str(name='xmloutput')
        
        pass  # end of Inventory


    def __init__(self, name = 'makeARCSxml'):
        Script.__init__(self, name )
        return


    def main(self):
        if not self.inventory.xmloutput:
            raise RuntimeError('Please specify output xml filename by -xmloutput')
        filename = self.inventory.detconfigfile
        long = self._parse( self.inventory.long )
        short1 = self._parse( self.inventory.short1 )
        short2 = self._parse( self.inventory.short2 )
        xmloutput = self.inventory.xmloutput
        
        from instrument.factories.ARCSBootstrap import InstrumentFactory as Factory
        factory = Factory()
        instrument, geometer = factory.construct(
            filename, long, short1, short2, xmloutput=xmloutput )

        params = {
            'detconfigfile': filename,
            'long': self.inventory.long,
            'short1': self.inventory.short1,
            'short2': self.inventory.short2,
            }
        cmd = 'makeARCSxml.py ' + ' '.join(
            [ '-%s="%s"' % (k,v) for k,v in params.items()] )
        open(xmloutput, 'a').write('<!-- created by %s -->\n' % cmd)
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
