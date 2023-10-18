#include <iostream>
#include <HCTTIExpProjConfig.h>
#include <basic/message.h>
void hello_world()
{
    std::cout << "Hello world!\n" << std::endl;
}

void print_version()
{
    std::cout << "Project version is: " << HCTTIExpProj_VERSION_MAJOR << "." << HCTTIExpProj_VERSION_MINOR << std::endl;
}