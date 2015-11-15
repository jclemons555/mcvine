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


ID_ELEMENTSELECTION = 201

import wx

class TreePanel(wx.Panel):

    """target tree must has element nodes and container nodes

    container node:
      name
      getDescendent( path )
      children()
       
    """

    def __init__(self, *args, **kwds):
        self.targetTree = kwds['targetTree']
        del kwds['targetTree']
        wx.Panel.__init__(self, *args, **kwds)

        sizer = wx.BoxSizer()
        
        tree = \
           wx.TreeCtrl(self, ID_ELEMENTSELECTION, style =
                       wx.TR_DEFAULT_STYLE
                       #| wx.TR_HAS_VARIABLE_ROW_HEIGHT
                       # wx.TR_HAS_BUTTONS
                       | wx.TR_EDIT_LABELS
                       #| wx.TR_MULTIPLE
                       #| wx.TR_HIDE_ROOT
                       )
        self.tree = tree

        self.currentTreeItem = self.treeroot = tree.AddRoot(self.targetTree.name)

        tree.Expand( self.treeroot )

        tree.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelChanged, id=ID_ELEMENTSELECTION)
        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.OnActivate, tree)
        self.Bind(wx.EVT_TREE_BEGIN_LABEL_EDIT, self.OnBeginEdit, self.tree)
        self.Bind(wx.EVT_TREE_END_LABEL_EDIT, self.OnEndEdit, self.tree)
        
        sizer.Add(tree, 1, wx.EXPAND, 5)

        self.SetSizer(sizer)
        self.SetAutoLayout(1)
        sizer.Fit(self)
        return


    def OnBeginEdit(self, event):
        # show how to prevent edit...
        item = event.GetItem()
        if item and item == self.treeroot:
            wx.Bell()
            print "You can't edit this one..."

            event.Veto()
            pass
        self._oldItemLabel = self.tree.GetItemText( item )
        print "OnBeginEdit: %s" % self._oldItemLabel
        return


    def OnEndEdit(self, event):
        print ("OnEndEdit: %s %s" %
               (event.IsEditCancelled(), event.GetLabel()) )
        label = event.GetLabel()
        path, item = self.getCurrentItem()
        parentPath = '/'.join( path.split('/')[:-1] )
        if parentPath == "": parent = self.targetTree
        else: parent = self.targetTree.getDescendent( parentPath )
        parent.relinkChild( self._oldItemLabel, label )
        return


    def OnActivate(self, event):
        item = event.GetItem()
        print "double click %s" % self.tree.GetItemText(item)
        from pyregui.guitoolkit.wx import InventoryDialogLoop
        import pyregui.guitoolkit.wx as wxtk
        path, element = self.getCurrentItem()
        print InventoryDialogLoop( self, element, wxtk )
        return
    
        
    def OnSelChanged(self, event):
        item = event.GetItem()
        self.currentTreeItem = item
        itemText = self.tree.GetItemText(item)
        print itemText
        #???
        return
    
    
    def addElementToTree(self, containerPath, elementName):
        node = self._findNode( containerPath )
        newNode = self.tree.AppendItem( node, elementName )
        newPath = '/'.join( [containerPath, elementName] )
        self.tree.Expand( node )
        return


    def _findNode(self, path):
        root = self.treeroot
        return self.findDescendentNode( root, path )


    def findDescendentNode(self, ancestor, bloodline):
        """find descendent node of an ancestor node.
        ancestor: gui element in the tree
        bloodline: sth like a/b/c/d
        """
        bloodline = bloodline.strip('/')
        if bloodline == '': return ancestor
        bloodline = bloodline.split('/')
        name_of_son = bloodline[0]
        son = self.findChildNode( ancestor, name_of_son )
        newbloodline = '/'.join( bloodline[1:] )
        return self.findDescendentNode( son, newbloodline )


    def findChildNode(self, parent, name):
        """find child node of the given parent in the gui tree.
        Child node must have the given name.
        """
        (child, cookie) = self.tree.GetFirstChild(parent)

        while child.IsOk():
            print ("Child [%s] visible = %d" %
                   (self.tree.GetItemText(child),
                    self.tree.IsVisible(child)))
            (child, cookie) = self.tree.GetNextChild(root, cookie)
            if self.tree.GetItemText(child) == name: return child
            continue
        raise RuntimeError, "cannot find child %s of %s" % (name, parent)
        

    def getShelf(self): return self.GetParent().getShelf()


    def getCurrentContainer(self):
        "get current container in the target tree"
        path, e = self.getCurrentItem()
        if not isContainer(e):
            targetTree = self.targetTree
            path = '/'.join( path.split('/')[:-1] )
            e = targetTree.getDescendent( path )
            if not isContainer(e): raise "Fatal: cannot find container"
            pass
        return path, e


    def getPathInTargetTree(self, treeitem):
        "given gui tree item, return path of corresponding item in the target tree"
        tree = self.tree
        path = getPath( treeitem, tree )
        return path


    def getCurrentItem(self):
        "get current item in the target tree"
        path = self.getPathInTargetTree( self.currentTreeItem )
        targetTree = self.targetTree
        if path == '': return path,  targetTree
        e = targetTree.getDescendent( path )
        return path, e


    def getCurrentChild(self):
        """get current item as child in the target tree.
        if the item is acutally a container, return None
        """
        path, e = self.getCurrentItem()
        if isContainer(e): return None, None
        return path, e


    pass #end of TreePanel



def getPath( item, tree ):
    this = tree.GetItemText(item)
    root = tree.GetRootItem()
    if root == item: return ""
    parent = tree.GetItemParent( item )
    return '/'.join( [getPath(parent, tree), this] ).lstrip('/')


def isContainer( c ):
    try: c.children()
    except: return False
    return True


# version
__id__ = "$Id$"

# End of file 
