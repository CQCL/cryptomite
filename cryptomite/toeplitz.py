"""
Toeplitz is a seeded extractor that takes two differing length,
independent, strings of bits to produce some error-perfect random bits.
"""
from __future__ import annotations

from math import floor
from typing import cast

from cryptomite.utils import BitT, BitsT, conv, log_2

__all__ = ['Toeplitz']


class Toeplitz:
    """Toeplitz extractor"""
    def __init__(self, n: int, m: int):
        """ Create a Toeplitz Extractor.

        Parameters
        ----------
        n : int
            The input size (the number of columns in the matrix).
        m : int
            The output size (the number of rows in the matrix).
        """
        self.n, self.m = n, m

    def extract(self, input1: BitsT, input2: BitsT) -> BitsT:
        """ Extract randomness.

        Parameters
        ----------
        input1 : list of bits
            The first list of bits.
        input2 : list of bits
            The second list of bits.

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
            seed_length: int,
            input_length: int,
            seed_entropy: int,
            input_entropy: int,
            error: int) -> Toeplitz:
        """
        Calculate the input size and output size for this extractor.

        The entropy input is a lower bound on the min-entropy of the
        related input string.
        This function defines the input size and output size for this
        seeded extractor.

        Parameters
        ----------
        seed_length : int
            The initial length of the seed.
        input_length : int
            The initial length of second input source.
        seed_entropy : int
            The min-entropy of the seed.
            If the seed is uniform, this should equal
            seed_length.
        input_entropy : int
            The min-entropy of second input source.
        error : int
            The acceptable maximum extractor error, in the form
            error = b where extractor error = 2 ^ b.

        Returns
        -------
        Toeplitz
            The Toeplitz extractor.
        """
        if error > 0:
            raise Exception('Cannot extract with these parameters. '
                            'Error must be < 0.')
        if seed_length <= input_length:
            raise Exception('Cannot extract with these parameters. '
                            'Increase the seed length. '
                            'The seed must be longer than the input.')
        if seed_entropy >= seed_length:
            output_length = input_entropy + 2 * error
            assert output_length >= 0
            if seed_length > output_length + input_length - 1:
                seed_length = output_length + input_length - 1
            if seed_length < output_length + input_length - 1:
                output_length = seed_length - input_length + 1
        if seed_entropy < seed_length:
            output_length = floor(
                1/3 * (input_entropy - 2 * (input_length - 1
                       - seed_entropy) + 2 * error))
            if seed_length > output_length + input_length - 1:
                if seed_length > output_length + input_length - 1:
                    penalty = 3*(seed_length - output_length
                                 - input_length + 1)
                    output_length = floor(output_length - penalty * 2/3)
                    seed_length = seed_length - penalty
            if seed_length < output_length + input_length - 1:
                seed_length = seed_length - input_length + 1
        assert seed_length == output_length + input_length - 1
        if output_length <= 0:
            raise Exception('Cannot extract with these parameters. '
                            'Increase input_entropy and/or seed_entropy.')
        return Toeplitz(n=input_length, m=output_length)
