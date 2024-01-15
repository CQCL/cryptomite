"""
Trevisan is a seeded extractor that takes two differing length,
independent, strings of bits to produce some error-perfect random bits.
"""
from __future__ import annotations

__all__ = ['Trevisan']

from cryptomite import _cryptomite


class Trevisan:
    """Trevisan extractor based on [Trev2001]_ and [Mauer2012]_. """
    def __init__(self, n: int, k: float, error: float):
        """Create a Trevisan Extractor.

        Parameters
        ----------
        n : int
            The length of the input bits.
        k : float
            The total min-entropy of the input bits.
        error : float
            The maximum acceptable extractor error.
        """
        self.config = _cryptomite.TrevisanConfig(n, k, error)
        self.ext = _cryptomite.Trevisan(self.config)

    def extract(self, input1: list[bool], input2: list[bool]) -> list[bool]:
        """
        Extract randomness.

        Parameters
        ----------
        input1 : list of bits
            The first list of bits, the 'input'.
        input2 : list of bits
            The second list of bits, the '(weak) seed'.

        Returns
        -------
        list of bool
            The output bits from the extractor.
        """
        self.ext.load_source(input1, input2)

        m = self.config.m
        bits = []
        for i in range(m):
            bit = self.ext.extract_bit(i)
            bits.append(bit)
        return bits
