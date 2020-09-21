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


def parse_file(xmlfile, **kwds):
    """read mantid xml file and get detector pack information"""
    import xml.etree.ElementTree as ET
    tree = ET.parse(xmlfile)
    root = tree.getroot()
    tag = root.tag
    if tag.startswith('{'):
        # tag is '{http://www.mantidproject.org/IDF/1.0}instrument'
        # get the url part
        url = tag[1:].split('}')[0]
        namespaces = dict(idf=url)
    else:
        namespaces = None
    return instrument(root, namespaces=namespaces, **kwds)


import weakref
class instrument:
    
    def __init__(self, xmlroot, rowtypename='row', namespaces=None, monitortag='monitors'):
        """instrument(...): wrapper of instrument IDF xml

    - rowtypename: typename postfix for toplevel detector elements
    - namespaces: xml namespaces
    - monitortag: tag name for monitor(s)
"""
        root = self._root = xmlroot
        self.namespaces = namespaces
        self.defaults = _find(root, 'defaults', namespaces)
        self.components = [
            component(c, root, root, namespaces)
            for c in _findall(root, 'component', namespaces)
            ]
        self.detectors = [
            c for c in self.components
            if c.type.endswith(rowtypename)
            ]
        self.monitor_locations = self._getMonitorLocations(monitortag)
        return


    def getNodes(self, tag):
        root = self._root
        namespaces = self.namespaces
        return [
            node(c, root, root, namespaces)
            for c in _findall(root, tag, namespaces)
            ]

    def _getMonitorLocations(self, monitortag):
        self.monitortag = monitortag
        namespaces = self.namespaces
        root = self._root
        if namespaces:
            ns = list(namespaces.keys())[0]
            xmlnode = root.find("%(ns)s:type[@name='%(monitortag)s']" % dict(ns=ns, monitortag=monitortag), namespaces=namespaces)
        else:
            xmlnode = root.find("type[@name='%s']" % monitortag)
        monitor_positions_container = node(xmlnode, root, root, namespaces)
        comps = monitor_positions_container.getChildren('component')
        if comps:
            # ARCS/SEQ/etc
            """
<component idlist="monitors" type="monitors">
  <location/>
</component>
<type name="monitors">
  <component type="monitor">
    <location name="monitor1" z="-5"/>
  </component>
</type>
"""
            return comps[0].getChildren('location')
        # MARI
        """
  <component type="monitor" idlist="monitor">
    <location z="-4.739" />
    <location z="-1.442" />
    <location z="5.82" />
  </component>
"""
        assert monitortag == 'monitor'
        if namespaces:
            ns = list(namespaces.keys())[0]
            xmlnode = root.find("%(ns)s:component[@type='%(monitortag)s']" % dict(ns=ns, monitortag=monitortag), namespaces=namespaces)
        else:
            xmlnode = root.find("component[@type='%s']" % monitortag)
        monitor_positions_container = node(xmlnode, root, root, namespaces)
        comps = monitor_positions_container.getChildren('location')
        return comps


def _make_operator(method):
    def _(node, tag, ns):
        m = getattr(node, method)
        if ns:
            assert len(ns)==1
            key = list(ns.keys())[0]
            val = list(ns.values())[0]
            return m('%s:%s' % (key, tag), namespaces=ns)
        else:
            return m(tag)
    return _
_find = _make_operator('find')
_findall = _make_operator('findall')
        

class node(object):

    instances = {}
    def __new__(cls, xmlnode, parent, root, namespaces=None):
        instances = cls.instances
        if xmlnode not in instances:
            instances[xmlnode] = object.__new__(cls)
#                cls, xmlnode, parent, root, namespaces)
        return instances[xmlnode]
    

    def __init__(self, xmlnode, parent, root, namespaces=None):
        self._node = weakref.proxy(xmlnode)
        try:
            self._parent = weakref.proxy(parent)
        except TypeError:
            self._parent = parent
        try:
            self._root = weakref.proxy(root)
        except TypeError:
            self._root = root

        self.namespaces = namespaces
        self.components = [
            component(c, xmlnode, root, namespaces)
            for c in _findall(xmlnode, 'component', namespaces)
            ]
        return

    
    def getChildren(self, type):
        root = self._root
        parent = self._node
        namespaces = self.namespaces
        return [
            node(c, parent, root, self.namespaces)
            for c in _findall(parent, type, namespaces)
            ]


    def __getattr__(self, key):
        return self._node.attrib[key]
    __getitem__ = __getattr__
    

    def __str__(self):
        attrs = self._node.attrib.copy()
        attrs = ', '.join(['%s=%r' % (k,v) for k,v in attrs.items()])
        return "%s(%s)" % (self._node.tag, attrs)
    __repr__ = __str__

    
class component(node):

    def __repr__(self):
        attrs = self._node.attrib.copy()
        type = attrs.pop('type')
        attrs = ', '.join(['%s=%r' % (k,v) for k,v in attrs.items()])
        return "%s(%s)" % (type, attrs)
        items = list(self._node)
        return "%s(%s, items=%s)" % (type, attrs, items) 
    __str__ = __repr__


    def getType(self):
        type = self.type
        root = self._root
        namespaces = self.namespaces
        # all "types" are defined in the "root" level
        nodes = _findall(root, "type[@name='%s']" % type, namespaces)
        assert len(nodes) == 1
        node = nodes[0]
        return Type(node, root, root, namespaces=namespaces)
    

class Type(node):
    
    pass


# version
__id__ = "$Id: __init__.py 1271 2007-10-26 23:48:04Z linjiao $"

#  End of file 

