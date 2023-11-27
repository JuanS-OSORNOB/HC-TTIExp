#include <basic/readwrite.h>
#include <fstream>
#include <iostream>
bool readfiles::readkineticfile(const std::string& kinFilename, double& kinArg1, double& kinArg2, double& kinArg3){
    std::ifstream kinFile(kinFilename);
    if(!kinFile.is_open())
    {
        std::cerr << "Error opening kinetic properties file\n";
        return false;//Indicate failure
    }

    kinFile >> kinArg1 >> kinArg2 >> kinArg3;
    kinFile.close();
    return true;//Indicate success
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

    lithoFile.close()

    return true;//Indicate success
}