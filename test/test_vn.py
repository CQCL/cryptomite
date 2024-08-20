import pytest
from cryptomite.utils import von_neumann

vn_testcases = [
    ([], []),
    ([0, 1, 0, 1], [0, 0]),
    ([0, 0, 0, 0], []),
    ([0, 0, 1, 1], []),
    ([0, 0, 0, 1, 1, 0, 1, 1, 1], [0, 1]),
    ([1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0],
     [1, 1, 1, 0, 1])
]


@pytest.mark.parametrize("bits, expect", vn_testcases)
def test_vn(bits, expect):
    assert von_neumann(bits) == expect
