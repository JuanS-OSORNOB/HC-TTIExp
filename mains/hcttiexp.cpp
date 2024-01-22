#include <basic/readwrite.h>
#include <basic/message.h>
#include <thermal_effects/tti.h>
#include <media_properties/mediaproperties.h>
#include <fluid_properties/fluidproperties.h>
#include <thermal_effects/tti.h>

#include <filesystem>
#include <string>
#include <vector>
#include <iostream>
#include <fstream>
#include <sstream>
#include <numeric>

#include <vtkPointData.h>
#include <vtkDoubleArray.h>
#include <vtkXMLUnstructuredGridWriter.h>


int main() {
    using namespace HCTTIEXP;
    
    hello_world();
    print_version();
    Mediaproperties mediaproperties;
    std::string gridFilename = "/home/juanse/Documents/GitHub/HC-TTIExp/mains/data/CORTE_NS.vtu";
    std::string lithoFilename = "/home/juanse/Documents/GitHub/HC-TTIExp/mains/data/litho_properties_2.txt";
    //std::string outgridFilename = "/home/juanse/Documents/GitHub/HC-TTIExp/mains/data/mod_CORTE_NS.vtu";
    std::vector<vtkSmartPointer<vtkUnstructuredGrid>> modifiedGrids = mediaproperties.modifygrid(gridFilename, lithoFilename);

    //Read the kinetic file
    std::string kinFilename = "/home/juanse/Documents/GitHub/HC-TTIExp/mains/data/kinetic_properties.txt";
    Fluidproperties fluidProperties(kinFilename);
    // Access the kinetic properties
    double activationEnergy = fluidProperties.kineticProperties.activationenergy[0];
    double exponentialFactor = fluidProperties.kineticProperties.exponentialfactor[0];
    double idealGasConstant = fluidProperties.kineticProperties.idealgasconstant[0];

    //Create instance of TTI
    TTI tti;
    std::cout << "\nComputing the TTI ..." << std::endl;
    
    //Create a map to store TTI values for each layer_id
    std::map<int, std::vector<double>> layerTTIMap;
    //Create a map to store original temperature ranges
    std::map<int, std::pair<double, double>> originalTempRangesMap;

    //Iterate over each modified grid to compute TTI values
    for (size_t i = 0; i < modifiedGrids.size(); ++i)
    {
        std::cout << "  Grid " << i << std::endl;
        // Access the modified grid
        vtkSmartPointer<vtkUnstructuredGrid> modifiedGrid = modifiedGrids[i];

        // Access arrays in the modified grid
        int layerId = 0; //A punctual one needs to be declared to store in the map and then apply it to the filename
        vtkDataArray* layerIdArray = modifiedGrid->GetPointData()->GetArray("layer_id");
        vtkDataArray* initialTimeArray = modifiedGrid->GetPointData()->GetArray("initialtime");
        vtkDataArray* finalTimeArray = modifiedGrid->GetPointData()->GetArray("finaltime");
        vtkDataArray* initialTempArray = modifiedGrid->GetPointData()->GetArray("initialtemp");
        vtkDataArray* finalTempArray = modifiedGrid->GetPointData()->GetArray("finaltemp");

        //Create empty arrays with the same size as original grid
        std::vector<double> ttiArray(modifiedGrid->GetNumberOfPoints(), 0.0);
        ttiArray.reserve(modifiedGrid->GetNumberOfPoints());

        //Compute TTI for each point
        for (vtkIdType j = 0; j < modifiedGrid->GetNumberOfPoints(); ++j)
        {
            // Access values for the current point
            double initialTime = initialTimeArray->GetTuple1(j);
            double finalTime = finalTimeArray->GetTuple1(j);
            double initialTemp = initialTempArray->GetTuple1(j);
            double finalTemp = finalTempArray->GetTuple1(j);

            // Compute TTI value using the TTI class and other variables
            double ttiValue = tti.ttiarr(
                exponentialFactor, 
                finalTime,
                initialTime,
                finalTemp,
                initialTemp,
                idealGasConstant,
                activationEnergy
            );

            ttiArray[j] = ttiValue;
            //Accesing the value for the current point and pushing back the TTI to the map
            int layerId = layerIdArray->GetTuple1(j);
            layerTTIMap[layerId].push_back(ttiValue);

            originalTempRangesMap[layerId] = {initialTemp, finalTemp};
        }
        
        // Create a new array to store the computed TTI values
        vtkSmartPointer<vtkDoubleArray> scalarArray = vtkSmartPointer<vtkDoubleArray>::New();
        scalarArray->SetNumberOfComponents(1);
        scalarArray->SetName("TTI");
        for (const auto& ttivalue : ttiArray)
        {
            scalarArray->InsertNextValue(ttivalue);
        }
        modifiedGrid->GetPointData()->AddArray(scalarArray);


        // Save (write) the modified grid to a new file
        std::filesystem::path filePath(gridFilename);//Extract original filename without path and without extension
        std::string originalfilename = filePath.stem().string();

        std::stringstream filenameStream;
        filenameStream << "/home/juanse/Documents/GitHub/HC-TTIExp/mains/results/TTI_" << originalfilename << "_" << originalTempRangesMap[layerId].first << "_" << originalTempRangesMap[layerId].second << ".vtu";  // Modify as needed
        std::string outputFilename = filenameStream.str();

        vtkSmartPointer<vtkXMLUnstructuredGridWriter> writer = vtkSmartPointer<vtkXMLUnstructuredGridWriter>::New();
        writer->SetFileName(outputFilename.c_str());
        writer->SetInputData(modifiedGrid);
        writer->Write();
    }

    //Compute the sum of TTI values for each layer_id
    std::map<int, double> layerTTISumMap;
    for (const auto& entry : layerTTIMap)
    {
        int layerId = entry.first;
        const std::vector<double>& ttiValues = entry.second;
        //Sum the TTI values for the current layer_id
        double ttiSum = std::accumulate(ttiValues.begin(), ttiValues.end(), 0.0);
        //Store the sum in the map
        layerTTISumMap[layerId] = ttiSum;
        double oilexpulsed_perc = 100 * (1.0 - std::exp(-ttiSum));
        std::cout << "Layer " << layerId << ". Sum TTI = " << ttiSum << ", Oil expulsed: " << oilexpulsed_perc << "%" << std::endl;
    }
    

    return 0;
}
