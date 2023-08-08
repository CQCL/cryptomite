#pragma once

#include <cstdint>
#include <vector>

std::vector<uint32_t> mul_vec(const std::vector<uint32_t> &a, const std::vector<uint32_t> &b);

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

    std::vector<uint32_t> ntt(const std::vector<uint32_t> &x, bool inverse);
};
