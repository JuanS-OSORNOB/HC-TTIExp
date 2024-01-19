#ifndef MEDIAPROPERTIES_H
#define MEDIAPROPERTIES_H

#include <basic/readwrite.h>
#include <vector>
#include <string>
#include <map>

#include <vtkSmartPointer.h>
#include <vtkUnstructuredGrid.h>

namespace HCTTIEXP
{
    struct LayerProperties
    {
    std::vector<double> lithology_id;
    std::vector<double> initial_temperature;
    std::vector<double> final_temperature;
    std::vector<double> initial_time;
    std::vector<double> final_time;
    };

    class UniqueTRangesCalculator {
    public:
        UniqueTRangesCalculator(const LayerProperties& data);
        void calculateUniqueTRanges();
        void printUniqueTRanges() const;

    private:
        LayerProperties layerProperties;
        std::map<std::pair<double, double>, int> uniqueTRanges;
    };

    class Mediaproperties
    {
        private:
            UniqueTRangesCalculator uniqueTRanges;  // Instance of UniqueTRangesCalculator
            // Function to read litho file and return std::vector<LithoData>
            std::vector<LithoData> readlithofile(const std::string& lithoFilename);
            // Function to populate LayerProperties from std::vector<LithoData>
            LayerProperties populateLayerProperties(const std::vector<LithoData>& lithoDataVector);
        public:
            Mediaproperties(); 
            std::vector<vtkSmartPointer<vtkUnstructuredGrid>> modifygrid(const std::string& gridFilename, const std::string& lithoFilename);//const std::string& outgridFilename
    };
} // namespace HCTTIEXP
#endif