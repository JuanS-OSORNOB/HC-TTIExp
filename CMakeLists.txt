cmake_minimum_required(VERSION 3.10)

#Set the project name
project(HCTTIExpProj VERSION 1.0)

#Specify the C++ standard and use the cmake_cxx_standard variable
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED TRUE)

#------------------------------------------------------------------------------------------------
# Adding Debug and Release mode 

ADD_CUSTOM_TARGET(debug
COMMAND ${CMAKE_COMMAND} -DCMAKE_BUILD_TYPE=Debug ${CMAKE_SOURCE_DIR}
COMMAND ${CMAKE_COMMAND} --build ${CMAKE_BINARY_DIR} --target all
COMMENT "Switch CMAKE_BUILD_TYPE to Debug"
)

ADD_CUSTOM_TARGET(release
COMMAND ${CMAKE_COMMAND} -DCMAKE_BUILD_TYPE=Release ${CMAKE_SOURCE_DIR}
COMMAND ${CMAKE_COMMAND} --build ${CMAKE_BINARY_DIR} --target all
COMMENT "Switch CMAKE_BUILD_TYPE to Release"
)
#------------------------------------------------------------------------------------------------

#Export configuration to source code
configure_file(cmake/HCTTIExpProjConfig.h.in HCTTIExpProjConfig.h)


#------------------------------------------------------------------------------------------------
# Finding Deal.II library
find_package(deal.II 9.4.1 REQUIRED)
if(${deal.II_FOUND})
  message(STATUS "Found Deal.II version ${DEAL_II_PACKAGE_VERSION}. Using Deal.II install directory = ${deal.II_DIR}")
else()
  message(FATAL_ERROR "\n *** Could not locate a (sufficiently recent) version of deal.II. ***\n\n You may want to either pass a flag -DDEAL_II_DIR=/path/to/deal.II to cmake\n or set an environment variable \"DEAL_II_DIR\" that contains this path.")
endif()
deal_ii_initialize_cached_variables()
  
#------------------------------------------------------------------------------------------------
# Finding the VTK library
  
find_package(VTK REQUIRED)
  #include(${VTK_USE_FILE})
  #message(STATUS "VTK Libraries: " ${VTK_LIBRARIES})
if(VTK_FOUND)
  message(STATUS "Found VTK version ${VTK_VERSION}. Using VTK install directory = ${VTK_DIR}")
  else()
  message(FATAL_ERROR "FATAL ERROR. VTK NOT found. Please set VTK_DIR")
  
endif()

#------------------------------------------------------------------------------------------------
# Finding the Catch2 library
find_package(Catch2 REQUIRED)
#if()

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
  target_link_libraries(HCTTIExp PRIVATE ${DEAL_II_LIBRARIES} ${VTK_LIBRARIES} ${Catch2_INCLUDE_DIRS} basic fluid_properties media_properties simulation thermal_effects visualization)
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