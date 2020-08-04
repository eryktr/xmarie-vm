import pytest

from xmarievm.parsing.ast_types import JnS, Jump, Halt, LoadX, LoadY, Push, Pop, Clear, ShiftR, ShiftL
import xmarievm.parsing.translator as translator


def instr(x):
    return int(x, 16)


@pytest.mark.parametrize('instructions, result', [
    (
        [JnS(0x10), Jump(0x20), Halt()],
        [instr('0010'), instr('0920'), instr('0700')],
    ),
    (
        [LoadX(), LoadY(), Push(), Pop(), Clear()],
        [instr('1500'), instr('1600'), instr('0F00'), instr('1000'), instr('0A00')],
    ),
    (
        [ShiftR(0x90), ShiftL(0xA1)],
        [instr('1290'), instr('11A1')],
    )
])
def test_translate_instructions(instructions, result):
    assert translator.translate(instructions) == result
