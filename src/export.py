import argparse
from copy import deepcopy
import dataclasses
import datetime
import json

import tqdm
import logic
from logic.model import Kenken


def main(args):
    file_name = args.output_file
    start_date = datetime.date.today()
    with open(file_name, "w+") as f:
        puzzle_count = 0
        output = {"puzzles": []}
        with tqdm.tqdm(total=args.num_puzzles) as pbar:
            while puzzle_count < args.num_puzzles:
                # generate a random puzzle with two freebies
                # TODO: make this configurable
                puzzle = logic.generate(args.size, args.freebies)
                solutions = logic.kenkenSolver(
                    Kenken([[0] * args.size for _ in range(args.size)], puzzle.cages)
                )

                # check that there is only one solution
                if solutions and len(solutions) == 1:
                    puzzle_dict = dataclasses.asdict(puzzle, dict_factory=factory)

                    # add a date to each puzzle so that a user can complete one puzzle each day
                    # TODO: make start date configurable
                    puzzle_dict["date"] = start_date.strftime("%Y-%m-%d")
                    start_date += datetime.timedelta(days=1)
                    output["puzzles"].append(puzzle_dict)
                    puzzle_count += 1
                    pbar.update(1)
        json.dump(output, f)


def factory(data):
    if data[0][0] == "cells":
        cells = list(data[0][1])
        for i, cell in enumerate(list(data[0][1])):
            converted = dataclasses.asdict(cell)
            cells[i] = converted
        data[0] = ("cells", cells)
    return dict(data)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate multiple valid kenken_puzzles."
    )
    parser.add_argument(
        "--output_file", type=str, default="./output/4x4", help="File to write to."
    )
    parser.add_argument(
        "--num_puzzles", type=int, default=2, help="Number of puzzles to generate."
    )
    parser.add_argument(
        "--size",
        type=int,
        default=4,
        help="Size of the board. Default is 4.",
    )
    parser.add_argument(
        "--freebies",
        type=int,
        default=2,
        help="Number of freebies to generate. Default is 2.",
    )
    args = parser.parse_args()
    main(args)
