Introduction
============
Random numbers, or equivalently random bits, are a vital ingredient in numerous cryptographic and scientific applications. For example, in the former, the one-time-pad depends upon a secret random bit string to provide security and in the latter, Monte Carlo simulations require random numbers to ensure meaningful results.

In all of these applications it is best to use random numbers that are perfectly random – that is, random numbers (or bits) that allow no additional information about their underlying distribution to an unbounded physical observer before generation
i.e. numbers that are equally probable to an unbounded observer who only obeys the laws of physics.

Despite the widespread need for so-called perfect random numbers, it is hard, if not impossible to generate them directly.

Software and classical physical process (so-called True) random number generators (RNGs) are based o
n computational hardness assumptions.
Consequently, when considering a computationally-unbounded physical observer, these random number ge
nerators are predictable and not sufficient.

Quantum random number generators (QRNG) aim to solve this problem by exploiting the probabilistic na
ture of measurement outcomes in quantum mechanics.
In the idealized case – exploiting this effect gives our desired resource: perfect random numbers.
Unfortunately, there is a disparity between the theory and what is experimentally possible, meaning
that isolating quantum effects is difficult if not unachievable.
Imperfections in devices potentially allow an unbounded physical observer to attain additional infor
mation about the output random numbers.
For example, it is tough to guarantee there are no memory e.g. memory in photon detectors could allo
w for exploitable correlations in the output random bits.
More recently, a class of QRNG known as device-independent quantum random number generators (DIQRNG)
, were introduced.
