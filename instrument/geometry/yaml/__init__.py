#!/usr/bin/env python
#
# Jiao Lin <jiao.lin@gmail.com>
#

def parse_file(path):
    import yaml
    d = yaml.load(open(path))
    from .parser import Parser
    parser = Parser()
    return parser.parse(d)

# End of file 
