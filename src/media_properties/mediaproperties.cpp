#include <HCTTIExpProjConfig.h>
#include <media_properties/mediaproperties.h>
#include <basic/readwrite.h>
#include <visualization/visualization.h>

#include <iostream>
#include <fstream>
#include <vector>
#include <set>
#include <filesystem>
//#include <deal.II/grid/tria.h>

#include <vtkSmartPointer.h>
#include <vtkPointData.h>
#include <vtkCellData.h>
#include <vtkIntArray.h>
#include <vtkDoubleArray.h>
#include <vtkStringArray.h>
#include <vtkUnstructuredGrid.h>
#include <vtkXMLUnstructuredGridReader.h>
#include <vtkXMLUnstructuredGridWriter.h>

namespace HCTTIEXP
{
    //using namespace dealii;

    UniqueTRangesCalculator::UniqueTRangesCalculator(const LayerProperties& data) : layerProperties(data) {}

    void UniqueTRangesCalculator::calculateUniqueTRanges() {
        std::cout << "lithology_id size: " << layerProperties.lithology_id.size() << std::endl;
        for (std::size_t i = 0; i < layerProperties.lithology_id.size(); ++i) {
            std::pair<double, double> tRange = std::make_pair(layerProperties.initial_temperature[i], layerProperties.final_temperature[i]);
            uniqueTRanges.insert(tRange);
        }
        
        for (const auto& TRange : uniqueTRanges)
        {
            uniqueTRangestoLithology[TRange] = std::vector<Times_lithologies>();
        }

        for (std::size_t i = 0; i < layerProperties.lithology_id.size(); ++i)
        {
            std::pair<double, double> tRange = std::make_pair(layerProperties.initial_temperature[i], layerProperties.final_temperature[i]);
            uniqueTRangestoLithology[tRange].push_back({layerProperties.lithology_id[i], layerProperties.initial_time[i], layerProperties.final_time[i]}); 
        }
    }

    const std::map<std::pair<double, double>, std::vector<Times_lithologies>>& UniqueTRangesCalculator::getUniqueRangestoLithology() const
    {
        return uniqueTRangestoLithology;
    }

    void UniqueTRangesCalculator::printUniqueTRanges() const {
        std::cout << "Elements in uniqueTRanges: " << uniqueTRanges.size() << std::endl;
        for (const auto& tRange : uniqueTRanges) {
            std::cout << "Temperature Range: (" << tRange.first << ", " << tRange.second << ")" << std::endl;
        }
    }


    std::map<int, std::string> Mediaproperties::readLayerInfo(const std::string& filename)
    {
        std::map<int, std::string> layerMap;

        std::ifstream file(filename);
        if (!file.is_open())
        {
            std::cerr << "Error opening file: " << filename << std::endl;
            return layerMap;
        }

        int layerId;
        std::string layerName;
        while (file >> layerName >> layerId)
        {
            layerMap[layerId] = layerName;
        }

        file.close();
        return layerMap;
    }

    #include <vtkIntArray.h>
#include <vtkStringArray.h>

    // Assuming layerMap is a std::unordered_map<int, std::string> containing layer_id and layer_name mapping.

    void Mediaproperties::addLayerNameArrayToGrid(vtkSmartPointer<vtkUnstructuredGrid>& grid, const std::map<int, std::string>& layerMap)
    {
        // Get the point data from the grid
        vtkSmartPointer<vtkPointData> pointData = grid->GetPointData();

        // Get the existing layer_id array from the grid
        vtkSmartPointer<vtkIntArray> layerIdArray = vtkIntArray::SafeDownCast(pointData->GetArray("layer_id"));

        // Create a new array for layer_name
        vtkSmartPointer<vtkStringArray> layerNameArray = vtkSmartPointer<vtkStringArray>::New();
        layerNameArray->SetName("LayerName");
        layerNameArray->SetNumberOfComponents(1);
        layerNameArray->SetNumberOfTuples(grid->GetNumberOfPoints());

        // Populate the layer_name array based on layer_id
        for (vtkIdType i = 0; i < grid->GetNumberOfPoints(); ++i) {
            int layerId = layerIdArray->GetValue(i);
            auto it = layerMap.find(layerId);
            if (it != layerMap.end()) {
                const std::string& layerName = it->second;
                layerNameArray->SetValue(i, layerName.c_str());
            } else {
                // Handle the case where layer ID is not found, set a default value or handle error.
                layerNameArray->SetValue(i, "");
            }
        }

        // Add the layer_name array to the point data
        pointData->AddArray(layerNameArray);
    }



    std::vector<LithoData> Mediaproperties::readlithofile(const std::string& lithoFilename)
    {
        Readfiles reader;  // Create an instance of Readfiles to use its functions
        return reader.readlithofile(lithoFilename);
    }
   
    LayerProperties Mediaproperties::populateLayerProperties(const std::vector<LithoData>& lithoDataVector)
    {
        LayerProperties layerProperties;

        // Iterate through the lithoDataVector and populate temperatureRange and exposureTime
        for (const auto& lithoData : lithoDataVector)
        {
            layerProperties.lithology_id.push_back(lithoData.column5);
            layerProperties.initial_temperature.push_back(lithoData.column1);
            layerProperties.final_temperature.push_back(lithoData.column2);
            layerProperties.initial_time.push_back(lithoData.column3);
            layerProperties.final_time.push_back(lithoData.column4);
        }

        return layerProperties;
    }
    
    void Mediaproperties::addScalarArrayToGrid(vtkSmartPointer<vtkUnstructuredGrid>& grid, const std::vector<double>& values, const char* arrayName)
    {
        vtkSmartPointer<vtkDoubleArray> scalarArray = vtkSmartPointer<vtkDoubleArray>::New();
        scalarArray->SetNumberOfComponents(1);
        scalarArray->SetName(arrayName);

        for (const auto& value : values)
        {
            scalarArray->InsertNextValue(value);
        }

        grid->GetPointData()->AddArray(scalarArray);
    }
    
    // std::vector<std::string>
    std::vector<vtkSmartPointer<vtkUnstructuredGrid>> Mediaproperties::modifygrid(const std::string& layerinfoFilename, const std::string& gridFilename, const std::string& lithoFilename)
    {
        /*1 Read the general layer info*/
        std::string layerInfoFilename = layerinfoFilename;
        std::map<int, std::string> layerMap = readLayerInfo(layerInfoFilename);

        /*2 Load VTU*/
        std::cout << "Loading the grid at: " << gridFilename << std::endl;
        const char* fileName = gridFilename.c_str();
        // Create a reader
        vtkSmartPointer<vtkXMLUnstructuredGridReader> reader =
            vtkSmartPointer<vtkXMLUnstructuredGridReader>::New();//Smart pointer to handle memory allocation
        reader->SetFileName(fileName);
        // Update the reader
        reader->Update();
        //Get unstructured grid data and get the point data      
        vtkSmartPointer<vtkUnstructuredGrid> unstructuredGrid = reader->GetOutput();
        vtkSmartPointer<vtkPointData> pointData = unstructuredGrid->GetPointData();
        int number_of_arrays=pointData->GetNumberOfArrays();
        std::cout<<"Number of arrays = "<<number_of_arrays<<std::endl;
        for(int i=0;i<number_of_arrays;i++)
        {
            const char* arrayName=pointData->GetArrayName(i);
            std::cout<<"Array "<<i+1<<": "<<arrayName<<std::endl;
        }

        /*3  Add layer name array to the grid based on layer ID*/
        addLayerNameArrayToGrid(unstructuredGrid, layerMap);
        
        /*4 Get the data array for layer_id and fault_id, density and viscosity*/
        vtkSmartPointer<vtkIntArray> layer_id_array = vtkIntArray::SafeDownCast(pointData->GetArray("layer_id"));//Converts the pointer of the base class to a pointer of the derived class.
        vtkSmartPointer<vtkIntArray> fault_id_array = vtkIntArray::SafeDownCast(pointData->GetArray("fault_id"));
        vtkSmartPointer<vtkDoubleArray> density_array = vtkDoubleArray::SafeDownCast(pointData->GetArray("density"));
        vtkSmartPointer<vtkDoubleArray> viscosity_array = vtkDoubleArray::SafeDownCast(pointData->GetArray("viscosity"));
        //vtkSmartPointer<vtkDoubleArray> pattern_array = vtkDoubleArray::SafeDownCast(pointData->GetArray("pattern"));

        UniqueValuesPrinter printer1(layer_id_array, "layer_id");
        printer1.printUniqueValues();
        UniqueValuesPrinter printer3(density_array, "density_array");
        printer3.printUniqueValues();
        UniqueValuesPrinter printer4(viscosity_array, "viscosity_array");
        printer4.printUniqueValues();
        UniqueValuesPrinter printer2(fault_id_array, "fault_id");
        printer2.printUniqueValues();

        /*5 Load temperature range and exposure time vectors*/
        std::cout << "\nLoading the lithological file at: " << lithoFilename << std::endl;
        std::vector<LithoData> lithoDataVector = readlithofile(lithoFilename);
        std::cout << "Contents of lithoDataVector:" << std::endl;
        for (const auto& lithoData : lithoDataVector)
        {
            std::cout// Add the modified grid to the vector
            << lithoData.column1 << " "
            << lithoData.column2 << " "
            << lithoData.column3 << " "
            << lithoData.column4 << " "
            << lithoData.column5 << " "
            << std::endl;
        }

        /*6 Populate layer properties*/
        LayerProperties layerProperties = populateLayerProperties(lithoDataVector);
        std::cout << "Contents of layerProperties:" << std::endl;
        for (size_t i = 0; i < layerProperties.lithology_id.size(); ++i)
        {
            std::cout
            << "Index " << i
            << " Layer_id : " << layerProperties.lithology_id[i] 
            << " Initial temperature : " << layerProperties.initial_temperature[i]
            << " Final temperature : " << layerProperties.final_temperature[i]
            << " Initial time : " << layerProperties.initial_time[i]
            << " Final time : " << layerProperties.final_time[i]
            << std::endl;
        }
        /*7 Compute unique temperature ranges */
        UniqueTRangesCalculator uniqueTRanges(layerProperties);
        uniqueTRanges.calculateUniqueTRanges();
        uniqueTRanges.printUniqueTRanges();
                
        /*8 Create a vectors to store modified grids*/
        std::vector<vtkSmartPointer<vtkUnstructuredGrid>> modifiedGrids;
        vtkSmartPointer<vtkUnstructuredGrid> modifiedGrid = vtkSmartPointer<vtkUnstructuredGrid>::New();
        
        /*9 Loop through each unique temp range, loop through each point in the grid and assign initial time and final time based on layer_id*/
        std::cout << "\nMODIFYING GRIDS" << std::endl;
        const auto& mapTemprangestolitho = uniqueTRanges.getUniqueRangestoLithology();//mapa
        std::vector<std::string> modifiedGridFileNames; // Vector to store file names
        for (const auto& [TRange, Timelithologies] : mapTemprangestolitho)
        {
            const auto initialTemp = TRange.first;
            const auto finalTemp = TRange.second;
            std::cout << "Modifying grid for temperature range: [" << initialTemp << ", "  << finalTemp << "]" << std::endl;

            // Create a copy of the unstructured grid for each temperature range
            vtkSmartPointer<vtkUnstructuredGrid> modifiedGridCopy = vtkSmartPointer<vtkUnstructuredGrid>::New();
            modifiedGridCopy->DeepCopy(unstructuredGrid);

            // Containers to store lithology-specific values
            std::unordered_map<int, double> lithologyInitialTimes;
            std::unordered_map<int, double> lithologyFinalTimes;

            // Compute lithology-specific values outside the innermost loop
            for (const auto& timeslithology : Timelithologies)
            {
                const auto lithology = timeslithology.lithology;
                const auto initialtime = timeslithology.initialtime;
                const auto finaltime = timeslithology.finaltime;

                std::cout << "  Lithology_" << lithology << " will have the following initial time and final time (m.y.): [" << initialtime << ", " << finaltime << "]" << std::endl;
                lithologyInitialTimes[lithology] = initialtime;
                lithologyFinalTimes[lithology] = finaltime;
            }
            //Create EMPTY arrays with the same size as original grid
            std::vector<double> initialTimeArray(modifiedGridCopy->GetNumberOfPoints(), 0.0);
            std::vector<double> finalTimeArray(modifiedGridCopy->GetNumberOfPoints(), 0.0);
            //Create DEFINED arrays with the same size as original grid
            std::vector<double> initialTempArray(modifiedGridCopy->GetNumberOfPoints(), initialTemp);
            std::vector<double> finalTempArray(modifiedGridCopy->GetNumberOfPoints(), finalTemp);
            // Iterate over each point of the grid and add lithology-specific arrays
            for (vtkIdType i = 0; i < modifiedGridCopy->GetNumberOfPoints(); i++)
            {
                // Assuming 'layer_id_array' is already defined
                vtkIntArray* layer_id_array = vtkIntArray::SafeDownCast(modifiedGridCopy->GetPointData()->GetArray("layer_id"));

                // Access the layer_id for the current point
                const int layer_id_value = layer_id_array->GetValue(i);

                // Check if the layer_id corresponds to a known lithology
                auto initialTimeIt = lithologyInitialTimes.find(layer_id_value);
                auto finalTimeIt = lithologyFinalTimes.find(layer_id_value);

                if (initialTimeIt != lithologyInitialTimes.end() && finalTimeIt != lithologyFinalTimes.end())
                {
                    // Set lithology-specific values for the current point
                    initialTimeArray[i] = initialTimeIt->second;
                    finalTimeArray[i] = finalTimeIt->second;
                }
            }

            
            addScalarArrayToGrid(modifiedGridCopy, initialTimeArray, "initialtime");
            addScalarArrayToGrid(modifiedGridCopy, finalTimeArray, "finaltime");
            addScalarArrayToGrid(modifiedGridCopy, initialTempArray, "initialtemp");
            addScalarArrayToGrid(modifiedGridCopy, finalTempArray, "finaltemp");
            modifiedGrids.push_back(modifiedGridCopy);// Add the modified grid copy to the grids vector


            // Save the modified grid to a new VTU file with a different identifier
            std::filesystem::path filePath(gridFilename);//Extract original filename without path and without extension
            std::string originalfilename = filePath.stem().string();
            //Adjust the path as needed
            int roundedInitialTemp = std::round(initialTemp);
            int roundedFinalTemp = std::round(finalTemp);
            std::string fileName = "/home/juanse/Documents/GitHub/HC-TTIExp/mains/results/TYPE_IID/" + originalfilename + "_" + std::to_string(roundedInitialTemp) + "_" + std::to_string(roundedFinalTemp) + ".vtu";
            modifiedGridFileNames.push_back(fileName);

            vtkSmartPointer<vtkXMLUnstructuredGridWriter> writer = vtkSmartPointer<vtkXMLUnstructuredGridWriter>::New();
            writer->SetFileName(fileName.c_str());
            writer->SetInputData(modifiedGridCopy);
            writer->Write();
        }
        /*10 Return the modified grids*/
        std::cout << "Total number of modified grids: " << modifiedGrids.size() << std::endl;
        return modifiedGrids;
        //return modifiedGridFileNames;
    }
}// namespace HCTTIEXP