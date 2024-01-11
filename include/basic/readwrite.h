#ifndef READWRITE_H
#define READWRITE_H

#include <string>
#include <vector>

namespace HCTTIEXP
{
    /**
     * @brief 
     * @param column1 Tn: Initial exposure absolute temperature (K = C+273).
     * @param column2 Tn+1: Final exposure absolute temperature (K = C+273).
     * @param column3 tn: Initial time of exposure for every 10~C interval.
     * @param column4 tn+1: Final time of exposure for every 10~C interval.
     * @param column5 Lihology: Lithology_id. Must match the one in the *.vtu file.
     */
    struct LithoData
    {//Assuming columns of doubles
        double column1;
        double column2;
        double column3;
        double column4;
        double column5;
        double temperature_range;
        double time_range;
    };

    /**
     * @brief 
     * Structure of the kinetic data based on the columns of my file.
    * @param column1 E: Activation energy (kJ/mol)
    * @param column2 A: Pre-exponential/frequency factor (1/m.y.)
    * @param column3 R: Ideal gas constant (J/K*mol)
     */
    struct KineticData
    {//Assuming columns of doubles
        double column1;
        double column2;
        double column3;
    };
    
    
    class Readfiles
    {
        public:
            /**
             * @brief 
             * This function reads the lithological file and extracts the arguments that will be employed in computing TTIArr
             * @param filename 
             * @return std::vector<LithoData> 
             */
            std::vector<LithoData> readlithofile(const std::string& filename);
            /**
             * @brief  
             * This function reads the kinetic file and extracts the arguments that will be employed in computing TTIArr
             * @param filename 
             * @return std::vector<Data> 
             */
            std::vector<KineticData> readkineticfile(const std::string& filename);
    };
}// namespace HCTTIEXP
#endif