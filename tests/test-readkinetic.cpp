#include "basic/readwrite.h"
#include <cassert>
#include <filesystem>
#include <iostream>

int main() {
    using namespace HCTTIEXP;
    
    std::string executableDirectory = std::filesystem::path(__FILE__).parent_path().string();
    std::string kinFilename = executableDirectory + "/test_data/test_kinetic_properties.txt";

    Readfiles reader;
    std::vector<KineticData> data = reader.readkineticfile(kinFilename);

    // Print the contents of the data vector
    std::cout << "Data vector contents:" << std::endl;
    for (const auto& entry : data) {
        std::cout << "Column1: " << entry.column1 << " Column2: " << entry.column2 << " Column3: " << entry.column3 << std::endl;
    }
    // Check if the data vector is non-empty
    if (!data.empty()) {
        // Test passed
        std::cout << "Data is not empty" << std::endl;
        return 0;
    } else {
        // Test failed
        assert(false && "Data vector is empty");
        return 1;
    }
}
