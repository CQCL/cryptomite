"""
This is a module.
"""
from __future__ import annotations

__all__ = ['Trevisan']

from math import ceil, exp, floor, log, log2

from cryptomite import _cryptomite


class Trevisan:
    """Trevisan extractor based on [Trev2001]_ and [Mauer2012]_. """
    def __init__(self, n: int, k: float, max_eps: float):
        """Create a Trevisan Extractor.

        The extractor accepts `n` input bits of min-entropy `k` and `d`
        seed bits and outputs `m` bits with total worst case error of
        `max_eps`. The parameters for the weak designs and 1-bit
        extractors are computed from `n`, `k`, and `max_eps`. To use
        the Trevisan extractor, provide `n`, `k` and `max_eps`.

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

    def extract(self, input1: list[bool], input2: list[bool]) -> list[bool]:
        """
        Load the source and the seed.

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

    @staticmethod
    def from_params(
            min_entropy1: float,
            min_entropy2: float,
            log2_error: float,
            input_length1: int,
            input_length2: int,
            markov_q_proof: bool,
            verbose: bool = True) -> Trevisan:
        """
        Calculate a valid input and output size for this extractor,
        given the initial lengths and min-entropies of the input sources
        and generate the associated extractor.

        *** Note: at present, this function (for Trevisan) only supports
        when input_length2 = min_entropy2, i.e. when the seed is
        uniform. ***
        The min entropy inputs are a lower bound on the
        :term:`min-entropy` of the related input string.

        Parameters
        ----------
        min_entropy1 : float
            The min-entropy of input source 1, the 'input'.
        min_entropy2 : float
            The min-entropy of input source 2, the '(weak) seed'.
        log_error : float
            The acceptable maximum extractor error, in the
            form error = b where extractor error = :math:`2 ^ b`.
        input_length1 : int
            The initial length of input source.
        input_length2 : int
            The initial length of the (weak) seed.
        markov_q_proof : bool
            Boolean indicator of whether the extractor parameters
            should be calculated to account for being quantum-proof
            in the Markov model or not.

        Returns
        -------
        Trevisan
            The Trevisan extractor.
        """
        if log2_error > 0:
            raise Exception('''Cannot extract with these parameters.
                            log2_error must be < 0.''')
        if min_entropy2 != input_length2:
            raise Exception('''Cannot calcuate with these parameters.
                            Set min_entropy2 = input_length2.''')
        r = 2 * exp(1)
        m = min_entropy1 + 4 * log2_error - 6
        output_length = floor(min_entropy1 + 4 * log2_error
                              - 4 * log2(m) - 6)
        t = 2 * ceil(log2(input_length1) + 1
                     - 2 * log2_error + 2 * log2(2 * output_length))
        a = max(1, ceil((log(output_length - r) - log(t - r))
                        / (log(r) - log(r-1))))
        if markov_q_proof:
            m = (1/7) * (min_entropy1 + 6 - 6 * log2(3) +
                         12 * log2_error)
            output_length = floor((1/7) * (min_entropy1 + 6 - 6 * log2(3) +
                                           12 * log2_error - 12 * log2(m)))
            t = 2 * ceil(log2(input_length1) + 1
                         - 2 * log2_error + 2 * log2(2 * output_length))
            a = max(1, ceil((log(output_length - r) - log(t - r))
                            / (log(r) - log(r-1))))
        if input_length2 < 4 * a * t**2:
            raise Exception('''Cannot extract with these parameters.
                            Increase input_length2.''')
        input_length2 = 4 * a * t**2
        if verbose:
            print('Min entropy1: ', min_entropy1,
                  'Min entropy2: ', min_entropy2,
                  'Log error: ', log2_error,
                  'Input length1: ', input_length1,
                  'Input length2: ', input_length2,
                  'Output length: ', output_length)
            print('Adjust length of the input and seed accordingly')
        return Trevisan(n=input_length1, m=output_length)
