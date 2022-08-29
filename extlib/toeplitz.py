"""
Toeplitz is a seeded extractor that takes two differing length,
independent, strings of bits to produce some error-perfect random bits.
"""
from __future__ import annotations

from extlib.utils import conv, log_2

__all__ = ["Toeplitz"]


class Toeplitz:
    """Toeplitz extractor"""
    def __init__(self):
        """Create a Toeplitz Extractor"""

    def extract(self,
                n: int,
                m: int,
                source1: list[bool],
                source2: list[bool]) -> list[bool]:
        """Extract randomness"""
        assert len(source1) == n
        assert len(source2) == m + n - 1
        assert n >= m
        l = log_2(2 * n)
        L = 1 << l
        source1 = source1 + [0] * (L - n)
        source2 = source2[:m] + [0] * (L - (m + n - 1)) + source2[m:]
        conv_output = conv(l, source1, source2)
        output = [x & 1 for x in conv_output[:m]]
        return output

    @classmethod
    def calc_parameters(seed_length: int, input_length: int, entropy: int,
                            error: int, q_proof: bool) -> tuple:
        """
        Calculate the input size and output size for this seeded extractor.

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
            q_proof (bool): Boolean indicator of whether the extractor
                            parameters should be calculated to account for
                            quantum side information or not.

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
