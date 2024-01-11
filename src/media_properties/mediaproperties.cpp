#include <HCTTIExpProjConfig.h>
#include <media_properties/mediaproperties.h>
#include <basic/readwrite.h>

#include <iostream>
#include <fstream>
#include <vector>

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

    void Mediaproperties::modifygrid(const std::string& gridFilename, const std::string& lithoFilename)
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
        
        /*4 Load temperature range and exposure time vectors*/
        std::cout << "Loading the lithological file at: " << lithoFilename << std::endl;
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
        
        /*5 Loop through each point in the grid*/
        
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
        std::cout << "It worked" << std::endl;

    }
}// namespace HCTTIEXP