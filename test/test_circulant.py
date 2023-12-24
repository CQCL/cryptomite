import pytest
from cryptomite.circulant import Circulant


circulant_testcases = [
    (3, 1, [0, 1], [1, 1, 1], [1]),
    (3, 2, [1, 0], [1, 1, 0], [1, 1]),
    (3, 2, [0, 1], [0, 0, 0], [0, 0]),
    (6, 5, [1, 0, 1, 0, 0], [1, 1, 1, 0, 1, 0], [0, 1, 0, 0, 0]),
    (
        9,
        7,
        [1, 1, 1, 0, 1, 1, 1, 1],
        [1, 1, 1, 0, 1, 1, 0, 0, 1],
        [0, 0, 1, 0, 0, 0, 1],
    ),
    (
        9,
        8,
        [0, 0, 1, 1, 0, 0, 0, 1],
        [1, 1, 1, 0, 1, 1, 1, 1, 0],
        [0, 1, 1, 1, 1, 1, 0, 1],
    ),
]


@pytest.mark.parametrize("n,m,x,y,z", circulant_testcases)
def test_circulant(n, m, x, y, z):
    assert Circulant(n, m).extract(x, y) == z
