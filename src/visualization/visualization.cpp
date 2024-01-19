#include <HCTTIExpProjConfig.h>
#include <visualization/visualization.h>

#include <set>

#include <vtkSmartPointer.h>
#include <vtkUnstructuredGrid.h>
#include <vtkDoubleArray.h>
#include <vtkPointData.h>

namespace HCTTIEXP
{
    void Visualization::addScalarArrayToGrid(vtkSmartPointer<vtkUnstructuredGrid>& grid, double value, const char* arrayName)
    {
        vtkSmartPointer<vtkDoubleArray> scalarArray = vtkSmartPointer<vtkDoubleArray>::New();
        //scalarArray->SetNumberOfComponents(1);
        scalarArray->SetName(arrayName);
        scalarArray->FillComponent(0, value);
        vtkSmartPointer<vtkPointData> pointData = grid->GetPointData();
        pointData->AddArray(scalarArray);
    }

    void UniqueValuesPrinter::printUniqueValues() const
    {
        std::cout << "Unique values in " << arrayName << ":" << std::endl;
        std::set<std::string> uniqueValues;
        for (vtkIdType i = 0; i < vtkArray->GetNumberOfTuples(); ++i)
        {
            std::string value;
            if (vtkIntArray* intArray = vtkIntArray::SafeDownCast(vtkArray))
            {
                value = std::to_string(intArray->GetValue(i));
            }
            else if (vtkDoubleArray* doubleArray = vtkDoubleArray::SafeDownCast(vtkArray))
            {
                value = std::to_string(doubleArray->GetValue(i));
            }
            else
            {
                // Handle other array types as needed
                value = "UnknownType";
            }
            uniqueValues.insert(value);
        }
        std::cout << "<";
        bool firstValue = true;
        for (const auto& uniqueValue : uniqueValues)
        {
            if (!firstValue) {
                std::cout << ", ";
            }
            std::cout << uniqueValue;
            firstValue = false;
        }
        std::cout << ">" << std::endl;
    }

}// namespace HCTTIEXP