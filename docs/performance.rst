Performance
==========

To demonstrate the capabilities of :code:`Cryptomite`, we perform some benchmarking on a MacBook Pro personal laptop (with 2 Ghz quad-core Intel i5 processor with 16GB RAM).
The varying degrees of computational efficiency for the extractors of :code:`Cryptomite` are evidenced in the following Figure. 

.. image:: figures/performance.pdf
   :width: 600

Some observations performance observations are:
* The Von-Neumann extractor is able to output at speeds above 7Mbit/s. 
* The Dodis and Toeplitz extractors are able to output at speeds of up to 1Mbit/s. The generation speed is faster for shorter input lengths.
* The Trevisan extractor can generate output at speeds comparable to the Toeplitz and Dodis extractors only when the input size is extremely short. 
* The Trevisan extractor unable to generate a non-vanishing bits/second rate for input lengths greater than approximately 30'000.
