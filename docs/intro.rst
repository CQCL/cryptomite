Introduction
============
Randomness extractors are functions that map weakly random variables to near-uniform variables. 
These functions have far-reaching applications including derandomisation in computational complexity theory, 
list-decodable error-correcting codes and, 
perhaps most notably, quantum cryptography. 

In quantum cryptography, tasks such as key distribution and random number generations
have a number of crucial (classical) post-processing subroutines.  
Randomness extractors play a fundamental role in realizing these, for example, providing an 
explicit technique to purify a shared raw secret key (known as privacy amplification) and/or
distil near-perfect randomness from a weakly random raw output string (known as randomness extraction) in the presence of an adversary.

Recent years have seen major advances in theoretical and experimental quantum cryptography, including exciting proof-of-concept 
demonstrations and even commercialized products. 
All of these require a suitable randomness extractor with the appropriate implementation complexity, loss/error and security.

To facilitate these advances, we have developed :code:`cryptomite`, a software library with multiple randomness extractor implementations.
This software library offers state-of-the-art randomness extractors that are easy to use, optimized and numerically precise
providing a trade-off of features that suits numerous practical use cases today. 