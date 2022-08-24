#include <vector>

#define P ((3u<<30) + 1)
#define G 5 // primitive root mod P

uint32_t add(uint32_t a, uint32_t b) {
    uint64_t c = a;
    c += b;
    uint64_t d = c - P;
    uint64_t e = d >> 32;
    return (c&e) | (d&~e);
}

/**
 * Subtraction: a-b mod P
 *
 * @pre a,b < P
 */
static uint32_t sub(uint32_t a, uint32_t b) {
    uint64_t c = a;
    c -= b;
    uint64_t d = c + P;
    uint64_t e = c >> 32;
    return (c&~e) | (d&e);
}

uint32_t mul(uint32_t a, uint32_t b) {
    uint64_t n = a; n*= b;
    return n % P;
}

/**
 * Modular exponentiation: a^e mod P
 */
static uint32_t modexp(uint32_t a, uint32_t e) {
    // e is not secret, no need to make constant time
    uint32_t r = 1;
    while (e) {
        if (e&1) {
            r = mul(r, a);
        }
        e >>= 1;
        a = mul(a, a);
    }
    return r;
}

/**
 * Reverse the bits of x (an l-bit number)
 */
static uint32_t reverse_bits(unsigned l, uint32_t x) {
    uint32_t y = 0;
    while (l) {
        l--;
        y |= ((x&1) << l);
        x >>= 1;
    }
    return y;
}


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
    NTT(unsigned l) : L(1<<l) {
        if (l < 1 || l > 30) {
            throw "Must have 1 <= l <= 30.";
        }

        Linv = modexp(L, P-2);

        uint32_t half_L = L/2;

        R = std::vector<uint32_t>(half_L);
        Rinv = std::vector<uint32_t>(half_L);
        revbits = std::vector<uint32_t>(L);

        uint32_t r = modexp(G, (P - 1) >> l); // primitive L'th root of unity

        {
            {
                uint64_t t = 1;
                for (uint32_t i = 0; i < half_L; i++) {
                    R[i] = t;
                    t = mul(t, r);
                }
            }

            {
                // r^(L/2) = -1
                uint32_t t = P - 1;
                for (uint32_t i = 1; i <= half_L; i++) {
                    t = mul(t, r);
                    Rinv[half_L - i] = t;
                }
            }
        }

        for (uint32_t i = 0; i < L; i++) {
            revbits[i] = reverse_bits(l, i);
        }

    }

    std::vector<uint32_t> ntt(const std::vector<uint32_t> x, bool inverse) {
        const std::vector<uint32_t>& U = inverse ? Rinv : R;

        std::vector<uint32_t> y(L, 0);

        // Bit inversion
        for (uint32_t i = 0; i < L; i++) {
            y[revbits[i]] = x[i];
        }

        // Main loop
        for (
            uint32_t h = 2, k = 1, u = L/2;
            h <= L;
            k = h, h <<= 1, u >>= 1)
        {
            for (uint32_t i = 0; i < L; i += h) {
                for (uint32_t j = 0, v = 0; j < k; j++, v += u) {
                    uint32_t r = i + j;
                    uint32_t s = r + k;
                    uint32_t a = y[r];
                    uint32_t b = mul(y[s], U[v]);
                    y[r] = add(a, b);
                    y[s] = sub(a, b);
                }
            }
        }

        // Normalization for inverse
        if (inverse) {
            for (uint32_t i = 0; i < L; i++) {
                y[i] = mul(Linv, y[i]);
            }
        }
        return y;
    }
};