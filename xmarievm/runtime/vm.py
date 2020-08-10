from typing import List, Callable

from xmarievm.parsing.ast_types import Program, Load
from xmarievm.runtime.decoder import decode_instruction
from xmarievm.runtime.input_stream import InputStream


class MarieVm:
    AC: int
    X: int
    Y: int
    PC: int
    MAR: int
    MBR: int
    stack: List[int]
    memory: List[int]
    running: bool

    def __init__(self, memory: List[int], input_stream: InputStream):
        self.AC = 0
        self.PC = 0
        self.X = 0
        self.Y = 0
        self.MAR = 0
        self.MBR = 0

        self.memory = memory
        self.input_stream = input_stream
        self.running = False

    def execute(self, program: Program) -> None:
        self._load_into_memory(program)
        self.running = True
        while self.running:
            instr = self._fetch_instruction()
            decoded_instr = decode_instruction(instr)
            action = self._get_action(decoded_instr.opcode)
            print(action.__name__)
            action(decoded_instr.arg)
            self.PC += 1

    def _load_into_memory(self, program: Program) -> None:
        last_addr = 0
        for i in program.instructions:
            self.memory[last_addr] = i
            last_addr += 1

    def _get_value_at(self, addr: int):
        return self.memory[addr]

    def _fetch_instruction(self) -> int:
        return self.memory[self.PC]

    def _jns(self, target):
        self.MAR = target
        self.MBR = self.PC + 1
        self.memory[self.MAR] = self.MBR
        self.AC = target + 1
        self.PC = self.AC

    def _jump(self, target):
        self.PC = target

    def _load(self, target):
        self.MAR = target
        self.MBR = self._get_value_at(self.MAR)
        self.AC = self.MBR

    def _loadi(self, target):
        self.MAR = target
        self.MBR = self._get_value_at(self.MAR)
        self.MAR = self.MBR
        self.MBR = self._get_value_at(self.MAR)
        self.AC = self.MBR

    def _store(self, target):
        self.MAR = target
        self.MBR = self.AC
        self.memory[self.MAR] = self.MBR

    def _subt(self, target):
        self.MAR = target
        self.MBR = self._get_value_at(self.MAR)
        self.AC = self.AC - self.MBR

    def _add(self, target):
        self.MAR = target
        self.MBR = self._get_value_at(self.MAR)
        self.AC = self.AC + self.MBR

    def _addi(self, target):
        self.MAR = target
        self.MBR = self._get_value_at(self.MAR)
        self.MAR = self.MBR
        self.MBR = self._get_value_at(self.MAR)
        self.AC = self.AC + self.MBR

    def _subti(self, target):
        self.MAR = target
        self.MBR = self._get_value_at(self.MAR)
        self.MAR = self.MBR
        self.MBR = self._get_value_at(self.MAR)
        self.AC = self.AC - self.MBR

    def _skipcond(self, target):
        ac = self.AC
        skipnext = (target == 0 and ac < 0
                    or target == 400 and ac == 0
                    or target == 800 and ac > 0)
        if skipnext:
            self.PC += 1

    def _halt(self, target):
        self.running = False

    def _get_action(self, opcode: int) -> Callable:
        if opcode == 0x0:
            return self._jns
        if opcode == 0x1:
            return self._load
        if opcode == 0x2:
            return self._store
        if opcode == 0x4:
            return self._subt
        if opcode == 0x7:
            return self._halt
        if opcode == 0x8:
            return self._skipcond