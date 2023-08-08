cmake_minimum_required(VERSION 3.22.1)

project(cryptomite)

include(CTest)

set(CMAKE_CXX_STANDARD 20)

add_subdirectory(src)

add_subdirectory(cryptomite)

if(BUILD_TESTING)
    add_subdirectory(test)
endif()
