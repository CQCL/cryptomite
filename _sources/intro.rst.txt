Introduction
============
Randomness extractors are functions that distil near-uniform randomness from weakly random inputs. 
These functions have extensive applications, including derandomization in computational complexity theory, list-decodable error-correcting codes, and most notably, quantum cryptography.
In quantum cryptography, tasks like key distribution and random number generation involve several critical (classical) post-processing steps. 
Randomness extractors are crucial in these processes, allowing to purify a shared raw secret key (known as privacy amplification) and to extract near-perfect randomness from a weakly random entropy source (known as randomness extraction) in the presence of an adversary.
Recent advancements in theoretical and experimental quantum cryptography have led to exciting proof-of-concept demonstrations and even commercial products. 
However, all of these require an appropriate randomness extractor with suitable implementation complexity, loss/error rates, and security.
To address this, we developed :code:`Cryptomite`, a software library with multiple state-of-the-art randomness extractors that are easy to use, highly optimized and numerically precise (using the number-theoretic transform where possible to reduce complexity, whilst not needing to use floating point arithmetic like the fast Fourier transform). 