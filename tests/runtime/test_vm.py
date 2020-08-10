from xmarievm.parsing.parser import parser
from xmarievm.runtime.input_stream import StandardInputStream
from xmarievm.runtime.vm import MarieVm


def test_parse_and_execute():
    code = '''\
Load X
Subt 20
Store 50
X, HEX 0x20
Skipcond 400
Halt
'''
    vm = MarieVm(memory=[0] * 1024, input_stream=StandardInputStream())
    program = parser.parse(code)
    vm.execute(program)
