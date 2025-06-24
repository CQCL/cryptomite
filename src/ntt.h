#pragma once

#include <cstdint>
#include <vector>

class NTT {
  private:
    /** Sequence length (power of 2) */
    uint32_t L;

    /** Inverse of L mod p */
    uint32_t Linv;

    /**
     * Powers 1, r, r^2, ..., r^(L/2-1) mod p, where r is a primitive L'th
     * root of unity mod p
     */
    std::vector<uint32_t> R;

    /**
     * Inverse powers 1, r^{-1}, r^{-2}, ..., r{-^(L/2-1)} mod p
     */
    std::vector<uint32_t> Rinv;

    /**
     * Lookup table for bit reversals
     */
    std::vector<uint32_t> revbits;

  public:
    explicit NTT(unsigned l);

    std::vector<uint32_t> ntt(const std::vector<uint32_t> &x, bool inverse, bool plusone = false);

    std::vector<uint32_t> mul_vec(const std::vector<uint32_t> &a, const std::vector<uint32_t> &b);
    std::vector<uint32_t> conv(const std::vector<uint32_t> &a, const std::vector<uint32_t> &b);
    std::vector<uint32_t> conv_and_reduce(const std::vector<uint32_t> &a, const std::vector<uint32_t> &b, uint32_t r, uint32_t s);
    std::pair<std::vector<uint32_t>, std::vector<uint32_t>> raz_iteration(const std::vector<uint32_t> &product, const std::vector<uint32_t> &delta, uint32_t r, uint32_t s);
};
