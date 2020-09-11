
from vtk.wx.wxVTKRenderWindowInteractor import wxVTKRenderWindowInteractor
import vtk


class VtkPanel( wxVTKRenderWindowInteractor ):

    def __init__(self, parent, id):
        wxVTKRenderWindowInteractor.__init__(self, parent, id)
        # It would be more correct (API-wise) to call widget.Initialize() and
        # widget.Start() here, but Initialize() calls RenderWindow.Render().
        # That Render() call will get through before we can setup the 
        # RenderWindow() to render via the wxWidgets-created context; this
        # causes flashing on some platforms and downright breaks things on
        # other platforms.  Instead, we call widget.Enable().  This means
        # that the RWI::Initialized ivar is not set, but in THIS SPECIFIC CASE,
        # that doesn't matter.
        widget = self
        widget.Enable(1)

        #widget.AddObserver("ExitEvent", lambda o,e,f=frame: f.Close())

        self.renderer = ren = vtk.vtkRenderer()
        widget.GetRenderWindow().AddRenderer(ren)

##         cone = vtk.vtkConeSource()
##         cone.SetResolution(8)
        
##         coneMapper = vtk.vtkPolyDataMapper()
##         coneMapper.SetInput(cone.GetOutput())
        
##         coneActor = vtk.vtkActor()
##         coneActor.SetMapper(coneMapper)
        
##         ren.AddActor(coneActor)
        
        return

    def render(self, instrument, geometer):
        from instrument.viewers.Instrument2VisualElements import Instrument2VisualElements
        i2ves = Instrument2VisualElements( geometer.storing_coordinate_system )
        ves = i2ves.render( instrument, geometer )
        from instrument.viewers.renderers.vtk.McStasConvention import VTKRenderer
        r = VTKRenderer( )
        print(ves)
        r.render( ves, self.renderer )
##         from instrument.viewers.renderers.vtk.Base import createVTKRenderWindowInteractor, startVTKRender
##         startVTKRender( iren )
    pass

