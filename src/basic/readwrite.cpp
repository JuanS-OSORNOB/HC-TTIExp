#include <HCTTIExpProjConfig.h>
#include <basic/readwrite.h>

#include <filesystem>
#include <fstream>
#include <iostream>
#include <vector>
#include <string>

bool readfiles::readkineticfile(const std::string& kinFilename, double& kinArg1, double& kinArg2, double& kinArg3) {
    std::cout << "Filepath: " << kinFilename << "\n"; // Checking for file existence

    if (!std::filesystem::exists(kinFilename)) {
        std::cerr << "Error: File does not exist: " << kinFilename << "\n";
        return false; // Indicate failure
    } else {
        std::ifstream kinFile(kinFilename, std::ios::in);

        if (!kinFile.is_open()) {
            std::cerr << "Error: Could not open kinetic properties file: " << kinFilename << "\n";
            return false; // Indicate failure
        }

        // Skip header lines starting with '#'
        std::string line;
        while (std::getline(kinFile, line)) {
            if (line.empty() || line[0] != '#')
                break;
        }

        // Read the kinetic parameters
        if (kinFile >> kinArg1 >> kinArg2 >> kinArg3) {
            std::cout << "The following kinetic parameters will be used for computation of the TTI:\n";
            std::cout << "E = " << kinArg1 << "\n";
            std::cout << "A = " << kinArg2 << "\n";
            std::cout << "R = " << kinArg3 << "\n";
            kinFile.close();
            return true; // Indicate success
        } else {
            if (kinFile.eof()) {
                std::cerr << "Error: End of file reached while reading kinetic parameters from file: " << kinFilename << "\n";
            } else if (kinFile.fail()) {
                std::cerr << "Error: Invalid format while reading kinetic parameters from file: " << kinFilename << "\n";
            } else {
                std::cerr << "Error: Unknown error occurred while reading kinetic parameters from file: " << kinFilename << "\n";
            }

            kinFile.close();
            return false; // Indicate failure
        }
    }
}



bool readfiles::readlithofile(const std::string& lithoFilename, std::vector <double>& lithoArg1, std::vector<double>& lithoArg2, std::vector<double>& lithoArg3, std::vector<double>& lithoArg4)
{
    std::ifstream lithoFile(lithoFilename);
    if(!lithoFile.is_open())
    {
        std::cerr << "Error opening lithology properties file: " << lithoFilename << "\n";
        return false;
    }
    
    int vectorSize;
    lithoFile >> vectorSize;
    lithoArg1.resize(vectorSize);
    lithoArg2.resize(vectorSize);
    lithoArg3.resize(vectorSize);
    lithoArg4.resize(vectorSize);

    for (int i=0; i < vectorSize; ++i)
    {
        lithoFile >> lithoArg1[i] >>lithoArg2[i] >>lithoArg3[i] >>lithoArg4[i];
    }

    lithoFile.close();

    return true;//Indicate success
}