import argparse
import dataclasses
import datetime
import json
import logic


def main(args):
    file_name = args.output_file
    start_date = datetime.date.today()
    with open(file_name, "w+") as f:
        puzzle_count = 0
        output = {"puzzles": []}
        print(args.num_puzzles)
        while puzzle_count < args.num_puzzles:
            puzzle = logic.generate(args.size, 2)
            solutions = logic.kenkenSolver(puzzle)
            if solutions and len(solutions) == 1:
                puzzle_dict = dataclasses.asdict(puzzle, dict_factory=factory)
                puzzle_dict["date"] = start_date.strftime("%Y-%m-%d")
                start_date += datetime.timedelta(days=1)
                output["puzzles"].append(puzzle_dict)
                puzzle_count += 1
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
    parser.add_argument("output_file", type=str, help="File to write to.")
    parser.add_argument("num_puzzles", type=int, help="Number of puzzles to generate.")
    parser.add_argument(
        "--size",
        type=int,
        default=4,
        help="Size of the board. Default is 4.",
    )
    args = parser.parse_args()
    main(args)
