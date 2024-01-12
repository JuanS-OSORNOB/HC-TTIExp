#ifndef MEDIAPROPERTIES_H
#define MEDIAPROPERTIES_H

#include <basic/readwrite.h>
#include <vector>
#include <string>

#include <vtkSmartPointer.h>
#include <vtkUnstructuredGrid.h>

namespace HCTTIEXP
{
    struct LayerProperties
    {
    std::vector<double> lithology_id;
    std::vector<double> temperatureRange;
    std::vector<double> exposureTime;
    };

    class Mediaproperties
    {
    private:
        // Function to read litho file and return std::vector<LithoData>
        std::vector<LithoData> readlithofile(const std::string& lithoFilename);
        // Function to populate LayerProperties from std::vector<LithoData>
        LayerProperties populateLayerProperties(const std::vector<LithoData>& lithoDataVector);
    public:
        vtkSmartPointer<vtkUnstructuredGrid> modifygrid(const std::string& gridFilename, const std::string& lithoFilename, const std::string& outgridFilename);
    };
} // namespace HCTTIEXP
#endif