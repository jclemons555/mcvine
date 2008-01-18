#this little script calculates the positions of tubes in the 8-pack
#

from pyre.units.length import *


def getPositions( radius, gap):
    #a list of 8 numbers. tube positions
    positions = [
        - i * (2*radius+gap) + 7*radius + 3.5* gap for i in range(8)
        ]
    from numpy import array
    return array(positions)


def main():
    #radius of tube:
    radius = 0.5 * inch

    #gap between two tubes
    gap = 0.08 * inch

    print getPositions( radius, gap ) / inch
    return


if __name__ == '__main__': main()

