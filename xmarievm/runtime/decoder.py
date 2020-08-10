from typing import NamedTuple

OPCODE_LEN_BITS = 8
ARG_LEN_BITS = 12


class InMemoryInstruction(NamedTuple):
    opcode: int
    arg: int


def decode_instruction(instruction: int) -> InMemoryInstruction:
    arg = instruction % (1 << ARG_LEN_BITS)
    opcode = (instruction >> ARG_LEN_BITS) % (1 << OPCODE_LEN_BITS)
    return InMemoryInstruction(opcode, arg)
