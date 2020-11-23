from dataclasses import dataclass
from typing import List, Dict
from copy import deepcopy
from xmarievm.runtime.streams.output_stream import OutputStream

IGNORED_ATTRS = 'variables'


@dataclass
class Snapshot:
    AC: int
    X: int
    Y: int
    PC: int
    MAR: int
    MBR: int
    IR: int
    stack: List[int]
    memory: List[int]
    output_stream: OutputStream
    running: bool
    lineno_to_num_calls: Dict[int, int]
    instr_to_call_count: Dict[str, int]
    cost_of_executed_instrs: int
    variables: Dict[str, int]


def make_snapshot(vm: 'MarieVm') -> Snapshot:
    snapshot_data = {attr: deepcopy(getattr(vm, attr)) for attr in Snapshot.__annotations__ if
                     attr not in IGNORED_ATTRS}
    snapshot_data['variables'] = {var: vm.memory[addr] for var, addr in vm.label_to_mem_addr.items()}
    return Snapshot(**snapshot_data)
