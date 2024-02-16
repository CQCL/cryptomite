==========
Cryptomite
==========

:py:mod:`Cryptomite` is a Python library of randomness extractors, created by Quantinuum's Quantum Cryptography team. 
At a high level, the library offers state-of-the-art randomness extractors that are easy to use, optimized and numerically precise --
providing a trade-off of features that suits numerous practical use cases today.

The performance critical parts of the library (e.g. NTT) are implemented in C++, but the rest of the
library (e.g. parameter estimation) is implemented in Python for accessibility and ease of installation.

The package is available for Python 3.8 and higher on Mac, Windows and Linux. To install, type:

.. code-block:: bash

   pip install cryptomite

To see the example notebooks, go to Examples.

User Support
============
If you need help with :py:mod:`Cryptomite` or think you have found a bug, please email 
qcrypto@quantinuum.com. 

Licence
=======
See `license <https://github.com/CQCL/cryptomite/blob/main/LICENSE>`_ here.
In summary, you are free to use, modify and distribute to :py:mod:`Cryptomite`
for academic purposes. If you wish to use it for commercial use, contact
qcrypto@quantinuum.com

How to Cite
===========
If you use :py:mod:`cryptomite` in your research, please cite the accompanying paper
`Cryptomite: A versatile and user-friendly library of randomness extractors <https://arxiv.org/abs/2402.09481>`_.


.. toctree::
   :caption: Toolkit
   :maxdepth: 4

   intro
   gettingstarted
   cryptomite
   performance
   notebooks
   glossary
   bibliography
