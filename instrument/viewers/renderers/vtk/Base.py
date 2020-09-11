#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2006 All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

"""
renderer of shapes that are typical of neutron components.
This renderer uses vtk.
"""


import journal
debug = journal.debug('VTKRenderer')
warning = journal.warning('VTKRenderer')


from instrument.viewers.renderers.Renderer import Renderer
class VTKRenderer(Renderer):


    #ctor
    def __init__(self, modelConventionAdaptor = None):
        if modelConventionAdaptor is None: modelConventionAdaptor = ModelConventionAdaptor()
        self._modelConventionAdaptor = modelConventionAdaptor
        return


    def render(self, visual_elements, renderer):
        self._vtkModel = renderer
        Renderer.render( self, visual_elements, renderer )
        return


    #handles shapes

    #this rectangular tube is defined by two rectangulars:
    #one for the front opening of the tube,
    #another for the back opening of the tube.
    #the tube tapers linearly from the front opening to
    #the back opening.
    def onRectTube(self, rectTube):
        #coordinates of vertexes relative to the tube coordinate system
        front = rectTube.frontVertexes()
        back  = rectTube.backVertexes()

        #create actors
        actors = createActorsForRectTube( front, back )
        
        debug.log("add a tube: %s, %s" % (front, back))        
        return actors


    def onBox(self, box):
        dimensions = box.diagonal
        actor = CubeActor( *dimensions )
        debug.log("add a box: %s, %s, %s" % (dimensions) )
        return actor


    onTubeBox = onBox


    onBlock = onBox
        

    def onCylinder(self, cylinder):
        dimensions = cylinder.radius, cylinder.height
        actor = CylinderActor( *dimensions )
        debug.log("add a cylinder: %s, %s" % dimensions)
        return actor
        

    def onHollowCyl(self, hollowCyl):
        dimensions = hollowCyl.inside_radius, hollowCyl.ouside_radius, hollowCyl.height
        actor = CylinderActor( *dimensions )
        debug.log("add a hollow cylinder: %s, %s, %s" % dimensions)
        return actor
        

    def onSphereShell(self, sphereShell):
        dimensions = sphereShell.minRadius, sphereShell.maxRadius, \
                     sphereShell.minAngleInPlane, sphereShell.maxAngleInPlane, \
                     sphereShell.minAngleOutOfPlane, sphereShell.maxAngleOutOfPlane,
        actor = SphereShellActor( *dimensions )
        debug.log("add a spherical shell: %s,%s, %s,%s, %s,%s" % dimensions)
        return actor


    def add(self, visualElement):
        #to render a visualElement,
        #1. understand the position and orientation of this object
        #2. use VTK conventiion to describe the position and orientation
        #3. carry out additional rotations necessary. see class ModelConventionAdaptor
        #4. add color and opacity
        
        position = visualElement.position; orientation = visualElement.orientation
        #position and orientation of the shape in the instrument
        position, orientation = self._toVTKconvention(position, orientation)
        debug.log( "postion = %s, rotation = %s" % (position, orientation) )

        shape = visualElement.shape
        try: actor = shape.identify(self)
        except Exception as msg:
            warning.log("%s cannot identify itself because %s" % (shape, msg))
            return
        modelRotations = shape.identify(self._modelConventionAdaptor)

        color = visualElement.color; opacity = visualElement.opacity

        if isinstance(actor, list):
            actors = actor
            for actor in actors:
                self._addActor( actor, position, orientation,
                                modelRotations,
                                color, opacity)
            pass
        else:
            self._addActor( actor, position, orientation,
                            modelRotations,
                            color, opacity)
            pass
        return


    def _toVTKconvention(self, position, orientation):
        "convert the position and orientation to VTK convention"
        raise NotImplementedError("'%s' must provide '%s' to convert position and orientation to "\
              "VTK convention" % (self.__class__.__name__, "_toVTKconvention"))


    def _addActor(self, actor, position, orientation,
                  modelRotations,
                  color, opacity):
        
        actor.AddPosition( position )
        #actor.AddOrientation( orientation )
        self._addRotations( actor, orientation )
        self._applyAdditionalRotations( actor, modelRotations )
        actor.GetProperty().SetColor( *color )
        actor.GetProperty().SetOpacity( opacity )
        self._vtkModel.AddActor( actor )
        return


    def _addRotations( self, actor, orientation ):
        x,y,z = orientation
        actor.RotateZ( z )
        actor.RotateX( x )
        actor.RotateY( y )
        return

    def _applyAdditionalRotations( self, actor, rotations ):
        for rotation in rotations:
            axis, angle = rotation
            self._applyRotation( actor, axis, angle)
            continue
        return

    def _applyRotation( self, actor, axis, angle):
        if axis == 'x': actor.RotateX(angle)
        elif axis == 'y': actor.RotateY(angle)
        elif axis == 'z': actor.RotateZ(angle)
        else: raise NotImplementedError("Unrecognized rotation: %s, %s" % (axis, angle))
        return


    pass # end of VTKRenderer



class ModelConventionAdaptor:

    """ a vtk model has a specific orientation. For example,
    the axis of a cylinder source in vtk is along y direction. So if the
    orientation of a cylinder to be rendered is specified by rotations applied
    to a cylinder with axis along z. Then additional rotations need to be
    carried out so that vtk can correctly display the cylinder.

    An instance of this class provide a way to specify those addtional rotations.

    Each method in this class should return
    a list of 2-tuples with the following format:
    
      ( axis, angle )

      axis = 'x', 'y', or 'z'
      angle is the rotation angle in degrees
      
    """

    def none(self, anything): return []

    onCylinder = onSphereShell = onBox = onBlock = onTubeBox = onRectTube = onHollowCyl = none

    pass # end of ModelConventionAdaptor



def createActorsForRectTube( front_vertexes, back_vertexes ):
    """return vtk actors that represent the a neutron guide
    It is assumed that the guide is a simple straight shape that almost looks
    like a long tube.
    @param front_vertexes: 4 vertexes that define the entrance
    @param back_vertexes: 4 vertexes that define the exit
    """
    # it assumes there are four sides
    fr_leftup, fr_rightup, fr_leftdown, fr_rightdown = front_vertexes
    bk_leftup, bk_rightup, bk_leftdown, bk_rightdown = back_vertexes
    lineActors = []
    lineActors.append( LineActor( fr_leftup, bk_leftup ) )
    lineActors.append( LineActor( fr_rightup, bk_rightup ) )
    lineActors.append( LineActor( fr_leftdown, bk_leftdown ) )
    lineActors.append( LineActor( fr_rightdown, bk_rightdown ) )
    
    lineActors.append( LineActor( fr_leftup, fr_rightup ) )
    lineActors.append( LineActor( fr_rightup, fr_rightdown ) )
    lineActors.append( LineActor( fr_rightdown, fr_leftdown ) )
    lineActors.append( LineActor( fr_leftdown, fr_leftup ) )

    lineActors.append( LineActor( bk_leftup, bk_rightup ) )
    lineActors.append( LineActor( bk_rightup, bk_rightdown ) )
    lineActors.append( LineActor( bk_rightdown, bk_leftdown ) )
    lineActors.append( LineActor( bk_leftdown, bk_leftup ) )
    return lineActors


def LineActor( point1, point2 ):
    from vtk import vtkActor, vtkPolyDataMapper as Mapper, vtkLineSource as Line
    mapper = Mapper()
    source = Line()
    source.SetPoint1( point1 )
    source.SetPoint2( point2 )
    mapper.SetInput( source.GetOutput() )
    actor = vtkActor()
    actor.SetMapper( mapper )
    return actor


def CubeActor( xLen, yLen, zLen ):
    from vtk import vtkActor, vtkPolyDataMapper as Mapper, vtkCubeSource as Cube
    mapper = Mapper()
    source = Cube()
    source.SetXLength( xLen )
    source.SetYLength( yLen )
    source.SetZLength( zLen )
    mapper.SetInput( source.GetOutput() )
    actor = vtkActor()
    actor.SetMapper( mapper )
    return actor


def CylinderActor( radius, height ):
    from vtk import vtkActor, vtkPolyDataMapper as Mapper, vtkCylinderSource as Cylinder
    mapper = Mapper()
    source = Cylinder()
    source.SetRadius( radius )
    source.SetHeight( height )
    mapper.SetInput( source.GetOutput() )
    actor = vtkActor()
    actor.SetMapper( mapper )
    return actor


def HollowCylActor( inside_radius, outside_radius, height ):
    from vtk import vtkActor, vtkPolyDataMapper as Mapper, vtkCylinderSource as Cylinder
    mapper = Mapper()
    source = Cylinder()
    source.SetRadius( outside_radius )
    source.SetHeight( height )
    mapper.SetInput( source.GetOutput() )
    actor = vtkActor()
    actor.SetMapper( mapper )
    return actor
    
    
def SphereShellActor( minRadius, maxRadius, \
                      minAngleInPlane, maxAngleInPlane, \
                      minAngleOutOfPlane, maxAngleOutOfPlane ):
    from vtk import vtkActor, vtkPolyDataMapper as Mapper, vtkSphereSource as Sphere
    mapper = Mapper()
    source = Sphere()
    source.SetRadius( maxRadius )
    
    #Phi is latitude. Phi = 0: north pole. 
    source.SetStartPhi( minAngleOutOfPlane + 90. )
    source.SetEndPhi( maxAngleOutOfPlane + 90. )
    #theta is longtitude, theta = 0 ~ 360
    source.SetStartTheta( minAngleInPlane + 180 )
    source.SetEndTheta( maxAngleInPlane + 180 )
    
    mapper.SetInput( source.GetOutput() )
    actor = vtkActor()
    actor.SetMapper( mapper )
    return actor





def startVTKRender(renderWindowInteractor):
    renderWindowInteractor.Initialize ()
    renderWindowInteractor.Start()
    return




def createVTKRenderWindowInteractor():
    #routine vtk initialization
    import vtk
    renWin = vtk.vtkRenderWindow()
    renderer = vtk.vtkRenderer()
    renWin.AddRenderer (renderer )
    renWin.SetSize (1024,768)
    iren = vtk.vtkRenderWindowInteractor ()
    iren.SetRenderWindow (renWin )
    return iren, renWin, renderer






# version
__id__ = "$Id: Base.py 9 2006-04-18 08:05:40Z jiao $"

# End of file 
