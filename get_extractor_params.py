#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 27 12:13:38 2022

@author: cforeman
"""

from typing import Tuple, List
from math import floor, log2, sqrt, exp, ceil

# # # PRELIMINARIES # # #


def is_prime(n: int) -> bool:
    """
    Checks an integer for primality.

    Parameters:
        n (int): integer to check for primality

    Returns:
        bool: Whether n is prime.
    """

    for i in range(2, round(sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True


def prime_facto(n: int) -> Tuple[List[int], List[int]]:
    """
    Defines the factors of the prime numbers used.
    It is required for the later function: na_set.

    Parameters:
        n (int): number to check

    Returns:
        list: Returns factors and powers.
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

    Parameters:
        k (int): number to check is in the set.

    Returns:
        int: This number +1 is in na_set.
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

# # # TWO-SOURCE EXTRACTORS # # #


def get_dodis_parameters(input_length1: int, input_length2: int, entropy1: int,
                         entropy2: int, error: int, q_proof: bool
                         ) -> Tuple:
    """
    Dodis is a 2-source extractor that takes two equal length, independent,
    strings of bits to produce some error-perfect random bits.
    The input_length -1 must be in na_set.
    The entropy inputs are a lower bound on the min-entropy of the
    related input string.
    This function defines the input size and output size for this 2-source
    extractor.

    Parameters:
        input_length1 (int): The initial length of input source 1.
        input_length2 (int): The initial length of input source 2.
        entropy1 (int): The min-entropy of input source 1.
        entropy2 (int): The min-entropy of input source 2.
        error (int): The acceptable maximum extractor error, in the
                     form error = b where extractor error = 2 ^ b.
        q_proof (bool): Boolean indicator of whether the extractor parameters
                        should be calculated to account for quantum side
                        information or not.

    Returns:
        int: The length parameter for input source 1.
        int: The length parameter for input source 2.
        int: The length parameter for the output from the extractor.
    """
    input_length = min(input_length1, input_length2)
    input_length = na_set(input_length - 1) + 1
    input_length1, input_length2 = input_length, input_length
    entropy1 -= (input_length1 - input_length)
    entropy2 -= (input_length2 - input_length)
    output_length = floor(entropy1 + entropy2 - input_length + 1 + 2*error)
    if q_proof:     # In the Markox Model
        output_length = floor(0.2 * (entropy1 + entropy2 - input_length)
                              + 8 * error + 9 - 4 * log2(3))
    if output_length <= 0:
        raise Exception('Cannot extract with these parameters.')
    return input_length1, input_length2, output_length


# # # SEEDED EXTRACTORS # # #


def get_hayashi_parameters(seed_length: int, entropy_rate: float,
                           error: int, q_proof: bool) -> Tuple:
    """
    Hayashi is a seeded extractor that takes two differing length, independent,
    strings of bits to produce some error-perfect random bits.
    The seed_length must be in na_set.
    The second input source must be Santha-Vazirani. Namely, all input bits
    have the same min-entropy rate.
    This function defines the input size and output size for this seeded
    extractor.

    Parameters:
        seed_length (int): The initial length of the seed.
        entropy_rate (int): The min-entropy rate of the second input source.
        error (int): The acceptable maximum extractor error, in the
                     form error = b where extractor error = 2 ^ b.
        q_proof (bool): Boolean indicator of whether the extractor parameters
                        should be calculated to account for quantum side
                        information or not.

    Returns:
        int: The length parameter for input seed.
        int: The length parameter for input second source.
        int: The length parameter for the output from the extractor.
    """

    seed_length = na_set(seed_length)
    c = 2
    while log2(c-1) + (-(seed_length/2) * (1 + c * (entropy_rate - 1))
                       ) <= error:
        c += 1
    c -= 1
    output_length = (c - 1) * seed_length
    input_length = c * seed_length
    if q_proof:     # In the Markox Model
        output_length = (c - 1) * seed_length
    if output_length <= 0:
        raise Exception('Cannot extract with these parameters.')
    return seed_length, input_length, output_length


def get_toeplitz_parameters(seed_length: int, input_length: int, entropy: int,
                            error: int, q_proof: bool) -> Tuple:
    """
    Toeplitz is a seeded extractor that takes two differing length,
    independent, strings of bits to produce some error-perfect random bits.
    The entropy input is a lower bound on the min-entropy of the
    related input string.
    This function defines the input size and output size for this seeded
    extractor.

    Parameters:
        seed_length (int): The initial length of the seed.
        input_length (int): The initial length of second input source.
        entropy (int): The min-entropy of second input source.
        error (int): The acceptable maximum extractor error, in the
                     form error = b where extractor error = 2 ^ b.
        q_proof (bool): Boolean indicator of whether the extractor parameters
                        should be calculated to account for quantum side
                        information or not.

    Returns:
        int: The length parameter for input seed.
        int: The length parameter for input second source.
        int: The length parameter for the output from the extractor.
    """
    output_length = entropy + 2 * error
    while seed_length < output_length + input_length - 1:
        output_length -= 1
    seed_length = output_length + input_length - 1
    if q_proof:     # In the Markox Model
        output_length = output_length
    if output_length <= 0:
        raise Exception('Cannot extract with these parameters.')
    return seed_length, input_length, output_length


def get_trevisan_parameters(seed_length: int, input_length: int, entropy: int,
                            error: int, q_proof: bool) -> Tuple:
    """
    Trevisan is a seeded extractor that takes two differing length,
    independent, strings of bits to produce some error-perfect random bits.
    The entropy input is a lower bound on the min-entropy of the
    related input string.
    This function defines the input size and output size for this seeded
    extractor.
    Note: this function assumes implementation using the block weak design.

    Parameters:
        seed_length (int): The initial length of the seed.
        input_length (int): The initial length of second input source.
        entropy (int): The min-entropy of second input source.
        error (int): The acceptable maximum extractor error, in the
                     form error = b where extractor error = 2 ^ b.
        q_proof (bool): Boolean indicator of whether the extractor parameters
                        should be calculated to account for quantum side
                        information or not.

    Returns:
        int: The length parameter for input seed.
        int: The length parameter for input second source.
        int: The length parameter for the output from the extractor.
    """
    t_req = 2 * ceil(log2(input_length) + 2 * (1 - error))
    x = ceil(log2(t_req))
    t = 2 ** x
    r = 1
    output_length = (entropy - 6 + 4 * error) / r
    a = ceil((log2(output_length - 2 * exp(1)) - log2(
             t - 2 * exp(1)))/(log2(2 * exp(1)) - log2(2 * exp(1) - 1)))
    al = max(1, a)
    while seed_length < (al + 1) * t**2:
        x -= 1
        t = 2 ** x
        pen = input_length - floor(log2(0.5 * t - (2 * (1 - error))))
        input_length -= pen
        entropy -= pen
        output_length = (entropy - 6 + 4 * error) / r
        a = ceil((log2(output_length - 2 * exp(1)) - log2(
                 t - 2 * exp(1)))/(log2(2 * exp(1)) - log2(2 * exp(1) - 1)))
        al = max(1, a)
    seed_length = (al + 1) * t**2
    if q_proof:
        x = 0
    if output_length <= 0:
        raise Exception('Cannot extract with these parameters.')
    return seed_length, input_length, int(output_length)
