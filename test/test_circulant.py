import pytest
from cryptomite.circulant import Circulant


circulant_testcases = [
    (2, 1, [0, 1], [1, 1, 1], [1]),
    (2, 2, [1, 0], [1, 1, 0], [1, 1]),
    (2, 2, [0, 1], [0, 0, 0], [0, 0]),
    (5, 5, [1, 0, 1, 0, 0], [1, 1, 1, 0, 1, 0], [0, 1, 0, 0, 0]),
    (
        8,
        8,
        [0, 0, 1, 1, 0, 0, 0, 1],
        [1, 1, 1, 0, 1, 1, 1, 1, 0],
        [0, 1, 1, 1, 1, 1, 0, 1],
    ),
]


@pytest.mark.parametrize("n,m,x,y,z", circulant_testcases)
def test_circulant(n, m, x, y, z):
    assert Circulant(n, m).extract(x, y) == z
