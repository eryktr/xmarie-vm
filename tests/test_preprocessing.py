from xmarievm.preprocessing import get_line_array


def test_get_line_array():
    code = """\
Load X
Store Y
Push


Pop

Some, Thing

Halt
"""

    assert get_line_array(code) == [1, 2, 3, 6, 8, 10]
