# modified from HYSPEC: height is 2 meter

#this little script calculates the size of a 8-pack
#
from pyre.units.length import *

#radius of tube:
radius = 0.5 *inch
#height of tube:
height = 2 *meter

#gap between two tubes
delta = 0.08 * inch



def getSize( radius, height, gap ):
    with_cushion = 1.005
    size = {
        'thickness': 2*radius * with_cushion,
        'width': (8*2*radius + 7*gap) * with_cushion,
        'height': height * with_cushion,
        }
    return size

if __name__ == '__main__':
    print(getSize( radius, height, delta ))
