"""
This is a module.
"""
from __future__ import annotations

__all__ = ['Trevisan']

from math import ceil, log, log2

from cryptomite import _cryptomite


class Trevisan:
    """Trevisan extractor based on [Trev2001]_ and [Mauer2012]_. """
    def __init__(self, n: int, k: float, max_eps: float):
        """Create a Trevisan Extractor.

        The extractor accepts `n` input bits of min-entropy `k` and `d`
        seed bits and outputs `m` bits with total worst case error of
        `max_eps`. The parameters for the weak designs and 1-bit
        extractors are computed from `n`, `k`, and `max_eps`. To use
        the Trevisan extractor, provide `n`, `k` and `max_eps` and call
        the method `get_seed_length()` to get the required seed length.

        Parameters
        ----------
            n : int
                The number of input bits.
            k : float
                The amount of min-entropy in the input bits.
            max_eps : float
                The total worst case error.
        """
        self.config = _cryptomite.TrevisanConfig(n, k, max_eps)
        self.ext = _cryptomite.Trevisan(self.config)

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

    @staticmethod
    def from_params(
            seed_length: int,
            input_length: int,
            seed_entropy: int,
            input_entropy: int,
            error: int) -> Trevisan:
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
        Trevisan
            The Trevisan extractor.
        """
        if error > 0:
            raise Exception('Cannot extract with these parameters. '
                            'Error must be < 0.')
        t = 2 * ceil(log2(input_length) + 1
                     - 2 * error)
        r = 1
        if seed_length <= seed_entropy:
            output_length = input_entropy + 4 * error - 6
            l = max(1, ceil((log(output_length - r) - log(t - r))
                            / (log(r) - log(r-1))))
            if seed_length > (l + 1) * t**2:
                seed_length = (l + 1) * t**2
            if seed_length < (l + 1) * t**2:
                raise Exception('Cannot extract with these parameters. '
                                'Increase seed length.')
        if seed_length > seed_entropy:
            diff = seed_length - seed_entropy
            output_length = input_entropy + 4 * error - 6 - 4 * diff
            l = max(1, ceil((log(output_length - r) - log(t - r))
                            / (log(r) - log(r-1))))
            if seed_length > (l + 1) * t**2:
                seed_length = (l + 1) * t**2
            if seed_length < (l + 1) * t**2:
                raise Exception('Cannot extract with these parameters. '
                                'Increase seed length.')
        return Trevisan(n=input_length, m=output_length)
