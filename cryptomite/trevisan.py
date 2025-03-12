"""
The Trevisan extractor [Trev2001]_ takes an input of `n_1' bits and
a seed of `n_2 = O(log n_1)' bits.
This implementation is based on the implementation in [Mauer2012]_
and [For2024]_.
"""
from __future__ import annotations

__all__ = ['Trevisan']

from cryptomite import _cryptomite


class Trevisan:
    """
    Trevisan extractor [Trev2001]_ with implementation
    based on [Mauer2012]_ and [For2024]_.
    """
    def __init__(self, n: int, k: float, error: float):
        """Initialize a Trevisan Extractor.

        Parameters
        ----------
        n : int
            The length of the input bits.
        k : float
            The min-entropy of the input bits.
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
        input1 : list of bits (0s and 1s)
            The first input (the 'weak input'), consisting of n bits.
        input2 : list of bits (0s and 1s)
            The second input (the '(weak) seed').

        Returns
        -------
        list of bits (0s and 1s)
            The extractor output bits, of length m.
        """
        self.ext.load_source(input1, input2)

        m = self.config.m
        bits = []
        for i in range(m):
            bit = self.ext.extract_bit(i)
            bits.append(bit)
        return bits
