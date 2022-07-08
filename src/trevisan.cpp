#include <iostream>
#include <fstream>
#include <algorithm>
#include <cmath>
#include <set>
#include "irreducible_poly.hpp"
#include <bitset>

typedef bitset<256> poly_bits;

// Implements ring operations in the Galois field (GF(t))
class GF2Poly {
public:
    // The order of the Galois field `t` must be a power of two. log(t) can
    // be up to 63.
    int log_t;
    poly_bits data, mask, irred_poly;

    GF2Poly(int log_t) : log_t(log_t) {
        if (log_t <= 0 || log_t >= 256 ) {
            cout << "log_t " << log_t << endl;
            throw runtime_error("log_t should be in the range (0, 256).");
        }

        // select irred_poly
        irred_poly = poly_bits();
        vector<int> coeffs = minweight_primpoly_coeffs[log_t];
        for (int coeff : coeffs) {
            irred_poly[coeff] = 1;
        }

        mask = 1ULL << log_t;
    }

    poly_bits poly_mul(poly_bits x, poly_bits y) {
        poly_bits result = poly_bits();
        for (size_t i = 0; i < 256; i++) {
            if (y[i]) {
                result ^= x;
            }
            x <<= 1;
            if (x[log_t]) {
                x ^= irred_poly;
            }
        }

        return result;
    }

    poly_bits poly_add(poly_bits x, poly_bits y) {
        return x ^ y;
    }

    // Evaluates the polynomial at `x` in a linear number of operations
    poly_bits horner_method(vector<poly_bits> &coeffs, poly_bits x) {
        poly_bits res = poly_bits();
        size_t n_coeffs = coeffs.size();
        for (size_t i = 0; i < n_coeffs; i++) {
            poly_bits coeff = coeffs[n_coeffs - i - 1];
            res = poly_mul(res, x);
            res = poly_add(res, coeff);
        }

        return res;
    }
};

// Implements the weak design by Hartman and Raz.
class HRWeakDesign {
private:
    int c, log_t, mask;
    GF2Poly field;

public:
    static constexpr double r = 5.43656365691809; // 2 * e
    int m, t, d;
    
    HRWeakDesign(int m, int log_t) : log_t(log_t), field(log_t), m(m) {
        int log_m = 0;
        while ((1 << log_m) < m) log_m += 1;
        mask = (1 << log_t) - 1;

        t = 1 << log_t;
        d = t * t;

        c = (log_m + log_t - 1) / log_t;
    }
    
    // Returns the ith subset of the HR weak design
    vector<uint64_t> get_s(int i) {
        if (i < 0 || i >= m) {
            cerr << "Index: " << i << ", HR weak design size: " << m << endl;
            throw runtime_error("Index out of bounds for HR weak design.");
        }

        auto alphas = vector<poly_bits>(c);
        for (int j = 0; j < c; j++) {
            alphas[j] = poly_bits((i >> j*log_t) & mask);
        }
        auto s = vector<uint64_t>(t);
        for (int a = 0; a < t; a++) {
            uint64_t b = field.horner_method(alphas, a).to_ullong();
            uint64_t pair = (a << log_t) + b;
            s[a] = pair;
        }

        return s;
    }
};

// Implements the block weak design from Maurer et al.
class BlockWeakDesign {
private:
    vector<int> ms, sum_ms;
    int l;
    HRWeakDesign base;

public:
    static constexpr double r = 1.0;
    int m, d, t;
    int log_t;
    
    BlockWeakDesign(int m, int log_t) 
    : base(max((int) ceil((double) m / HRWeakDesign::r - 1), 1 << log_t), log_t), m(m) {
        double base_r = HRWeakDesign::r;
        t = 1ULL << log_t;
        l = max(1, (int)ceil( (log((double) m-base_r) - log((double) t-base_r)) / (log(base_r) - log(base_r - 1)) ));

        // compute size of subweak designs
        auto ns = vector<double>(l);
        auto sum_ns = vector<double>(l);
        double acc = 0;
        for (int i = 0; i < l; i++) {
            ns[i] = pow(1 - 1/base_r, i) * ((double) m/base_r - 1);
            acc += ns[i];
            sum_ns[i] = ceil(acc);
        }

        // sum_ms[i] stores sum of ms from 0 to i -> sum_ms[0] = 0
        sum_ms.push_back(0);
        for (int i = 0; i < l; i++) {
            ms.push_back(sum_ns[i] - sum_ms.back());
            sum_ms.push_back(ms.back() + sum_ms.back());
        }
        ms.push_back(m - sum_ms.back());
        sum_ms.push_back(ms.back() + sum_ms.back());

        d = (l+1) * t * t;

        // base = HRWeakDesign(max(ms[0], t), log_t);
    }

    // Returns the ith subset of the block weak design.
    vector<uint64_t> get_s(int i) {
        if (i < 0 || i >= m) {
            cerr << "Index: " << i << ", block weak design size: " << m << endl;
            throw runtime_error("Index out of bounds for block weak design.");
        }

        // find correct index using binary search
        int ind = 0;
        int step = 1 << 30;
        while (step > 0) {
            // invariant: sum_ms[ind] <= i
            if (ind + step <= l and sum_ms[ind + step] <= i) {
                ind += step;
            }
            step >>= 1;
        }

        int base_i = i - sum_ms[ind];
        int base_inc = ind * t * t;
        vector<uint64_t> base_s = base.get_s(base_i);
        auto s = vector<uint64_t>();
        for (uint64_t elem : base_s) {
            s.push_back(elem + base_inc);
        }

        return s;
    }
};

// Implements the Reed-Solomon-Hadamard extractor.
class RSHExtractor {
private:
    GF2Poly field;
public:
    int n, l, s;

    RSHExtractor(int n, int l) : field(l), n(n), l(l) {
        s = (n + l - 1) / l;
    }

    poly_bits reed_solomon_step(vector<bool> &r_input, vector<bool> &alpha_bits) {
        // reverse bits to do conversion using big-endian convention
        // Example: 0101 -> 5 instead of 0101 -> 10
        // the coefficients of RS are reversed
        auto coeffs = vector<poly_bits>(s);
        for (size_t i = 0; i < s; i++) {
            for (size_t j = 0; j < l; j++) {
                coeffs[s - i - 1][j] = r_input[i*l + j];
            }
        }

        auto alpha = poly_bits();
        for (size_t i = 0; i < alpha_bits.size(); i++) {
            alpha[i] = alpha_bits[i];
        }
        poly_bits r = field.horner_method(coeffs, alpha);
        return r;
    }

    bool hadamard_step(poly_bits r_bits, vector<bool> beta) {
        bool b = 0;
        for (size_t i = 0; i < r_bits.size(); i++) {
            bool r_bit = r_bits[i], beta_bit = beta[i];
            b ^= r_bit & beta_bit;
        }
        return b;
    }

    bool extract(vector<bool> &r_input, vector<bool> &r_seed) {
        if (r_input.size() != n && r_input.size() != s*l) {
            cerr << "Actual: " << r_input.size() << " Expected: " << n << endl;
            throw runtime_error("Input length doesn't match extractor parameters");
        }
        if (r_seed.size() != 2*l) {
            cerr << "Actual: " << r_seed.size() << " Expected: " << 2*l << endl;
            throw runtime_error("Seed length doesn't match extractor parameters");
        }

        // split seed into two halves, alpha and beta
        auto alpha_bits = vector<bool>(r_seed.begin(), r_seed.begin() + l);
        auto beta_bits = vector<bool>(r_seed.begin() + l, r_seed.end());
        
        // right pad input bits with zeros
        while (r_input.size() < s*l) {
            r_input.push_back(0);
        }
        poly_bits r = reed_solomon_step(r_input, alpha_bits);

        // extract the bits of r
        bool b = hadamard_step(r, beta_bits);
        return b;
    }
};

class TrevisanConfig {
public:
    int m, log_t, l;
    int n, t;
    double max_eps, log_eps;

    TrevisanConfig(int n, int k, double max_eps) : n(n) {
        double r = BlockWeakDesign::r;
        // choose largest m s.t. m*eps <= max_eps
        m = 0;
        int step = 1 << 30;
        double log_max_eps = log2(max_eps);
        while (step > 0) {
            // eps = 2 ** (((m+step)*r - k + 6) / 4)
            double try_log_eps = ((double) (m+step)*r - k + 6) / 4;
            if ((log2(m+step) + try_log_eps) <= log_max_eps) {
                m += step;
                log_eps = try_log_eps;
            }
            step >>= 1;
        }

        // l = ceil(log(n) + 2 * log(2 / eps))
        l = (int) ceil(log2(n) + 2 * (1 - log_eps));
        int t_req = 2*l;
        // make t a power of 2 for weak design
        log_t = (int) ceil(log2(t_req));
        t = 1 << log_t;

        cout << "Trevisan Config:" << endl;
        cout << "max_eps " << max_eps << endl;
        cout << "m " << m << endl;
        cout << "log_t " << log_t << endl;
    }

};

class Trevisan {
private:
    BlockWeakDesign wd;
    RSHExtractor ext;
    vector<bool> source_inp;
    vector<bool> source_seed;
public:
    int n, m, log_t, l;
    int t, k;
    double log_eps;
    bool source_loaded = false;

    Trevisan(TrevisanConfig config) 
    : wd(config.m, config.log_t), ext(config.n, config.l), 
      n(config.n), m(config.m), l(config.l) {};

    int get_seed_length() {
        return wd.d;
    }

    void load_source(vector<bool> &source_inp, vector<bool> &source_seed) {
        if (source_inp.size() != n) {
            cerr << "Actual: " << source_inp.size() << " Expected: " << n << endl;
            throw runtime_error("Input length doesn't match extractor parameters");
        }
        if (source_seed.size() != get_seed_length()){
            cerr << "Actual: " << source_seed.size() << " Expected: " << get_seed_length() << endl;
            throw runtime_error("Seed length doesn't match extractor parameters");
        }
        source_loaded = true;
        this->source_inp = source_inp;
        this->source_seed = source_seed;
    }

    vector<bool> extract() {
        auto bits = vector<bool>(m);
        for (int i = 0; i < m; i++) {
            bits[i] = extract_bit(i);
            cout << bits[i];
        }
        cout << endl;

        return bits;
    }

    bool extract_bit(int i) {
        if (!source_loaded) {
            throw runtime_error("Load source with load_source(input, seed).");
        }

        auto design_set = wd.get_s(i);
        auto selected_bits = vector<bool>(2*l);
        for (int i = 0; i < 2*l; i++) {
            selected_bits[i] = source_seed[design_set[i]];
        }

        bool bit = ext.extract(source_inp, selected_bits);
        return bit;
    }
};