#ifndef MEDIAPROPERTIES_H
#define MEDIAPROPERTIES_H

#include <basic/readwrite.h>
#include <string>
#include <set>
#include <iostream>
#include <vector>
#include <map>

#include <vtkSmartPointer.h>
#include <vtkUnstructuredGrid.h>

namespace HCTTIEXP
{
    struct LayerProperties
    {
    std::vector<int> lithology_id;
    std::vector<double> initial_temperature;
    std::vector<double> final_temperature;
    std::vector<double> initial_time;
    std::vector<double> final_time;
    };

    struct Times_lithologies
    {
        int lithology;
        double initialtime;
        double finaltime;
    };

    class UniqueTRangesCalculator {
    public:
        UniqueTRangesCalculator(const LayerProperties& data);
        void calculateUniqueTRanges();
        void printUniqueTRanges() const;
        const std::map<std::pair<double, double>, std::vector<Times_lithologies>>& getUniqueRangestoLithology() const;

    private:
        LayerProperties layerProperties;
        std::set<std::pair<double, double>> uniqueTRanges;
        std::map<std::pair<double, double>, std::vector<Times_lithologies>> uniqueTRangestoLithology;
    };

    class Mediaproperties
    {
        private:
            UniqueTRangesCalculator uniqueTRanges;  // Instance of UniqueTRangesCalculator
            // Function to read litho file and return std::vector<LithoData>
            std::vector<LithoData> readlithofile(const std::string& lithoFilename);
            // Function to populate LayerProperties from std::vector<LithoData>
            LayerProperties populateLayerProperties(const std::vector<LithoData>& lithoDataVector);
            // Helper function to add a scalar array to the point data of a grid
            void addScalarArrayToGrid(vtkSmartPointer<vtkUnstructuredGrid>& grid, const std::vector<double>& values, const char* arrayName);
        public:
            Mediaproperties() : uniqueTRanges(LayerProperties{}){};
            //std::vector<std::string>
            std::vector<vtkSmartPointer<vtkUnstructuredGrid>> modifygrid(const std::string& gridFilename, const std::string& lithoFilename);//const std::string& outgridFilename
    };
} // namespace HCTTIEXP
#endif