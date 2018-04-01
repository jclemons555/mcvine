from pyre.geometry.operations import *


from pyre.geometry.operations.Difference import Difference as DifferenceBase
class Difference(DifferenceBase):

    def __str__(self):
        return "difference(op1=%s, opt2=%s)" % (self.op1, self.op2)
    def todict(self):
        return dict(difference=[self.op1.todict(), self.op2.todict()])


from pyre.geometry.operations.Dilation import Dilation


#overload union and intersection to allow more-than-two elements
from pyre.geometry.operations.Composition import Composition as base
class Composition(base):

    def __init__(self, *shapes):
        self.shapes = shapes
        return


class Union(Composition):
    def identify(self, visitor): return visitor.onUnion(self)
    def __str__(self):
        return "union(" + ','.join(map(str, self.shapes)) + ")"
    def todict(self):
        return dict(union=[e.todict() for e in self.shapes])
    pass


class Intersection(Composition):
    def identify(self, visitor): return visitor.onIntersection(self)
    def __str__(self):
        return "intersection(" + ','.join(map(str, self.shapes)) + ")"
    def todict(self):
        return dict(intersection=[e.todict() for e in self.shapes])
    pass


#overload translation
from pyre.geometry.operations.Translation import Translation as base
class Translation(base):

    def __init__(self, body, vector=None, beam="0.*m", transversal="0.*m", vertical="0.*m"):
        """Translation(body, vector=)
        Rotation(body, beam=, transversal=, vertical=)

        When vector is specified, it means the coordinate system is implicit
        When beam, transversal, vertical is specified, it uses the convention in instrument.geometry
        """
        self.body = body
        self.vector = vector if vector is not None else (beam, transversal, vertical)
        self.implicit_coordinate_system = vector is not None
        return

    def __str__(self):
        return "translation: body={%s}, vector(beam, transversal, vertical)={%s}" %(
            self.body, self.vector)

    def todict(self):
        beam, transversal, vertical = self.vector
        vector = dict(beam=str(beam), transversal=str(transversal), vertical=str(vertical))
        t = self.body.todict()
        t.update(vector=vector)
        return dict(translation=t)


#overload rotation
from pyre.geometry.operations.Rotation import Rotation as base
class Rotation(base):

    def __init__(self, body, axis=None, beam=0., transversal=0., vertical=0., angle=0., euler_angles=None):
        """
        Rotation(body, euler_angles=)
        Rotation(body, axis=, angle=)
        Rotation(body, beam=, transversal=, vertical=, angle=)

        When axis is specified, it means the coordinate system is implicit
        When beam, transversal, vertical is specified, it uses the convention in instrument.geometry
        When euler_angles is specified, it is using the Tait-Bryan convention, and the coordinate
        system is implicit.
        """
        self.body = body
        self.euler_angles = euler_angles
        if euler_angles is not None:
            self.implicit_coordinate_system = True
            return
        self.angle = angle
        if axis is not None:
            self.axis = axis
            self.implicit_coordinate_system = True
            return
        self.axis = beam, transversal, vertical
        self.implicit_coordinate_system = False
        return


    def __str__(self):
        if self.euler_angles:
            return "rotation: body={%s}, euler_angles(xy'z\")={%s}" %(
                self.body, self.euler_angles)
        return "rotation: body={%s}, axis(beam, transversal, vertical)={%s}, angle={%s}" %(
            self.body, self.axis, self.angle)


    def todict(self):
        beam, transversal, vertical = self.axis
        axis = dict(beam=beam, transversal=transversal, vertical=vertical)
        r = self.body.todict()
        r.update(axis=axis, angle=str(self.angle))
        return dict(rotation=r)

    
def unite(*shapes):
    return Union(*shapes)


def intersect(*shapes):
    return Intersection(*shapes)


def rotate(shape, **kwds):
    return Rotation(shape, **kwds)

def translate(shape, **kwds):
    return Translation(shape, **kwds)

def subtract(op1, op2):
    return Difference(op1, op2)
