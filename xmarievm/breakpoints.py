import re
from dataclasses import dataclass
from typing import List

from xmarievm.runtime.snapshot_maker import Snapshot


@dataclass
class Breakpoint:
    current_lineno: int
    original_lineno: int
    instr: str


@dataclass
class BreakpointHit:
    breakpoint: Breakpoint
    snapshot: Snapshot


def parse_breakpoints(breakpoints: List[int], code: str):
    new_breakpoints = []
    code_lines = code.split('\n')
    code_with_breakpoint_markers = []
    for lineno, line in enumerate(code_lines, start=1):
        if lineno in breakpoints:
            code_with_breakpoint_markers.append(f'{lineno}*{line}')
        else:
            code_with_breakpoint_markers.append(line)
    code_with_breakpoint_markers = '\n'.join(code_with_breakpoint_markers)
    cleaned_code = re.sub(r'\n+', '\n', code_with_breakpoint_markers)
    cleaned_code_lines = cleaned_code.split('\n')
    for lineno, line in enumerate(cleaned_code_lines, start=1):
        match = re.match(r'(\d+)\*(.*)$', line)
        if match:
            breakpoint = Breakpoint(current_lineno=lineno, original_lineno=int(match.group(1)), instr=match.group(2))
            new_breakpoints.append(breakpoint)
    return new_breakpoints
