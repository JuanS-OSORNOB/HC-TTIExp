#include <basic/readwrite.h>
#include <basic/message.h>
#include <thermal_effects/tti.h>
#include <media_properties/mediaproperties.h>
#include <thermal_effects/tti.h>

#include <filesystem>
#include <string>
#include <vector>
#include <iostream>
#include <fstream>

int main() {
    using namespace HCTTIEXP;
    
    hello_world();
    print_version();
    Mediaproperties mediaproperties;
    std::string gridFilename = "/home/juanse/Documents/GitHub/HC-TTIExp/mains/data/CORTE_NS.vtu";
    std::string lithoFilename = "/home/juanse/Documents/GitHub/HC-TTIExp/mains/data/litho_properties_2.txt";
    //std::string outgridFilename = "/home/juanse/Documents/GitHub/HC-TTIExp/mains/data/mod_CORTE_NS.vtu";
    mediaproperties.modifygrid(gridFilename, lithoFilename);
      
    return 0;
}
