
# factory methods to create table of { ContainerType: list of children types }

def createByLookupElementModules( elements_package, isElement, isContainer ):
    elements, containers = getAllElementsAndContainers(
        elements_package, isElement, isContainer)
    table = {}
    for container in containers:
        l = []
        for e in elements:
            for t in container.allowed_item_types:
                if issubclass(e,t): l.append(e)
                continue
            continue
        table[container] = l
        continue
    return table


def getAllElementsAndContainers( elements_package, isElement, isContainer ):
    "get a list of element types and container types"
    path = elements_package.__path__[0]
    package = elements_package.__name__
    import os.path, os
    if not os.path.isdir(path): "%s is not a python package" % elements_package
    elements = []
    containers = []
    for filename in os.listdir( path ):
        if filename[-3:] != ".py": continue
        name = filename[:-3]
        m = "%s.%s" % (package,name)
        print("-> try importing %s" % m)
        module = __import__( m, globals(), locals(), [''] )
        klass = module.__dict__.get(name)
        if klass is None: continue
        if isElement(klass): elements.append( klass )
        if isContainer(klass): containers.append( klass )
        continue
    print(elements, containers)
    return elements, containers
            
        
def test():
    import instrument.elements as ie
    from instrument.elements.Element import Element
    from instrument.elements.ElementContainer import ElementContainer
    def isElementClass(klass): return issubclass( klass, Element )
    def isElementContainerClass(klass): return issubclass( klass, ElementContainer )
    t = createByLookupElementModules( ie, isElementClass, isElementContainerClass )
    print(t)
    return


if __name__ == "__main__" : test()
