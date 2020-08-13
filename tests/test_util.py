import pytest

from xmarievm.util import int_from_2c


@pytest.mark.parametrize('val, bitsize, expected', (
    (0x01, 4, 0x01),
    (0b1111,  4, -1),
    (0b10111, 4, 7),
    (0b11111, 4, -1),
    (0xFFFFE, 20, -2)
))
def test_int_from_2c(val, bitsize, expected):
    assert int_from_2c(val, bitsize) == expected
