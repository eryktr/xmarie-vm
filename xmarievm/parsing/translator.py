"""
Translates the Abstract Syntax Tree into machine code
"""
from typing import List, Dict

from xmarievm.parsing.ast_types import Instruction


def translate(instructions: List[Instruction], labels: Dict[str, int]) -> List[int]:
    encoded_instructions = []
    for i in instructions:
        if isinstance(i.arg, str):
            try:
                i.arg = labels[i.arg]
            except KeyError:
                raise ValueError(f'Undefined label: {i.arg}')
        encoded_instructions.append(i.translate())
    return encoded_instructions
