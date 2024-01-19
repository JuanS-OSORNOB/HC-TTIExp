#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <string>
#include <vtkSmartPointer.h>
#include <vtkXMLUnstructuredGridReader.h>
#include <vtkXMLUnstructuredGridWriter.h>
#include <vtkIntArray.h>
#include <vtkDoubleArray.h>
#include <vtkPointData.h>
#include <vtkUnstructuredGrid.h>

// Assuming you have a LithoData struct
struct LithoData {
    int column1;  // Assuming column1 corresponds to layer_id
    double column2;  // Assuming column2 corresponds to temperature
    double column3;  // Assuming column3 corresponds to exposure
    int column4;  // Assuming column4 corresponds to another property (e.g., fault_id)
    double column5;  // Placeholder for additional properties, adjust accordingly
    double temperature_range;  // Assuming temperature_range is a double
    double time_range;  // Assuming time_range is a double
};

namespace YourNamespace {

    struct LayerProperties {
        std::vector<int> lithology_id;
        std::vector<double> temperatureRange;
        std::vector<double> exposureTime;
    };

    class YourClass {
    public:
        // Function to be used in main
        std::vector<vtkSmartPointer<vtkUnstructuredGrid>> modifyGrids(const std::string& gridFilename, const std::string& lithoFilename) {
            // Load data from your LithoData vector
            std::vector<LithoData> lithoDataVector = readlithofile(lithoFilename);

            // Process the loaded data and populate LayerProperties
            LayerProperties layerProperties = populateLayerProperties(lithoDataVector);

            // Load VTU
            vtkSmartPointer<vtkXMLUnstructuredGridReader> reader =
                vtkSmartPointer<vtkXMLUnstructuredGridReader>::New();
            reader->SetFileName(gridFilename.c_str());
            reader->Update();
            vtkSmartPointer<vtkUnstructuredGrid> unstructuredGrid = reader->GetOutput();

            // Create a vector to store modified grids
            std::vector<vtkSmartPointer<vtkUnstructuredGrid>> modifiedGrids;

            // Loop through each temperature range and exposure time in layerProperties
            for (size_t i = 0; i < layerProperties.lithology_id.size(); ++i) {
                // Create a copy of the structure of the original grid
                vtkSmartPointer<vtkUnstructuredGrid> modifiedGrid = vtkSmartPointer<vtkUnstructuredGrid>::New();
                modifiedGrid->ShallowCopy(unstructuredGrid);

                // Get the temperature range and exposure time for the current iteration
                double temperature = layerProperties.temperatureRange[i];
                double exposure = layerProperties.exposureTime[i];

                // Add temperature range and exposure time arrays to the point data
                addScalarArrayToGrid(modifiedGrid, temperature, "temperatureRange");
                addScalarArrayToGrid(modifiedGrid, exposure, "exposureTime");

                // Add the modified grid to the vector
                modifiedGrids.push_back(modifiedGrid);
            }

            return modifiedGrids;
        }

    private:
        // Helper function to add a scalar array to the point data of a grid
        void addScalarArrayToGrid(vtkSmartPointer<vtkUnstructuredGrid>& grid, double value, const char* arrayName) {
            vtkSmartPointer<vtkDoubleArray> scalarArray = vtkSmartPointer<vtkDoubleArray>::New();
            scalarArray->SetNumberOfComponents(1);
            scalarArray->SetName(arrayName);
            scalarArray->FillComponent(0, value);
            grid->GetPointData()->AddArray(scalarArray);
        }
    };

} // End of namespace YourNamespace
