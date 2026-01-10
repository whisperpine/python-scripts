# /// script
# requires-python = ">=3.13"
# dependencies = []
# ///

"""
Convert a csv file to a markdown table.

This script takes a CSV file as input and converts it into a markdown table.
The markdown table is written to a new file with the same name as the input file,
but with a `.md` extension instead of `.csv`.

Usage:
    python csv_to_markdown CSV_FILE

This script originates from the following repo:
https://github.com/whisperpine/python-scripts

MIT License.
"""

import argparse
import csv
import itertools
import sys
from pathlib import Path

CSV_FILE = "CSV_FILE"


def parse_arg() -> dict[str, str]:
    """
    Parse command line arguments.

    Returns:
        dict[str, str]: arguments in key-value pairs.
    """
    parser = argparse.ArgumentParser(
        description="Convert a CSV file to a markdown table."
    )
    _ = parser.add_argument(CSV_FILE, help="the target CSV's file path")
    args: argparse.Namespace = parser.parse_args()
    return dict(args._get_kwargs())  # noqa: SLF001


def csv_to_markdown_table(csv_file: Path) -> str:
    """
    Convert a CSV file to a markdown table.

    Parameters:
        csv_file (str): The path to the CSV file to be converted.

    Returns:
        str: The markdown table as a string.
    """
    with csv_file.open() as file:
        reader = csv.reader(file)
        table: list[str] = []
        for i, row in enumerate(reader):
            stripped_row: list[str] = [item.strip() for item in row]
            table.append("| " + " | ".join(stripped_row) + " |")
            if i == 0:
                separators = itertools.repeat("-", len(stripped_row))
                table.append("| " + " | ".join(separators) + " |")
        return "\n".join(table)


def main() -> None:
    csv_file: Path = Path(parse_arg()[CSV_FILE])
    markdown_file: Path = Path(csv_file).with_suffix(".md")
    if not csv_file.exists():
        print(f"Error: No such file or directory: '{csv_file}'")
        sys.exit(1)
    if markdown_file.exists():
        user_input: str = (
            input(f"'{markdown_file}' exists. Do you want to overwrite it? (y/n): ")
            .lower()
            .strip()
        )
        if user_input not in ["yes", "y"]:
            print(
                f"'{markdown_file}' stays intact.",
                "If you intend to overwrite the existing one,",
                "run the command again and input 'y' after the prompt.",
            )
            sys.exit(1)
    with markdown_file.open("w") as f:
        f.write(csv_to_markdown_table(csv_file))


if __name__ == "__main__":
    main()
