cmake_minimum_required(VERSION 3.22.1)

project(cryptomite)

include(CTest)

set(CMAKE_CXX_STANDARD 20)

set(_SKBUILD_FORCE_MSVC FALSE)

add_subdirectory(src)

add_subdirectory(cryptomite)

