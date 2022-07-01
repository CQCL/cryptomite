"""
Dodis is a 2-source extractor that takes two equal length, independent,
strings of bits to produce some error-perfect random bits.
"""
from __future__ import annotations

from math import floor, log2
from extlib.utils import na_set

__all__ = ["Dodis"]


class Dodis:
    """Dodis extractor"""
    def __init__(self):
        """Create a Dodis Extractor"""

    def extract(self) -> list[bool]:
        """Extract randomness"""

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
