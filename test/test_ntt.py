import pytest
from cryptomite._cryptomite import BigNTT, NTT
import numpy as np

test_range = list(range(2, 21))


def slow_conv(a, b):
    """ direct implementation """
    c = [0] * len(a)
    for i in range(len(a)):
        for j in range(len(b)):
            c[(i + j) % len(c)] += a[i] * b[j]
    return c


@pytest.mark.parametrize('n', test_range)
def test_ntt_inv(n):
    ntt = NTT(n)
    for _ in range(10):
        v = np.random.randint(0, 1 << n, 1 << n).tolist()
        assert ntt.ntt(ntt.ntt(v, False), True) == v


@pytest.mark.parametrize('n', test_range)
def test_big_ntt_inv(n):
    ntt = BigNTT(n)
    for _ in range(10):
        v = np.random.randint(0, 1 << n, 1 << n).tolist()
        assert ntt.ntt(ntt.ntt(v, False), True) == v


@pytest.mark.parametrize('n', list(range(2, 11)))
def test_ntt_conv(n):
    ntt = NTT(n)
    a = np.random.randint(0, 2, 1 << n).tolist()
    b = np.random.randint(0, 2, 1 << n).tolist()
    assert ntt.conv(a, b) == slow_conv(a, b)


@pytest.mark.parametrize('n', test_range)
def test_big_ntt_conv(n):
    ntt = NTT(n)
    big_ntt = BigNTT(n)
    a = np.random.randint(0, 2, 1 << n).tolist()
    b = np.random.randint(0, 2, 1 << n).tolist()
    assert ntt.conv(a, b) == big_ntt.conv(a, b)
