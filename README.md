# 2022 Group 2 Scientific Visualization - Earthquakes

### Group Members
Josh Peterson

Colton Hill

Jeremy Young

### Dataset

Our dataset is from the [2006 IEEE Visualization Contest](http://sciviscontest.ieeevis.org/2006/index.html) which consists of a simulated earthquake in California.

### Instructions

1. [Download](http://sciviscontest.ieeevis.org/2006/download.html) the full dataset.
2. Extract each `TS21z_*_R2_*.gz` archive, yielding a binary file for each timestep/direction combination.
3. Run the [conversion script](./scripts//vtk_read_and_convert.py) to convert each binary file to a VTK file.
4. Open the [PSVM state file](./psvm-files/best_state.pvsm) in Paraview, directing it to the correct location where the VTK files are kept as well as the [highways](./data/highways/all.csv) CSV file containing information on the California border and highways.
5. You should now be able to view the visualization and change time steps.