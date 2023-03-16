Selecting a Randomness Extractor
===============
In the following, we use the notation :math:`n1, n2` to denote the length and :math:`k1, k2` to denote the min-entropy of 
any first or second input string respectively. Additionally, :math:`m` denotes the length of an output string, :math:`\epsilon` 
the extractor error and :math:`\bigO(.)` denotes the asymptotic behaviour of a function.

:code:`Dodis`
-----------------
The Dodis extractor is a two-source extractor, meaning that it requires two independent bit 
strings of randomness that only 'contain' entropy (as opposed to one or both being fully entropic). 
It requires equal length inputs (:math:`n1 = n2`) that are prime with 2 as a primitive root (see :code:`na_set` in glossary) 
and outputs approximately :math:`m \approx k1 + k2 - n1` when considering classical side information and :math:`m \approx \frac{1}{5}(k1 + k2 - n1)`.
Our implementation of this extractor has near-linear computational complexity.

This extractor is best suited to scenarios where a two-source extractor is required, 
or a computationally efficient extractor considering classical side information only (then Dodis can be 
used as a seeded extractor, giving approximately the same output length as Toeplitz, whilst reducing required seed size.)

:code:`Toeplitz`
-----------------
The Toeplitz extractor is a seeded extractor, meaning that it requires two independent bit 
strings of randomness, where one is already (near-)perfectly random (called a seed).
It requires a seed length of :math:`n2 = n1 + m - 1`
and outputs approximately :math:`m \approx k1` when considering classical or quantum side information.
Our implementation of this extractor has near-linear computational complexity. 
We also offer a two-source extension of this extractor, whereby the error scales with :math:`\epsilon \rightarrow 2^{n2 - k2} \epsilon`, 
where :math:`n2-k2` is the difference between the seed length and the seed min-entropy.  

This extractor is best suited to scenarios where a computationally efficient seeded extractor is needed and security 
against quantum side information.

:code:`Trevisan`
-----------------
The Trevisan extractor is a seeded extractor, meaning that it requires two independent bit 
strings of randomness, where one is already (near-)perfectly random (called a seed).
It requires a seed length of :math:`n2 = \bigO(\log_2 (n1))` and outputs approximately :math:`m \approx k1` when considering classical or quantum side information.
Our implementation of this extractor has :math:`\bigO(n1^2)` computational complexity. 
We also offer a two-source extension of this extractor, whereby the error scales with :math:`\epsilon \rightarrow 2^{n2 - k2} \epsilon`, 
where :math:`n2-k2` is the difference between the seed length and the seed min-entropy.  

This extractor is best suited to scenarios where only a seeded extractor is needed, but only a 
small (in terms of length) seed is available as a resource. 

:code:`Von Neumann`
-----------------
The Von-Neumann extractor is a deterministic extractor, meaning that it requires a 
single input string of randomness that has some known (and specific) structure. 
Our implementation of this extractor has linear computational complexity. 

This extractor is best suited to scenarios where a fast extractor is needed and the input has more structure than simply min-entropy. 

