#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                       (C) 2006 All Rights Reserved  
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


import wx


from .MainFrame import MainFrame


WxPyAppBase = wx.PySimpleApp
#WxPyAppBase = wx.PyApp


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


# version
__id__ = "$Id$"

# End of file 
