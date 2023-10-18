cmake_minimum_required(VERSION 3.10)
#Set the project name
project(HCTTIExpProj VERSION 1.0)
#Specify the C++ standard and use the cmake_cxx_standard variable
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED TRUE)
#Export configuration to source code
configure_file(cmake/HCTTIExpProjConfig.h.in HCTTIExpProjConfig.h)
#Add libraries
add_subdirectory(src/basic)
#Add the executables
option(HCTTIExp_WITH_EXECUTABLES "Compile mains" ON)
if(HCTTIExp_WITH_EXECUTABLES)
    message(STATUS "Configuring HC-TTIExp with executables")
    add_subdirectory(mains)
endif()
