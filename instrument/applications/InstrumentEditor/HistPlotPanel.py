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
debug = journal.debug("HistPlotPanel")
warning = journal.warning("HistPlotPanel")


import wx


class Plot(object):

    def __init__(self, plotPanel):
        self.plotPanel = plotPanel
        self.figure = plotPanel.figure
        return


    def replot(self, *args, **kwds):
        self.plotPanel.plotter.plot( *args, **kwds )
        return


    def __getattribute__(self, name):
        if name in [ 
            'figure', 'plotPanel', 'replot',
            ]: return object.__getattribute__(self, name)
        try:
            return getattr(self.plotPanel, name)
        except:
            try:
                return getattr(self.figure, name )
            except:
                return getattr(self.figure.gca(), name)
            raise
        raise

    pass

    

from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg, Toolbar, FigureManager
from matplotlib.figure import Figure

class HistPlotPanel(wx.Panel):

    def __init__(self, parent, id, size=(4,3), dpi=75, **kwds ):
        wx.Panel.__init__(self, parent, id)

        import wxmpl.wxmpl as wxmpl
        self.canvas = wxmpl.PlotPanel(self, -1, size = size, dpi = dpi)
        self.figure = self.canvas.figure
        self.figure.add_subplot(111)
        
        self.toolbar = Toolbar(self.canvas)
        self.toolbar.Realize()

        # On Windows, default frame size behaviour is incorrect
        # you don't need this under Linux
        tw, th = self.toolbar.GetSizeTuple()
        fw, fh = self.canvas.GetSizeTuple()
        self.toolbar.SetSize(wx.Size(fw, th))

        # Create a figure manager to manage things
        self.figmgr = FigureManager(self.canvas, 1, self)
        # Now put all into a sizer
        sizer = wx.BoxSizer(wx.VERTICAL)
        # This way of adding to sizer allows resizing
        sizer.Add(self.canvas, 1, wx.LEFT|wx.TOP|wx.GROW)

        # add a spacer between figure and toolbar
        sizer.AddSpacer( (10,10) )
        
        # Best to allow the toolbar to resize!
        sizer.Add(self.toolbar, 0, wx.GROW)
        self.SetSizer(sizer)
        self.sizer = sizer
        self.SetAutoLayout(1)
        sizer.Fit(self)
        
        #FigureCanvasWxAgg.__init__(self, parent, id, Figure(size, dpi) )
        from histogram.plotter import HistogramMplPlotter as HMP
        self.plotter = HMP( self.figure )
        shelf = self.getShelf()
        shelf.update( {"plot": Plot(self)} )
        return


    def GetToolBar(self):
        return self.toolbar


    def getShelf(self): return self.GetParent().getShelf()


    def showHist(self, histIdentifier):
        hist = self.getShelf().get(histIdentifier)
        if hist is None: print("Unable to retrieve histogram %s" % histIdentifier); return
        self.currentHist = hist
        self.showCurrentHist()
        return
    

    def showCurrentHist(self):
        hist = self.currentHist
        self.plotter.plot( hist )
        self.Refresh()
        return


    pass # end of HistPlotPanel



def test():
    class MainFrame(wx.Frame):
        
        def __init__(self, parent=None, id=-1, name = "hello", pos = wx.DefaultPosition):
            wx.Frame.__init__(self, parent,id,name, pos, (640,480))
            self.panel = HistPlotPanel(self, -1)
            sizer = wx.BoxSizer(wx.VERTICAL)
            sizer.Add(self.panel, 1, wx.ALL|wx.EXPAND, 5)
            self.SetSizer(sizer)
            self.Fit()
            return

        pass # end of MainFrame

    WxPyAppBase = wx.PySimpleApp
    
    class MainWinApp(WxPyAppBase):
        
        def __init__(self,   *args, **kwargs):
            import os
            WxPyAppBase.__init__(self, *args, **kwargs)
            return
        

        def OnInit(self):
            self.frame = MainFrame(None, -1)
            self.SetTopWindow(self.frame)
            self.frame.Show(True)
            return True

        pass

    mainWin = MainWinApp()
    plotPanel = mainWin.frame.panel
    figure = plotPanel.get_figure()
    axes = figure.gca()
    axes.plot([1,2,3],[1,2,3])
    plotPanel.draw()
    mainWin.MainLoop()

    return


if __name__  == "__main__": test()
    

# version
__id__ = "$Id$"

# End of file 
