"""
Toeplitz is a seeded extractor that takes two differing length,
independent, strings of bits to produce some error-perfect random bits.
"""
from __future__ import annotations

from math import floor, log2
from typing import cast

from cryptomite.utils import BitT, BitsT, conv, log_2

__all__ = ['Toeplitz']


class Toeplitz:
    """Toeplitz extractor"""
    def __init__(self, n: int, m: int):
        """Create a Circulant Extractor.

        Parameters
        ----------
        n : int
            The length of the input bits.
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
        assert len(input1) == n
        assert len(input2) == m + n - 1
        assert n >= m
        l = log_2(2 * n)
        L = 1 << l
        input1, input2 = list(input1), list(input2)
        input1 = input1 + [0] * (L - n)
        input2 = input2[:m] + [0] * (L - (m + n - 1)) + input2[m:]
        conv_output = conv(l, input1, input2)
        output: BitsT = [cast(BitT, x & 1) for x in conv_output[:m]]
        return output

    @staticmethod
    def from_params(
            min_entropy1: float,
            min_entropy2: float,
            log2_error: float,
            input_length1: int,
            input_length2: int,
            markov_q_proof: bool,
            verbose: bool = True) -> Toeplitz:
        """
        Calculate a valid input and output size for this extractor,
        given the initial lengths and min-entropies of the input sources
        and generate the associated extractor.

        The min entropy inputs are a lower bound on the
        :term:`min-entropy` of the related input string.

        Parameters
        ----------
        min_entropy1 : float
            The min-entropy of input source 1, the 'input'.
        min_entropy2 : float
            The min-entropy of input source 2, the '(weak) seed'.
        log2_error : float
            The maximum acceptable extractor error, in the
            form error = b where extractor error = :math:`2 ^ b`.
        input_length1 : int
            The initial length of input source.
        input_length2 : int
            The initial length of the (weak) seed.
        markov_q_proof : bool
            Boolean indicator of whether the extractor parameters
            should be calculated to account for being quantum-proof
            in the Markov model or not.

        Returns
        -------
        Toeplitz
            The Toeplitz extractor.
        """
        if log2_error > 0:
            raise Exception("""Cannot extract with these parameters.
                            log2_error must be < 0.""")
        if input_length2 <= input_length1:
            raise Exception("""Cannot extract with these parameters.
                            Increase the seed length (input_length2).
                            The seed must be longer than the input.""")
        if min_entropy2 >= input_length2:
            output_length = min_entropy1 + 2 * log2_error
            if input_length2 >= output_length + input_length1 - 1:
                input_length2 = output_length + input_length1 - 1
            while input_length2 < output_length + input_length1 - 1:
                input_length1 -= 1
                min_entropy1 -= 1
                output_length = min_entropy1 + 2 * log2_error
        if min_entropy2 < input_length2:
            output_length = floor(1/2 * (min_entropy1 + min_entropy2
                                         - input_length1 + 1
                                         + 2 * log2_error))
            while input_length2 > output_length + input_length1 - 1:
                input_length2 -= 1
                min_entropy2 -= 1
                output_length = floor(1/2 * (min_entropy1 + min_entropy2
                                             - input_length1 + 1
                                             + 2 * log2_error))
            if input_length2 < output_length + input_length1 - 1:
                output_length = input_length2 - input_length1 + 1
        if markov_q_proof:
            output_length = floor((1/6) * (min_entropy1 + min_entropy2
                                           - input_length1 + 8 * log2_error
                                           + 9 - 4 * log2(3)))
            while input_length2 > output_length + input_length1 - 1:
                input_length2 -= 1
                min_entropy2 -= 1
                output_length = floor((1/6) * (min_entropy1 + min_entropy2
                                               - input_length1 + 8 * log2_error
                                               + 9 - 4 * log2(3)))
            if input_length2 < output_length + input_length1 - 1:
                output_length = input_length2 - input_length1 + 1
        if output_length <= 0:
            raise Exception("""Cannot extract with these parameters.
                            Increase min_entropy1 and/or min_entropy2
                            and/or log2_error.""")
        if verbose:
            print('Min entropy1: ', min_entropy1,
                  'Min entropy2: ', min_entropy2,
                  'Log error: ', log2_error,
                  'Input length1: ', input_length1,
                  'Input length2: ', input_length2,
                  'Output length: ', output_length)
            print('Adjust length of the input and (weak) seed accordingly')
        return Toeplitz(n=input_length1, m=output_length)
