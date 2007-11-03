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


from Parser import Parser
default_parser = Parser()


def parse( stream ): return default_parser.parse( stream )

def parse_file( filename ): return parse( open( filename ) )


from Renderer import Renderer
default_renderer = Renderer()
def render( instrument ):
    '''render(instrument) --> text of the xml file

  - Inputs:
    instrument: instrument hierarchy
  - return: a list of strings
  '''
    from pyre.applications.Script import Script
    class T(Script):
        class Inventory(Script.Inventory):
            import pyre.inventory
            weaver = pyre.inventory.facility(
                'weaver', default = pyre.weaver.weaver() )
            pass # end of Inventory
        def __init__(self, name = "instrument.nixml.render"):
            Script.__init__(self, name)
            return
        def main(self):
            self.weaver.renderer = default_renderer
            return 
        def _init(self):
            Script._init(self)
            self.weaver = self.inventory.weaver
            return
        pass # 
    t = T()
    t.run()
    text = t.weaver.render( instrument )
    return text


def weave( instrument, stream = None ):
    if stream is None:
        import sys
        stream = sys.stdout
        pass

    print >> stream, '\n'.join( render(instrument) )
    return


# version
__id__ = "$Id$"

# End of file

