from collections import defaultdict
from typing import List, Callable, Dict, Optional

import xmarievm.parsing.ast_types as ast_types
from xmarievm.breakpoints import Breakpoint, BreakpointHit, StepHit
from xmarievm.const import MEM_BITSIZE
from xmarievm.parsing.ast_types import Program, get_instr_name_by_opcode
from xmarievm.runtime import snapshot_maker, memory
from xmarievm.runtime.decoder import decode_instruction
from xmarievm.runtime.snapshot_maker import Snapshot
from xmarievm.runtime.streams.input_stream import InputStream, BufferedInputStream
from xmarievm.runtime.streams.output_stream import OutputStream
from xmarievm.util import int_from_2c, int_in_2c_to_hex

MAX_NUM_OF_EXECUTED_INSTRS = 1_000_000

OPCODE_TO_COST = {
    ast_types.JnS.opcode: 4,
    ast_types.Load.opcode: 3,
    ast_types.Store.opcode: 3,
    ast_types.Add.opcode: 3,
    ast_types.Subt.opcode: 3,
    ast_types.Input.opcode: 2,
    ast_types.Output.opcode: 2,
    ast_types.Halt.opcode: 1,
    ast_types.Skipcond.opcode: 3,
    ast_types.Jump.opcode: 1,
    ast_types.Clear.opcode: 1,
    ast_types.AddI.opcode: 5,
    ast_types.ShiftL.opcode: 3,
    ast_types.ShiftR.opcode: 3,
    ast_types.SubtI.opcode: 5,
    ast_types.Incr.opcode: 1,
    ast_types.Decr.opcode: 1,
    ast_types.StoreI.opcode: 5,
    ast_types.JumpI.opcode: 5,
    ast_types.Push.opcode: 1,
    ast_types.Pop.opcode: 1,
    ast_types.LoadI.opcode: 5,
    ast_types.StoreX.opcode: 1,
    ast_types.StoreY.opcode: 1,
    ast_types.LoadX.opcode: 1,
    ast_types.LoadY.opcode: 1,
}


class MarieVm:
    AC: int
    X: int
    Y: int
    PC: int
    MAR: int
    MBR: int
    IR: int
    stack: List[int]
    memory: List[int]
    input_stream: InputStream
    output_stream: OutputStream
    running: bool

    cost_of_executed_instrs: int
    instr_to_call_count: Dict[str, int]

    num_of_executed_instrs: int
    breakpoints: List[Breakpoint]
    pc_to_breakpoint: Dict[int, Breakpoint]

    is_in_debug_mode: bool
    line_array: List[int]

    def __init__(
        self,
        memory: List[int],
        input_stream: InputStream,
        output_stream: OutputStream,
        stack: List[int],
        max_num_of_executed_instrs: int,
    ):
        self.AC = 0
        self.PC = 0
        self.X = 0
        self.Y = 0
        self.MAR = 0
        self.MBR = 0
        self.IR = 0
        self.cost_of_executed_instrs = 0
        self.instr_to_call_count = defaultdict(lambda: 0)

        self.memory = memory
        self.stack = stack
        self.input_stream = input_stream
        self.output_stream = output_stream
        self.running = False

        self.num_of_executed_instrs = 0
        self.max_num_of_executed_instrs = max_num_of_executed_instrs

        self.breakpoints = []
        self.pc_to_breakpoint = {}
        self.is_in_debug_mode = False
        self.line_array = []

    @classmethod
    def get_default(cls) -> 'MarieVm':
        return cls(
            memory=memory.uninitialized(1024),
            input_stream=BufferedInputStream(''),
            output_stream=OutputStream(),
            stack=[],
            max_num_of_executed_instrs=MAX_NUM_OF_EXECUTED_INSTRS
        )

    @property
    def AC(self):
        return self._AC

    @AC.setter
    def AC(self, val):
        self._AC = int_from_2c(val, MEM_BITSIZE)

    def execute(self, program: Program) -> None:
        self._load_into_memory(program)
        self.running = True
        while self.running:
            self.step()

    def setup_debug(self, program: Program, breakpoints: List[Breakpoint], line_array: List[int]):
        self.pc_to_breakpoint = {
            b.current_lineno - 1: b
            for b in breakpoints
        }
        self.running = True
        self.is_in_debug_mode = True
        self._load_into_memory(program)
        self.line_array = line_array

    def hit_breakpoint(self) -> Optional[BreakpointHit]:
        while self.running:
            if self.PC in self.pc_to_breakpoint:
                hit = BreakpointHit(self.pc_to_breakpoint[self.PC], snapshot_maker.make_snapshot(self))
                self.step()
                return hit
            self.step()
        self.is_in_debug_mode = False

    def step(self) -> StepHit:
        if self.num_of_executed_instrs > self.max_num_of_executed_instrs:
            raise TimeoutError(f'Maximum number of executed instructions exceeded')
        instr = self._fetch_instruction()
        self.IR = instr
        decoded_instr = decode_instruction(instr)
        opcode = decoded_instr.opcode
        action = self._get_action(opcode)
        action(decoded_instr.arg)
        self.PC += 1
        if self.PC in self.pc_to_breakpoint:
            print(f'Breakpoints reached! {self.pc_to_breakpoint[self.PC]}')
        self.num_of_executed_instrs += 1
        self.cost_of_executed_instrs += OPCODE_TO_COST[opcode]
        instr_name = get_instr_name_by_opcode(opcode)
        self.instr_to_call_count[instr_name] += 1
        snapshot = snapshot_maker.make_snapshot(self)
        curr_lineno = self._get_lineno()
        return StepHit(current_lineno=curr_lineno, original_lineno=self.line_array[curr_lineno], snapshot=snapshot)

    def setup_with(self, program: Program):
        self._load_into_memory(program)

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
        self.PC = self.AC - 1

    def _jump(self, target):
        """
        PC increases automatically after each instr, -1 ensures instr jumped to gets executed
        """
        self.PC = target - 1

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

    def _storei(self, target):
        self.MAR = target
        self.MBR = self._get_value_at(self.MAR)
        self.MAR = self.MBR
        self.MBR = self._get_value_at(self.MAR)
        self.memory[self.MBR] = self.AC

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

    def _shiftl(self, target):
        self.MAR = target
        self.MBR = self._get_value_at(self.MAR)
        self.AC = self.AC << self.MBR

    def _shiftr(self, target):
        self.MAR = target
        self.MBR = self._get_value_at(self.MAR)
        self.AC = self.AC >> self.MBR

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

    def _jumpi(self, target):
        self.MAR = target
        self.MBR = self._get_value_at(self.MAR)
        self.PC = self.MBR - 1  # PC increases by one per each instruction

    def _incr(self, target):
        self.AC += 1

    def _decr(self, target):
        self.AC -= 1

    def _clear(self, target):
        self.AC = 0

    def _input(self, target):
        val = self.input_stream.read()
        self.AC = int_from_2c(int(val, 16), MEM_BITSIZE)

    def _output(self, target):
        self.output_stream.write(int_in_2c_to_hex(self.AC, MEM_BITSIZE))

    def _skipcond(self, target):
        ac = self.AC
        skipnext = (target == 0 and ac < 0
                    or target == 400 and ac == 0
                    or target == 800 and ac > 0)
        if skipnext:
            self.PC += 1

    def _halt(self, target):
        self.running = False

    def _push(self, target):
        self.stack.insert(0, self.AC)

    def _pop(self, target):
        self.stack.pop(0)

    def _loadx(self, target):
        self.AC = self.X

    def _loady(self, target):
        self.AC = self.Y

    def _storex(self, target):
        self.X = self.AC

    def _storey(self, target):
        self.Y = self.AC

    def _get_action(self, opcode: int) -> Callable:
        if opcode == ast_types.JnS.opcode:
            return self._jns
        if opcode == ast_types.Load.opcode:
            return self._load
        if opcode == ast_types.Store.opcode:
            return self._store
        if opcode == ast_types.Add.opcode:
            return self._add
        if opcode == ast_types.Subt.opcode:
            return self._subt
        if opcode == ast_types.Input.opcode:
            return self._input
        if opcode == ast_types.Output.opcode:
            return self._output
        if opcode == ast_types.Halt.opcode:
            return self._halt
        if opcode == ast_types.Skipcond.opcode:
            return self._skipcond
        if opcode == ast_types.Jump.opcode:
            return self._jump
        if opcode == ast_types.Clear.opcode:
            return self._clear
        if opcode == ast_types.AddI.opcode:
            return self._addi
        if opcode == ast_types.ShiftL.opcode:
            return self._shiftl
        if opcode == ast_types.ShiftR.opcode:
            return self._shiftr
        if opcode == ast_types.SubtI.opcode:
            return self._subti
        if opcode == ast_types.Incr.opcode:
            return self._incr
        if opcode == ast_types.Decr.opcode:
            return self._decr
        if opcode == ast_types.StoreI.opcode:
            return self._storei
        if opcode == ast_types.JumpI.opcode:
            return self._jumpi
        if opcode == ast_types.Push.opcode:
            return self._push
        if opcode == ast_types.Pop.opcode:
            return self._pop
        if opcode == ast_types.LoadI.opcode:
            return self._loadi
        if opcode == ast_types.StoreX.opcode:
            return self._storex
        if opcode == ast_types.StoreY.opcode:
            return self._storey
        if opcode == ast_types.LoadX.opcode:
            return self._loadx
        if opcode == ast_types.LoadY.opcode:
            return self._loady

    def _get_lineno(self):
        return self.PC
