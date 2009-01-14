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
    vars = lines[0].split('\t')
    vars = [ var.lower() for var in vars ]

    records = []

    for line in lines[1:]:
        try:
            record = {}
            for var, value in zip( vars, line.split('\t')[:len(vars)] ):
                record[var] = value
                continue
            print record
            
            for a in [ 'radius', 'azimuth', 'polar', 'xrot', 'yrot', 'zrot',
                       'xtrn', 'ytrn', 'ztrn' ]:
                exec '%s=float(record[a])' % (a,)
                continue

            # the whole ARCS detector system was off-center to 
            # avoid gaps in Q space
            ztrn -= 50

            packID =  record.get('arcs module no.')
            if packID is None: packID = len(records)+1 # ARCS convention: pack ID starts with 1, not 0
            else: packID = int(packID)
            
        except Exception, err:
            print "Warning: the following line is not parsed because of %s:%s" % (err.__class__.__name__, err)
            print line
            continue


        if 'SHORT' in line:
            if '32A' in line:
                type = 'short1' # short tube that is longer
            elif '32B' in line:
                type = 'short2' # short tube that is shorter
            else:
                raise RuntimeError
        else: type = 'long'

        record = [ packID, type, (xtrn, ytrn, ztrn), (xrot, yrot, zrot),  ]

        records.append( record )
        continue

    #sort by packID
    records.sort( lambda x,y: x[0]-y[0] )

    return records



# version
__id__ = "$Id$"

# End of file 
