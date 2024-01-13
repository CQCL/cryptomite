Selecting a Randomness Extractor
================================
In the following, we use the notation :math:`n_1, n_2` to denote the length and :math:`k_1, k_2` to denote the :term:`min-entropy` of 
any first or second input string respectively. Additionally, :math:`m` denotes the length of an output string, :math:`\epsilon` 
the extractor error and :math:`O(.)` denotes the asymptotic behaviour of a function.

:py:class:`.Circulant`
------------------
The Circulant extractor is a :term:`seeded randomness extractor`, meaning that it requires two independent bit 
strings of randomness, where one is already (near-)perfectly random (called a seed). 
It requires the weak input to be of length :math:`n_1 = n_2 - 1`, where the length of the seed :math:`n_2` is prime
and outputs approximately :math:`m \approx k_1 + k_2 - n_1` when considering classical side information or in the quantum product-source model
and :math:`m \approx \frac{1}{5}(k_1 + k_2 - n_1)`.
Our implementation of this extractor has near-linear computational complexity.

This extractor is best suited to scenarios where a seeded extractor is required in both the classical and quantum side information setting.

:py:class:`.Dodis`
------------------
The Dodis extractor is a :term:`2-source randomness extractor`, meaning that it requires two independent bit 
strings of randomness that only 'contain' entropy (as opposed to one or both being fully entropic). 
It requires equal length inputs (:math:`n_1 = n_2`) that are prime with 2 as a primitive root (see :py:func:`.na_set` in glossary) 
and outputs approximately :math:`m \approx k_1 + k_2 - n_1` when considering classical side information and :math:`m \approx \frac{1}{5}(k_1 + k_2 - n_1)`.
Our implementation of this extractor has near-linear computational complexity.

This extractor is best suited to scenarios where a two-source extractor is required, 
or a computationally efficient extractor considering classical side information only (then Dodis can be 
used as a seeded extractor, giving approximately the same output length as Toeplitz, whilst reducing required seed size.)

:py:class:`.Toeplitz`
---------------------
The Toeplitz extractor is a :term:`seeded randomness extractor`, meaning that it requires two independent bit 
strings of randomness, where one is already (near-)perfectly random (called a seed).
It requires a seed length of :math:`n_2 = n_1 + m - 1`
and outputs approximately :math:`m \approx k_1` when considering classical or quantum side information.
Our implementation of this extractor has near-linear computational complexity. 
We also offer a two-source extension of this extractor, whereby the error scales with :math:`\epsilon \rightarrow 2^{n_2 - k_2} \epsilon`, 
where :math:`n_2-k_2` is the difference between the seed length and the seed min-entropy.  

This extractor is best suited to scenarios where a computationally efficient seeded extractor is needed and security 
against quantum side information.

:py:class:`.Trevisan`
---------------------
The Trevisan extractor is a :term:`seeded randomness extractor`, meaning that it requires two independent bit 
strings of randomness, where one is already (near-)perfectly random (called a seed).
It requires a seed length of :math:`n_2 = O(\log_2 (n_1))` and outputs approximately :math:`m \approx k_1` when considering classical or quantum side information.
Our implementation of this extractor has :math:`O(n_1^2)` computational complexity. 
We also offer a two-source extension of this extractor, whereby the error scales with :math:`\epsilon \rightarrow 2^{n_2 - k_2} \epsilon`, 
where :math:`n_2-k_2` is the difference between the seed length and the seed min-entropy.  

This extractor is best suited to scenarios where only a seeded extractor is needed, but only a 
small (in terms of length) seed is available as a resource. 

:py:func:`.von_neumann`
-----------------------
The Von-Neumann extractor is a :term:`deterministic randomness extractor`, meaning that it requires a 
single input string of randomness that has some known (and specific) structure. 
Our implementation of this extractor has linear computational complexity. 

This extractor is best suited to scenarios where a fast extractor is needed and the input has more structure than simply min-entropy. 

