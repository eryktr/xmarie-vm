import pytest

from xmarievm.parsing.ast_types import Store, Halt, ShiftR, Add, AddI, LoadI, Skipcond
from xmarievm.runtime.decoder import decode_instruction
import xmarievm.parsing.translator as translator


@pytest.mark.parametrize('instr, opcode, arg', (
    (int('01002', 16), 0x1, 2),
    (int('11000', 16), 0x11, 0),
    (int('00000', 16), 0x0, 0),
))
def test_decode_instruction(instr, opcode, arg):
    decoded_instr = decode_instruction(instr)

    assert decoded_instr.opcode == opcode
    assert decoded_instr.arg == arg


@pytest.mark.parametrize('instr, arg', (
    (Store(0x010), 0x010),
    (Halt(), 0x0),
    (ShiftR(0xAB), 0xAB),
    (Add(0x1), 0x1),
    (AddI(0x2), 0x2),
    (LoadI(0xF1), 0xF1),
    (Skipcond(400), 400),
    (Skipcond(800), 800),
    (Skipcond(0), 0),
))
def test_decode_and_translate(instr, arg):
    encoded_instr = translator.translate([instr], labels={})[0]
    decoded_instr = decode_instruction(encoded_instr)

    assert decoded_instr.opcode == instr.opcode
    assert decoded_instr.arg == arg
