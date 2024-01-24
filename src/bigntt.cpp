#include "bigntt.h"

#include <stdexcept>
#include <vector>

#define P ((9ull<<42) + 1)
#define G 5 // primitive root mod P

uint64_t add(uint64_t a, uint64_t b) {
    uint64_t c = a + b;
    if (c >= P) {
        c -= P;
    }

    return c;
}

/**
 * Subtraction: a-b mod P
 *
 * @pre a,b < P
 */
static uint64_t sub(uint64_t a, uint64_t b) {
    uint64_t c = a - b;
    if (a < b) {
        c += P;
    }

    return c;
}

uint64_t mul(uint64_t a, uint64_t b) {
    // correct if a,b,P < 2^57
    uint64_t c = (double)a * b / P;
    int64_t ans = int64_t(a * b - c * P) % int64_t(P);
    if (ans < 0)
        ans += P;
    return ans;
}

/**
 * Modular exponentiation: a^e mod P
 */
static uint64_t modexp(uint64_t a, uint64_t e) {
    // e is not secret, no need to make constant time
    uint64_t r = 1;
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
static uint64_t reverse_bits(unsigned l, uint64_t x) {
    uint64_t y = 0;
    while (l) {
        l--;
        y |= ((x&1) << l);
        x >>= 1;
    }
    return y;
}

BigNTT::BigNTT(unsigned l) : L(1ll<<l) {
    if (l < 1 || l > 40) {
        throw std::runtime_error("Must have 1 <= l <= 40.");
    }

    Linv = modexp(L, P-2);

    uint64_t half_L = L/2;

    R = std::vector<uint64_t>(half_L);
    Rinv = std::vector<uint64_t>(half_L);
    revbits = std::vector<uint64_t>(L);

    uint64_t r = modexp(G, (P - 1) >> l); // primitive L'th root of unity

    {
        {
            uint64_t t = 1;
            for (uint64_t i = 0; i < half_L; i++) {
                R[i] = t;
                t = mul(t, r);
            }
        }

        {
            // r^(L/2) = -1
            uint64_t t = P - 1;
            for (uint64_t i = 1; i <= half_L; i++) {
                t = mul(t, r);
                Rinv[half_L - i] = t;
            }
        }
    }

    for (uint64_t i = 0; i < L; i++) {
        revbits[i] = reverse_bits(l, i);
    }

}

std::vector<uint64_t> BigNTT::ntt(const std::vector<uint64_t> &x, bool inverse) {
    const std::vector<uint64_t>& U = inverse ? Rinv : R;

    std::vector<uint64_t> y(L, 0);

    // Bit inversion
    for (uint64_t i = 0; i < L; i++) {
        y[revbits[i]] = x[i];
    }

    // Main loop
    for (
        uint64_t h = 2, k = 1, u = L/2;
        h <= L;
        k = h, h <<= 1, u >>= 1)
    {
        for (uint64_t i = 0; i < L; i += h) {
            for (uint64_t j = 0, v = 0; j < k; j++, v += u) {
                uint64_t r = i + j;
                uint64_t s = r + k;
                uint64_t a = y[r];
                uint64_t b = mul(y[s], U[v]);
                y[r] = add(a, b);
                y[s] = sub(a, b);
            }
        }
    }

    // Normalization for inverse
    if (inverse) {
        for (uint64_t i = 0; i < L; i++) {
            y[i] = mul(Linv, y[i]);
        }
    }
    return y;
}

std::vector<uint64_t> BigNTT::mul_vec(const std::vector<uint64_t> &a, const std::vector<uint64_t> &b) {
    std::vector<uint64_t> c(a.size());
    for (uint64_t i = 0; i < a.size(); i++) {
        c[i] = mul(a[i], b[i]);
    }
    return c;
}

std::vector<uint64_t> BigNTT::conv(const std::vector<uint64_t> &a, const std::vector<uint64_t> &b) {
    std::vector<uint64_t> c = mul_vec(ntt(a, false), ntt(b, false));
    return ntt(c, true);
}