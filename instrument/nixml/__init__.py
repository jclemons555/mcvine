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


from .Parser import Parser
default_parser = Parser()


def parse( stream ): return default_parser.parse( stream )

def parse_file( filename ): return parse( open( filename ) )


from .Renderer import Renderer
default_renderer = Renderer()
def render( instrument, renderer = None ):
    '''render(instrument) --> text of the xml file

  - Inputs:
    instrument: instrument hierarchy
  - return: a list of strings
  '''
    if  renderer is None: renderer = default_renderer

    class Options: pass
    options = Options()
    options.author = "Jiao Lin"
    options.organization = "Caltech"
    options.copyright = ""
    options.bannerWidth = 78
    options.bannerCharacter = '~'
    options.creator = ''
    options.timestamp = True
    options.lastLine = " End of file "
    options.copyrightLine = "(C) %s  All Rights Reserved"
    options.licenseText = ["{LicenseText}"]
    options.timestampLine = " Generated automatically by %s on %s"
    options.versionId = ' $' + 'Id' + '$'
    options.print_docs = True
    renderer.options = options

    text = renderer.render( instrument )
    return text


def weave( instrument, stream = None ):
    if stream is None:
        import sys
        stream = sys.stdout
        pass

    print('\n'.join( render(instrument) ), file=stream)
    return


# version
__id__ = "$Id$"

# End of file

