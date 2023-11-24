from typing import Optional
from .model import Cage, Cell, Kenken
from functools import reduce
from operator import mul


def isValid(kenken: Kenken, cell: Cell, value: int) -> bool:
    board = kenken.board
    for i in range(len(board)):
        if (board[cell.y][i] == value and i != cell.x) or (
            board[i][cell.x] == value and i != cell.y
        ):
            return False

    for cage in kenken.cages:
        if cell in cage.cells and cage.target:
            match cage.operation:
                case "=":
                    return board[cell.y][cell.x] == cage.target
                case "+":
                    return sum(board[c.y][c.x] for c in cage.cells) <= cage.target
                case "-":
                    values = [board[c.y][c.x] for c in cage.cells]
                    if values[0] == 0 or values[1] == 0:
                        return True
                    return abs(values[0] - values[1]) == cage.target
                case "*":
                    output = reduce(mul, [board[c.y][c.x] for c in cage.cells])
                    return output == 0 or output == cage.target
                case "/":
                    values = [board[c.y][c.x] for c in cage.cells]
                    if values[0] == 0 or values[1] == 0:
                        return True
                    return max(values) // min(values) == cage.target

    return True


def solve(kenken: Kenken, solutions: list[list[list[int]]]) -> bool:
    emptyCell = findEmptyCell(kenken)
    if not emptyCell:
        solutions.append(kenken.board)
        return True

    for value in range(1, len(kenken.board) + 1):
        kenken.board[emptyCell.y][emptyCell.x] = value

        if isValid(kenken, emptyCell, value) and solve(kenken, solutions):
            return True

        kenken.board[emptyCell.y][emptyCell.x] = 0

    return False


def findEmptyCell(kenken: Kenken):
    board = kenken.board
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == 0:
                return Cell(j, i)
    return None


def kenkenSolver(kenken: Kenken) -> Optional[list[list[int]]]:
    solutions = []
    solve(kenken, solutions)
    return solutions


# if __name__ == "__main__":
#     # solution = [[3, 2, 1, 4], [2, 1, 4, 3], [4, 3, 2, 1], [1, 4, 3, 2]]
#     example = Kenken(
#         board=[[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
#         cages=[
#             Cage(cells={Cell(x=2, y=2)}, operation="=", target=2),
#             Cage(
#                 cells={Cell(x=0, y=1), Cell(x=1, y=1), Cell(x=2, y=1), Cell(x=0, y=2)},
#                 operation="*",
#                 target=32,
#             ),
#             Cage(cells={Cell(x=1, y=0), Cell(x=0, y=0)}, operation="-", target=1),
#             Cage(
#                 cells={Cell(x=2, y=3), Cell(x=1, y=2), Cell(x=1, y=3), Cell(x=0, y=3)},
#                 operation="+",
#                 target=11,
#             ),
#             Cage(
#                 cells={Cell(x=3, y=1), Cell(x=3, y=2), Cell(x=2, y=0), Cell(x=3, y=0)},
#                 operation="+",
#                 target=9,
#             ),
#             Cage(cells={Cell(x=3, y=3)}, operation="=", target=2),
#         ],
#     )

#     solutions = kenkenSolver(example)

#     print(solutions)
