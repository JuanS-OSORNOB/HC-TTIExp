#include <HCTTIExpProjConfig.h>
#include <media_properties/mediaproperties.h>
#include <basic/readwrite.h>
#include <visualization/visualization.h>

#include <iostream>
#include <fstream>
#include <vector>
#include <set>
//#include <deal.II/grid/tria.h>

#include <vtkSmartPointer.h>
#include <vtkIntArray.h>
#include <vtkDoubleArray.h>
#include <vtkXMLUnstructuredGridReader.h>
#include <vtkXMLUnstructuredGridWriter.h>
#include <vtkUnstructuredGrid.h>
#include <vtkCellData.h>
#include <vtkPointData.h>

namespace HCTTIEXP
{
    //using namespace dealii;

    UniqueTRangesCalculator::UniqueTRangesCalculator(const LayerProperties& data) : layerProperties(data) {}

    void UniqueTRangesCalculator::calculateUniqueTRanges()
    {
        for (std::size_t i = 0; i < layerProperties.lithology_id.size(); ++i) {
            std::pair<double, double> tRange = std::make_pair(layerProperties.initial_temperature[i], layerProperties.final_temperature[i]);
            uniqueTRanges[tRange]++;
        }
    }

    void UniqueTRangesCalculator::printUniqueTRanges() const
    {
        std::cout << "Elements in uniqueTRanges:\n";
        for (const auto& entry : uniqueTRanges) {
            std::cout << "Key: (" << entry.first.first << ", " << entry.first.second
                      << "), Value: " << entry.second << '\n';
        }
    }
    
    Mediaproperties::Mediaproperties() : uniqueTRanges(LayerProperties{}){};

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
    
    std::vector<vtkSmartPointer<vtkUnstructuredGrid>> Mediaproperties::modifygrid(const std::string& gridFilename, const std::string& lithoFilename)
    {
        /*1 Load VTU*/
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
        
        /*2 Get the data array for layer_id and fault_id, density and viscosity*/
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

        /*3 Load temperature range and exposure time vectors*/
        std::cout << "\nLoading the lithological file at: " << lithoFilename << std::endl;
        std::vector<LithoData> lithoDataVector = readlithofile(lithoFilename);
        std::cout << "Contents of lithoDataVector:" << std::endl;
        for (const auto& lithoData : lithoDataVector)
        {
            std::cout
            << lithoData.column1 << " "
            << lithoData.column2 << " "
            << lithoData.column3 << " "
            << lithoData.column4 << " "
            << lithoData.column5 << " "
            << std::endl;
        }

        /*4 Populate layer properties*/
        LayerProperties layerProperties = populateLayerProperties(lithoDataVector);
        std::cout << "Contents of layerProperties:" << std::endl;
        for (size_t i = 0; i < layerProperties.lithology_id.size(); ++i)
        {
            std::cout
            << "Index " << i
            << " Layer_id: " << layerProperties.lithology_id[i] 
            << " Initial temperature: " << layerProperties.initial_temperature[i]
            << " Final temperature: " << layerProperties.final_temperature[i]
            << "Initial time: " << layerProperties.initial_time[i]
            << "Initial time: " << layerProperties.final_time[i]
            << std::endl;
        }
                
        /*6 Create a vectors to store modified grids*/
        std::vector<vtkSmartPointer<vtkUnstructuredGrid>> modifiedGrids;
        vtkSmartPointer<vtkUnstructuredGrid> modifiedGrid = vtkSmartPointer<vtkUnstructuredGrid>::New();

        
        /*7 Loop through each temperature range in uniqueTRange and for each loop go trough of each point in the grid based on layer_id */
        uniqueTRanges.calculateUniqueTRanges();
        uniqueTRanges.printUniqueTRanges();
        
        /*{
            modifiedGrids.push_back(modifiedGrid);
        }*/

        /*8 Return the modified grid*/
        return modifiedGrids;
    }
}// namespace HCTTIEXP