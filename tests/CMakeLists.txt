# Copy test data to build directory
#The test data lies in the source dir and is not copied into the build folder when constructing binaries
#file(COPY ${CMAKE_CURRENT_SOURCE_DIR}/test_data DESTINATION ${CMAKE_CURRENT_BINARY_DIR})

#First test
add_executable(test_hello test-hello.cpp)
target_link_libraries(test_hello PUBLIC basic)
add_test(NAME test_hello COMMAND test_hello)

#Second test
add_executable(test_version test-version.cpp)
target_link_libraries(test_version PUBLIC basic)
add_test(NAME test_version COMMAND test_version)

#Third test
add_executable(test_readkinetic test-readkinetic.cpp)
target_link_libraries(test_readkinetic PUBLIC basic)
add_test(NAME test_readkinetic COMMAND test_readkinetic)

#Third test
add_executable(test_readlitho test-readlitho.cpp)
target_link_libraries(test_readlitho PUBLIC basic)
add_test(NAME test_readlitho COMMAND test_readlitho)