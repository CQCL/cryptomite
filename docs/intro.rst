Introduction
============
Randomness extractors are functions that map weakly random variables to near-uniform variables. 
These functions have far-reaching applications including derandomisation in computational complexity theory, 
list-decodable error-correcting codes and, 
perhaps most notably, quantum cryptography. 

Arguably started by Vazirani and others in their study of pseudo-random objects [.], randomness extractor theory was first formalized by Zuckerman and others[.]. 
Since then, randomness extractors have been extensively studied, with numerous new constructions invented, 
efficient implementations developed and improved parameters derived. 
Recent years have seen interesting advances, with the introduction of new tools and frameworks that 
paved the way for rapid progress on many long-standing open problems. 

In quantum cryptography, tasks such as key distribution and random number generations
have a number of crucial (classical) post-processing subroutines.  
Randomness extractors play a fundamental role in realizing these, for example, providing an 
explicit technique to purify a shared raw secret key (known as privacy amplification) and/or
distil near-perfect randomness from a weakly random raw output string (known as randomness extraction) in the presence of an adversary.\\

Recent years have seen major advances in theoretical and experimental quantum cryptography, including exciting quantum cryptography proof-of-concept demonstrations [.] and even commercialized products [.]. 
Each of these require a suitable randomness extractor, considering the following features:

Can it be implemented?: 
There are numerous explicit randomness extractors - however 
    many do not have a clear implementation. An end-to-end demonstration requires the randomness extractor algorithm to be written in software. 

What are the initial required resources?: 
Often, randomness extractors require 
    auxiliary randomness, known as a seed, independent of any generated during the protocol. 
    Some extractors allow for the seed to be any combination of i) short, ii) weakly random 
    and iii) dependent to some degree.

How well does it extract?: 
Some randomness extractors are able to map weakly random variables to 
    near-uniform random variables with only constant loss in length (implying exponentially small error) against both quantum 
    and classical side information. 
    Not all extractors have this property.

What is its computational complexity?: 
Many randomness extractors have generic 
    polynomial computational complexity. For some applications, this may not be sufficient. 

To facilitate these advances, we have developed \texttt{cryptomite}. 
This software library offers state-of-the-art randomness extractors that are easy to use, optimized and numerically precise
providing a trade-off of features that suits numerous practical use cases today. 