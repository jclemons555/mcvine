
import wx


class AddItemDialog(wx.Dialog):


    def __init__(self, parent = None,
                 size = wx.DefaultSize, pos = wx.DefaultPosition,
                 style = wx.DEFAULT_DIALOG_STYLE,
                 container = None, item = None,
                 allowed_children_types = None,
                 ):

        self.parent = parent
        self.targetContainer = container
        self.currentItem = item
        self.allowed_children_types = allowed_children_types

        #build a table so we can look up class from name
        typeTable = {}
        for t in allowed_children_types: typeTable[t.__name__] = t
        self.typeTable = typeTable

        container_name = container.name
        
        apptitle = "Add item to %r" % container_name

        pre = wx.PreDialog()
        pre.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
        pre.Create(parent, -1, apptitle, pos, size, style)
        self.PostCreate(pre)

        # dialog created. get the main view
        sizer = wx.BoxSizer( wx.VERTICAL )

        # input panel
        sizer.Add( self._getInputPanel( allowed_children_types ) )

        sizer.AddSpacer( (20,20 ) )
        
        # add ok and cancel buttons to sizer
        sizer.Add( self._getButtons() )

        # now paint the screen
        border = wx.BoxSizer()
        border.Add(sizer, 1, wx.GROW|wx.ALL, 25)
        border.Fit(self)
        self.SetSizer(border)
        self.Layout()

        #print "%s.__init__ done" % self.__class__.__name__
        return


    def getSelection(self):
        tname = self.element_type_selector.GetValue()
        t = self.typeTable[ tname ]
        name = str(self.element_name_inputbox.GetValue())
        return t,  name


    #event handlers
    def OnComboBox(self, evt):
        type = evt.GetString()
        self.element_name_inputbox.SetValue( type.lower() )
        return 


    def _getButtons(self):
        sizer = wx.BoxSizer( wx.HORIZONTAL )
        ok = wx.Button(self, wx.ID_OK, "OK")
        cancel = wx.Button(self, wx.ID_CANCEL, "Cancel")
        helpbutton = wx.Button(self, -1, "Help")

        docstr = "help..."
        self.Bind(wx.EVT_BUTTON, self.OnHelpButton(docstr), helpbutton)

        okcancelSizer = wx.BoxSizer(wx.HORIZONTAL)
        okcancelSizer.Add(ok)
        okcancelSizer.AddSpacer( (7,7) )
        okcancelSizer.Add(cancel)
        sizer.Add(okcancelSizer)
        sizer.AddSpacer( (20,1) )
        sizer.Add(helpbutton)
        return sizer


    def _getInputPanel(self, allowed_types):
        sizer = wx.GridBagSizer(vgap = 10, hgap = 5)
        typeText = wx.StaticText(self, -1, "Type")
        typeSelector = self._getElementTypeSelector( allowed_types )
        sizer.Add( typeText, pos = (0,0) )
        sizer.Add( typeSelector, pos = (0,1) )
        
        nameText = wx.StaticText(self, -1, "Name")
        defaultName = typeSelector.GetValue().lower()
        nameSelector = self._getElementNameInputBox( defaultName )
        sizer.Add( nameText, pos = (1,0) )
        sizer.Add( nameSelector, pos = (1,1) )
        return sizer
        

    def _getElementTypeSelector( self, allowed_children_types ):
        types = [t.__name__ for t in allowed_children_types]
        default_choice = types[0]
        cb = wx.ComboBox(
            self, -1, default_choice, (90, 50), 
            (140, -1), types, wx.CB_DROPDOWN #|wxTE_PROCESS_ENTER
            )
        self.element_type_selector = cb
        self.Bind(wx.EVT_COMBOBOX, self.OnComboBox, cb)
        return cb


    def _getElementNameInputBox( self, defaultName ):
        t = self.element_name_inputbox =  wx.TextCtrl(
            self, -1, defaultName, (90, 50), (200,-1))
        return t


    def _getElementConfiguration(self, element):
        
        sizer = wx.GridBagSizer(vgap = 10, hgap = 5)

        row = 1
        for attribute_name in element:
            l = self.labelFactory( trait ); sizer.Add( l, pos=(row,0), flag = wx.ALIGN_RIGHT)
            t = self.inputBoxFactory( trait ); sizer.Add( t, pos=(row, 1))
            b = self.setButtonFactory( trait )
            if b: sizer.Add(b, pos = (row, 2) )

            row = row+1
            continue

        return sizer


    def OnHelpButton(self, docstr, title="Pyre Docstring"):
        def _(event): 
            dlg = wx.lib.dialogs.ScrolledMessageDialog(self, docstr, title)
            dlg.ShowModal()
        return _


    # end of class AddItemDialog


