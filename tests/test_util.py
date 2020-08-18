import pytest

from xmarievm.util import int_from_2c, int_in_2c_to_hex


@pytest.mark.parametrize('val, bitsize, expected', (
    (0x01, 4, 0x01),
    (0b1111, 4, -1),
    (0b10111, 4, 7),
    (0b11111, 4, -1),
    (0xFFFFE, 20, -2)
))
def test_int_from_2c(val, bitsize, expected):
    assert int_from_2c(val, bitsize) == expected


@pytest.mark.parametrize('val, bitsize, expected', (
    (-1, 4, '0xF'),
    (-1, 20, '0xFFFFF'),
    (-2, 20, '0xFFFFE'),
    (1, 4, '0x1'),
    (255, 12, '0xFF'),
))
def test_int_in_2c_to_hex(val, bitsize, expected):
    assert int_in_2c_to_hex(val, bitsize) == expected
