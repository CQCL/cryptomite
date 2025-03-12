"""
The Dodis et al. extractor [Dodis2004]_ takes two equal length inputs,
each of length `n = n_1 = n_2'. This implementation is based on the
improved cyclic shift matrices construction from [For2020]_, which
requires n to be prime with primitive root 2.
"""
from __future__ import annotations

from math import floor, log2
from typing import cast

from cryptomite.utils import BitsT, closest_na_set, conv, log_2

__all__ = ['Dodis']


class Dodis:
    """
    Dodis et al. extractor [Dodis2004]_, with implementation
    based on [For2020, For2024]_.
    """
    def __init__(self, n: int, m: int):
        """
        Initialize a Dodis extractor.

        Parameters
        ----------
        n : int
            The length of the first input (in bits).
            **Note:** n must be prime with primitive root 2.
        m : int
            The length of the extractor output (in bits).
        """
        self.n, self.m = n, m

    def extract(self, input1: BitsT, input2: BitsT) -> BitsT:
        """
        Perform randomness extraction.

        Parameters
        ----------
        input1 : list of bits (0s and 1s)
            The first input (the 'weak input'), consisting of n bits.
        input2 : list of bits (0s and 1s)
            The second input (the '(weak) seed'), consisting of n bits.

        Returns
        -------
        list of bits (0s and 1s)
            The extractor output bits, of length m.
        """
        n, m = self.n, self.m
        assert len(input1) == len(input2) == n
        assert n >= m
        l = log_2(2 * n - 2)
        L = 1 << l
        input1, input2 = list(input1), list(input2)
        input1 = input1[0:1] + input1[1:][::-1] + [0] * (L - n)
        input2 = input2 + [0] * (L - len(input2))
        conv_output = conv(l, input1, input2)
        output: BitsT = cast(BitsT, [
            (conv_output[i] + conv_output[i + n]) & 1 for i in range(m)])
        return output

    @staticmethod
    def from_params(
            n_1: int,
            k_1: float,
            n_2: int,
            k_2: float,
            log2_error: float,
            q_proof: bool,
            verbose: bool = True) -> Dodis:
        """
        Generate a Dodis et al. extractor with valid parameters
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
        Dodis
            A configured Dodis et al. extractor.

        Raises
        ------
        ValueError
            If the output length is non-positive.

        Notes
        -----
        - If n is not prime with primitive root 2, the function
          selects the closest prime with primitive root 2 and
          adjusts the other parameters accordingly.
        """
        assert log2_error <= 0

        # Find the closest prime with primitive root 2
        # to the average of input lengths.
        n_adjusted = closest_na_set((n_1 + n_2) // 2)

        # Adjust min-entropy values if input lengths exceed the
        # computed prime with primitive root 2.
        k_1_adjusted = k_1 - max(0, n_1 - n_adjusted)
        k_2_adjusted = k_2 - max(0, n_2 - n_adjusted)

        # Compute the output length based on entropy constraints and
        # extraction error.
        if q_proof:
            m = floor(0.2 * (k_1_adjusted + (k_2_adjusted
                      - n_adjusted) + 8 * log2_error
                      + 9 - 4 * log2(3)))
        else:
            m = floor(k_1 + (k_2 - n_adjusted)
                      + 1 + 2 * log2_error)

        # Ensure the output length is valid.
        if m <= 0:
            raise ValueError(
                'Cannot extract with these parameters. '
                'Increase k_1, k_2, or log2_error.'
            )

        # Print parameter details (if verbose).
        if verbose:
            print(
                f'--- New Dodis et al. Extractor Parameters ---\n'
                f'Input Length 1 (n_1): {n_adjusted}, '
                f'Min Entropy of Input 1 (k_1): {k_1_adjusted}, '
                f'Input Length 2 (n_2): {n_adjusted}, '
                f'Min Entropy of Input 2 (k_2): {k_2_adjusted}, '
                f'Output Length (m): {m}, '
                f'Extraction Error (log2_error): {log2_error}. '
            )
            print("""Adjust the length of the input
                  and (weak) seed accordingly.""")
        return Dodis(n_adjusted, m)
