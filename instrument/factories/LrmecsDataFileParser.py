#!/usr/bin/env python
# Jiao Lin Copyright (c) 2006 All rights reserved

import journal
jnlTag = 'LrmecsDetCSVParser'
warning = journal.warning(jnlTag)



#tubeLength = 0.5 # meter. It is a guess here. It does not really matter because it is not pixellated

from PseudoSingleton import PseudoSingleton

class Parser( PseudoSingleton ):

    def __init1__( self, filename, interpolateData = False):
        its = self.__class__.__its__
        k = filename, interpolateData
        if k not in its.keys():
            for key in its.keys():
                if key[0] == filename:
                    msg = "You have requested reading Lrmecs data file %s with "\
                          "interpolateData=%s, and now you are requesting"\
                          "reading Lrmecs data file %s with interpolateData=%s" % (
                        key[0], key[1], filename, interpolateData)
                    warning.log( msg )
                    break
                continue
            pass
        self._filename = filename
        self._interpolateData = interpolateData
        return


    def parse(self):
        #don't need to reparse
        if self.__dict__.get( "records" ) is None: self.records = self._parse()
        return self.records


    def _parse( self):
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
        
        mod2sample, records = self.__lines2records( lines)

        monitors, tubes = self.__categorizeRecords( records )

        if self._interpolateData:
            tubes = self.__addMissingDetectors( tubes )
            self.__interpolateDetectorsOfZeroIntensities( tubes )
            pass

        #self.__saveI_phi( tubes )
        return mod2sample, monitors, tubes


    def __fetchLines(self, filename):
        f = open(filename)
        return f.readlines()


    def __lines2records(self, lines):
        "convert lines to records"
        mod2samp = float(lines[1].split()[0]) * 1000.0 # unit : mm
        detlines = lines[3:] #after the first 3 lines, all lines are for detectors
        linesPerValidDet = 15
        linesPerInvalidDet = 2
        records = []
        i = 0
        while i < len(detlines):
            record = {}
            if detlines[i].split()[0] == 'Detector':
                if detlines[i+1].split()[0] == '1':
                    record = self.__toValidDet( detlines[i:i+linesPerValidDet] )
                    i += linesPerValidDet
                    records.append(record)
                    pass
                else:
                    #record = self.__toInvalidDet( detlines[i:i+linesPerInvalidDet] )
                    i += linesPerInvalidDet
                    pass
                #print record
                pass
            else:
                warning.log( "**ignored this line: %s" % detlines[i] )
                pass
            continue

        return mod2samp, records


    def __categorizeRecords( self, records ):
        #split records to monitor records and tube records
        monitors = []
        dets = []
        for record in records:
            if record['type'] == 'monitor': monitors.append( record )
            elif record['type'] == 'tube': dets.append( record )
            else : raise NotImplementedError , "Unknown record type %s" % record['type']
            continue
        return monitors, dets
    

    def __parseDetName(self, name ):
        """
        name is sth like 'Detector 23 centered at 4.80'
        this method will return 23, 4.80
        """
        pieces = name.split()
        assert pieces[0] == "Detector"
        assert pieces[-2] == "Detector"
        assert pieces[-1] == "name"
        assert pieces[2] == "centered"
        assert pieces[3] == "at"
        detId = int(pieces[1])
        angle = float(pieces[4])
        return detId, angle


    def __parseDetDesc(self, desc):
        """
        detector description for monitor:
          3in pancake 1.5in thick .001 eff
        detector description for tube:
          1in x 9in x 2.377cm dia 1.00 eff
        """
        pieces = desc.split()
        if 'pancake' in desc:
            radius = float(pieces[0].strip( 'in' ))*25.4 #unit: mm
            thick = float(pieces[2].strip('in'))*25.4 
            eff = float(pieces[4])
            return {'radius':radius, 'thickness': thick, 'efficiency': eff}
        else:
            height = float(pieces[2].strip('in'))*25.4
            radius = float(pieces[4].strip('cm'))*10/2.
            eff = float(pieces[6])
            return {'radius':radius, 'height': height, 'efficiency': eff}
        return


    def __toValidDet( self, lines ):
        "convert lines to a valid detector record"
        name    =         lines[ 0]
        isValid =  bool(  lines[ 1].split()[0] ) 
        tmin =     float( lines[ 2].split()[0] ) 
        tmax =     float( lines[ 3].split()[0] ) 
        tstep =    float( lines[ 4].split()[0] ) 
        detAng =   float( lines[ 5].split()[0] ) 
        plugged =         lines[ 6].split()[0]   
        detType =    int( lines[ 7].split()[0] ) 
        detDesc =         lines[ 8]              
        samp2det = float( lines[ 9].split()[0] )
        firstBin = float( lines[10].split()[0] )
        nTofBins =   int( lines[11].split()[0] )
        _tofBinWidths  =  lines[12].split()
        nCntsBins=   int( lines[13].split()[0] )
        _cnts =           lines[14].split()
        

        id, angle = self.__parseDetName( name )

        if abs(detAng) > 0.:
            assert abs(angle-detAng)/detAng < 1.e-2, \
                   "Det angle mismatch: %s, %s" % (angle, detAng)
            pass

        assert nTofBins == nCntsBins and len(_tofBinWidths) == nTofBins and len(_cnts) == nCntsBins

        if 'pancake' in detDesc : type = "monitor"
        else: type = "tube"
        geom = self.__parseDetDesc( detDesc )

        cnts = [ float(cnt) for cnt in _cnts ]
        tofBinWidths = [ float(tof) for tof in _tofBinWidths ]
        for binW in tofBinWidths: assert float(binW) == float(tstep)
        
        tofBBs = []
        #tof bin boundaries
        for i in range(nTofBins+1): tofBBs.append( firstBin + sum( tofBinWidths[:i] ) ) 
            

        record = {'id'            : id,
                  'type'          : type,
                  'geometry'      : geom,
                  'angle'         : { 'value': detAng, 'unit':'degree'},
                  'distance'      : { 'value': samp2det*1000.,'unit':'mm'},
                  'tofBBs'        : { 'value': tofBBs, 'unit':'microsecond'},
                  'cnts'          : { 'value': cnts, 'unit':None},
                   }

        return record


    def __addMissingDetectors( self, dets ):
        """for some reasons, it might happen that detectors are missing from a data file.
        This method go through all detectors and make sure that for
        every two neighboring detector, the difference of scattering angle is about
        0.6 degree. If the difference is large, then it means some detectors
        are missing between these two detectors. This method then add those missing
        detectors back by add records with interpolating scattering angles.
        But the counts in those interpolating detectors will be left to zeros.
        They will be filled in the method "__interpolateDetectorsOfZeroIntensities".
        """
        detAngles = [ det['angle']['value'] for det in dets ]
        n = len(detAngles)
        newDets = []
        newID = dets[-1]['id'] + 1
        
        for i in range( n -1 ):
            newDets.append( dets[i] )
            
            angle1 = detAngles[i]
            angle2 = detAngles[i+1]
            dphi = angle2 - angle1

            if abs(dphi - 0.6) < 0.05 :
                continue

            det1 = dets[i]
            det2 = dets[i+1]
            
            nMissingDets = int(dphi/0.6 + 0.5) - 1
            if nMissingDets < 1: raise "don't know how to insert detectors into (%s, %s)" %(
                angle1, angle2)

            angles = calcInterpolations( angle1, angle2, nMissingDets )

            import numpy as N
            for i in range( nMissingDets ):
                id = newID; newID += 1
                type = det1['type']
                geom = det1['geometry']
                detAng = angles[i]
                distance = det1['distance']['value']
                tofBBs = det1['tofBBs']['value']
                cnts  = N.zeros( len(det1['cnts']['value']) )
                
                record = {'id'            : id,
                          'type'          : type,
                          'geometry'      : geom,
                          'angle'         : { 'value': detAng, 'unit':'degree'},
                          'distance'      : { 'value': distance,'unit':'mm'},
                          'tofBBs'        : { 'value': tofBBs, 'unit':'us'},
                          'cnts'          : { 'value': cnts, 'unit':None},
                          }
                newDets.append( record )
                continue

            continue

        return newDets
            

    def __interpolateDetectorsOfZeroIntensities( self, dets ):
        """for some reason, some detectors might have unreasonable low counts.
        this method uses interpolation to add counts to those detectors.
        """
        #integrated intensities
        int_ints = [ sum(det['cnts']['value']) for det in dets]
        average_intensity = sum(int_ints)/len(int_ints)        

        #find dets of zero intensity
        indexes_zeroint = []
        for i in range(1, len(dets)-1):
            if int_ints[i] < 0.05*average_intensity: indexes_zeroint.append(i)
            continue

        #print indexes_zeroint

        #group neighbor detectors of zero intensity
        idxes_zeroint = []
        previous_index = None
        for index in indexes_zeroint:
            if previous_index is None: idxes_zeroint.append( [index] )
            elif index == previous_index + 1: idxes_zeroint[-1].append( index )
            elif index <= previous_index: raise \
                 "previoius index %s should be smaller than current index %s" %(
                previous_index, index)
            else: idxes_zeroint.append( [index] )
            previous_index = index
            continue

        #print idxes_zeroint

        #interpolate
        for indexes in idxes_zeroint:
            self.__calcInterpolations( indexes, dets )
            continue
        return


    def __calcInterpolations( self, indexes, dets ):
        """indexes: contiguous indexes of detectors of zero intensity
        dets: all detector records
        """
        index1 = indexes[0] - 1
        index2 = indexes[-1] + 1
        det1 = dets[index1]
        det2 = dets[index2]

        assert det1['tofBBs'] == det2['tofBBs']
        assert det1['type'] == det2['type']
        assert det1['geometry'] == det2['geometry']

        n = len(indexes)
        
        from numpy import array
        cntss = calcInterpolations( array(det1['cnts']['value']),
                                    array(det2['cnts']['value']), n )

        for cnts, index in zip(cntss, indexes): dets[index]['cnts']['value'] = cnts

        return 


    def __saveI_phi(self, tubes):
        "save I(phi)"
        angles = [ tube['angle']['value'] for tube in tubes]
        intensities = [ sum(tube['cnts']['value']) for tube in tubes]
        import pickle
        pickle.dump( (angles, intensities), open('I_phi.pkl', 'w') )
        import pylab
        pylab.plot( angles, intensities )
        pylab.show()
        return


    pass  # end of Parser


def calcInterpolations( x1, x2, n ):
    dx = (x2-x1)/(n+1)
    return [x1+dx*(i+1) for i in range(n)]


# version
__id__ = "$Id$"

# End of file
