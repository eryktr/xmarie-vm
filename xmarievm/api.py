from typing import List

from xmarievm.parsing import parser
from xmarievm.runtime import snapshot_maker
from xmarievm.runtime.snapshot_maker import Snapshot
from xmarievm.runtime.vm import MarieVm


def run(code: str, debug: bool) -> List[Snapshot]:
    vm = MarieVm.get_default()
    program = parser.parse(code)
    if debug:
        return vm.debug(program)
    vm.execute(program)
    return [snapshot_maker.make_snapshot(vm)]
