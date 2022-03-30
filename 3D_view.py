import sys
import vtk

# Define a class for the keyboard interface
class KeyboardInterface(object):
    """Keyboard interface.

    Provides a simple keyboard interface for interaction. You may
    extend this interface with keyboard shortcuts for, e.g., moving
    the slice plane(s) or manipulating the streamline seedpoints.
    """

    def __init__(self):
        self.screenshot_counter = 0
        self.render_window = None
        self.window2image_filter = None
        self.renderer = None

    def keypress(self, obj, event):
        """This function captures keypress events and defines actions for
        keyboard shortcuts."""
        global SLICE_PLANE_POS

        key = obj.GetKeySym()
        if key == 'Escape':
            sys.exit(0)
            
def main():
    file_name = 'data/TS21z_X_R2_008000.bin'
    # Read file using VTK
    reader = vtk.vtkImageReader()
    reader.SetFileName(file_name)

    # Configure file
    reader.SetFileDimensionality(3)
    reader.SetDataScalarTypeToFloat()
    reader.SetDataByteOrderToBigEndian()
    reader.SetNumberOfScalarComponents(1)
    reader.SetDataExtent(0, 749, 0, 374, 0, 99)
    reader.SetDataOrigin(0, 0, 0)
    reader.SetDataSpacing(800, 800, 800)    
    reader.Update()

    width, height, depth = reader.GetOutput().GetDimensions()

    ### Outline ###
    outline = vtk.vtkOutlineFilter()
    outline.SetInputConnection(reader.GetOutputPort())
    # mapper
    outline_mapper = vtk.vtkPolyDataMapper()
    outline_mapper.SetInputConnection(outline.GetOutputPort())
    # actor
    outline_actor = vtk.vtkActor()
    outline_actor.SetMapper(outline_mapper)
    # Define actor properties (color, shading, line width, etc)
    outline_actor.GetProperty().SetColor(0.8, 0.8, 0.8)
    outline_actor.GetProperty().SetLineWidth(2.0)


    ### Vol ###
    opacityTransferFunction = vtk.vtkPiecewiseFunction()
    opacityTransferFunction.AddPoint(0, 0.0)
    opacityTransferFunction.AddPoint(255, 1)
    # Create transfer mapping scalar value to color.
    colorTransferFunction = vtk.vtkColorTransferFunction()
    colorTransferFunction.AddRGBPoint(0.0, 0.0, 0.0, 0.0)
    colorTransferFunction.AddRGBPoint(64.0, 1.0, 0.0, 0.0)
    colorTransferFunction.AddRGBPoint(128.0, 0.0, 0.0, 1.0)
    colorTransferFunction.AddRGBPoint(192.0, 0.0, 1.0, 0.0)
    colorTransferFunction.AddRGBPoint(255.0, 0.0, 0.2, 0.0)
    # properties
    volumeProperty = vtk.vtkVolumeProperty()
    # volumeProperty.SetColor(colorTransferFunction)
    # volumeProperty.SetScalarOpacity(opacityTransferFunction)
    volumeProperty.ShadeOn()
    volumeProperty.SetInterpolationTypeToLinear()
    # mapper
    volumeMapper = vtk.vtkFixedPointVolumeRayCastMapper()
    volumeMapper.SetInputConnection(reader.GetOutputPort())
    # actor
    volume = vtk.vtkVolume()
    volume.SetMapper(volumeMapper)
    # volume.SetProperty(volumeProperty)



    ### render ###
    renderer = vtk.vtkRenderer()
        
    renderer.SetBackground(0.2, 0.2, 0.2)
    renderer.AddActor(outline_actor)
    renderer.AddActor(volume)

    # Create a render window
    render_window = vtk.vtkRenderWindow()
    render_window.SetWindowName("Earth Quake")
    render_window.SetSize(1200, 1200)
    render_window.AddRenderer(renderer)

    # Create an interactor
    interactor = vtk.vtkRenderWindowInteractor()
    interactor.SetRenderWindow(render_window)

    # Create a window-to-image filter and a PNG writer that can be used
    # to take screenshots
    window2image_filter = vtk.vtkWindowToImageFilter()
    window2image_filter.SetInput(render_window)
    png_writer = vtk.vtkPNGWriter()
    png_writer.SetInputConnection(window2image_filter.GetOutputPort())

    # Set up the keyboard interface
    keyboard_interface = KeyboardInterface()
    keyboard_interface.render_window = render_window
    keyboard_interface.window2image_filter = window2image_filter
    keyboard_interface.png_writer = png_writer

    # Connect the keyboard interface to the interactor
    interactor.AddObserver("KeyPressEvent", keyboard_interface.keypress)


    # Initialize the interactor and start the rendering loop
    interactor.Initialize()
    render_window.Render()
    interactor.Start()



main()