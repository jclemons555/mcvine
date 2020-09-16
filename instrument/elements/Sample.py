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


from .Element import Element, debug


class Sample( Element ):

    class Attributes(Element.Attributes):

        from . import Attribute

        pass
        

    def __init__( self, name, shape = None, **attributes):
        """ Sample ctor
"""
        Element.__init__(
            self, name, shape = shape, **attributes)
        return


    def identify( self, visitor):
        return visitor.onSample( self)

    pass # end of Guide



# version
__id__ = "$Id: Moderator.py 487 2005-06-22 22:52:09Z tim $"

# End of file
