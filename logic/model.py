from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Cell:
    x: int
    y: int

    def __lt__(self, other):
        return self.x < other.x and self.y < other.y


@dataclass
class Cage:
    cells: set[Cell]
    operation: str
    target: Optional[int] = None


@dataclass
class Kenken:
    board: list
    cages: list[Cage]
