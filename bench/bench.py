from cryptomite.dodis import Dodis
from cryptomite.toeplitz import Toeplitz
from cryptomite.utils import von_neumann
from cryptomite.trevisan import Trevisan 
from numpy.random import randint
import numpy as np

from time import time

import pandas as pd


cache1 = dict()
cache2 = dict()

N_REPEATS = 5

seed_caches = [dict() for _ in range(N_REPEATS)]
cache3 = dict()
def get_random(cache, n):
    if n not in cache:
        cache[n] = randint(0, 2, size=n)

    return cache[n]

# compare with naive

inp_lens = [x * 10 ** n for x in [10, 18, 32, 56] for n in range(1, 10)]
# inp_lens = [10 ** 8]
names = ["Extractor", "Input Length", "Ratio"]
#ratios = (0.5, 0.75)
ratios = [0.5]
columns = ["Wait (s)"]
indices = []
rows = []

# Dodis
print("\nDodis: ", end="", flush=True)
for inp_len in inp_lens:
    inp1 = get_random(cache1, inp_len)
    inp2 = get_random(cache2, inp_len)

    for ratio in ratios:
        waits = []
        for i in range(N_REPEATS):
            inp2 = get_random(seed_caches[i], inp_len)
            out_len = int(inp_len * ratio)
            ext = Dodis(inp_len, out_len)
            start = time()
            ext.extract(inp1, inp2)
            wait = time() - start
            waits.append(wait)
            print(".", end="", flush=True)
        print("|", end="", flush=True)
        rows.append(sum(waits) / len(waits))
        indices.append(('Dodis', inp_len, ratio))

# VN
print("\nVN: ", end="", flush=True)
for inp_len in inp_lens:
    waits = []
    for i in range(N_REPEATS):
        inp1 = get_random(seed_caches[i], inp_len)
        start = time()
        von_neumann(inp1)
        wait = time() - start
        waits.append(wait)
        print(".", end="", flush=True)
    print("|", end="", flush=True)
    rows.append(sum(waits) / len(waits))
    indices.append(('Von Neumann', inp_len, np.nan))

# Toeplitz
print("\nToeplitz", end="", flush=True)
for inp_len in inp_lens:
    inp1 = get_random(cache1, inp_len)

    for ratio in ratios:
        out_len = int(inp_len * ratio)
        waits = []
        for i in range(N_REPEATS):
            seed = get_random(seed_caches[i], inp_len + out_len - 1)
            ext = Toeplitz(inp_len, out_len)
            start = time()
            ext.extract(inp1, seed)
            wait = time() - start
            waits.append(wait)
            print(".", end="", flush=True)
        print("|", end="", flush=True)
        rows.append(sum(waits) / len(waits))
        indices.append(('Toeplitz', inp_len, ratio))

# Trevisan
print("\nTrevisan: ", end="", flush=True)
for inp_len in inp_lens:
    if inp_len > 10000:
        continue
    inp1 = get_random(cache1, inp_len)

    for ratio in ratios:
        min_ent = int(inp_len * ratio)
        ext = Trevisan(inp_len, min_ent, 2 ** -20)
        seed_length = ext.ext.get_seed_length()
        waits = []
        for i in range(N_REPEATS):
            seed = get_random(seed_caches[i], seed_length)
            start = time()
            ext.extract(inp1, seed)
            wait = time() - start
            waits.append(wait)
            print(".", end="", flush=True)
        rows.append(sum(waits) / len(waits))
        indices.append(('Trevisan', inp_len, ratio))
print("")

index = pd.MultiIndex.from_tuples(indices, names=names)

df = pd.DataFrame(rows, index=index, columns=columns)

print(df)

ndf = df.copy().reset_index()
ndf.loc[ndf["Extractor"] == "Von Neumann", "Ratio"] = 0.5
ndf["Rate"] = ndf["Input Length"] * ndf["Ratio"] / ndf["Wait (s)"]
