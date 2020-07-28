from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class NumberDefinition:
    val: Any

    def eval(self):
        pass


@dataclass(frozen=True)
class HEX(NumberDefinition):
    def eval(self):
        return int(self.val, 16)


@dataclass(frozen=True)
class DEC(NumberDefinition):
    def eval(self):
        return int(self.val)


@dataclass(frozen=True)
class Label:
    name: str
    target: Any


@dataclass(frozen=True)
class Action:
    pass


@dataclass(frozen=True)
class Command:
    arg: Any


@dataclass(frozen=True)
class _Halt(Action):
    def __repr__(self):
        return 'Halt'


@dataclass(frozen=True)
class Push(Action):
    def __repr__(self):
        return 'Push'


@dataclass(frozen=True)
class Pop(Action):
    def __repr__(self):
        return 'Pop'


@dataclass(frozen=True)
class Store(Command):
    pass


@dataclass(frozen=True)
class Load(Command):
    pass


@dataclass(frozen=True)
class JnS(Command):
    pass


@dataclass(frozen=True)
class Hex(Command):
    pass


@dataclass(frozen=True)
class Add(Command):
    pass


@dataclass(frozen=True)
class Subt(Command):
    pass


@dataclass(frozen=True)
class Skipcond(Command):
    pass


@dataclass(frozen=True)
class Jump(Command):
    pass


@dataclass(frozen=True)
class AddI(Command):
    pass


@dataclass(frozen=True)
class LoadI(Command):
    pass


@dataclass(frozen=True)
class StoreI(Command):
    pass


@dataclass(frozen=True)
class ShiftL(Command):
    pass


@dataclass(frozen=True)
class ShiftR(Command):
    pass


Halt = _Halt()
