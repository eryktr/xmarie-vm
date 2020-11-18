import pytest

from xmarievm.runtime.streams.input_stream import StandardInputStream
from xmarievm.runtime.streams.output_stream import OutputStream
from xmarievm.runtime.vm import MarieVm, MAX_NUM_OF_EXECUTED_INSTRS


@pytest.fixture
def vm():
    vm = MarieVm(memory=[0] * 1024, input_stream=StandardInputStream(), output_stream=OutputStream(), stack=[],
                 max_num_of_executed_instrs=MAX_NUM_OF_EXECUTED_INSTRS)
    return vm


@pytest.fixture
def dummy_linearray():
    return [*range(100)]
