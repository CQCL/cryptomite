# Extlib

An awesome random extraction library. Work in progress.


## Example Usage

```python
from extlib.trevisan import Trevisan
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
