#pragma once

#include <bitset>
#include <cstdint>
#include <vector>

typedef std::bitset<256> poly_bits;

// Implements ring operations in the Galois field (GF(t))
class GF2Poly {
  public:
    // The order of the Galois field `t` must be a power of two. log(t) can
    // be up to 63.
    int log_t;
    poly_bits data, mask, irred_poly;

    explicit GF2Poly(int log_t);

    poly_bits poly_mul(poly_bits x, poly_bits y) const;
    static poly_bits poly_add(poly_bits x, poly_bits y);

    // Evaluates the polynomial at `x` in a linear number of operations
    poly_bits horner_method(const std::vector<poly_bits> &coeffs, poly_bits x) const;
};

// Implements the weak design by Hartman and Raz.
class HRWeakDesign {
  private:
    int c, log_t, mask;
    GF2Poly field;

  public:
    static constexpr double r = 5.43656365691809; // 2 * e
    int m, t, d;

    HRWeakDesign(int m, int log_t);

    // Returns the ith subset of the HR weak design
    std::vector<uint64_t> get_s(int i);
};

// Implements the block weak design from Maurer et al.
class BlockWeakDesign {
  private:
    std::vector<int> ms, sum_ms;
    int l;
    HRWeakDesign base;

  public:
    static constexpr double r = 1.0;
    int m, d, t;

    BlockWeakDesign(int m, int log_t);

    // Returns the ith subset of the block weak design.
    std::vector<uint64_t> get_s(int i);
};

// Implements the Reed-Solomon-Hadamard extractor.
class RSHExtractor {
  private:
    GF2Poly field;
  public:
    int n, l, s;

    RSHExtractor(int n, int l);

    poly_bits reed_solomon_step(const std::vector<bool> &r_input, const std::vector<bool> &alpha_bits);

    static bool hadamard_step(poly_bits r_bits, std::vector<bool> beta);

    bool extract(std::vector<bool> &r_input, const std::vector<bool> &r_seed);
};

class TrevisanConfig {
  public:
    int m, log_t, l;
    int n, t;
    double log_eps;

    TrevisanConfig(int n, int k, double max_eps);
};

class Trevisan {
  private:
    BlockWeakDesign wd;
    RSHExtractor ext;
    std::vector<bool> source_inp;
    std::vector<bool> source_seed;
  public:
    int n, m, l;
    bool source_loaded = false;

    explicit Trevisan(TrevisanConfig config);

    int get_seed_length() const;

    void load_source(const std::vector<bool> &source_inp, const std::vector<bool> &source_seed);

    std::vector<bool> extract();
    bool extract_bit(int i);
};
