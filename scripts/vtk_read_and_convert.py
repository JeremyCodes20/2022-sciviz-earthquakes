import sys
import re
import time
import os
from vtk import vtkImageReader, vtkImageFlip, vtkStructuredPointsWriter

#
# Convert a binary file to the .vtk format for use by the VTK Library
#
def bin_to_vtk(files = None, inDir='data/2006/data_files', outDir='/data/2006/vtk_data'):
    # Convert all files
    if files != None:
        inputFileNames = [os.path.join(inDir, f) for f in files]
        outputFileNames = [re.sub(r"\.[^\/\\]+", ".vtk", inFile) for inFile in files] # replace 'filename.*' with 'filename.vtk'
        outputFileNames = [os.path.join(outDir, outFile) for outFile in outputFileNames] # add dirpath to file
        os.makedirs(outDir)
    elif len(sys.argv) == 2:
        inputFileNames = [str(sys.argv[1])]
        outputFileNames = [re.sub(r"\.[^\/\\]+", ".vtk", inputFileNames[0])] # replace 'filename.*' with 'filename.vtk'

    else:
        print("Usage: python ./vtk_read_and_convert.py [filename]")
        exit(1)

    for inputFileName, outputFileName in zip(inputFileNames,outputFileNames):
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
    # use terminal version
    # bin_to_vtk()
    # using automated mass version
    bin_to_vtk(files = [i for i in os.listdir('data/2006/data_files') if not i.endswith('.gz')], 
               inDir='data/2006/data_files', 
               outDir='data/2006/vtk_data')

