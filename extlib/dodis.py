"""
Dodis is a 2-source extractor that takes two equal length, independent,
strings of bits to produce some error-perfect random bits.
"""
from __future__ import annotations

from extlib.utils import conv, log_2, na_set

__all__ = ["Dodis"]


class Dodis:
    """Dodis extractor"""
    def __init__(self):
        """Create a Dodis Extractor"""

    def extract(self,
                n: int,
                m: int,
                source1: list[bool],
                source2: list[bool]) -> list[bool]:
        """Extract randomness"""
        assert len(source1) == len(source2) == n
        assert n >= m
        l = log_2(2 * n - 2)
        L = 1 << l
        source1 = source1[0:1] + source1[1:][::-1] + [0] * (L - n)
        source2 = source2 + [0] * (L - len(source2))
        conv_output = conv(l, source1, source2)
        output = [(conv_output[i] + conv_output[i + n]) & 1 for i in range(m)]
        return output

    @classmethod
    def calc_params(input_length1: int, input_length2: int, entropy1: int,
                    entropy2: int, error: int, q_proof: bool
                    ) -> tuple:
        """
        Calculate the input size and output size for this 2-source
        extractor.

        The input_length -1 must be in :py:func:`~.na_set`.
        The entropy inputs are a lower bound on the :term:`min-entropy` of the
        related input string.

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
            int
                The length parameter for input source 1.
            int
                The length parameter for input source 2.
            int
                The length parameter for the output from the extractor.
        """
        input_length = min(input_length1, input_length2)
        input_length = na_set(input_length - 1) + 1
        entropy1 -= input_length1 - input_length
        entropy2 -= input_length2 - input_length
        output_length = floor(entropy1 + entropy2 - input_length + 1 + 2 * error)
        if q_proof:
            output_length = floor(0.2 * (entropy1 + entropy2 - input_length)
                                  + 8 * error + 9 - 4 * log2(3))
        if output_length <= 0:
            raise Exception('Cannot extract with these parameters.')
        return input_length, input_length, output_length
