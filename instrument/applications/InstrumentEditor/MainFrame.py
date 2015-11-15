#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                       (C) 2005 All Rights Reserved  
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


import wx



ID_ABOUT=201
ID_HELPONLINETUTORIAL=902
ID_FILEOPENINSTRUMENT=102
ID_FILESAVEINSTRUMENT=103
ID_EXIT=199
ID_EDITADDITEM=201
ID_EDITITEMSHAPE=202


about_msg = """
Instrument editor is a GUI application for editing
neutron instruments.

   DANSE team INS subgroup
   California Institute of Technology
   (C) 2006 All Rights Reserved
"""


tutorial_url = "http://wiki.cacr.caltech.edu/danse/index.php/InstrumentEditor-tutorial"



class MainFrame(wx.Frame):
    
    def __init__(self, parent=None, id=-1, name = "Instrument Editor", pos = wx.DefaultPosition):
        wx.Frame.__init__(self, parent,id,name, pos, (960,720))
        self.createShelf()
        self.createInstrument()
        self.drawscreen()
        return


    def drawscreen(self):
        self.CreateStatusBar() # A Statusbar in the bottom of the window
        self.createMenu()
        self.createPanel()
        self.Show(True)
        return
    

    def createMenu(self):
        # Setting up the menu.
        filemenu= wx.Menu()
        filemenu.Append(ID_FILEOPENINSTRUMENT, "&Open instrument", " Open an existing instrument") 
        filemenu.Append(ID_FILESAVEINSTRUMENT, "&Save instrument", " Save current instrument to a file")
        filemenu.AppendSeparator()
        filemenu.Append(ID_EXIT,"E&xit"," Terminate the program")

        editmenu = wx.Menu()
        editmenu.Append( ID_EDITADDITEM, "&Add item", " Add an item" )
        editmenu.Append( ID_EDITITEMSHAPE, "Item &shape", " Edit the shape of an item" )

        helpmenu = wx.Menu()
        helpmenu.Append(ID_HELPONLINETUTORIAL, "&Online Tutorial",
                        " Open online tutorial")
        helpmenu.Append(ID_ABOUT, "&About"," Information about this program")
        
        # Creating the menubar.
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu,"&File") # Adding the "filemenu" to the MenuBar
        menuBar.Append(editmenu,"&Edit") # Adding the "editmenu" to the MenuBar
        menuBar.Append(helpmenu,"&Help") # Adding the "helpmenu" to the MenuBar
        
        self.SetMenuBar(menuBar)  # Adding the MenuBar to the Frame content.

        #event handler connections
        wx.EVT_MENU(self, ID_FILEOPENINSTRUMENT, self.OnFileOpenInstrument)
        wx.EVT_MENU(self, ID_FILESAVEINSTRUMENT, self.OnFileSaveInstrument)
        wx.EVT_MENU(self, ID_ABOUT, self.OnAbout) # 
        wx.EVT_MENU(self, ID_HELPONLINETUTORIAL, self.OnOnlineTutorial) # 
        wx.EVT_MENU(self, ID_EXIT, self.OnExit)   #
        wx.EVT_MENU(self, ID_EDITADDITEM, self.OnAddItem)
        wx.EVT_MENU(self, ID_EDITITEMSHAPE, self.OnEditItemShape)
        return


    def createShelf(self):
        self.shelf = {}
        return


    def getShelf(self): return self.shelf


    def createInstrument(self):
        from instrument.elements import createInstrument
        instrument = createInstrument( "instrument" )
        self.shelf['instrument'] = instrument
        
        from instrument.geometers.Geometer import Geometer
        instrument_geometer = Geometer( instrument )
        from instrument.geometers.InstrumentGeometer import InstrumentGeometer
        local_geometers = [instrument_geometer]
        global_instrument_geometer = InstrumentGeometer( instrument, local_geometers )
        self.shelf['geometer'] = global_instrument_geometer
        
        self.createInstrumentElementContainerChildrenTable()
        return


    def createInstrumentElementContainerChildrenTable(self):
        import instrument.elements as ie
        from instrument.elements.Element import Element
        from instrument.elements.ElementContainer import ElementContainer
        def isElementClass(klass): return issubclass( klass, Element )
        def isElementContainerClass(klass): return issubclass( klass, ElementContainer )
        import ChildrenTable
        self.shelf['children-table-for-instrument-element-containers']  = ChildrenTable.createByLookupElementModules( ie, isElementClass, isElementContainerClass )
        return


    def createPanel(self):
        from MainPanel import MainPanel
        self.panel = MainPanel( self )
        return


    def getCurrentContainer(self):
        return self.panel.getCurrentContainer()


    def getCurrentItem(self):
        return self.panel.getCurrentItem()


    # event handlers

    def OnEditItemShape(self,evt):
        itemPath, item = self.getCurrentItem()
        shape = item.shape()
        shapeTreePanel = self.shelf['shapeTreePanel']
        shapeTreePanel.changeTargetTree( shape )
        treeNotebook = self.shelf['treeNotebook']
        treeNotebook.changePage( "shape" )
        return
    

    def OnAddItem(self, evt):
        from AddItemDialog import AddItemDialog
        containerPath, container = self.getCurrentContainer()
        itemPath, item = self.getCurrentItem()
        children_table = self.shelf['children-table-for-instrument-element-containers']
        allowed_children_types = children_table[ container.__class__ ]
        dlg = AddItemDialog(
            parent = self,
            container = container,
            item = item,
            allowed_children_types = allowed_children_types)

        result = dlg.ShowModal()
        if result != wx.ID_OK : return
        klass, name = dlg.getSelection()
        dlg.Destroy()
        new = klass(name)
        container.addChild( name, new )
        treePanel = self.shelf['treePanel']
        treePanel.addElementToTree( containerPath, name )
        vtkPanel = self.shelf['vtkPanel']
        instrument = self.shelf['instrument']
        geometer = self.shelf['geometer']
        geometer.register( str('/'.join( [containerPath, name] ) ),
                           (0,0,0), (0,0,0), containerPath )
        vtkPanel.render( instrument, geometer )
        print "hello there"
        #???
        return 


    def OnFileOpenInstrument(self, evt):
        d = wx.FileDialog( self, "load instrument" )
        if d.ShowModal() != wx.ID_OK: d.Destroy(); return
        filename = d.GetPath()
        d.Destroy()
        import pickle
        loaded = pickle.load( open( filename ) )
        #????
        #self.panel.addHistogram( hist.name(), hist )
        return

    
    def OnFileSaveInstrument(self, e):
        #????
        return


    def OnOnlineTutorial(self, e):
        import webbrowser
        webbrowser.open( tutorial_url )
        return

    
    def OnAbout(self,e):
        d= wx.MessageDialog( self, about_msg, "Instrument Editor", wx.OK)
        # Create a message dialog box
        d.ShowModal() # Shows it
        d.Destroy() # finally destroy it when finished.
        return


    def OnExit(self,e):
        self.Close(True)  # Close the frame.return
        return

    pass # end of MainFrame


# version
__id__ = "$Id$"

# End of file 
