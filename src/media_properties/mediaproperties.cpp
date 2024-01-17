#include <HCTTIExpProjConfig.h>
#include <media_properties/mediaproperties.h>
#include <basic/readwrite.h>

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
    class UniqueValuesPrinter {
    public:
        UniqueValuesPrinter(vtkAbstractArray* array, const std::string& arrayName)
            : vtkArray(array), arrayName(arrayName) {}

        void printUniqueValues() const {
            std::cout << "Unique values in " << arrayName << ":" << std::endl;
            std::set<std::string> uniqueValues;
            for (vtkIdType i = 0; i < vtkArray->GetNumberOfTuples(); ++i) {
                std::string value;
                if (vtkIntArray* intArray = vtkIntArray::SafeDownCast(vtkArray)) {
                    value = std::to_string(intArray->GetValue(i));
                } else if (vtkDoubleArray* doubleArray = vtkDoubleArray::SafeDownCast(vtkArray)) {
                    value = std::to_string(doubleArray->GetValue(i));
                } else {
                    // Handle other array types as needed
                    value = "UnknownType";
                }
                uniqueValues.insert(value);
            }
            std::cout << "<";
            bool firstValue = true;
            for (const auto& uniqueValue : uniqueValues) {
                if (!firstValue) {
                    std::cout << ", ";
                }
                std::cout << uniqueValue;
                firstValue = false;
            }
            std::cout << ">" << std::endl;
        }

    private:
        vtkAbstractArray* vtkArray;
        std::string arrayName;
    };

    
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
            layerProperties.temperatureRange.push_back(lithoData.temperature_range);
            layerProperties.exposureTime.push_back(lithoData.time_range);
        }

        return layerProperties;
    }

     vtkSmartPointer<vtkUnstructuredGrid> Mediaproperties::modifygrid(const std::string& gridFilename, const std::string& lithoFilename, const std::string& outgridFilename)
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
        
        /*2 Get the data array for layer_id and fault_id*/
        vtkSmartPointer<vtkIntArray> layer_id_array = vtkIntArray::SafeDownCast(pointData->GetArray("layer_id"));//Converts the pointer of the base class to a pointer of the derived class.
        vtkSmartPointer<vtkIntArray> fault_id_array = vtkIntArray::SafeDownCast(pointData->GetArray("fault_id"));

        /*3 Get the data array for density and viscosity*/
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

        /*4 Load temperature range and exposure time vectors*/
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
            << lithoData.temperature_range << " "
            << lithoData.time_range << std::endl;
        }

        LayerProperties layerProperties = populateLayerProperties(lithoDataVector);
        std::cout << "Contents of layerProperties:" << std::endl;
        for (size_t i = 0; i < layerProperties.temperatureRange.size(); ++i)
        {
            std::cout
            << "Index " << i
            << " Layer_id: " << layerProperties.lithology_id[i] 
            << " Temperature Range: " << layerProperties.temperatureRange[i]
            << " Exposure Time: " << layerProperties.exposureTime[i] 
            << std::endl;
        }
        
        /*5 Create a vector to store modified grids*/
        std::vector<vtkSmartPointer<vtkUnstructuredGrid>> modifiedGrids;

        
        /*5 Loop through each point in the grid and assign temperature range and exposure time based on layuer_id*/
        // Assume you have vtkDoubleArray for temperatureRange and exposureTime
        
        vtkSmartPointer<vtkDoubleArray> temperatureRangeArray = vtkSmartPointer<vtkDoubleArray>::New();
        vtkSmartPointer<vtkDoubleArray> exposureTimeArray = vtkSmartPointer<vtkDoubleArray>::New();
        temperatureRangeArray->SetName("temperatureRange");
        exposureTimeArray->SetName("exposureTime");

        for (vtkIdType pointId = 0; pointId < unstructuredGrid->GetNumberOfPoints(); ++pointId)
        {
            // Get lithology_id for the current point
            int lithologyId = layer_id_array->GetValue(pointId);
            // Find the corresponding index in layerProperties.lithology_id
            auto it = std::find(layerProperties.lithology_id.begin(), layerProperties.lithology_id.end(), lithologyId);
            // If lithologyId is found in layerProperties.lithology_id, associate temperatureRange and exposureTime
            if (it != layerProperties.lithology_id.end())
            {
                size_t index = std::distance(layerProperties.lithology_id.begin(), it);
                // Append the values to the temperatureRange and exposureTime arrays
                temperatureRangeArray->InsertNextTuple1(layerProperties.temperatureRange[index]);
                exposureTimeArray->InsertNextTuple1(layerProperties.exposureTime[index]);
            }
            else
            {
                std::cerr << "Error: Could not find lithology_id " << lithologyId << " in layerProperties.lithology_id." << std::endl;
                // Handle the case where lithologyId is not found, e.g., set default values or handle error.
            }
        }

        // Add the arrays to the point data
        pointData->AddArray(temperatureRangeArray);
        pointData->AddArray(exposureTimeArray);

        
        /*for (vtkIdType i = 0; i < unstructuredGrid->GetNumberOfPoints(); i++)
        {   
            // Get the coordinates for this point
            std::cout << "Point no. = " << i << std::endl;
            double coord[3];
            unstructuredGrid->GetPoint(i, coord);
            std::cout << "Coordinate: (" << coord[0] << "," << coord[1] << "," << coord[2] << ")" << std::endl;
            //Get layer_id for this point
            int layer_id = layer_id_array->GetValue(i);
            std::cout<<"layer_id for this point= "<<layer_id<<std::endl;
            //Get fault_id for this point
            int fault_id = fault_id_array->GetValue(i);
            std::cout<<"fault_id for this point= "<<fault_id<<std::endl;
            //Get density for this point
            double density_i=density_array->GetValue(i);
            std::cout<<"Density for this point= "<<density_i<<std::endl;
            //Get viscosity for this point
            double viscosity_i=viscosity_array->GetValue(i);
            std::cout<<"Viscosity for this point= "<<viscosity_i<<"\n"<<std::endl;     
            // Update density and viscosity
            //density_array->SetValue(i, 2444); //Manual update without caring for the layer
            //viscosity_array->SetValue(i,1e+44); //Manual update without caring for the layer
        }
        */
        
        /*6 Return the modified grid*/

        vtkSmartPointer<vtkUnstructuredGrid> modifiedGrid = vtkSmartPointer<vtkUnstructuredGrid>::New();
        modifiedGrid->ShallowCopy(unstructuredGrid);  // Copy the structure of the original grid
        return modifiedGrid;
        /*
        std::cout << "Saving the modified grid to a new VTU file at: " << outgridFilename << std::endl;
        vtkSmartPointer<vtkXMLUnstructuredGridWriter> writer = vtkSmartPointer<vtkXMLUnstructuredGridWriter>::New();
        const char* outfileName = outgridFilename.c_str();
        writer->SetFileName(outfileName);
        writer->SetInputData(unstructuredGrid);
        writer->Write();
        std::cout << "It worked" << std::endl;*/
    }
}// namespace HCTTIEXP