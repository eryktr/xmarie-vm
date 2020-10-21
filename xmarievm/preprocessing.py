from typing import List


def get_line_array(code: str) -> List[int]:
    """
    Index represents the new line number,
    values represents the old line number
    """
    code_lines = code.split('\n')
    return [num + 1 for num, line in enumerate(code_lines) if line]
