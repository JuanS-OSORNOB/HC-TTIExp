##
#  CMake script for HCTTIExp
##

# Set the name of the project and target:
set(TARGET "HCTTIExpProj")
#------------------------------------------------------------------------------------------------
# Options of the HCTTIExp project 
#------------------------------------------------------------------------------------------------
cmake_minimum_required(VERSION 3.10)

#Set the project name
project(${TARGET} VERSION 1.0)

#Specify the C++ standard and use the cmake_cxx_standard variable
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED TRUE)

#------------------------------------------------------------------------------------------------
# Set a default build type if none is specified
#if(NOT CMAKE_BUILD_TYPE)
#    set(CMAKE_BUILD_TYPE Release)
#endif()

# Adding Release mode
ADD_CUSTOM_TARGET(release
COMMAND ${CMAKE_COMMAND} -DCMAKE_BUILD_TYPE=Release ${CMAKE_SOURCE_DIR}
COMMAND ${CMAKE_COMMAND} --build ${CMAKE_BINARY_DIR} --target all
COMMENT "Switch CMAKE_BUILD_TYPE to Release"
VERBATIM
)
set(CMAKE_CXX_FLAGS_RELEASE "-O3 -DNDEBUG")

# Adding Debug mode
ADD_CUSTOM_TARGET(debug
    COMMAND ${CMAKE_COMMAND} -DCMAKE_BUILD_TYPE=Debug ${CMAKE_SOURCE_DIR}
    COMMAND ${CMAKE_COMMAND} --build ${CMAKE_BINARY_DIR} --target all
    COMMENT "Switch CMAKE_BUILD_TYPE to Debug"
    VERBATIM
)
set(CMAKE_CXX_FLAGS_DEBUG "-g -O0")

# Adding DebugRelease mode
ADD_CUSTOM_TARGET(debugrelease
    COMMAND ${CMAKE_COMMAND} -DCMAKE_BUILD_TYPE=DebugRelease ${CMAKE_SOURCE_DIR}
    COMMAND ${CMAKE_COMMAND} --build ${CMAKE_BINARY_DIR} --target all
    COMMENT "Switch CMAKE_BUILD_TYPE to DebugRelease"
    VERBATIM
)

#------------------------------------------------------------------------------------------------
#Export configuration to source code
configure_file(cmake/HCTTIExpProjConfig.h.in HCTTIExpProjConfig.h)

#------------------------------------------------------------------------------------------------
#find_package(Boost 1.74.0 REQUIRED COMPONENTS system thread)
#if(${Boost_FOUND})
#  message(STATUS "Found Boost at ${Boost_DIR}")
#else()
#  message(FATAL_ERROR "Boost not found")
#endif()
# Finding Deal.II library
find_package(deal.II 9.4.1 REQUIRED HINTS ${DEAL_II_DIR} ../ ../../ $ENV{DEAL_II_DIR})
if(${deal.II_FOUND})
  message(STATUS "Found Deal.II version ${DEAL_II_PACKAGE_VERSION}. Using Deal.II install directory = ${deal.II_DIR}")
  deal_ii_initialize_cached_variables()
else()
  message(FATAL_ERROR "\n *** Could not locate a (sufficiently recent) version of deal.II. ***\n\n You may want to either pass a flag -DDEAL_II_DIR=/path/to/deal.II to cmake\n or set an environment variable \"DEAL_II_DIR\" that contains this path.")
endif()
  
#------------------------------------------------------------------------------------------------
# Finding the VTK library
find_package(VTK REQUIRED COMPONENTS CommonCore CommonDataModel IOXML)
#include(${VTK_USE_FILE})

if(VTK_FOUND)
  message(STATUS "Found VTK version ${VTK_VERSION}. Using VTK install directory = ${VTK_DIR}")
  #message(STATUS "VTK Libraries: " ${VTK_LIBRARIES})
else()
  message(FATAL_ERROR "FATAL ERROR. VTK NOT found. Please set VTK_DIR")
endif()

#------------------------------------------------------------------------------------------------
# Finding the Catch2 library
find_package(Catch2 REQUIRED)

#------------------------------------------------------------------------------------------------
# Setting the extra libraries
set(EXTRA_LIBS ${EXTRA_LIBS} VTK::CommonCore VTK::CommonDataModel VTK::IOXML)

#------------------------------------------------------------------------------------------------
#Adding project library directories
add_subdirectory(src/basic)
add_subdirectory(src/fluid_properties)
add_subdirectory(src/media_properties)
add_subdirectory(src/simulation)
add_subdirectory(src/thermal_effects)
add_subdirectory(src/visualization)

# Set CMP0079 policy to NEW (to add link libraries to target not built in this directory)
cmake_policy(SET CMP0079 NEW)

#Adding executables
option(HCTTIExp_WITH_EXECUTABLES "Compile mains" ON)
if(HCTTIExp_WITH_EXECUTABLES)
  message(STATUS "Configuring HC-TTIExp with executables")
  add_subdirectory(mains)
  target_link_libraries(HCTTIExp PRIVATE basic fluid_properties media_properties simulation thermal_effects visualization)
endif()

#dealii::dealii

#Adding tests
option(HCTTIExp_WITH_TESTS "Compile tests" ON)
if(HCTTIExp_WITH_TESTS)
  enable_testing()
  message(STATUS "Configuring HC-TTIExp with tests")
  add_subdirectory(tests)
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