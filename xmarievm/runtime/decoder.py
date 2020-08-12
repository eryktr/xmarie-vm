from typing import NamedTuple

from xmarievm.const import OPCODE_LEN_BITS, ARG_LEN_BITS


class InMemoryInstruction(NamedTuple):
    opcode: int
    arg: int


def decode_instruction(instruction: int) -> InMemoryInstruction:
    arg = instruction % (1 << ARG_LEN_BITS)
    opcode = (instruction >> ARG_LEN_BITS) % (1 << OPCODE_LEN_BITS)
    return InMemoryInstruction(opcode, arg)
