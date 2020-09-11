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
debug = journal.debug("ViewNotebook")
warning = journal.warning("ViewNotebook")


import wx

class ViewNotebook(wx.Notebook):

    def __init__(self, *args, **kwds):
        wx.Notebook.__init__(self, *args, **kwds)
        self._addStartingPages()
        return


    def getShelf(self): return self.GetParent().getShelf()


    def update(self):
        #???
        return
    
    
    def _addStartingPages(self):
        from .VtkPanel import VtkPanel
        self.getShelf()['vtkPanel'] = self.vtkPanel = VtkPanel( self, -1 )
        self.AddPage( self.vtkPanel, "vtk windodw" )
        #from HistInfoPanel import HistInfoPanel
        #self.histInfoPanel = HistInfoPanel(self)
        #self.AddPage( self.histInfoPanel, "histogram info" )
        return


    pass #end of ViewNotebook



# version
__id__ = "$Id$"

# End of file 
