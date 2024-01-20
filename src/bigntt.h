#pragma once

#include <cstdint>
#include <vector>

class BigNTT {
  private:
    /** Sequence length (power of 2) */
    uint64_t L;

    /** Inverse of L mod p */
    uint64_t Linv;

    /**
     * Powers 1, r, r^2, ..., r^(L/2-1) mod p, where r is a primitive L'th
     * root of unity mod p
     */
    std::vector<uint64_t> R;

    /**
     * Inverse powers 1, r^{-1}, r^{-2}, ..., r{-^(L/2-1)} mod p
     */
    std::vector<uint64_t> Rinv;

    /**
     * Lookup table for bit reversals
     */
    std::vector<uint64_t> revbits;

  public:
    explicit BigNTT(unsigned l);

    std::vector<uint64_t> ntt(const std::vector<uint64_t> &x, bool inverse);

    std::vector<uint64_t> mul_vec(const std::vector<uint64_t> &a, const std::vector<uint64_t> &b);
    std::vector<uint64_t> conv(const std::vector<uint64_t> &a, const std::vector<uint64_t> &b);
};
