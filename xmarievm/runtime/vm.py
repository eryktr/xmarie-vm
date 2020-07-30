from typing import List

from xmarievm.parsing.ast_types import Program


class MarieVm:
    AC: int
    X: int
    Y: int
    PC: int
    MAR: int
    MBR: int
    stack: List[int]
    memory: List[int]

    def __init__(self, memory: List[int]):
        self.AC = 0
        self.PC = 0
        self.X = 0
        self.Y = 0
        self.MAR = 0
        self.MBR = 0

        self.memory = memory

    def execute(self, program: Program) -> None:
        pass

    def _load_into_memory(self, program: Program) -> None:
        last_addr = 0
        for i in program.instructions:
            self.memory[last_addr] = i
