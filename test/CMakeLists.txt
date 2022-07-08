cmake_minimum_required(VERSION 3.9)
set (CMAKE_CXX_STANDARD 17)
project(trevisan-extractor)
 
# Locate GTest
find_package(GTest REQUIRED)
include_directories(${GTEST_INCLUDE_DIRS})
 
# Link runTests with what we want to test and the GTest and pthread library
add_executable(runTests tests.cpp)
target_link_libraries(runTests ${GTEST_LIBRARIES} pthread trevisan)
