package require vtk
package require vtkinteraction

# Reader to get the data from the file.  This describes the on-disk file
# format so that VTK can parse it correctly.

vtkImageReader  reader
	reader SetFileName "TS21z_X_R2_008000.bin"

#	There are three dimensions in the file (X, Y, and Z)
#	Note that this file only stores the value for the X
#	component of the velocity, but it does this over the
#	whole 3D volume.
	reader SetFileDimensionality 3

#	There is one scalar field stored, and it is in big-endian floats
	reader SetDataScalarTypeToFloat
	reader SetDataByteOrderToBigEndian
	reader SetNumberOfScalarComponents 1

#	The first and last index of data values in X, Y, and Z
	reader SetDataExtent 0 749 0 374 0 99

#	Picking an origin at zero, for no good reason
	reader SetDataOrigin 0 0 0

# 	The data samples are 800 meters apart in X,Y,Z
	reader SetDataSpacing 800 800 800

# Get all of the parameters filled in by parsing the file
reader Update
scan [[reader GetOutput] GetWholeExtent] "%d %d %d %d %d %d" \
        xMin xMax yMin yMax zMin zMax

# Flip the image over in Y to make the coordinate system match
# that of the data computation.  The VTK image reader assumes
# pixel (0,0) is at the upper-left, which is left-handed.
vtkImageFlip reslice1
  reslice1 SetInput [reader GetOutput]
  reslice1 SetFilteredAxis 1

# Magnify the image

set mag_factor 1
vtkImageMagnify magnify
  magnify SetInput [reslice1 GetOutput]
  magnify SetMagnificationFactors $mag_factor $mag_factor 1

# Create the image viewer

vtkImageViewer viewer2
  viewer2 SetInput [magnify GetOutput]
  viewer2 SetZSlice 14
# Set the scale so that we can see something in the data
  viewer2 SetColorWindow 1
  viewer2 SetColorLevel 0.05

# Create the GUI, i.e. two Tk image viewer, one for the image
# the other for a slice slider

wm withdraw .
toplevel .top 

# Set the window manager (wm command) so that it registers a
# command to handle the WM_DELETE_WINDOW protocal request. This
# request is triggered when the widget is closed using the standard
# window manager icons or buttons. In this case the exit callback
# will be called and it will free up any objects we created then exit
# the application.

wm protocol .top WM_DELETE_WINDOW ::vtk::cb_exit

# Create the vtkTkImageViewerWidget

frame .top.f1 

set vtkiw [vtkTkImageViewerWidget .top.f1.r1 \
        -width [expr ($xMax - $xMin + 1) * $mag_factor] \
        -height [expr ($yMax - $yMin + 1) * $mag_factor] \
        -iv viewer2]

# Setup some Tk bindings, a generic renwin interactor and VTK observers 
# for that widget

::vtk::bind_tk_imageviewer_widget $vtkiw

# Add a 'Quit' button that will call the usual cb_exit callback and destroy
# all VTK objects

button .top.btn \
        -text Quit \
        -command ::vtk::cb_exit

# Add a slice scale to browse the whole stack

scale .top.slice \
        -from $zMin \
        -to $zMax \
        -orient horizontal \
        -command SetSlice \
        -variable slice_number \
        -label "Z Slice"

proc SetSlice {slice} {
    global xMin xMax yMin yMax

    viewer2 SetZSlice $slice
    viewer2 Render
}

# Pack all gui elements

pack $vtkiw \
        -side left -anchor n \
        -padx 3 -pady 3 \
        -fill x -expand f

pack .top.f1 \
        -fill both -expand t

pack .top.slice .top.btn \
        -fill x -expand f

# You only need this line if you run this script from a Tcl shell
# (tclsh) instead of a Tk shell (wish) 

tkwait window .
