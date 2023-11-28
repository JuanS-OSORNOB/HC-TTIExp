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
add_subdirectory(src/fluid_properties)
add_subdirectory(src/media_properties)
add_subdirectory(src/simulation)
add_subdirectory(src/thermal_effects)
add_subdirectory(src/visualization)

#Add the executables
option(HCTTIExp_WITH_EXECUTABLES "Compile mains" ON)
if(HCTTIExp_WITH_EXECUTABLES)
    message(STATUS "Configuring HC-TTIExp with executables")
    add_subdirectory(mains)
endif()
#Add tests
option(HCTTIExp_WITH_TESTS "Compile tests" ON)
if()
    enable_testing()
    message(STATUS "Configuring HC-TTIExp with tests")
    add_subdirectory(test)
endif()

#Create package configuration file
include(CMakePackageConfigHelpers)
configure_package_config_file(cmake/HCTTIExpProjConfig.cmake.in HCTTIExpProjConfig.cmake INSTALL_DESTINATION cmake/)

#Install project configuration file
install(FILES ${PROJECT_BINARY_DIR}/HCTTIExpProjConfig.cmake DESTINATION cmake/)

#Configure cpack
if(WIN32)
    set(CPACK_GENERATOR "ZIP")
else()
    set(CPACK_GENERATOR "TGZ")
endif()
#This must always be last!
include(CPack)