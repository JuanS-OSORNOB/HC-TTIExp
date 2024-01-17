#include <HCTTIExpProjConfig.h>
#include <fluid_properties/fluidproperties.h>
#include <basic/readwrite.h>

#include <iostream>
#include <fstream>
#include <vector>

namespace HCTTIEXP
{
    std::vector<KineticData> Fluidproperties::readkineticfile(const std::string& fluidFilename)
    {
        Readfiles reader;  // Create an instance of Readfiles to use its functions
        return reader.readkineticfile(fluidFilename);
    }

    KineticProperties Fluidproperties::populateFluidProperties(const std::vector<KineticData>& fluidDataVector)
    {
        KineticProperties kineticProperties;
        // Iterate through the fluidDataVector and populate
        for (const auto& kineticData : fluidDataVector)
        {
            kineticProperties.activationenergy.push_back(kineticData.column1);
            kineticProperties.exponentialfactor.push_back(kineticData.column2);
            kineticProperties.idealgasconstant.push_back(kineticData.column3);
        }

        return kineticProperties;

    }

    Fluidproperties::Fluidproperties(const std::string& fluidFilename)
    {
        std::cout << "\nLoading the fluid file at: " << fluidFilename << std::endl;
        std::vector<KineticData> fluidDataVector = readkineticfile(fluidFilename);
        std::cout << "Contents of fluidDataVector:" << std::endl;
        for (const auto& KineticData : fluidDataVector)
        {
            std::cout
            << KineticData.column1 << " "
            << KineticData.column2 << " "
            << KineticData.column3 << " "
            << std::endl;
        }

        KineticProperties kineticProperties = populateFluidProperties(fluidDataVector);
        std::cout << "Contents of fluidProperties:" << std::endl;
        for (size_t i = 0; i < kineticProperties.activationenergy.size(); ++i)
        {
            std::cout
            << "Index " << i
            << " Activation energy: " << kineticProperties.activationenergy[i]
            << " Exponential factor: " << kineticProperties.exponentialfactor[i]
            << " Ideal gas constant: " << kineticProperties.idealgasconstant[i]
            << std::endl;
        }
    }
}// namespace HCTTIEXP