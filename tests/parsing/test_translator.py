import pytest

from xmarievm.parsing.ast_types import JnS, Jump, Halt, LoadX, LoadY, Push, Pop, Clear, ShiftR, ShiftL, HEX, DEC
import xmarievm.parsing.translator as translator


def instr(x):
    return int(x, 16)


@pytest.mark.parametrize('instructions, result', [
    (
        [JnS(0x10), Jump(0x20), Halt()],
        [instr('00010'), instr('09020'), instr('07000')],
    ),
    (
        [LoadX(), LoadY(), Push(), Pop(), Clear()],
        [instr('15000'), instr('16000'), instr('0F000'), instr('10000'), instr('0A000')],
    ),
    (
        [ShiftR(0x90), ShiftL(0xA1)],
        [instr('12090'), instr('110A1')],
    ),
    (
        [HEX(0x00020), HEX(0xFFFFF), HEX(0xFFFFE)],
        [instr('00020'), -1, -2],
    ),
    (
        [DEC(1024), DEC(0), DEC(2048)],
        [1024, 0, 2048],
    )
])
def test_translate_instructions(instructions, result):
    assert translator.translate(instructions, labels={}) == result
