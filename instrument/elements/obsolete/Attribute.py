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


class Attribute(object):

    def __init__(self, name, doc = '', default = None):
        self.name = name
        self.doc = doc
        self.val = default
        return
    

    def __get__(self, obj, type=None):
        if obj is None: return type.__dict__[ self.name ]
        return obj.__dict__.get(self.name)


    def __set__(self, obj, value):
        obj.__dict__[self.name] = value
        return value


    def __delete__(self, obj):
        del obj.__dict__[self.name]

    pass


# version
__id__ = "$Id$"

# Generated automatically by PythonMill on Tue Sep 18 20:23:44 2007

# End of file 
