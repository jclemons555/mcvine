#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                      (C) 2005-2010 All Rights Reserved  
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from instrument.factories.ARCSBootstrap_fromnxs import InstrumentFactory, units


from pyre.applications.Script import Script


class MakeARCSxml(Script):

    class Inventory(Script.Inventory):

        import pyre.inventory as pinv

        nxfile = pinv.str('nxfile', default = '')
        nxfile.meta['tip'] = 'nexus file name. eg. ARCS_5610.nxs'

        nxentry = pinv.str('nxentry', default = '/entry')
        nxentry.meta['tip'] = 'the entry in the nexus file'

        mod2sample = pinv.dimensional('mod2sample', default = 13.6*units.length.meter)
        mod2sample.meta['tip'] = 'distance from moderator to sample'

        xmloutput = pinv.str(name='xmloutput')
        xmloutput.meta['tip'] = 'The output xml file'
        
        pass  # end of Inventory


    def __init__(self, name = 'makeARCSxml_fromnxs'):
        Script.__init__(self, name )
        return


    def main(self):
        if not self.inventory.xmloutput:
            raise RuntimeError('Please specify output xml filename by -xmloutput')
        
        filename = self.inventory.nxfile
        entry = self.inventory.nxentry
        mod2sample = self.inventory.mod2sample
        xmloutput = self.inventory.xmloutput
        
        factory = InstrumentFactory()
        instrument, geometer = factory.construct(
            filename, nxentry=entry, mod2sample=mod2sample, xmloutput=xmloutput )

        params = {
            'nxfile': filename,
            'nxentry': entry,
            'mod2sample': mod2sample,
            }
        cmd = 'makeARCSxml.py ' + ' '.join(
            [ '-%s="%s"' % (k,v) for k,v in params.items()] )
        open(xmloutput, 'a').write('<!-- created by %s -->\n' % cmd)
        return


    pass # end of MakeARCSxml


def main():
    app = MakeARCSxml()
    app.run()
    return

if __name__ == '__main__': main()

# version
__id__ = "$Id$"

# End of file 
