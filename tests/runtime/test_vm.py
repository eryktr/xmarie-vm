import pytest

import xmarievm.parsing.parser as parser
from xmarievm import api
from xmarievm.runtime.streams.input_stream import BufferedInputStream
from xmarievm.runtime.streams.output_stream import OutputStream
from xmarievm.runtime.vm import MarieVm


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
Add Z
Halt
X, HEX 0xFFFFF
Y, HEX 0x00003
Z, HEX 0x00004
'''
    program = parser.parse(code)

    vm.execute(program)

    assert vm.AC == 3


def test_skipcond_400(vm):
    code = '''\
Load X
Skipcond 400
Add Y
Add Z
Halt
X, HEX 0x00000
Y, HEX 0x00003
Z, HEX 0x00001
'''
    program = parser.parse(code)

    vm.execute(program)

    assert vm.AC == 1


def test_skipcond_800(vm):
    code = '''\
    Load X
    Skipcond 800
    Add Y
    Add Z
    Halt
    X, HEX 0x00001
    Y, HEX 0x00003
    Z, HEX 0x00001
    '''
    program = parser.parse(code)

    vm.execute(program)

    assert vm.AC == 2


def test_overflow(vm):
    code = '''\
    Load X
    Add Y
    Halt
    X, DEC 524287
    Y, DEC 524286
    '''
    program = parser.parse(code)

    vm.execute(program)

    assert vm.AC == -3


def test_jump(vm):
    code = '''\
            Load X
            Jump here
            Add Y
    here,   Add Z
            Halt
    X,      DEC 0
    Y,      DEC 5
    Z,      DEC 10
    '''
    program = parser.parse(code)

    vm.execute(program)

    assert vm.AC == 10


@pytest.mark.parametrize('input_, acc', (
    ('0x20', 0x20),
    ('0xFFFFF', -1),
    ('0xFFFFE', -2),
    ('0x000FF', 255),
))
def test_input(input_, acc):
    code = '''\
    Input
    Halt
    '''
    vm = MarieVm(
        memory=[0] * 1024,
        input_stream=BufferedInputStream(input_),
        output_stream=OutputStream(),
        stack=[],
        max_num_of_executed_instrs=1000,
    )
    program = parser.parse(code)

    vm.execute(program)

    assert vm.AC == acc


@pytest.mark.parametrize('output, buf', (
    ('0x10', ['0x10']),
    ('0xFFFFF', ['0xFFFFF']),
))
def test_output(vm, output, buf):
    code = f'''
    Load X
    Output
    Halt
    X, HEX {output}
    '''

    program = parser.parse(code)

    vm.execute(program)

    assert vm.output_stream.buf == buf


def test_shiftl(vm):
    code = '''
    Load X
    ShiftL Y
    Halt
    
    X, DEC 2
    Y, DEC 3
    '''

    program = parser.parse(code)

    vm.execute(program)

    assert vm.AC == 16


def test_shiftr(vm):
    code = '''
    Load X
    ShiftR Y
    Halt
    
    
    X, DEC 8
    Y, DEC 1
    '''

    program = parser.parse(code)

    vm.execute(program)

    assert vm.AC == 4


def test_clear(vm):
    code = '''\
    Load X
    Clear
    Halt
    X, HEX 0x20
    '''

    program = parser.parse(code)

    vm.execute(program)

    assert vm.AC == 0


def test_incr(vm):
    code = '''
    Load X
    Incr
    Halt
    
    X, DEC 1
    '''

    program = parser.parse(code)

    vm.execute(program)

    assert vm.AC == 2


def test_decr(vm):
    code = '''
    Load X
    Decr
    Halt

    X, DEC 10
    '''

    program = parser.parse(code)

    vm.execute(program)

    assert vm.AC == 9


def test_storei(vm):
    code = '''
    Load Y
    StoreI X
    Load X
    Halt
    
    X, DEC 5
    Y, DEC 4
    '''

    program = parser.parse(code)

    vm.execute(program)

    assert vm.AC == 4


def test_jumpi(vm):
    code = '''
    Load X
    JumpI Z
    Add Y
    Add Y
    Add Y 
    Halt
    
    X, DEC 5
    Y, DEC 6
    Z, DEC 5
    '''

    program = parser.parse(code)

    vm.execute(program)

    assert vm.AC == 5


def test_push_and_pop(vm):
    code = '''
    Load X
    Push
    
    Load Y
    Push
    
    Load Z
    Push
    Pop
    Halt
    
    X, HEX 0xFFFFF
    Y, HEX 0xFFFFE
    Z, HEX 0xFFFFD
    '''

    program = parser.parse(code)

    vm.execute(program)

    assert vm.stack == [-2, -1]


def test_loadi(vm):
    code = '''
    LoadI X
    Halt
    X, DEC 3
    Z, DEC 99
    '''

    program = parser.parse(code)

    vm.execute(program)

    assert vm.AC == 99


def test_storex(vm):
    code = '''
    Load X
    StoreX
    Halt
    X, DEC 10
    '''

    program = parser.parse(code)

    vm.execute(program)

    assert vm.X == 10


def test_storey(vm):
    code = '''
    Load X
    StoreY
    Halt
    X, DEC 10
    '''
    program = parser.parse(code)

    vm.execute(program)

    assert vm.Y == 10


def test_loadx(vm):
    code = '''
    Load X
    StoreX
    Load Y
    LoadX
    Halt
    
    X, DEC 10
    Y, DEC 20
    '''

    program = parser.parse(code)

    vm.execute(program)

    assert vm.AC == 10


def test_loady(vm):
    code = '''
    Load X
    StoreY
    Load Y
    LoadY
    Halt

    X, DEC 10
    Y, DEC 20
    '''

    program = parser.parse(code)

    vm.execute(program)

    assert vm.AC == 10


def test_jns(vm):
    code = '''
JnS PrintX
JnS PrintX
Halt

PrintX, HEX 0x00000
        Load X
        StoreX
        Output

        JumpI PrintX

        X, DEC 42
'''

    program = parser.parse(code)

    vm.execute(program)

    assert vm.output_stream.buf == ['0x2A', '0x2A']
    assert vm.X == 42


def test_profiling_stats(vm):
    code = '''
    Load X
    StoreY
    Load Y
    LoadY
    Halt

    X, DEC 10
    Y, DEC 20
    '''

    program = parser.parse(code)

    vm.execute(program)

    assert vm.cost_of_executed_instrs == 9
    assert vm.instr_to_call_count == {
        'Load': 2,
        'Halt': 1,
        'StoreY': 1,
        'LoadY': 1,
    }


def test_debug_generates_the_right_number_of_snapshots(vm):
    code = '''
    Load X
    StoreY
    Load Y
    LoadY
    Halt

    X, DEC 10
    Y, DEC 20
    '''

    program = parser.parse(code)

    snapshots = vm.debug(program, breakpoints=[])

    assert len(snapshots) == 5


def test_run_incorrect_code():
    code = '''
    BadIntr Z
    Load X
    Add Y
   
    
    X, DEC 10
    Y, DEC 16
    '''

    with pytest.raises(SyntaxError):
        api.run(code, debug=False)


def test_vm_raises_when_max_allowed_num_of_executed_instrs_is_exceeded(vm):
    vm.max_num_of_executed_instrs = 1000
    vm.num_of_executed_instrs = 998

    code = '''
    Load X
    StoreY
    Load Y
    LoadY
    Halt

    X, DEC 10
    Y, DEC 20
    '''

    program = parser.parse(code)

    with pytest.raises(TimeoutError):
        vm.execute(program)
