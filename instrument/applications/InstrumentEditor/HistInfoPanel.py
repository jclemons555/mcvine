#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#              (C) 2005 All Rights Reserved  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


import journal
debug = journal.debug("HistInfoPanel")
warning = journal.warning("HistInfoPanel")


import wx

class HistInfoPanel(wx.Panel):

    def __init__(self, *args, **kwds):
        wx.Panel.__init__(self, *args, **kwds)

        sizer = wx.BoxSizer( wx.VERTICAL )

        histInfoTextsSizer = wx.BoxSizer( wx.VERTICAL )

        self.titleText = wx.StaticText( self, -1, "Histogram title" )
        self.titleText.SetFont( wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD ) )

        self.axesText = wx.StaticText( self, -1, " - Axes:" )

        self.shapeText = wx.StaticText( self, -1, " - Shape:  ")

        self.metadataText = wx.StaticText( self, -1, " - Metadata: ")

        histInfoTextsSizer.Add( self.titleText, 0, wx.GROW|wx.ALL, 10 )
        histInfoTextsSizer.Add( self.axesText, 0, wx.GROW|wx.ALL, 10 )
        histInfoTextsSizer.Add( self.shapeText, 0, wx.GROW|wx.ALL, 10 )
        histInfoTextsSizer.Add( self.metadataText, 0, wx.GROW|wx.ALL, 10 )

        sizer.Add( histInfoTextsSizer, 0, wx.ALL, 20 )

        self.sizer = sizer
        self.SetSizer(sizer)
        self.SetAutoLayout(1)
        sizer.Fit(self)

        self.currentHist = None
        return


    def getShelf(self): return self.GetParent().getShelf()


    def showHist(self, histIdentifier):
        hist = self.getShelf().get(histIdentifier)
        if hist is None: print("Unable to retrieve histogram %s" % histIdentifier); return
        title = "Histogram \"%s\"" %   hist.name()

        axes = "- Axes:\n"
        for axisName in hist.axisNameList():
            axis = hist.axisFromName(axisName)
            axes += "   - Axis %s: %s\n" % (
                axisName, _str(axis.binCenters() ) )
            continue

        shape = "- Shape: %s" % hist.shape()

        attrs = [ (name, hist.getAttribute(name)) for name in \
                  hist.listAttributes() ]
        meta = "- Metadata: %s" % (attrs,)
        
        self.titleText.SetLabel( title )
        self.axesText.SetLabel( axes )
        self.shapeText.SetLabel( shape )
        self.metadataText.SetLabel( meta )

        self.sizer.Fit(self)
        
        self.currentHist = hist
        return


    pass #end of HistInfoPanel



def _str(l):
    if len(l) <  10: return str(l)
    else: return "[ %s, %s, ... %s, %s ]"%(l[0],l[1], l[-2], l[-1])



from histogram.plotter import plot1d, plot2d


# version
__id__ = "$Id$"

# End of file 
