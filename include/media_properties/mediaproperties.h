/**
 * @file mediaproperties.h
 * @author Juan Sebastian Osorno Bolivar (juansebosornob@gmail.com)
 * @brief This file sets the media properties
 * @version 0.1
 * @date 2024-01-22
 * 
 * @copyright Copyright (c) 2024
 * 
 */
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
    /**
     * @brief 
     * The struct handles the media properties
     */
    struct LayerProperties
    {
    std::vector<int> lithology_id;
    std::vector<double> initial_temperature;
    std::vector<double> final_temperature;
    std::vector<double> initial_time;
    std::vector<double> final_time;
    };
    /**
     * @brief 
     * This struct is created to hanlde a map that related lithology to temperature ranges
     */
    struct Times_lithologies
    {
        int lithology;
        double initialtime;
        double finaltime;
    };
    /**
     * @brief 
     * This class helps computing the unique temperature ranges in a input file
     */
    class UniqueTRangesCalculator {
    public:
        /**
         * @brief Construct a new Unique T Ranges Calculator object
         * 
         * @param data 
         */
        UniqueTRangesCalculator(const LayerProperties& data);
        /**
         * @brief 
         * The function that calculates the unique T ranges
         */
        void calculateUniqueTRanges();
        /**
         * @brief 
         * The function that prints them
         */
        void printUniqueTRanges() const;
        /**
         * @brief Get the Unique Rangesto Lithology object
         * 
         * @return const std::map<std::pair<double, double>, std::vector<Times_lithologies>>& 
         */
        const std::map<std::pair<double, double>, std::vector<Times_lithologies>>& getUniqueRangestoLithology() const;

    private:
        /**
         * @brief 
         * Creates a new object of LayerProperties struct
         */
        LayerProperties layerProperties;
        /**
         * @brief 
         * Map for the temp ranges
         */
        std::set<std::pair<double, double>> uniqueTRanges;
        /**
         * @brief 
         * Map for the temp ranges and the lithology
         */
        std::map<std::pair<double, double>, std::vector<Times_lithologies>> uniqueTRangestoLithology;
    };
    /**
     * @brief 
     * Class that handles the media properties
     */
    class Mediaproperties
    {
        private:
            /**
             * @brief 
             * Instance of UniqueTRangesCalculator
             */
            UniqueTRangesCalculator uniqueTRanges;
            /**
             * @brief 
             * Function to read litho file
             * @param lithoFilename 
             * @return std::vector<LithoData> 
             */
            std::vector<LithoData> readlithofile(const std::string& lithoFilename);
            /**
             * @brief 
             * Function to populate LayerProperties from std::vector<LithoData>
             * @param lithoDataVector 
             * @return LayerProperties 
             */
            LayerProperties populateLayerProperties(const std::vector<LithoData>& lithoDataVector);
            /**
             * @brief 
             * Helper function to add a scalar array to the point data of a grid
             * @param grid 
             * @param values 
             * @param arrayName 
             */
            void addScalarArrayToGrid(vtkSmartPointer<vtkUnstructuredGrid>& grid, const std::vector<double>& values, const char* arrayName);
        public:
            /**
             * @brief Construct a new Mediaproperties object
             * 
             */
            Mediaproperties() : uniqueTRanges(LayerProperties{}){};
            //std::vector<std::string>
            /**
             * @brief 
             * The most important function in the class, modifies the grid to add new arrays that will help compute the TTI.
             * @param gridFilename 
             * @param lithoFilename 
             * @return std::vector<vtkSmartPointer<vtkUnstructuredGrid>> 
             */
            std::vector<vtkSmartPointer<vtkUnstructuredGrid>> modifygrid(const std::string& gridFilename, const std::string& lithoFilename);//const std::string& outgridFilename
    };
} // namespace HCTTIEXP
#endif