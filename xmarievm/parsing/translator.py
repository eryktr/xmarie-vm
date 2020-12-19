"""
Translates the Abstract Syntax Tree into machine code
"""
from typing import List, Dict

from xmarievm.parsing.ast_types import Instruction
from xmarievm.parsing.parser import ParsingError


def translate(instructions: List[Instruction], labels: Dict[str, int]) -> List[int]:
    encoded_instructions = []
    for i in instructions:
        if isinstance(i.arg, str):
            try:
                i.arg = labels[i.arg]
            except KeyError:
                raise ParsingError(f'Undefined label: {i.arg}')
        encoded_instructions.append(i.translate())
    return encoded_instructions
