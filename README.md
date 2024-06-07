# cryptomite

![Build Status](https://github.com/CQCL/cryptomite/actions/workflows/build_test.yml/badge.svg)
[![PyPI version](https://img.shields.io/pypi/v/cryptomite)](//pypi.org/project/cryptomite)
[![Downloads](https://static.pepy.tech/badge/cryptomite)](https://pepy.tech/project/cryptomite)
[![Downloads](https://static.pepy.tech/badge/cryptomite/month)](https://pepy.tech/project/cryptomite)
[![arXiv](https://img.shields.io/badge/arXiv-2402.09481-green)](//arxiv.org/abs/2402.09481)


![image](https://github.com/CQCL/cryptomite/assets/13847804/671c8eec-0f2a-46b0-92ba-3a0c040492e8)

`cryptomite` is a modular, extensible high-level Python library 
of randomness extractors, created by Quantinuum's Quantum Cryptography team. 
At a high level, the library offers state-of-the-art randomness extractors that are easy to use, optimized for performance and numerically precise
providing a trade-off of features that suit numerous practical use cases. Find more information in our accompanying [paper](https://arxiv.org/abs/2402.09481).
For additional examples of usage and guidance on getting started with Cryptomite, see our related [blog post](https://medium.com/quantinuum/introducing-cryptomite-randomness-extraction-simplified-857fc2f87673)
and repository [documentation](https://cqcl.github.io/cryptomite/).


The library is available for non-commercial use only; see the [license](https://github.com/CQCL/cryptomite/blob/main/LICENSE) for details.

The performance-critical parts of the library (e.g. the number theoretic transform) are implemented in C++, while the rest of the library (e.g. parameter estimation) is implemented in Python for accessibility and ease of installation.

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

## Testing

Install `pytest`, then run `pytest test`.

To run the C++ tests, run

```bash
cmake .
make
test/runTest
```

## How to Cite
If you use `cryptomite` in your research, please cite the accompanying [paper](https://arxiv.org/abs/2402.09481):

```
@misc{foreman2024cryptomite,
      title={Cryptomite: A versatile and user-friendly library of randomness extractors}, 
      author={Cameron Foreman and Richie Yeung and Alec Edgington and Florian J. Curchod},
      year={2024},
      eprint={2402.09481},
      archivePrefix={arXiv},
      primaryClass={cs.CR}
}
```
