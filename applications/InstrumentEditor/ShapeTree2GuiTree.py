
from geometry.Visitor import Visitor


class ShapeTree2GuiTree( Visitor ):

    def __init__(self, guitree, guitreenode ):
        self.guitree = guitree
        self.guitreenode = guitreenode
        self.shape2gui = {}
        self.gui2shape = {}
        return


    def render(self, tree):
        self._currentGuiTreeNode = self.guitreenode
        tree.identify(self)
        return self.shape2gui, self.gui2shape
    

    def onBinary(self, binary):
        currentGuiTreeNode = self._currentGuiTreeNode
        guitree = self.guitree
        name = binary.__class__.__name__
        new = guitree.AppendItem( currentGuiTreeNode, name )
        self.shape2gui[ binary ] = new
        self.gui2shape[ new ] = binary
        self._currentGuiTreeNode = new
        op1 = binary.op1; op1.identify(self)
        op2 = binary.op2; op2.identify(self)
        self._currentGuiTreeNode = currentGuiTreeNode
        return


    onIntersection = onDifference = onUnion \
                     = onBinary
    

    def onPrimitive(self, primitive):
        currentGuiTreeNode = self._currentGuiTreeNode
        guitree = self.guitree
        name = primitive.__class__.__name__
        new = guitree.AppendItem( currentGuiTreeNode, name )
        self.shape2gui[ primitive ] = new
        self.gui2shape[ new ] = primitive
        return

    onBlock = onCone = onCylinder = onPrism = onPyramid = onSphere \
              = onTorus = onGeneralizedCone = onRectTube \
              = onPrimitive
    
    pass # end of ShapeTree2GuiTree
        
        
