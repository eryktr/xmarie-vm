import pytest

from xmarievm.runtime.streams.input_stream import StandardInputStream
from xmarievm.runtime.streams.output_stream import OutputStream
from xmarievm.runtime.vm import MarieVm


@pytest.fixture
def vm():
    return MarieVm(memory=[0] * 1024, input_stream=StandardInputStream(), output_stream=OutputStream(), stack=[])
