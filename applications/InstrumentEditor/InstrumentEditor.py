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


def main():
    import journal
    journal.debug("instrument.visitors.Instrument2VisualElements")
    
    from instrument.applications.InstrumentEditor.MainWinApp import MainWinApp
    mainWin = MainWinApp()
    mainWin.MainLoop()
    return


if __name__ == "__main__": main()


# version
__id__ = "$Id$"

# End of file 
