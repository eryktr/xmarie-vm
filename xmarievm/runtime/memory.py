import random
from typing import List


def uninitialized(size: int) -> List[int]:
    return [random.randint(0, 2 ** 16) for _ in range(size)]
