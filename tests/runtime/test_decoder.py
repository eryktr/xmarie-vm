import pytest

from xmarievm.parsing.ast_types import Store, Halt, ShiftR, Add, AddI, LoadI
from xmarievm.runtime.decoder import decode_instruction
import xmarievm.parsing.translator as translator


@pytest.mark.parametrize('instr, opcode, arg', (
    (int('0102', 16), 0x1, 2),
    (int('1100', 16), 0x11, 0),
    (int('0000', 16), 0x0, 0),
))
def test_decode_instruction(instr, opcode, arg):
    decoded_instr = decode_instruction(instr)

    assert decoded_instr.opcode == opcode
    assert decoded_instr.arg == arg


@pytest.mark.parametrize('instr, arg', (
    (Store(0x10), 0x10),
    (Halt(), 0x0),
    (ShiftR(0xAB), 0xAB),
    (Add(0x1), 0x1),
    (AddI(0x2), 0x2),
    (LoadI(0xF1), 0xF1),
))
def test_decode_and_translate(instr, arg):
    encoded_instr = translator.translate([instr])[0]
    decoded_instr = decode_instruction(encoded_instr)

    assert decoded_instr.opcode == instr.opcode
    assert decoded_instr.arg == arg
