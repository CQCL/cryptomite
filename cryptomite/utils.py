"""
This is a module.
"""
from __future__ import annotations

from math import sqrt
from typing import Literal, Sequence

from cryptomite._cryptomite import NTT, mul_vec

__all__ = ['is_prime', 'prime_facto', 'na_set', 'von_neumann']


BitT = Literal[0, 1]
BitsT = Sequence[BitT]


def log_2(n: int) -> int:
    """ Take the base 2 logarithm of an integer. """
    x = 0
    while n > 0:
        n >>= 1
        x += 1
    return x


def conv(l: int, source1: Sequence[int], source2: Sequence[int]) -> list[int]:
    """
    Perform a cyclic convolution of size 2^l.

    Parameters
    ----------
        l : int
            log_2 of the size of the convolution
        source1: list of int
            first vector
        source2: list of int
            second vector

    Returns
    -------
        list[int] : The convolved output.
    """
    L = 1 << l
    assert len(source1) == len(source2) == L
    ntt = NTT(l)
    ntt_source1 = ntt.ntt(source1, False)
    ntt_source2 = ntt.ntt(source2, False)
    mul_source = mul_vec(ntt_source1, ntt_source2)
    conv_output = ntt.ntt(mul_source, True)
    return conv_output


def is_prime(n: int) -> bool:
    """
    Checks an integer for primality.

    Parameters
    ----------
        n : int
            integer to check for primality

    Returns
    -------
        bool : Whether n is prime.
    """

    for i in range(2, round(sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True


def prime_facto(n: int) -> tuple[list[int], list[int]]:
    """
    Defines the factors of the prime numbers used.
    It is required for the later function: na_set.

    Parameters
    ----------
        n : int
            number to check

    Returns
    -------
        list :
            Returns factors and powers.
    """
    factors = []
    i = 2
    while i <= round(sqrt(n)) + 1:
        if n % i == 0:
            factors.append(i)
            n = n // i
        else:
            i = i + 1
    if n != 1:
        factors.append(n)
    factors2 = [factors[0]]
    powers = [1]
    p = 0
    # this will put 24 = 2 * 2 * 2 * 3 in the form
    # factors=(2,3) and powers=(3,1) for (2^3) * (3^1)
    for i in range(1, len(factors)):
        if factors[i] == factors[i - 1]:
            powers[p] = powers[p] + 1
        if factors[i] != factors[i - 1]:
            # sz = sz + 1
            powers.append(1)
            p = p + 1
            factors2.append(factors[i])

    return factors2, powers


def na_set(k: int) -> int:
    """
    Ensure the number of runs falls within the correct set:
    i.e. that we run enough times.

    Parameters
    ----------
        k : int
            number to check is in the set.

    Returns
    -------
        int :
            This number +1 is in na_set.
    """

    if k % 2 != 0:
        k = k - 1
    stop = False
    while not stop:
        stop = True
        while not is_prime(k + 1):
            k = k - 2
        primes, _ = prime_facto(k)
        for prime in primes:
            if pow(2, k // prime, k + 1) == 1:
                stop = False
                k = k - 2
                break
    return k


def von_neumann(bits: BitsT) -> BitsT:
    """ Extract using Von-Neumann extractor. """
    return [x for x, y in zip(bits[::2], bits[1::2]) if x == y]
