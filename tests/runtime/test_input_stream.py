import pytest

from xmarievm.runtime.input_stream import BufferedInputStream, StandardInputStream
import xmarievm.runtime.input_stream as input_stream


def test_buffered_input_stream():
    stream = BufferedInputStream("One\nTwo\nThree\n")

    first_line = stream.read()
    second_line = stream.read()
    third_line = stream.read()

    with pytest.raises(StopIteration):
        stream.read()

    assert first_line == "One"
    assert second_line == "Two"
    assert third_line == "Three"


def test_standard_input_stream(monkeypatch):
    stream = StandardInputStream()
    monkeypatch.setattr('builtins.input', lambda: 'Line')

    assert stream.read() == 'Line'
