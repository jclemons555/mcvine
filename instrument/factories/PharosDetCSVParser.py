#!/usr/bin/env python
# Timothy M. Kelley Copyright (c) 2005 All rights reserved

import journal
jnlTag = 'PharosDetCSVParser'
warning = journal.warning(jnlTag)


class Parser( object):

    # This is here for remembering
##     nameMap = { 'index'      :'IDX',
##                 'name'   :'NEW',
##                 'old_name'   :'OLD',
##                 'distance'   :'RADIUS',
##                 'polar_angle':'POLAR',
##                 'azimuthal_angle':'AZIMUTH',
                
##                 'x_rotation':"XROT",
##                 'y_rotation':"YROT",
##                 'z_rotation':"ZROT",
                
##                 'x_translation':"XTRN",
##                 'y_translation':"YTRN",
##                 'z_translation':"ZTRN"
##                 }

    def parse( self):
        """parse() -> [detPackRecords]
        Parse a detector pack CSV file to get the required information
        Input:
            None
        Output:
            list of records
        Exceptions: IOError
        Notes (1):
            (1) each record consists of a dictionary with the keys
            'index', 'name', 'old_name', 'distance', 'azimuthal_angle',
            'polar_angle', 'x_rotation', 'y_rotation', 'z_rotation',
            'x_translation', 'y_translation', 'z_translation'. The value of
            each record is a dictionary with keys 'value' and 'unit'.
            The value of unit is a string.
        """
        lines = self.__fetchLines( self._filename)
        self.__stripHeader( lines, ['@', '!', '#'])
        
        columnHeads = self.__getColumnHeads( lines[0])
        rows = self.__getRows( lines[1:], columnHeads)
        records = self.__makeRecords( rows)
        
        return records


    def __makeRecords( self, rows):
        records = []
        for i,row in enumerate( rows):
            try:
                # skip short detectors (unused at this time)
                if 'short' in row['Type']:
                    record = { 'tubeNo'        : { 'value':int(row['TubeNo' ]), 'unit':None},
                               'IDLArrayIndex' : { 'value':row['IDLArrayIndex'], 'unit':None},
                               'type'          : { 'value':row['Type'], 'unit':None},
                               }
                else:
                    record = { 'tubeNo'        : { 'value':int(row['TubeNo' ]), 'unit':None},
                               'IDLArrayIndex' : { 'value':row['IDLArrayIndex'], 'unit':None},
                               'type'          : { 'value':row['Type'], 'unit':None},
                               'length'        : { 'value':float( row['Length']), 'unit':'m'},
                               'pixelSize'     : { 'value':float( row['PixelSize']), 'unit':'m'},
                               'angle'         : { 'value':float( row['Angle']), 'unit':'degree'},
                               'distance'      : { 'value': float( row["Distance"]),'unit':'m'},
                               }

                records.append( record)
            except KeyError as msg:
                print("KeyError in row %s" % i)
                print("Keys: %s" % str( list(row.keys())))
                print("in keys: %s" % ('TubeNo' in list(row.keys())))
                raise
            except ValueError:
                print("ValueError in row %s" % i)
                print("row has items: %s" % str( list(row.items())))
                raise
        return records
        

    def __init__( self, filename):
        self._filename = filename
        return


    def __fetchLines( self, filename):
        """get raw ascii lines from text file"""
        import csv
        reader = csv.reader( open( filename, 'r'))
        
        lines = [line for line in reader]
        return lines


    def __stripHeader( self, lines, headers = []):
        """Remove all lines whose first entry is a header string in headers"""

        hindices = []
    
        for i, line in enumerate(lines):
            for header in headers:
                headSize = len( header)
                try:
                    if line[0][:headSize] == header:
                        hindices.append( i)
                except IndexError:
                    pass
        hindices.sort(); hindices.reverse()
        hlines = [lines.pop(index) for index in hindices]
        return


    def __getColumnHeads( self, line):
        columns = {}
        for i, entry in enumerate( line):
            if entry != '':
                if entry[0] == ' ':
                    warning.log( "'%s', '%s'" % (entry, entry[1:]) )
                    entry = entry[1:]
                    pass
                columns[ entry] = i
                pass
            continue
        return columns
            

    def __getRows( self, lines, columns):
        rows = []
        heads = list(columns.keys())
        for line in lines:
            row = {}
            for head in heads:
                row[head] = line[ columns[head]]
            rows.append( row)
        return rows


# version
__id__ = "$Id$"

# End of file
