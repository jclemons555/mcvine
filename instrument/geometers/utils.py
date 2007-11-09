#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                       (C) 2005 All Rights Reserved 
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

def isMatrix3(m):
    try: tmp = m[0][0]
    except: return False
    if len(m) != 3 or len(m[0]) != 3: return False
    #should we test if every element is a number?
    return True


def isVector3(v):
    try: l = len(v)
    except: return False
    if l!=3 : return False
    for i in v:
        if not isNumber(i): return False
        continue
    return True


def isNumber(i):
    return isinstance(i,int) or isinstance(i,float)
        

from math import pi
def toradian( angle_in_degree ):
    return angle_in_degree*pi/180;

                                                                                
def todegree( angle_in_radian ):
    return angle_in_radian*180/pi;



from numpy import array
def displacement( v1, v2 ):
    return array(v2) - array(v1)


from numpy import sqrt, array, sum
def length( v ):
    v = array(v)
    return sum( v*v )**(0.5)


# version
__id__ = "$Id: mcstasRotations.py 1208 2007-01-12 17:11:01Z linjiao $"

# End of file 
