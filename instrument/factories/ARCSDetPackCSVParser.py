#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2007  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#



def readConf( conffn ):
    lines = open(conffn).readlines()
    vars = lines[0].split()
    vars = [ var.lower() for var in vars ]

    records = []
    
    for line in lines[1:]:
        try:
            cmd = ','.join(vars) + '=' + 'line.split()[:len(vars)]'
            exec cmd
            
            idx = int(idx)
            
            for a in [ 'radius', 'azimuth', 'polar', 'xrot', 'yrot', 'zrot',
                       'xtrn', 'ytrn', 'ztrn' ]:
                exec '%s=float(%s)' % (a,a)
                continue
            
        except Exception, err:
            print "Warning: the following line is not parsed because of %s:%s" % (err.__class__.__name__, err)
            print line
            continue


        if 'SHORT' in line: type = 'short'
        else: type = 'long'

        record = [ type, (xtrn, ytrn, ztrn), (xrot, yrot, zrot),  ]

        records.append( record )
        continue
            
    return records



# version
__id__ = "$Id$"

# End of file 
