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


import journal
debug = journal.debug("TreeNotebook")
warning = journal.warning("TreeNotebook")


import wx

class TreeNotebook(wx.Notebook):

    def __init__(self, *args, **kwds):
        wx.Notebook.__init__(self, *args, **kwds)
        self._pageName2No = {}
        self._pageCounter = 0
        self._addStartingPages()
        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnPageChanged)
        return


    def getShelf(self):
        return self.GetParent().getShelf()


    def update(self):
        #???
        return


    def changePage(self, pageName):
        no = self._pageName2No[ pageName ]
        self.SetSelection( no )
        return


    #event handlers
    def OnPageChanged(self, evt):
        no = evt.GetSelection()
        print "current page no: %s" % no
        if no == self._pageName2No[ "shape" ]:
            path, item = self.treePanel.getCurrentItem()
            self.shapeTreePanel.changeTargetTree( item.shape() )
            pass
        evt.Skip()
        return
        

    def _addStartingPages(self):
        self._addInstrumentTree()
        self._addShapeTree()
        return


    def _addPage(self, name, page):
        self.AddPage( page, name )
        self._pageName2No[ name ] = self._pageCounter
        self._pageCounter += 1
        return


    def _addInstrumentTree(self):
        name = "Instrument tree"
        from TreePanel import TreePanel
        self.treePanel = TreePanel(self, targetTree = self.getShelf()["instrument"] )
        self._addPage( name, self.treePanel )
        return


    def _addShapeTree(self):
        name = "shape"
        from ShapeTreePanel import ShapeTreePanel
        #self.shapeTreePanel = ShapeTreePanel(self, targetName = "shape", targetTree = testshape())
        self.shapeTreePanel = ShapeTreePanel(self, targetName = "shape", targetTree = None)
        self._addPage( name, self.shapeTreePanel )
        return


    pass #end of TreeNotebook



def testshape():
    from geometry.shapes import *
    from geometry.operations import *
        
    block1 = block( (1,1,1) )
    block2 = block( (2,2,2) )
    u = unite( block1, block2 )
    return u
    
##     b1 = translate( self.block1, (0,0,0.75) )
##     u = unite( b1, self.block2 )
    
##     b1 = translate( self.block1, (0,0,0.75) )
##     u = subtract( self.block2, b1 )
    
##     b1 = translate( self.block1, (0,0,0.75) )
##     u = intersect( self.block2, b1 )
    
##     b1 = translate( self.block1, (0.5,0.5,0.5) )
##     u = rotate( b1, (0,0,1), 90. )


# version
__id__ = "$Id$"

# End of file 
