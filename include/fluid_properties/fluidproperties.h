/**
 * @file fluidproperties.h
 * @author Juan Sebastian Osorno Bolivar (juansebosornob@gmail.com)
 * @brief This file sets the fluid properties
 * @version 0.1
 * @date 2024-01-22
 * 
 * @copyright Copyright (c) 2024
 * 
 */
#ifndef FLUIDPROPERTIES_H
#define FLUIDPROPERTIES_H

#include <basic/readwrite.h>
#include <vector>
#include <string>

namespace HCTTIEXP
{
    /**
     * @brief The struct saves the kinetic properties of the fluid
     * 
     */
    struct KineticProperties
    {
    std::vector<double> activationenergy;
    std::vector<double> exponentialfactor;
    std::vector<double> idealgasconstant;
    };
    /**
     * @brief This class handles the fluid properties
     * 
     */
    class Fluidproperties
    {
        private:
            /**
             * @brief 
             * Function to read fluid file and return std::vector<FluidData>
             * @param fluidFilename 
             * @return std::vector<KineticData> 
             */
            std::vector<KineticData> readkineticfile(const std::string& fluidFilename);
            /**
             * @brief 
             * Function to populate the fluid properties vector
             * @param fluidDataVector 
             * @return KineticProperties 
             */
            KineticProperties populateFluidProperties(const std::vector<KineticData>& fluidDataVector);
        public:
            /**
             * @brief 
             * Constructor of public access to the class
             */
            KineticProperties kineticProperties;
            /**
             * @brief Construct a new Fluidproperties object
             * 
             * @param fluidFilename 
             */
            Fluidproperties(const std::string& fluidFilename);
    };
}// namespace HCTTIEXP
#endif