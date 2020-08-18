from xmarievm.runtime.streams.output_stream import OutputStream


def test_output_stream():
    stream = OutputStream()

    stream.write('hello')

    assert stream.buf == ['hello']
