import pytest
import xmarievm.parsing.parser as parser
from xmarievm.runtime.input_stream import StandardInputStream
from xmarievm.runtime.vm import MarieVm


@pytest.fixture
def vm():
    return MarieVm(memory=[0] * 1024, input_stream=StandardInputStream())


def test_load_label_hex(vm):
    code = '''\
Load X
Halt
X, HEX 0xFFFFF
'''
    program = parser.parse(code)

    vm.execute(program)

    assert vm.AC == -1


def test_load_label_dec(vm):
    code = '''\
Load X
Halt
X, DEC 20    
'''
    program = parser.parse(code)

    vm.execute(program)

    assert vm.AC == 20


def test_add_label_hex(vm):
    code = '''\
Load X
Add Y
Halt
X, HEX 0xFFFFF
Y, HEX 0x00003    
'''
    program = parser.parse(code)

    vm.execute(program)

    assert vm.AC == 2


def test_subt_label_hex(vm):
    code = '''\
Load X
Subt Y
Halt
X, HEX 0x1
Y, HEX 0xFFFFF    
'''
    program = parser.parse(code)

    vm.execute(program)

    assert vm.AC == 2


def test_addi_label_hex(vm):
    code = '''\
Load X
AddI 4
Halt
X, HEX 0x1
Y, HEX 0x5
Z, HEX 0x20
'''
    program = parser.parse(code)

    vm.execute(program)

    assert vm.AC == 0x21


def test_subti_label_hex(vm):
    code = '''\
Load X
SubtI 4
Halt
X, HEX 0x7
Y, HEX 0x5
Z, HEX 0x5
'''
    program = parser.parse(code)

    vm.execute(program)

    assert vm.AC == 0x2


def test_skipcond_000(vm):
    code = '''\
Load X
Skipcond 000
Add Y
Halt
X, HEX 0xFFFFF
Y, HEX 0x00003
'''
    program = parser.parse(code)

    vm.execute(program)

    assert vm.AC == -1
