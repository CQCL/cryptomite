add_library(trevisan trevisan.cpp irreducible_poly.cpp ntt.cpp bigntt.cpp)

target_include_directories(trevisan PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})

set_property(TARGET trevisan PROPERTY POSITION_INDEPENDENT_CODE ON)
