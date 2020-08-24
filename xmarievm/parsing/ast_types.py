from dataclasses import dataclass, field
from typing import Any, List, Dict

from xmarievm.const import MEM_BITSIZE
from xmarievm.util import int_from_2c


@dataclass
class Label:
    name: str
    addr: int
    val: 'Instruction'


@dataclass
class Instruction:
    opcode: int = field(repr=False, init=False)
    arg: Any

    def translate(self):
        pass


@dataclass
class Action(Instruction):
    arg: Any = 0

    def translate(self):
        return int(f'{self.opcode:02X}{0:03X}', 16)


@dataclass
class Command(Instruction):

    def translate(self):
        return int(f'{self.opcode:02X}{self.arg:03X}', 16)


@dataclass
class Halt(Action):
    opcode = 0x7


@dataclass
class Input(Action):
    opcode = 0x5


@dataclass
class Output(Action):
    opcode = 0x6


@dataclass
class Clear(Action):
    opcode = 0xA


@dataclass
class StoreX(Action):
    opcode = 0x19


@dataclass
class StoreY(Action):
    opcode = 0x14


@dataclass
class LoadX(Action):
    opcode = 0x15


@dataclass
class LoadY(Action):
    opcode = 0x16


@dataclass
class Push(Action):
    opcode = 0xF


@dataclass
class Pop(Action):
    opcode = 0x10


@dataclass
class Store(Command):
    opcode = 0x2


@dataclass
class Load(Command):
    opcode = 0x1


@dataclass
class JnS(Command):
    opcode = 0x0


@dataclass
class HEX(Command):
    def translate(self):
        return int_from_2c(self.arg, MEM_BITSIZE)


@dataclass
class DEC(Command):
    def translate(self):
        return self.arg


@dataclass
class Add(Command):
    opcode = 0x3


@dataclass
class Subt(Command):
    opcode = 0x4


@dataclass
class Skipcond(Command):
    opcode = 0x8


@dataclass
class Jump(Command):
    opcode = 0x9


@dataclass
class JumpI(Command):
    opcode = 0xC


@dataclass
class AddI(Command):
    opcode = 0xB


@dataclass
class LoadI(Command):
    opcode = 0xE


@dataclass
class StoreI(Command):
    opcode = 0xD


@dataclass
class ShiftL(Command):
    opcode = 0x11


@dataclass
class ShiftR(Command):
    opcode = 0x12


@dataclass
class SubtI(Command):
    opcode = 0x13


@dataclass
class Incr(Action):
    opcode = 0x17


@dataclass
class Decr(Action):
    opcode = 0x18


@dataclass
class Program:
    instructions: List[int]
    labels: Dict[str, int]
