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

class ShapeTreePanel(wx.Panel):

    """target tree must has element nodes and operation nodes

    operation node:

      Difference, Union
      ...

    primitive node:

      Cylinder, Box
      ...
       
    """

    def __init__(self, *args, **kwds):
        self.targetName = kwds['targetName']
        self.targetTree = kwds['targetTree']
        del kwds['targetTree']
        del kwds['targetName']
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
        self.initializeTree( self.targetTree )

        tree.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelChanged, id=ID_ELEMENTSELECTION)
        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.OnActivate, tree)
        
        sizer.Add(tree, 1, wx.EXPAND, 5)

        self.SetSizer(sizer)
        self.SetAutoLayout(1)
        sizer.Fit(self)
        return


    def changeTargetTree(self, targetTree):
        self.tree.DeleteAllItems()
        self.initializeTree( targetTree )
        return


    def initializeTree(self, targetTree):
        if targetTree is None: return
        tree = self.tree
        self.targetTree = targetTree
        root = self.currentTreeItem = self.treeroot = tree.AddRoot( self.targetName )
        
        from .ShapeTree2GuiTree import ShapeTree2GuiTree
        renderer = ShapeTree2GuiTree( tree, root )
        target2me, me2target = renderer.render( targetTree )
        self.target2me = target2me 
        self.me2target = me2target
        tree.Expand( root )
        return


    def changeSubTree( self, branchInTargetTree, newTargetBranch ):
        """replace a branch of original tree by a new tree"""
        tree = self.tree
        node = self.target2me[ branchInTargetTree ]
        tree.DeleteChildren( node ); tree.Detete( node )
        
        from .ShapeTree2GuiTree import ShapeTree2GuiTree
        renderer = ShapeTree2GuiTree( tree, guinode )
        target2me, me2target = renderer.render( newTargetBranch )
        self.target2me.update( target2me )
        self.me2target.update( me2target )
        tree.Expand( node )
        return


    def OnActivate(self, event):
        item = event.GetItem()
        print("double click %s" % self.tree.GetItemText(item))
        return
    
        
    def OnSelChanged(self, event):
        item = event.GetItem()
        self.currentTreeItem = item
        itemText = self.tree.GetItemText(item)
        print(itemText)
        return
    
    
    def addElementToTree(self, containerPath, elementName):
        node = self._findNode( containerPath )
        newNode = self.tree.AppendItem( node, elementName )
        newPath = '/'.join( [containerPath, elementName] )
        self.path2treeNode[ newPath ] = newNode
        self.tree.Expand( node )
        return


    def _findNode(self, path):
        path = path.strip('/')
        return self.path2treeNode[ path ]


    def getShelf(self): return self.GetParent().getShelf()


    def getCurrentContainer(self):
        "get current container in the target tree"
        path, e = self.getCurrentItem()
        if not isContainer(e):
            targetTree = self.targetTree
            path = '/'.join( path.split('/')[:-1] )
            e = targetTree.getDescendent( path )
            if not isContainer(e): 
                raise RuntimeError("Fatal: cannot find container")
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


    pass #end of ShapeTreePanel



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
