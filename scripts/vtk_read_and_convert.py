import sys
import re
import time
from vtk import vtkImageReader, vtkImageFlip, vtkStructuredPointsWriter

#
# Convert a binary file to the .vtk format for use by the VTK Library
#
def main():
    # CLI
    if len(sys.argv) != 2:
        print("Usage: python ./vtk_read_and_convert.py [filename]")
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

    # Timing
    startTime = time.time()
    # Read file using VTK
    reader = vtkImageReader()
    reader.SetFileName(inputFileName)

    # Configure file
    reader.SetFileDimensionality(3)
    reader.SetDataScalarTypeToFloat()
    reader.SetDataByteOrderToBigEndian()
    reader.SetNumberOfScalarComponents(1)
    reader.SetDataExtent(0, 749, 0, 374, 0, 99)
    reader.SetDataOrigin(0, 0, 0)
    reader.SetDataSpacing(800, 800, 800)

    flipper = vtkImageFlip()
    flipper.SetInputConnection(reader.GetOutputPort())
    flipper.SetFilteredAxis(1)

    # Write to .vtk file
    writer = vtkStructuredPointsWriter()
    writer.SetInputConnection(reader.GetOutputPort())
    writer.SetFileName(outputFileName)
    writer.SetFileTypeToBinary()
    writer.Write()
    endTime = time.time()
    print("[INFO]: Wrote output to '{}' after {} seconds".format(outputFileName, (endTime - startTime)))
    

if __name__ == '__main__':
    main()
