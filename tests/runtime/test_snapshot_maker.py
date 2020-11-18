import xmarievm.parsing.parser as parser
from xmarievm.runtime import snapshot_maker


def test_make_snapshot(vm, dummy_linearray):
    code = """
    Load X
    Push
    Add Y
    Halt
    X, HEX 0xFFFFF
    Y, HEX 0x00003    
    """

    program = parser.parse(code)

    vm.execute(program, dummy_linearray)

    snapshot = snapshot_maker.make_snapshot(vm)

    assert snapshot.AC == 2
    assert -1 in snapshot.memory
    assert 3 in snapshot.memory
    assert snapshot.stack == [-1]
