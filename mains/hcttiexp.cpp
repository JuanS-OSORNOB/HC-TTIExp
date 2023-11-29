#include <basic/readwrite.h>
#include <basic/message.h>
#include <thermal_effects/tti.h>
#include <basic/message.h>

#include <string>
#include <vector>
#include <iostream>
#include <fstream>

int main() {
    hello_world();
    print_version();
/*     // Read kinetic properties from the first file
    std::string kinFilename = "kinetic_properties.txt";
    double kinArg1, kinArg2, kinArg3;
    if(!readkineticfile(kinFilename, kinArg1, kinArg2, kinArg3))
    {
        return 1;//Handle the error
    }

    // Read lithology properties from the file
    std::string lithoFilename = "lithologic_properties.txt";
    std::vector<double> lithoArg1, lithoArg2, lithoArg3, lithoArg4;
    if(!readlithofile(lithoFilename, lithoArg1, lithoArg2, lithoArg3, lithoArg4))
    {
        return 1;//Handle the error
    }

    // Iterate over components of lithology vectors
    for (int i = 0; i < vectorSize; ++i) {
        // Call the function to compute the formula with all five arguments
        double result = ttiarr(kinArg1, kinArg2, kinArg3, lithoArg1[i], lithoArg2[i], lithoArg3[i], lithoArg4[i]);

        // Output the result for each component
        std::cout << "Result for Component " << (i + 1) << ": " << result << std::endl;
    }
 */
    return 0;
}
