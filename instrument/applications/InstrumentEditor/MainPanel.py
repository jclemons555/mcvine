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

from .LowerPanel import LowerPanel
from .UpperPanel import UpperPanel



class MainPanel(wx.SplitterWindow):


    def __init__(self, parent):
        wx.SplitterWindow.__init__(self, parent, -1, style = wx.SP_LIVE_UPDATE)
        self.Bind(wx.EVT_SPLITTER_SASH_POS_CHANGED, self.OnSashChanged)
        self.Bind(wx.EVT_SPLITTER_SASH_POS_CHANGING, self.OnSashChanging)


        sty = wx.BORDER_SUNKEN
        
        self.upper = p1 = UpperPanel(self, style=sty)
        
        self.lower = p2 = LowerPanel(self, style=sty)
        
        self.SetMinimumPaneSize(20)
        self.SplitHorizontally(p1, p2, -200)

        self.addPanelsToShelf()
        return


    def addPanelsToShelf(self):
        mainPanel = self
        upperPanel = mainPanel.upper
        lowerPanel = mainPanel.lower
        treeNotebook = upperPanel.treeNotebook
        viewNotebook = upperPanel.viewNotebook
        treePanel = treeNotebook.treePanel
        shapeTreePanel = treeNotebook.shapeTreePanel
        d = {"mainPanel": mainPanel,
             "upperPanel": upperPanel,
             "lowerPanel": lowerPanel,
             "treeNotebook": treeNotebook,
             "viewNotebook": viewNotebook,
             "treePanel": treePanel,
             "shapeTreePanel": shapeTreePanel,
             } 
        self.getShelf().update(d)
        return


    def getShelf(self): return self.GetParent().getShelf()


    def getCurrentContainer(self):
        return self.getShelf()["treePanel"].getCurrentContainer()

    
    def getCurrentItem(self):
        return self.getShelf()["treePanel"].getCurrentItem()


    def OnSashChanged(self, evt):
        #print "sash changed to %s\n" % str(evt.GetSashPosition())
        return
        

    def OnSashChanging(self, evt):
        #print "sash changing to %s\n" % str(evt.GetSashPosition())
        # uncomment this to not allow the change
        #evt.SetSashPosition(-1)
        return
    
                                            
    pass # end of MainPanel



# version
__id__ = "$Id$"

# End of file 
