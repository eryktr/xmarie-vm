"""
Translates the Abstract Syntax Tree into machine code
"""
from builtins import str
from typing import List

from xmarievm.parsing.ast_types import Instruction


def translate(instructions: List[Instruction]) -> List[str]:
    return [i.to_binary() for i in instructions]
