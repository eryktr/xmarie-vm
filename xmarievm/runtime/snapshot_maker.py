from dataclasses import dataclass
from typing import List

from xmarievm.runtime.streams.output_stream import OutputStream


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


def make_snapshot(vm: 'MarieVm') -> Snapshot:
    snapshot_data = {attr: getattr(vm, attr) for attr in Snapshot.__annotations__}
    return Snapshot(**snapshot_data)
