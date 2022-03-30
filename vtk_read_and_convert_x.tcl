package require vtk

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

# Flip the image over in Y to make the coordinate system match
# that of the data computation.  The VTK image reader assumes
# pixel (0,0) is at the upper-left, which is left-handed.
vtkImageFlip reslice1
  reslice1 SetInput [reader GetOutput]
  reslice1 SetFilteredAxis 1

# Write the data to a Structured Points file
vtkStructuredPointsWriter	writer
	writer SetInput [reslice1 GetOutput]
	writer SetFileName "TS21z_X_R2_008000.vtk"
	writer SetFileTypeToBinary
	writer Write

exit
