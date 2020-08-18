import abc
from typing import List


class OutputStream(abc.ABC):
    buf: List[str]

    def __init__(self):
        self.buf = []

    def write(self, txt) -> None:
        self.buf.append(txt)
