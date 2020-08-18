import abc
from typing import Generator


class InputStream(abc.ABC):
    @abc.abstractmethod
    def read(self) -> str:
        pass


class StandardInputStream(InputStream):
    def read(self) -> str:
        return input()


class BufferedInputStream(InputStream):
    stream: Generator[str, None, None]

    def __init__(self, txt: str):
        self.stream = (l for l in txt.strip().split('\n'))

    def read(self) -> str:
        return next(self.stream)
