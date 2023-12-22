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

    void mediaproperties::generategrid(){
        Triangulation<2> triangulation;
        GridGenerator::subdivided_hyper_rectangle(
        triangulation,
        {10, 5}, /* repetitions */
        Point<2>(0, 0), /* lower left corner */
        Point<2>(10, 5) /* upper right corner */
        );
        triangulation.refine_global(2);  // Refine the mesh globally (example value)
        //Output the mesh
        std::ofstream out("mesh.vtk");
        GridOut grid_out;
        grid_out.write_vtk(triangulation, out);

    }
    
    



}