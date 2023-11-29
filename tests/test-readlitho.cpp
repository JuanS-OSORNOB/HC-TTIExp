#include <basic/readwrite.h>

int main()
{
    std::string kinFilename = "test_data/kinetic_properties.txt";
    double kinArg1, kinArg2, kinArg3;
    readkineticfile(kinFilename, kinArg1, kinArg2, kinArg3);
    return 0;
}