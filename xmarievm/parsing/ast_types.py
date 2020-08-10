from dataclasses import dataclass, field
from typing import Any, List, Dict


@dataclass
class Label:
    name: str
    addr: int


@dataclass
class Instruction:
    opcode: int = field(repr=False, init=False)
    arg: Any

    def to_hex(self):
        pass


@dataclass
class Action(Instruction):
    arg: Any = 0

    def to_hex(self):
        return f'{self.opcode:02X}{0:03X}'


@dataclass
class Command(Instruction):

    def to_hex(self):
        return f'{self.opcode:02X}{self.arg:03X}'


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
    opcode = 0x13


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
    pass


@dataclass
class DEC(Command):
    pass


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
class Program:
    instructions: List[int]
    labels: Dict[str, int]
