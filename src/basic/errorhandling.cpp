#include <HCTTIExpProjConfig.h>
#include <basic/errorhandling.h>
#include <iostream>
void print_version()
{
    std::cout << "Project version is: " << HCTTIExpProj_VERSION_MAJOR << "." << HCTTIExpProj_VERSION_MINOR << std::endl;
}

Errorhandler::Errorhandler(){};
Errorhandler::~Errorhandler(){};