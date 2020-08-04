"""
Translates the Abstract Syntax Tree into machine code
"""
from typing import List

from xmarievm.parsing.ast_types import Instruction


def translate(instructions: List[Instruction]) -> List[int]:
    return [int(i.to_hex(), 16) for i in instructions]
