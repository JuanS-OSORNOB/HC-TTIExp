#ifndef FLUIDPROPERTIES_H
#define FLUIDPROPERTIES_H

#include <basic/readwrite.h>
#include <vector>
#include <string>

namespace HCTTIEXP
{
    struct KineticProperties
    {
    std::vector<double> activationenergy;
    std::vector<double> exponentialfactor;
    std::vector<double> idealgasconstant;
    };

    class Fluidproperties
    {
        private:
        // Function to read fluid file and return std::vector<FluidData>
            std::vector<KineticData> readkineticfile(const std::string& fluidFilename);
            KineticProperties populateFluidProperties(const std::vector<KineticData>& fluidDataVector);
        public:
            Fluidproperties(const std::string& fluidFilename);
    };
}// namespace HCTTIEXP
#endif