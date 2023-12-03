#include <HCTTIExpProjConfig.h>
#include <basic/readwrite.h>

#include <filesystem>
#include <fstream>
#include <iostream>
#include <vector>
#include <string>

std::vector<KineticData> Readfiles::readkineticfile(const std::string& filename) {
    std::vector<KineticData> dataVector;

    std::ifstream file(filename);
    if (!file.is_open()) {
        std::cerr << "Error opening file: " << filename << std::endl;
        return dataVector;
    }

    std::string line;
    while (std::getline(file, line)) {
        // Skip lines starting with "#"
        if (line.size() > 0 && line[0] == '#') {
            continue;
        }

        // Process non-header lines
        std::istringstream iss(line);
        KineticData data;

        // Assuming two columns of integers in this example
        iss >> data.column1 >> data.column2 >> data.column3;

        // Add data to the vector
        dataVector.push_back(data);
    }

    file.close();
    return dataVector;
}

std::vector<LithoData> Readfiles::readlithofile(const std::string& filename) {
    std::vector<LithoData> dataVector;

    std::ifstream file(filename);
    if (!file.is_open()) {
        std::cerr << "Error opening file: " << filename << std::endl;
        return dataVector;
    }

    std::string line;
    while (std::getline(file, line)) {
        // Skip lines starting with "#"
        if (line.size() > 0 && line[0] == '#') {
            continue;
        }

        // Process non-header lines
        std::istringstream iss(line);
        LithoData data;

        // Assuming two columns of integers in this example
        iss >> data.column1 >> data.column2 >> data.column3 >> data.column4;

        // Add data to the vector
        dataVector.push_back(data);
    }

    file.close();
    return dataVector;
}
