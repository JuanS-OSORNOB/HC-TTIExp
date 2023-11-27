#pragma once
class readfiles
{
    public:
        /**
         * @brief 
         * This function reads the kinetic file and extracts the arguments that will be employed in computing TTIArr
         * @param kinFilename Filename/relative path for the kinetic properties
         * @param kinArg1 E: Activation energy (kJ/mol)
         * @param kinArg2 A: Pre-exponential/frequency factor (1/m.y.)
         * @param kinArg3 R: Ideal gas constant (J/K*mol)
         * @return true 
         * @return false 
         */
        bool readkineticfile(const std::string& kinFilename, double& kinArg1, double& kinArg2, double& kinArg3){};
        /**
         * @brief 
         * This function reads the lithological file and extracts the arguments that will be employed in computing TTIArr
         * @param lithoFilename 
         * @param lithoArg1 
         * @param lithoArg2 
         * @param lithoArg3 
         * @param lithoArg4 
         * @return true 
         * @return false 
         */
        bool readlithofile(const std::string& lithoFilename, std::vector<double>& lithoArg1, std::vector<double>& lithoArg2, std::vector<double>& lithoArg3, std::vector<double>& lithoArg4){};
};