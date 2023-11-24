import random
from itertools import product
from copy import deepcopy

from .model import Cage, Cell, Kenken


def generate(size, freebies) -> Kenken:
    # initialise board
    kenken = Kenken(
        [[((x + i) % size) + 1 for x in range(0, size)] for i in range(0, size)], []
    )

    # shuffle board
    kenken.board = twoDimensionalShuffle(kenken.board)

    # add freebie cages
    addFreeCells(kenken, freebies, size, size)

    # cage adding loop
    fillCages(kenken)

    return kenken


def twoDimensionalShuffle(board: list[list[int]]):
    random.shuffle(board)

    shuffleCoords = list(range(0, len(board[0])))
    random.shuffle(shuffleCoords)

    copy = deepcopy(board)
    for x in range(len(board)):
        for y in range(len(board)):
            copy[y][shuffleCoords[x]] = board[y][x]
    return copy


def addFreeCells(kenken: Kenken, count: int, xSize: int, ySize: int):
    offset = random.randint(1, xSize * ySize)
    for c in range(1, count + 1):
        x = ((offset * c) - 1) % xSize
        y = (((offset * c) - 1) // xSize) % ySize
        kenken.cages.append(Cage(set([Cell(x, y)]), "=", target=kenken.board[y][x]))


def fillCages(kenken: Kenken):
    while True:
        freeCell = firstFreeCell(kenken)
        if freeCell:
            cage = makeCage(kenken, freeCell)
            kenken.cages.append(cage)
        else:
            break


def firstFreeCell(kenken: Kenken):
    cells = availableCells(kenken)
    if len(cells) > 0:
        cell = sorted(cells)[0]
        return cell
    else:
        return None


def availableCells(kenken: Kenken):
    availableCells = list(product(range(len(kenken.board)), range(len(kenken.board))))
    availableCells = set(map(lambda t: Cell(t[0], t[1]), availableCells))
    cages = kenken.cages
    for cage in cages:
        for cell in cage.cells:
            availableCells.discard(cell)
    return list(availableCells)


def makeCage(kenken: Kenken, freeCell: Cell) -> Cage:
    maxSize = 4
    targetSize = random.randint(2, maxSize)
    cageNeighbors: set[Cell] = validMultiNeighbors(kenken, set([freeCell]))
    cells: set[Cell] = set([freeCell])

    while len(cells) < targetSize and len(cageNeighbors) > 0:
        chosen = random.choice(list(cageNeighbors))
        cells.add(chosen)
        cageNeighbors = validMultiNeighbors(kenken, cells).difference(cells)

    validOps = validOperations(kenken.board, cells)
    op = random.choice(list(validOps))
    target = makeTarget(kenken, cells, op)
    return Cage(cells=cells, operation=op, target=target)


def makeTarget(kenken: Kenken, cells: set[Cell], operation: str):
    target = 0
    if operation == "+":
        for cell in cells:
            target += kenken.board[cell.y][cell.x]
    elif operation == "*":
        target = 1
        for cell in cells:
            target *= kenken.board[cell.y][cell.x]
    elif operation == "-":
        orderedCells = list(cells)
        cell1 = kenken.board[orderedCells[0].y][orderedCells[0].x]
        cell2 = kenken.board[orderedCells[1].y][orderedCells[1].x]
        target = abs(cell1 - cell2)
    elif operation == "/":
        orderedCells = list(cells)
        cell1 = kenken.board[orderedCells[0].y][orderedCells[0].x]
        cell2 = kenken.board[orderedCells[1].y][orderedCells[1].x]
        target = max(cell1, cell2) // min(cell1, cell2)
    else:
        orderedCells = list(cells)
        target = kenken.board[orderedCells[0].y][orderedCells[0].x]
    return target


def validOperations(board: list[list[int]], cells: set[Cell]) -> set[str]:
    n = len(cells)
    if n == 1:
        return set(["="])
    if n == 2:
        ordered = list(cells)
        larger = max(
            board[ordered[0].y][ordered[0].x], board[ordered[1].y][ordered[1].x]
        )
        smaller = min(
            board[ordered[0].y][ordered[0].x], board[ordered[1].y][ordered[1].x]
        )
        if larger % smaller == 0:
            return set(["+", "-", "*", "/"])
        return set(["+", "-", "*"])
    else:
        return set(["+", "*"])


def validMultiNeighbors(kenken: Kenken, cells: set[Cell]) -> set[Cell]:
    neighs = multiNeighbors(cells, len(kenken.board))
    avail = availableCells(kenken)
    validNeighs = neighs.intersection(avail)
    return validNeighs


def multiNeighbors(cells: set[Cell], size: int) -> set[Cell]:
    output = set()
    for cell in cells:
        cellNeighbors = neighbors(cell, size)
        output.update(cellNeighbors)
    return output


def neighbors(cell: Cell, size: int) -> set[Cell]:
    neighbors = set()
    if cell.x > 0:
        neighbors.add(Cell(cell.x - 1, cell.y))
    if cell.x < size - 1:
        neighbors.add(Cell(cell.x + 1, cell.y))
    if cell.y > 0:
        neighbors.add(Cell(cell.x, cell.y - 1))
    if cell.y < size - 1:
        neighbors.add(Cell(cell.x, cell.y + 1))
    return neighbors
