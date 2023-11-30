#include <basic/readwrite.h>
#include <filesystem>
#include <iostream>

int main()
{
    
    //std::filesystem::path currentPath = std::filesystem::current_path();
    //std::cout << "Current path: " << currentPath << "\n";
    //std::string kinFilename = (currentPath / "test_data" / "kinetic_properties.txt").string();

    std::string executableDirectory = std::filesystem::path(__FILE__).parent_path().string();
    std::cout << "Executable directory: " <<  executableDirectory << "\n";
    std::string kinFilename = executableDirectory + "/test_data/kinetic_properties.txt";


    double kinArg1, kinArg2, kinArg3;

    readfiles reader;
    if (reader.readkineticfile(kinFilename, kinArg1, kinArg2, kinArg3))
    {
        return 0;
    }
    else
    {
        return 1;
    }
}