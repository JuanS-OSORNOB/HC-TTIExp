#include <basic/readwrite.h>
#include <iostream>

int main()
{
    std::string kinFilename = "test_data/kinetic_properties.txt";
    double kinArg1, kinArg2, kinArg3;

    // Use the function directly
    readfiles reader;
    if (reader.readkineticfile(kinFilename, kinArg1, kinArg2, kinArg3))
    {
        std::cout << "Succesful reading";// Process the data as needed
    }
    else
    {
        std::cout << "Unsuccessfu reading";// Handle the case where reading fails
    }

    return 0;
}
