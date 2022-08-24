#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <ntt.cpp>
#include <trevisan.cpp>


namespace py = pybind11;

// PYBIND11_MAKE_OPAQUE(std::vector<int>);

PYBIND11_MODULE(_extlib, m) {
    // optional module docstring
    m.doc() = "C++ Implementation of Randomness Extractors";

    py::class_<TrevisanConfig>(m, "TrevisanConfig")
        .def(py::init<int, int, double>())
        .def_readonly("n", &TrevisanConfig::n)
        .def_readonly("m", &TrevisanConfig::m)
        .def_readonly("t", &TrevisanConfig::t)
        .def_readonly("l", &TrevisanConfig::l);

    py::class_<Trevisan>(m, "Trevisan")
        .def(py::init<TrevisanConfig>())
        .def("get_seed_length", &Trevisan::get_seed_length)
        .def("load_source", &Trevisan::load_source)
        .def("extract_bit", &Trevisan::extract_bit);

    py::class_<NTT>(m, "NTT")
        .def(py::init<int>())
        .def("ntt", &NTT::ntt);
}
