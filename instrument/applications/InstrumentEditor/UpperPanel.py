#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2006 All Rights Reserved 
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


import wx


from TreeNotebook import TreeNotebook
from ViewNotebook import ViewNotebook


class UpperPanel(wx.SplitterWindow):

    def __init__(self, *args, **kwds):
        wx.SplitterWindow.__init__(self, *args, **kwds)

        sty = wx.BORDER_SUNKEN
        
        p1 = TreeNotebook(self, style = sty)
        
        p2 = ViewNotebook(self, style = sty)
        
        self.SetMinimumPaneSize(250)
        self.SplitVertically(p1, p2, 250)

        self.treeNotebook = p1; self.viewNotebook = p2
        return


    def getShelf(self): return self.GetParent().getShelf()


    pass # end of UpperPanel



# version
__id__ = "$Id$"

# End of file 
