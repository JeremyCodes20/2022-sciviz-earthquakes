import sys
import vtk
import re

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
    if len(sys.argv) != 2:
        print("Usage: python ./vtk_read_and_display.py [filename]")
        exit(1)
    inputFileName = str(sys.argv[1])
    outputFileName = re.sub(r"\.[^\/\\]+", ".vtk", inputFileName) # replace 'filename.*' with 'filename.vtk'
    
    # Try to open file (Update() does not throw exception)
    try:
        file = open(inputFileName, 'r')
        file.close()
    except OSError:
        print("[ERR]: Could not open file at '{}'".format(inputFileName))
        exit(1)

    # Read file using VTK
    reader = vtk.vtkImageReader()
    reader.SetFileName(inputFileName)

    # Configure file
    reader.SetFileDimensionality(3)
    reader.SetDataScalarTypeToFloat()
    reader.SetDataByteOrderToBigEndian()
    reader.SetNumberOfScalarComponents(1)
    reader.SetDataExtent(0, 749, 0, 374, 0, 99)
    reader.SetDataOrigin(0, 0, 0)
    reader.SetDataSpacing(800, 800, 800)

    # Get all of the parameters filled in by parsing the file
    reader.Update()
    xMin, xMax, yMin, yMax, zMin, zMax = reader.GetOutput().GetBounds()

    # Flip the image over in Y to make the coordinate system match
    # that of the data computation.  The VTK image reader assumes
    # pixel (0,0) is at the upper-left, which is left-handed.
    reslice1 = vtk.vtkImageFlip()
    reslice1.SetInputData(reader.GetOutput())
    reslice1.SetFilteredAxis(1)

    # Magnify the image

    mag_factor = 1
    magnify = vtk.vtkImageMagnify()
    magnify.SetInputData(reslice1.GetOutput())
    magnify.SetMagnificationFactors(mag_factor,mag_factor, 1)

    # Create the image viewer

    viewer2 = vtk.vtkImageViewer()
    help(viewer2)
    viewer2.SetInputData(magnify.GetOutput())
    viewer2.SetZSlice(14)
    # Set the scale so that we can see something in the data
    viewer2.SetColorWindow(1)
    viewer2.SetColorLevel(0.05)

    # Create the GUI, i.e. two Tk image viewer, one for the image
    # the other for a slice slider

    ### render ###
    renderer = vtk.vtkRenderer()
        
    renderer.SetBackground(0.2, 0.2, 0.2)

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