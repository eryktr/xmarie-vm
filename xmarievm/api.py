from typing import List

from xmarievm.parsing import parser
from xmarievm.runtime import snapshot_maker
from xmarievm.runtime.snapshot_maker import Snapshot
from xmarievm.runtime.streams.input_stream import BufferedInputStream
from xmarievm.runtime.vm import MarieVm


def run(code: str, debug: bool, input_=None) -> List[Snapshot]:
    vm = MarieVm.get_default()
    if input_:
        istream = BufferedInputStream(input_)
        vm.input_stream = istream
    program = parser.parse(code)
    if debug:
        return vm.debug(program)
    vm.execute(program)
    return [snapshot_maker.make_snapshot(vm)]
