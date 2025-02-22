Performance
===========

To demonstrate the capabilities of :py:mod:`Cryptomite`, we conducted benchmarking on a MacBook Pro with a 2 GHz quad-core Intel i5 processor and 16GB RAM
The code for this benchmarking is available in `cryptomite/bench/bench.py`, enabling users to reproduce the results on their own machines.
This testing assumes that the min-entropy of the first source (the weak input) is :math:`k_1 = n_1 / 2`.

.. image:: figures/performance.png
   :width: 600