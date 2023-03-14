# cryptomite

`cryptomite` is a modular, extensible high-level Python library 
for randomness extractions, created by Quantinuum's Quantum Cryptography team. 
At a high level, the library offers state-of-the-art randomness extractors that are easy to use, optimized and numerically precise
providing a trade-off of features that suits numerous practical use cases today.

The performance critical parts of the library (e.g. NTT) are implemented in C++, but the rest of the
library (e.g. parameter estimation) is implemented in Python for accessibility and ease of installation.

The package is available for Python 3.8 and higher on Mac, Windows and Linux. To install, type:

```bash 
pip install cryptomite
```



## Example Usage

```python
from cryptomite.trevisan import Trevisan
from random import randint

n, m, max_eps = 1000, 200, 0.01

ext = Trevisan(n, m, max_eps)

input_bits = [randint(0, 1) for _ in range(n)]
seed_bits = [randint(0, 1) for _ in range(ext.ext.get_seed_length())]

output_bits = ext.extract(input_bits, seed_bits)
```

## Documentation

To build the docs, run

```bash
cd docs
pip install -r requirements.txt
make clean
make html
```
