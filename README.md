# README #
Generating a histogram on the thickness of sediments from different depositional environment over modelling time for UnderWorld model.

## Usage ##
### steps ###

1. Create Badlands vtk stratigraphic mesh 
  * this gives the information of thickness , layer ID , relative elevation and x-y-z coordinates of regularly spaced grid over each layer time interval 
  
2. Visulise the pvd file on ParaView

3. Slice the model's stratigraphic mesh layer at the area of interest

4. Output the data of the slice as csv file using the tab "/File /Save Data" on ParaView

5. Follow the instruction of the TODO tag

6. Compile the script



## Suggestions ##
This histsorgram is a good complement with the Wheeler diagram, which shows the spatial distribution of sediments from different depositional environemnt over time. 
