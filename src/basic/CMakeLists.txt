#Set the library name
set(target_name basic)
add_library(${target_name} STATIC "")
target_sources(${target_name}
 PRIVATE "${PROJECT_SOURCE_DIR}/src/basic/errorhandling.cpp"
 PRIVATE "${PROJECT_SOURCE_DIR}/include/basic/errorhandling.h"
 PRIVATE "${PROJECT_SOURCE_DIR}/src/basic/logger.cpp"
 PRIVATE "${PROJECT_SOURCE_DIR}/include/basic/logger.h"
 PRIVATE "${PROJECT_SOURCE_DIR}/src/basic/message.cpp"
 PRIVATE "${PROJECT_SOURCE_DIR}/include/basic/message.h"
 PRIVATE "${PROJECT_SOURCE_DIR}/src/basic/readwrite.cpp"
 PRIVATE "${PROJECT_SOURCE_DIR}/include/basic/readwrite.h"
)
target_include_directories(${target_name}
 PUBLIC
 $<BUILD_INTERFACE:${PROJECT_SOURCE_DIR}/include>
 $<BUILD_INTERFACE:${PROJECT_SOURCE_DIR}/src/basic> #Include this library
 $<BUILD_INTERFACE:${PROJECT_BINARY_DIR}>
 $<INSTALL_INTERFACE:include>
)


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