from pyre.geometry.operations import *


from pyre.geometry.operations.Difference import Difference
from pyre.geometry.operations.Dilation import Dilation
from pyre.geometry.operations.Translation import Translation


#overload union and intersection to allow more-than-two elements
from pyre.geometry.operations.Composition import Composition as base
class Composition(base):

    def __init__(self, *shapes):
        self.shapes = shapes
        return


class Union(Composition):
    def identify(self, visitor): return visitor.onUnion(self)
    pass


class Intersection(Composition):
    def identify(self, visitor): return visitor.onIntersection(self)
    pass


#overload translation
from pyre.geometry.operations.Translation import Translation as base
class Translation(base):

    def __init__(self, body, beam="0.*m", transversal="0.*m", vertical="0.*m"):
        self.body = body
        self.vector = beam, transversal, vertical
        return

    def __str__(self):
        return "translation: body={%s}, vector(beam, transversal, vertical)={%s}" %(
            self.body, self.vector)


#overload rotation
from pyre.geometry.operations.Rotation import Rotation as base
class Rotation(base):

    def __init__(self, body, beam=0., transversal=0., vertical=0., angle=0.):
        self.body = body
        self.axis = beam, transversal, vertical
        self.angle = angle
        return


    def __str__(self):
        return "rotation: body={%s}, axis(beam, transversal, vertical)={%s}, angle={%s}" %(
            self.body, self.axis, self.angle)



def unite(*shapes):
    return Union(*shapes)


def intersect(*shapes):
    return Intersection(*shapes)


def rotate(shape, **kwds):
    return Rotation(shape, **kwds)

def translate(shape, **kwds):
    return Translation(shape, **kwds)

