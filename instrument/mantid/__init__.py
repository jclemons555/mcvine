#!/usr/bin/env python
# 
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 
#                                    Jiao Lin
#                        California Institute of Technology
#                        (C) 2006-2013  All Rights Reserved
# 
#  <LicenseText>
# 
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


import weakref
class instrument:
    
    def __init__(self, xmlroot):
        root = self._root = xmlroot
        self.defaults = root.find('defaults')
        self.components = [
            component(c, root, root) for c in root.findall('component')
            ]
        self.detectors = [
            c for c in self.components
            if c.type.endswith('row')
            ]
        return


class node:

    def __init__(self, xmlnode, parent, root):
        self._node = weakref.proxy(xmlnode)
        try:
            self._parent = weakref.proxy(parent)
        except TypeError:
            self._parent = parent
        try:
            self._root = weakref.proxy(root)
        except TypeError:
            self._root = root

        self.components = [
            component(c, xmlnode, root) for c in xmlnode.findall('component')
            ]
        return

    
    def getChildren(self, type):
        root = self._root
        parent = self._node
        return [
            node(c, parent, root) for c in parent.findall(type)
            ]


    def __getattr__(self, key):
        return self._node.attrib[key]


    def __str__(self):
        attrs = self._node.attrib.copy()
        attrs = ', '.join(['%s=%r' % (k,v) for k,v in attrs.iteritems()])
        return "%s(%s)" % (self._node.tag, attrs)
    __repr__ = __str__

    
class component(node):

    def __repr__(self):
        attrs = self._node.attrib.copy()
        type = attrs.pop('type')
        attrs = ', '.join(['%s=%r' % (k,v) for k,v in attrs.iteritems()])
        return "%s(%s)" % (type, attrs)
        items = list(self._node)
        return "%s(%s, items=%s)" % (type, attrs, items) 
    __str__ = __repr__


    def getType(self):
        type = self.type
        root = self._root
        nodes = root.findall("type[@name='%s']" % type)
        assert len(nodes) == 1
        node = nodes[0]
        return Type(node, root, root)
    

class Type(node):
    
    pass


def parse_file(xmlfile):
    """read mantid xml file and get detector pack information"""
    import xml.etree.ElementTree as ET
    tree = ET.parse(xmlfile)
    root = tree.getroot()
    return instrument(root)


# version
__id__ = "$Id: __init__.py 1271 2007-10-26 23:48:04Z linjiao $"

#  End of file 

