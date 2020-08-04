from dataclasses import dataclass, field
from typing import Any, List, Dict


@dataclass(frozen=True)
class Label:
    name: str
    addr: int


@dataclass(frozen=True)
class Instruction:
    opcode: int = field(repr=False, init=False)

    def to_hex(self):
        pass


@dataclass(frozen=True)
class Action(Instruction):
    def to_hex(self):
        return f'{self.opcode:02X}{0:02X}'


@dataclass(frozen=True)
class Command(Instruction):
    arg: Any

    def to_hex(self):
        return f'{self.opcode:02X}{self.arg:02X}'


@dataclass(frozen=True)
class Halt(Action):
    opcode = 0x7


@dataclass(frozen=True)
class Input(Action):
    opcode = 0x5


@dataclass(frozen=True)
class Output(Action):
    opcode = 0x6


@dataclass(frozen=True)
class Clear(Action):
    opcode = 0xA


@dataclass(frozen=True)
class StoreX(Action):
    opcode = 0x13


@dataclass(frozen=True)
class StoreY(Action):
    opcode = 0x14


@dataclass(frozen=True)
class LoadX(Action):
    opcode = 0x15


@dataclass(frozen=True)
class LoadY(Action):
    opcode = 0x16


@dataclass(frozen=True)
class Push(Action):
    opcode = 0xF


@dataclass(frozen=True)
class Pop(Action):
    opcode = 0x10


@dataclass(frozen=True)
class Store(Command):
    opcode = 0x2


@dataclass(frozen=True)
class Load(Command):
    opcode = 0x1


@dataclass(frozen=True)
class JnS(Command):
    opcode = 0x0


@dataclass(frozen=True)
class Hex(Command):
    pass


@dataclass(frozen=True)
class Add(Command):
    opcode = 0x3


@dataclass(frozen=True)
class Subt(Command):
    opcode = 0x4


@dataclass(frozen=True)
class Skipcond(Command):
    opcode = 0x8


@dataclass(frozen=True)
class Jump(Command):
    opcode = 0x9


@dataclass(frozen=True)
class JumpI(Command):
    opcode = 0xC


@dataclass(frozen=True)
class AddI(Command):
    opcode = 0xB


@dataclass(frozen=True)
class LoadI(Command):
    opcode = 0xE


@dataclass(frozen=True)
class StoreI(Command):
    opcode = 0xD


@dataclass(frozen=True)
class ShiftL(Command):
    opcode = 0x11


@dataclass(frozen=True)
class ShiftR(Command):
    opcode = 0x12


@dataclass(frozen=True)
class Program:
    instructions: List[int]
    labels: Dict[str, int]
