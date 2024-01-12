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
        // Iterate through the fluidDataVector and populate  and 
        for (const auto& kineticData : fluidDataVector)
        {
            kineticProperties.activationenergy.push_back(kineticData.column1);
            kineticProperties.exponentialfactor.push_back(kineticData.column2);
            kineticProperties.idealgasconstant.push_back(kineticData.column3);
        }
    }
}