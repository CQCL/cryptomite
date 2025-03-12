"""
The Toeplitz extractor takes an input of `n_1' bits and
a (weak) seed of `n_2 = n_1 + m - 1' bits, where `m' is output length.
This implementation is based on the efficient implementation
presented in [For2024]_.
"""
from __future__ import annotations

from math import floor
from typing import cast

from cryptomite.utils import BitT, BitsT, conv, log_2

__all__ = ['Toeplitz']


class Toeplitz:
    """
    Toeplitz extractor with implementation
    based on [For2024]_.
    """
    def __init__(self, n_1: int, m: int):
        """
        Initialize a Toeplitz extractor.

        Parameters
        ----------
        n_1 : int
            The length of the first input (in bits).
        m : int
            The length of the extractor output (in bits).
        """
        self.n_1, self.m = n_1, m

    def extract(self, input1: BitsT, input2: BitsT) -> BitsT:
        """
        Perform randomness extraction.

        Parameters
        ----------
        input1 : list of bits (0s and 1s)
            The first input (the 'weak input'), consisting of n_1 bits.
        input2 : list of bits (0s and 1s)
            The second input (the '(weak) seed'), consisting
            of n_2 = n_1 + m - 1 bits.

        Returns
        -------
        list of bits (0s and 1s)
            The extractor output bits, of length m.
        """
        n_1, m = self.n_1, self.m
        assert len(input1) == n_1
        assert len(input2) == n_1 + m - 1
        assert n_1 >= m
        l = log_2(2 * n_1)
        L = 1 << l
        input1, input2 = list(input1), list(input2)
        input1 = input1 + [0] * (L - n_1)
        input2 = input2[:m] + [0] * (L - (m + n_1 - 1)) + input2[m:]
        conv_output = conv(l, input1, input2)
        output: BitsT = [cast(BitT, x & 1) for x in conv_output[:m]]
        return output

    @staticmethod
    def from_params(
            n_1: int,
            k_1: float,
            n_2: int,
            k_2: float,
            log2_error: float,
            q_proof: bool,
            verbose: bool = True) -> Toeplitz:
        """
        Generate a Toeplitz extractor with valid parameters
        based on input constraints.

        Parameters
        ----------
        n_1 : int
            The length of the first input (in bits).
        k_1 : float
            The min-entropy of the first input.
        n_2 : int
            The length of the second input (in bits).
        k_2 : float
            The min-entropy of the second input.
        log2_error : float
            The logarithm (base 2) of the acceptable extractor error.
            Must be negative, as the extractor error is 2^log2_error.
        q_proof : bool
            If True, adjusts parameters to ensure quantum-proof extraction
            in the Markov and product sources models (see [For2024]_).
        verbose : bool
            If True, prints the parameters used for extraction (default: True).

        Returns
        -------
        Toeplitz
            A configured Toeplitz extractor.

        Raises
        ------
        ValueError
            If the length of the first source is great than or equal to
            that of the second.
        ValueError
            If the output length is non-positive.

        Notes
        -----
        - For this extractor, the output length remains the same when it is
          classical-proof, quantum-proof in the product sources model, and
          quantum-proof in the Markov model (see [For2024]_).
        """
        assert log2_error <= 0

        # Ensure the second input is longer than the first.
        if n_2 <= n_1:
            raise ValueError(
                'The second input must be longer than the first.'
                'Re-order the inputs or increase n_2.'
            )

        n_2_adjusted = n_2
        k_2_adjusted = k_2

        if q_proof:
            m_max = floor(k_1 + (k_2 - n_2) + 2 * log2_error)
        else:
            m_max = floor(k_1 + (k_2 - n_2) + 2 * log2_error)

        # Compute the output length.
        if n_2 > n_1 + m_max - 1:
            n_2_adjusted = n_1 + m_max - 1
            m = m_max
        if n_2 < n_1 + m_max - 1:
            m = n_2 - n_1 + 1

        # Ensure the output length is valid.
        if m <= 0:
            raise ValueError(
                'Cannot extract with these parameters. '
                'Increase k_1, k_2, or log2_error.'
            )

        # Adjust the relevant parameters.
        n_2_adjusted = n_1 + m - 1
        k_2_adjusted = k_2 - max(0, n_2 - n_2_adjusted)

        # Print parameter details (if verbose).
        if verbose:
            print(
                f'--- New Circulant Extractor Parameters ---\n'
                f'Input Length 1 (n_1): {n_1}, '
                f'Min Entropy of Input 1 (k_1): {k_1}, '
                f'Input Length 2 (n_2): {n_2_adjusted}, '
                f'Min Entropy of Input 2 (k_2): {k_2_adjusted}, '
                f'Output Length (m): {m}, '
                f'Extraction Error (log2_error): {log2_error}. '
            )
            print("""Adjust the length of the input
                  and (weak) seed accordingly.""")

        return Toeplitz(n_1, m)
