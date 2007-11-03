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


prompt = ">>> "


import wx
import wx.py


ShellBase = wx.py.shell.Shell
class Shell(ShellBase):

    def __init__(self, *args, **kwds):
        ShellBase.__init__(self, *args, **kwds)
        return
    

    def processLine(self):
        ShellBase.processLine(self)
        self._postProcessing()
        return
    

    def _postProcessing(self):
        # this is a special instance kept in shelf
        # take a look at HistPlotPanel
        # this instance can be used to refer to a lot of plotting commands
        plotInstance = "plot" 
        
        if self.history[0].startswith( plotInstance ): self._refreshHistPlot()
        self._addHistogram()
        return


    def _refreshHistPlot(self):
        self.GetParent().GetParent().redrawHistogramPlot()
        return
    

    def _addHistogram(self):
        parent = self.GetParent()
        
        shelf = parent.getShelf()

        histShelf = parent.getHistShelf()

        from histogram.Histogram import Histogram
        newHist = None
        for key, item in shelf.iteritems():
            if isinstance(item, Histogram) and key not in histShelf.keys():
                histShelf[key] = item
                newHist = key, item
                break
            continue
        if newHist is None: return
        identifier, hist = newHist
        parent.GetParent().addHistogram( identifier, hist )
        return


    pass
        

class LowerPanel(wx.Panel):

    def __init__(self, *args, **kwds):
        wx.Panel.__init__(self, *args, **kwds)
        
        #self.SetBackgroundColour("sky blue")
        
        sizer = wx.BoxSizer()
        t = self.pythonInput = Shell(self, -1, locals = self.getShelf())
        #self.Bind(wx.EVT_TEXT, self.EvtText, t)
        #wx.EVT_KEY_UP(t,  self.EvtTextEnter)
        
        sizer.Add( self.pythonInput, 1, wx.EXPAND, 5 )

        self.SetSizer(sizer)
        self.SetAutoLayout(1)
        sizer.Fit(self)

        #import sys
        #self.saved_sysstdout = sys.stdout; self.saved_sysstderr = sys.stderr
        #sys.stderr = sys.stdout = self
        #self.write( prompt )
        return


    def write(self, text):
        self.pythonInput.AppendText( text )
        return


    def getShelf(self): return self.GetParent().getShelf()
    def getHistShelf(self): return self.GetParent().histShelf


    def EvtText(self, event):
        #print 'Pressed key'
        return
    

    def EvtTextEnter(self, event):
        print "hello"
        if wx.KeyEvent.GetKeyCode(event) != 13: return
        pythonInput = self.pythonInput
        s = pythonInput.GetValue()
        lines = s.split("\n")
        lastline = lines[-2]
        cmd = lastline.lstrip(prompt)

        shelf = self.getShelf()
        try: exec cmd in shelf
        except Exception, msg:
            import traceback
            print traceback.print_exc()
            print "Unable to execute %r because of %s: %s" % (
                cmd, msg.__class__.__name__, msg)
            pass
        self.write( prompt )

        histShelf = self.getHistShelf()

        from histogram.Histogram import Histogram
        newHist = None
        for key, item in shelf.iteritems():
            if isinstance(item, Histogram) and key not in histShelf.keys():
                histShelf[key] = item
                newHist = key, item
                break
            continue
        if newHist is None: return
        identifier, hist = newHist
        self.GetParent().addHistogram( identifier, hist )
        return


    pass # end of LowerPanel



# version
__id__ = "$Id$"

# End of file 
