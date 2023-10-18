#First test
add_executable(test_hello test-hello.cpp)
target_link_libraries(test_hello PUBLIC basic)
add_test(NAME test_hello COMMAND test_hello)
#Second test
add_executable(test_version test-version.cpp)
target_link_libraries(test_version PUBLIC basic)
add_test(NAME test_version COMMAND test_version)