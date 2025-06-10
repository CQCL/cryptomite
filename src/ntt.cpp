#include "ntt.h"

#include <stdexcept>
#include <vector>
#include <future>

#define P ((3u<<30) + 1)
#define G 5 // primitive root mod P

uint32_t add(uint32_t a, uint32_t b) {
    uint64_t c = a;
    c += b;
    uint64_t d = c - P;
    uint64_t e = d >> 32;
    // return d if d >= 0 else c
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
    // return c if c >= 0 else d
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

NTT::NTT(unsigned l) : L(1<<l) {
    if (l < 1 || l > 30) {
        throw std::runtime_error("Must have 1 <= l <= 30.");
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

std::vector<uint32_t> NTT::ntt(const std::vector<uint32_t> &x, bool inverse, bool plusone) {
    const std::vector<uint32_t>& U = inverse ? Rinv : R;
    std::vector<uint32_t> y(L, 0);

    // Bit inversion
    y[0] = x[0] ^ plusone;
    for (uint32_t i = 1; i < L; i++) {
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

std::vector<uint32_t> NTT::mul_vec(const std::vector<uint32_t> &a, const std::vector<uint32_t> &b) {
    std::vector<uint32_t> c(a.size());
    for (uint32_t i = 0; i < a.size(); i++) {
        c[i] = mul(a[i], b[i]);
    }
    return c;
}

std::vector<uint32_t> NTT::conv(const std::vector<uint32_t> &a, const std::vector<uint32_t> &b) {
    std::vector<uint32_t> c = mul_vec(ntt(a, false), ntt(b, false));
    return ntt(c, true);
}

std::vector<uint32_t> NTT::conv_and_reduce(const std::vector<uint32_t> &a, const std::vector<uint32_t> &b, uint32_t r, uint32_t s) {
    auto call_ntt = [this](const std::vector<uint32_t> &x, bool inverse){ return ntt(x, inverse); };
    std::future<std::vector<uint32_t>> ntt_a = std::async(std::launch::async, call_ntt, a, false);
    std::future<std::vector<uint32_t>> ntt_b = std::async(std::launch::async, call_ntt, b, false);
    auto finish_and_reduce = [this](const std::vector<uint32_t> &x, const std::vector<uint32_t> &y, uint32_t r, uint32_t s){
        auto out = ntt(mul_vec(x, y), true);
        for(int32_t i = r-1; i >= 0; --i) {
            auto red = out[r+i] % 2;
            out[i] = (out[i] % 2) ^ red;
            out[s+i] = (out[s+i] % 2) ^ red;
            out[r+i] = 0;
        }
        return out;
    };

    std::future<std::vector<uint32_t>> conv = std::async(std::launch::async, finish_and_reduce, ntt_a.get(), ntt_b.get(), r, s);
    return conv.get();
}

std::pair<std::vector<uint32_t>, std::vector<uint32_t>> NTT::raz_iteration(const std::vector<uint32_t> &product, const std::vector<uint32_t> &delta, uint32_t r, uint32_t s) {
    auto call_ntt = [this](const std::vector<uint32_t> &x, bool inverse, bool plusone = false){ return ntt(x, inverse, plusone); };
    std::future<std::vector<uint32_t>> ntt_delta = std::async(std::launch::async, call_ntt, delta, false, false);
    std::future<std::vector<uint32_t>> ntt_delta_p1 = std::async(std::launch::async, call_ntt, delta, false, true);
    std::future<std::vector<uint32_t>> ntt_product = std::async(std::launch::async, call_ntt, product, false, false);


    auto finish_and_reduce = [this](const std::vector<uint32_t> &x, const std::vector<uint32_t> &y, uint32_t r, uint32_t s){
        auto out = ntt(mul_vec(x, y), true);
        for(int32_t i = r-1; i >= 0; --i) {
            auto red = out[r+i] % 2;
            out[i] = (out[i] % 2) ^ red;
            out[s+i] = (out[s+i] % 2) ^ red;
            out[r+i] = 0;
        }
        return out;
    };
    std::future<std::vector<uint32_t>> new_product = std::async(std::launch::async, finish_and_reduce, ntt_product.get(), ntt_delta_p1.get(), r, s);

    auto ndelta = ntt_delta.get();
    std::future<std::vector<uint32_t>> new_delta = std::async(std::launch::async, finish_and_reduce, ndelta, ndelta, r, s);

    return {new_product.get(), new_delta.get()};
}
