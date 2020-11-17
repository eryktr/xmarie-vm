from builtins import str
from typing import List

import xmarievm.breakpoints as breakpoints_module
import xmarievm.preprocessing as preprocessing
from xmarievm.parsing import parser
from xmarievm.parsing.ast_types import Program
from xmarievm.runtime import snapshot_maker
from xmarievm.runtime.snapshot_maker import Snapshot
from xmarievm.runtime.streams.input_stream import BufferedInputStream
from xmarievm.runtime.vm import MarieVm


def run(code: str, debug: bool, input_=None, breakpoints=None) -> List[Snapshot]:
    vm = MarieVm.get_default()
    parsed_breakpoints = []
    if breakpoints:
        parsed_breakpoints = breakpoints_module.parse_breakpoints(breakpoints, code)
    if input_:
        istream = BufferedInputStream(input_)
        vm.input_stream = istream
    program = parser.parse(code)
    if debug:
        return vm.setup_debug(program, parsed_breakpoints, [])
    vm.execute(program, [])
    return [snapshot_maker.make_snapshot(vm)]


def parse_code(code: str) -> Program:
    return parser.parse(code)


def parse_breakpoints(code: str, breakpoints: List[int]) -> List[breakpoints_module.Breakpoint]:
    return breakpoints_module.parse_breakpoints(breakpoints, code)


def get_line_array(code: str) -> List[int]:
    return preprocessing.get_line_array(code)
