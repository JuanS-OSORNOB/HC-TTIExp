#ifndef VISUALIZATION_H
#define VISUALIZATION_H

#include <vtkSmartPointer.h>
#include <vtkUnstructuredGrid.h>

namespace HCTTIEXP
{
    class Visualization
    {
        public:
            // Helper function to add a scalar array to the point data of a grid
            void addScalarArrayToGrid(vtkSmartPointer<vtkUnstructuredGrid>& grid, double value, const char* arrayName);
        private:
    };

    class UniqueValuesPrinter
    {
        public:
            UniqueValuesPrinter(vtkAbstractArray* array, const std::string& arrayName) : vtkArray(array), arrayName(arrayName) {}
            void printUniqueValues() const;

        private:
            vtkAbstractArray* vtkArray;
            std::string arrayName;
    };

}// namespace HCTTIEXP
#endif