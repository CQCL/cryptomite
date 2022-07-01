"""
Hayashi is a seeded extractor that takes two differing length, independent,
strings of bits to produce some error-perfect random bits.
"""
from __future__ import annotations

from math import log2
from extlib.utils import na_set

__all__ = ["Hayashi"]


class Hayashi:
    """Hayashi extractor"""
    def __init__(self):
        """Create a Hayashi Extractor"""

    def extract(self) -> list[bool]:
        """Extract randomness"""

    @classmethod
    def calc_parameters(seed_length: int, entropy_rate: float,
                           error: int, q_proof: bool) -> tuple:
        """
        Calculate the input size and output size for this seeded extractor.
    
        The seed_length must be in :py:func:`~.na_set`.
        The second input source must be Santha-Vazirani. Namely, all input bits
        have the same :term:`min-entropy` rate.

        Parameters:
            seed_length : int
                The initial length of the seed.
            entropy_rate : int
                The min-entropy rate of the second input source.
            error : int
                The acceptable maximum extractor error, in the
                form error = b where extractor error = 2 ^ b.
            q_proof : bool
                Whether the extractor parameters
                should be calculated to account for quantum side
                information or not.

        Returns:
            int
                The length parameter for input seed.
            int
                The length parameter for input second source.
            int
                The length parameter for the output from the extractor.
        """

        seed_length = na_set(seed_length-2) + 2
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
