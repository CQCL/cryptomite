"""
This is a module.
"""
from __future__ import annotations

__all__ = ["Trevisan"]

from extlib import _extlib


class Trevisan:
    """Trevisan extractor"""
    def __init__(self, n: int, k: float, max_eps: float):
        """Create a Trevisan Extractor.

        The extractor accepts `n` input bits of min-entropy `k` and `d` seed
        bits and outputs `m` bits with total worst case error of `max_eps`.
        The parameters for the weak designs and 1-bit extractors are computed
        from `n`, `k`, and `max_eps`. To use the Trevisan extractor, provide
        `n`, `k` and `max_eps` and call the method `get_seed_length()`
        to get the required seed length.

        Parameters
        ----------
            n : int
                The number of input bits.
            k : float
                The amount of min-entropy in the input bits.
            max_eps : float
                The total worst case error.
        """
        self.config = _extlib.TrevisanConfig(n, k, max_eps)
        self.ext = _extlib.Trevisan(self.config)

    def extract(self, source: list[bool], seed: list[bool]) -> list[bool]:
        """
        Load the source and the seed.

        Parameters
        ----------
        source : list of bool
            The input bits.
        seed : list of bool
            The seed bits.

        Returns
        -------
        list of bool
            The output bits from the extractor.
        """
        self.ext.load_source(source, seed)

        m = self.config.m
        bits = []
        for i in range(m):
            bit = self.ext.extract_bit(i)
            bits.append(bit)
        return bits
