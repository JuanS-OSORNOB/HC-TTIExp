set(target_name visualization)
add_library(${target_name} STATIC "")
target_sources(${target_name}
 PRIVATE "${PROJECT_SOURCE_DIR}/src/visualization/visualization.cpp"
 PRIVATE "${PROJECT_SOURCE_DIR}/include/visualization/visualization.h"
)
target_include_directories(${target_name}
 PUBLIC
 $<BUILD_INTERFACE:${PROJECT_SOURCE_DIR}/include>
 $<BUILD_INTERFACE:${PROJECT_BINARY_DIR}>
 $<INSTALL_INTERFACE:include>
)
deal_ii_setup_target(${target_name})
target_link_libraries(${target_name} ${VTK_LIBRARIES})
#Export the target
export(TARGETS ${target_name} FILE $(PROJECT_BINARY_DIR)/${target_name}_target.cmake)

#Install target library
install(TARGETS ${target_name} EXPORT ${target_name} DESTINATION lib)
#Install target export
install(EXPORT ${target_name} FILE ${target_name}_target.cmake DESTINATION cmake/)
#Install includes
install(DIRECTORY ${PROJECT_SOURCE_DIR}/include/ DESTINATION include/)
#Generated include
install(FILES ${PROJECT_BINARY_DIR}/HCTTIExpProjConfig.h DESTINATION include/)