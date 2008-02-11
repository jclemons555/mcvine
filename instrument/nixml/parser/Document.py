#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                 Jiao Lin   
#                      California Institute of Technology
#                      (C)   2007    All Rights Reserved
#
# <LicenseText>
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from instrument.geometry.pml.parser.Document import Document as base


class Document(base):


    tags = [
        "Instrument",
        'Copy',
        'Moderator', 'Monitor', 'Guide',
        'Sample',
        'DetectorSystem', 'DetectorArray', 'DetectorPack',
        'Detector',
        'Pixel',

        'LocalGeometer',
        'Register',
        'InstrumentGeometer',

        'Shape',
        ]


    def onInstrument(self, instrument):
        self.document = instrument
        return


# version
__id__ = "$Id: Document.py,v 1.1.1.1 2005/03/08 16:13:43 linjiao Exp $"

# End of file 
