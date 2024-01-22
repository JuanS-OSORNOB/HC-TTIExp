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

    //Iterate over each modified grid to compute TTI values
    for (size_t i = 0; i < modifiedGrids.size(); ++i)
    {
        // Access the modified grid
        vtkSmartPointer<vtkUnstructuredGrid> modifiedGrid = modifiedGrids[i];

        // Access arrays in the modified grid
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
        std::stringstream filenameStream;
        filenameStream << "TTI_" << i << ".vtu";  // Modify as needed
        std::string outputFilename = filenameStream.str();

        vtkSmartPointer<vtkXMLUnstructuredGridWriter> writer = vtkSmartPointer<vtkXMLUnstructuredGridWriter>::New();
        writer->SetFileName(outputFilename.c_str());
        writer->SetInputData(modifiedGrid);
        writer->Write();
    }


    return 0;
}
