#include <HCTTIExpProjConfig.h>
#include <media_properties/mediaproperties.h>

#include <iostream>
#include <fstream>
#include <vector>

#include <deal.II/grid/tria.h>
#include <deal.II/grid/grid_generator.h>
#include <deal.II/grid/manifold_lib.h>
#include <deal.II/grid/grid_out.h>

namespace HCTTIEXP
{
    using namespace dealii;

    void Mediaproperties::generategrid()
    {
        Triangulation<2, 2> triangulation;

        // Define the number of subdivisions in each direction
        std::vector<unsigned int> repetitions = {4, 3};

        // Define the two diagonally opposite corner points
        Point<2> p1(0, 0);
        Point<2> p2(145, 9);

        // Create a subdivided hyperrectangle mesh
        GridGenerator::subdivided_hyper_rectangle(triangulation, repetitions, p1, p2, true);

        // Output the mesh for visualization (optional)
        std::ofstream out("mesh.vtk");
        GridOut grid_out;
        grid_out.write_vtk(triangulation, out);
    }
}
