"""
Dodis is a 2-source extractor that takes two equal length, independent,
strings of bits to produce some error-perfect random bits.
"""
from __future__ import annotations

from math import floor, log2
from typing import cast

from cryptomite.utils import BitsT, conv, log_2, na_set

__all__ = ['Dodis']


class Dodis:
    """ Dodis extractor based on [Dodis20]_. """
    def __init__(self, n: int, m: int):
        """Create a Dodis Extractor.

        Parameters
        ----------
        n : int
            The length of the two input bits.
        m : int
            The length of the output bits.
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
        assert len(input1) == len(input2) == n
        assert n >= m
        l = log_2(2 * n - 2)
        L = 1 << l
        input1, input2 = list(input1), list(input2)
        input1 = input1[0:1] + input1[1:][::-1] + [0] * (L - n)
        input2 = input2 + [0] * (L - len(input2))
        conv_output = conv(l, input1, input2)
        output: BitsT = cast(BitsT, [
            (conv_output[i] + conv_output[i + n]) & 1 for i in range(m)])
        return output

    @staticmethod
    def from_params(
            input_length1: int,
            input_length2: int,
            entropy1: int,
            entropy2: int,
            error: int,
            q_proof: bool) -> Dodis:
        """
        Calculate the input size and output size for this 2-source
        extractor.

        The input_length -1 must be in :py:func:`~.na_set`.
        The entropy inputs are a lower bound on the :term:`min-entropy`
        of the related input string.

        Parameters
        ----------
        input_length1 : int
            The initial length of input source 1.
        input_length2 : int
            The initial length of input source 2.
        entropy1 : int
            The min-entropy of input source 1.
        entropy2 : int
            The min-entropy of input source 2.
        error : int
            The acceptable maximum extractor error, in the
            form error = b where extractor error = :math:`2 ^ b`.
        q_proof : bool
            Boolean indicator of whether the extractor parameters
            should be calculated to account for quantum side
            information or not.

        Returns
        -------
        Dodis
            The Dodis extractor.
        """
        if error > 0:
            raise Exception('Cannot extract with these parameters.'
                            'Error must be < 0.')
        input_length = na_set(min(input_length1, input_length2) - 1) + 1
        entropy1 -= input_length1 - input_length
        entropy2 -= input_length2 - input_length
        output_length = floor(
            entropy1 + entropy2 - input_length + 1 + 2 * error)
        if q_proof:
            output_length = floor(0.2 * (entropy1 + entropy2 - input_length)
                                  + 8 * error + 9 - 4 * log2(3))
        if output_length <= 0:
            raise Exception('Cannot extract with these parameters. '
                            'Increase entropy1 and/or entropy2.')
        return Dodis(n=input_length, m=output_length)
