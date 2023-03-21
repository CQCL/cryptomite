include(GNUInstallDirs)

include(FetchContent)
FetchContent_Declare(
  pybind11
  URL https://github.com/pybind/pybind11/archive/refs/tags/v2.10.4.tar.gz
)
FetchContent_MakeAvailable(pybind11)
pybind11_add_module(_cryptomite MODULE pycryptomite.cpp)

target_link_libraries(_cryptomite PUBLIC trevisan)

install(TARGETS _cryptomite DESTINATION .)

set(ignoreMe "${SKBUILD}")
