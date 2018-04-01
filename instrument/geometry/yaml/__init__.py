#!/usr/bin/env python
#
# Jiao Lin <jiao.lin@gmail.com>
#

import yaml

def parse_file(path):
    d = yaml.load(open(path))
    from .parser import Parser
    parser = Parser()
    return parser.parse(d)

def render_file(shape, path):
    d = shape.todict()
    with open(path, 'w') as outfile:
        yaml.dump(d, outfile, default_flow_style=False)
    return

# End of file 
