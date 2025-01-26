import argparse
from typing import List
import re


def test_constraint(constraint: str, line: str) -> bool:
    operator: str = re.search(r"[A-Z]+", constraint).group(0)
    [column_index, column_value] = constraint.split(operator)
    column_index: int = int(column_index)
    column_value: int = int(column_value)

    if operator == "EQ":
        return int(line.split(",")[column_index]) == column_value
    elif operator == "LT":
        return int(line.split(",")[column_index]) < column_value
    elif operator == "GT":
        return int(line.split(",")[column_index]) > column_value
    else:
        print(f"Error: unsupported constraint operator: {operator}")
        exit(1)


def cmp_csvs(csv1_path: str,
             csv2_path: str,
             primary_key_col_idx: int = 0,
             constraints: List[str] = [],
             ignore_header_row: bool = False):
    set1 = set()
    with open(csv1_path, 'r') as csv1:
        if ignore_header_row:
            next(csv1)
        for line in csv1:
            if all(test_constraint(constraint, line) for constraint in constraints):
                set1.add(line.split(",")[primary_key_col_idx])

    set2 = set()
    with open(csv2_path, 'r') as csv2:
        if ignore_header_row:
            next(csv2)
        for line in csv2:
            if all(test_constraint(constraint, line) for constraint in constraints):
                set2.add(line.split(",")[primary_key_col_idx])

    set_difference = set1.difference(set2)

    with open(csv1_path, 'r') as csv1:
        for line in csv1:
            if line.split(",")[primary_key_col_idx] in set_difference:
                print(line, end="")  # line already contains a line break!


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=r"Computes the set difference A \ B of two CSV files A.csv and B.csv."
    )

    # Positional arguments:
    parser.add_argument(
        "CSV1_PATH",
        type=str,
        help=r"Path to the first CSV file (the A in A \ B)."
    )
    parser.add_argument(
        "CSV2_PATH",
        type=str,
        help=r"Path to the second CSV file (the B in A \ B)."
    )

    # Optional positional arguments:
    parser.add_argument(
        "PRIMARY_KEY_COLUMN_INDEX",
        type=int,
        nargs='?',
        default=0,
        help="Index of the primary key column (0-based). If not provided, the 0-th column is used."
    )
    parser.add_argument(
        "CONSTRAINTS",
        type=str,
        nargs='*',
        default="",
        help="An optional list of constraints (enacted on both CSV input files). "
             "Supported operators: EQ, LT, GT. "
             "Example (value of 3rd column (0-based) shall be greater than zero): 3GT0"
    )

    # Optional flags:
    parser.add_argument(
        "--ignore-header-row",
        dest='ignore_header_row',
        action='store_true',
        help="Ignore the 0th row of both CSV input files."
    )

    # Parse arguments:
    args = parser.parse_args()

    cmp_csvs(csv1_path=args.CSV1_PATH,
             csv2_path=args.CSV2_PATH,
             primary_key_col_idx=args.PRIMARY_KEY_COLUMN_INDEX,
             constraints=args.CONSTRAINTS,
             ignore_header_row=args.ignore_header_row)
