"""
Toeplitz is a seeded extractor that takes two differing length,
independent, strings of bits to produce some error-perfect random bits.
"""
from __future__ import annotations

from extlib.utils import BitT, conv, log_2

__all__ = ["Toeplitz"]


class Toeplitz:
    """Toeplitz extractor"""
    def __init__(self, n: int, m: int):
        """ Create a Toeplitz Extractor.

        Parameters
        ----------
        n : int
            The input size, also the number of columns in the Toeplitz matrix.
        m : int
            The output size, also the number of rows in the Toeplitz matrix.
        """
        self.n, self.m = n, m

    def extract(self,
                input1: list[BitT],
                input2: list[BitT]) -> list[BitT]:
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
        input1 = input1 + [0] * (L - n)
        input2 = input2[:m] + [0] * (L - (m + n - 1)) + input2[m:]
        conv_output = conv(l, input1, input2)
        output = [x & 1 for x in conv_output[:m]]
        return output

    @classmethod
    def from_params(
            seed_length: int,
            input_length: int,
            entropy: int,
            error: int) -> Toeplitz:
        """
        Calculate the input size and output size for this seeded extractor.

        The entropy input is a lower bound on the min-entropy of the
        related input string.
        This function defines the input size and output size for this seeded
        extractor.

        Parameters
        ----------
        seed_length : int
            The initial length of the seed.
        input_length : int
            The initial length of second input source.
        entropy : int
            The min-entropy of second input source.
        error : int
            The acceptable maximum extractor error, in the form
            error = b where extractor error = 2 ^ b.

        Returns
        -------
        Toeplitz
            The Toeplitz extractor.
        """
        output_length = entropy + 2 * error
        output_length = min(seed_length - input_length + 1,
                            entropy + 2 * error)
        assert seed_length >= output_length + input_length - 1
        if output_length <= 0:
            raise Exception('Cannot extract with these parameters.')
        return Toeplitz(n=input_length, m=output_length)
