import journal
debug = journal.debug('instrument.elements.elementTypes')


def _getTypes():
    from Element import Element

    f = __file__
    import os
    d = os.path.dirname( f )
    if d == '': d = '.'
    debug.log( 'directory: %s' % d )

    pyexts = ['.py', '.pyc', '.pyd' , '.pyo' ]
    _modules = []
    types = {}
    for f in os.listdir( d ):
        for ext in pyexts:
            if f.endswith( ext ):
                name = f[: -len(ext)]
                debug.log('module %s' % name)
                debug.log('_modules = %s' % _modules)
                if name in _modules: break
                if name.startswith( '_' ): break # ignore private modules
                _modules.append( name )
                try:
                    exec "from %s import %s" % (name, name )
                except Exception, msg:
                    debug.log( '%s:%s' % (msg.__class__.__name__, msg) )
                    break
                klass = eval( name )
                debug.log('class %s' % klass)
                try:
                    if issubclass( klass, Element ): types[name] = klass
                    pass
                except:
                    print name, klass
                    raise
                break
            continue
        continue
    return types


def typeFromName( name ):
    global _types
    if _types is None: _types = _getTypes()
    if name not in _types:
        raise "Unknown element type: %s" % name
    return _types[name]


_types = None


if __name__ == '__main__': print typeFromName( 'Detector' )


