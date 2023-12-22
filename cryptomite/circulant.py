"""
Circulant is a seeded extractor that takes an input of n - 1 bits and 
a seed of n bits, where n is prime, to produce some error-perfect random bits.
"""
from __future__ import annotations

from math import floor, log2
from typing import cast

from cryptomite.utils import BitsT, conv, log_2, closest_prime

__all__ = ['Circulant']


class Circulant:
    """ Circulant extractor based on [Foreman23]_. """
    def __init__(self, n: int, m: int):
        """Create a Circulant Extractor.

        Parameters
        ----------
        n : int
            The length of the (weak) seed bits.
            *** This should be prime. ***
        m : int
            The length of the output bits.
        """
        self.n, self.m = n, m

    def extract(self, input1: BitsT, input2: BitsT) -> BitsT:
        """ Extract randomness.

        Parameters
        ----------
        input1 : list of bits
            The first list of bits, the 'input'.
        input2 : list of bits
            The second list of bits, the '(weak) seed'.

        Returns
        -------
        list of bits
            The extracted output.
        """
        n, m = self.n, self.m
        assert len(input1) + 1 == len(input2) == n
        assert n >= m
        l = log_2(2 * n - 2)
        L = 1 << l
        input1.append(0)
        input1, input2 = list(input1), list(input2)
        input1 = input1[0:1] + input1[1:][::-1] + [0] * (L - n)
        input2 = input2 + [0] * (L - len(input2))
        conv_output = conv(l, input1, input2)
        output: BitsT = cast(BitsT, [
            (conv_output[i] + conv_output[i + n]) & 1 for i in range(m)])
        return output

    @staticmethod
    def from_params(
            min_entropy1: int,
            min_entropy2: int,
            log_error: int,
            input_length1: int,
            input_length2: int,
            markov_q_proof: bool,
            verbose: bool = True) -> Circulant:
        """
        Calculate a valid input and output size for this extractor,
        given the initial lengths and min-entropies of the input sources.

        The input_length must be prime with primitive root 2.
        The entropy inputs are a lower bound on the :term:`min-entropy`
        of the related input string.

        Parameters
        ----------
        min_entropy1 : float
            The min-entropy of input source 1, the 'input'.
        min_entropy2 : float
            The min-entropy of input source 2, the '(weak) seed'.
        log_error : float
            The acceptable maximum extractor error, in the
            form error = b where extractor error = :math:`2 ^ b`.
        input_length1 : int
            The initial length of input source 1.
        input_length2 : int
            The initial length of input source 2.
        markov_q_proof : bool
            Boolean indicator of whether the extractor parameters
            should be calculated to account for being quantum-proof
            in the Markov model or not.

        Returns
        -------
        Circulant
            The Circulant extractor.
        """
        if log_error >= 0:
            raise Exception('Cannot extract with these parameters.'
                            'Error must be < 0.')
        input_length = closest_prime((input_length1 + input_length2)//2)
        if input_length1 > input_length - 1:
            min_entropy1 -= input_length1 - input_length
        if input_length2 > input_length:
            min_entropy2 -= input_length2 - input_length
        output_length = floor(min_entropy1 + min_entropy2
                              - input_length + 2 * log_error)
        if markov_q_proof:
            output_length = floor(0.2 * (min_entropy1 + min_entropy2
                                         - input_length)
                                  + 8 * log_error + 8 - 4 * log2(3))
        if output_length <= 0:
            raise Exception('Cannot extract with these parameters. '
                            'Increase min_entropy1 and/or min_entropy2.')
        if verbose:
            print('Adjusted entropy1: ', min_entropy1,
                  'Adjusted entropy2: ', min_entropy2,
                  'Log error: ', log_error,
                  'Input length1: ', input_length - 1,
                  'Input length2: ', input_length,
                  'Output length: ', output_length)
            print('Adjust length of input and (weak) seed accordingly')
        return Circulant(n=input_length, m=output_length)