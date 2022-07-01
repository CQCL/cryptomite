"""
This is a module.
"""
from __future__ import annotations

from typing import Tuple, List
from math import sqrt

__all__ = ["is_prime", "prime_facto", "na_set"]


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


def prime_facto(n: int) -> Tuple[List[int], List[int]]:
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
