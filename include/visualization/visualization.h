/**
 * @file visualization.h
 * @author Juan Sebastian Osorno Bolivar (juansebosornob@gmail.com)
 * @brief File to hanlde visualization of results
 * @version 0.1
 * @date 2024-01-22
 * 
 * @copyright Copyright (c) 2024
 * 
 */
#ifndef VISUALIZATION_H
#define VISUALIZATION_H

#include <vtkSmartPointer.h>
#include <vtkUnstructuredGrid.h>

namespace HCTTIEXP
{
    class Visualization
    {
        public:
            /**
             * @brief 
             * Helper function to add a scalar array to the point data of a grid
             * @param grid 
             * @param value 
             * @param arrayName 
             */
            void addScalarArrayToGrid(vtkSmartPointer<vtkUnstructuredGrid>& grid, double value, const char* arrayName);
        private:
    };

    class UniqueValuesPrinter
    {
        public:
            /**
             * @brief Construct a new Unique Values Printer object
             * 
             * @param array 
             * @param arrayName 
             */
            UniqueValuesPrinter(vtkAbstractArray* array, const std::string& arrayName) : vtkArray(array), arrayName(arrayName) {}
            /**
             * @brief 
             * Prints the unique values
             */
            void printUniqueValues() const;

        private:
            /**
             * @brief 
             * Pointer to vtkArray
             */
            vtkAbstractArray* vtkArray;
            /**
             * @brief 
             * Array name string
             */
            std::string arrayName;
    };

}// namespace HCTTIEXP
#endif