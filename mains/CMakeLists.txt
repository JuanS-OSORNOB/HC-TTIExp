#add the executable target named HelloWorld
add_executable(HCTTIExp hcttiexp.cpp)
target_link_libraries(HCTTIExp PRIVATE ${VTK_LIBRARIES} basic fluid_properties media_properties simulation thermal_effects visualization)