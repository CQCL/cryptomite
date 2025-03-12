"""
The Circulant extractor [For2024]_ takes an input of `n_1' bits and
a (weak) seed of `n_1 + 1' bits, where `n_1 + 1' is prime.
"""
from __future__ import annotations

from math import floor
from typing import cast

from cryptomite.utils import BitsT, closest_prime, conv, log_2

__all__ = ['Circulant']


class Circulant:
    """
    Circulant extractor based on [For2024]_.
    """
    def __init__(self, n_1: int, m: int):
        """
        Initialize a Circulant extractor.

        Parameters
        ----------
        n_1 : int
            The length of the first input (in bits).
            **Note:** n_1 + 1 must be prime.
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
            of n_2 = n_1 + 1 bits.

        Returns
        -------
        list of bits (0s and 1s)
            The extractor output bits, of length m.
        """
        n_1, m = self.n_1, self.m
        assert len(input1) == len(input2) - 1 == n_1
        assert n_1 >= m
        input1 = input1 + [0]
        n_1 += 1
        input1, input2 = list(input1), list(input2)
        l = log_2(2 * n_1 - 2)
        L = 1 << l
        input1 = input1[0:1] + input1[1:][::-1] + [0] * (L - n_1)
        input2 = input2 + [0] * (L - len(input2))
        conv_output = conv(l, input1, input2)
        output: BitsT = cast(BitsT, [
            (conv_output[i] + conv_output[i + n_1]) & 1 for i in range(m)])
        return output

    @staticmethod
    def from_params(
            n_1: int,
            k_1: float,
            n_2: int,
            k_2: float,
            log2_error: float,
            q_proof: bool,
            verbose: bool = True) -> Circulant:
        """
        Generate a Circulant extractor with valid parameters
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
        Circulant
            A configured Circulant extractor.

        Raises
        ------
        ValueError
            If the output length is non-positive.

        Notes
        -----
        - If n_2 is not prime, the function selects the closest prime and
          adjusts the other parameters accordingly.
        - For this extractor, the output length remains the same when it is
          classical-proof, quantum-proof in the product sources model, and
          quantum-proof in the Markov model (see [For2024]_).
        """
        assert log2_error <= 0

        # Find the closest prime to the average of input lengths.
        n_2_adjusted = closest_prime((n_1 + n_2) // 2)

        # Adjust min-entropy values if input lengths exceed the computed prime.
        k_1_adjusted = k_1 - max(0, n_1 - (n_2_adjusted - 1))
        k_2_adjusted = k_2 - max(0, n_2 - n_2_adjusted)

        # Compute the output length based on entropy constraints and
        # extraction error.
        if q_proof:
            m = floor(k_1_adjusted + (k_2_adjusted - n_2_adjusted)
                      + 2 * log2_error)
        else:
            m = floor(k_1_adjusted + (k_2_adjusted - n_2_adjusted)
                      + 2 * log2_error)

        # Ensure the output length is valid.
        if m <= 0:
            raise ValueError(
                'Cannot extract with these parameters. '
                'Increase k_1, k_2, or log2_error.'
            )

        # Print parameter details (if verbose).
        if verbose:
            print(
                f'--- New Circulant Extractor Parameters ---\n'
                f'Input Length 1 (n_1): {n_2_adjusted-1}, '
                f'Min Entropy of Input 1 (k_1): {k_1_adjusted}, '
                f'Input Length 2 (n_2): {n_2_adjusted}, '
                f'Min Entropy of Input 2 (k_2): {k_2_adjusted}, '
                f'Output Length (m): {m}, '
                f'Extraction Error (log2_error): {log2_error}. '
            )
            print("""Adjust the length of the input
                  and (weak) seed accordingly.""")

        return Circulant(n_2_adjusted - 1, m)
