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

CSV_FILE = "CSV_FILE"


def main() -> None:
    import os
    import sys

    csv_file = parse_arg()[CSV_FILE]
    markdown_file = os.path.splitext(csv_file)[0] + ".md"
    if os.path.exists(csv_file) == False:
        print(f"Error: No such file or directory: '{csv_file}'")
        sys.exit(1)
    if os.path.exists(markdown_file):
        user_input = (
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
    with open(markdown_file, "w") as f:
        _ = f.write(csv_to_markdown_table(csv_file))


def parse_arg() -> dict[str, str]:
    """
    Parse command line arguments.

    Returns:
        dict[str, str]: arguments in key-value pairs.
    """
    import argparse

    parser = argparse.ArgumentParser(
        description="Convert a CSV file to a markdown table."
    )
    _ = parser.add_argument(CSV_FILE, help="the target CSV's file path")
    args = parser.parse_args()
    return dict(args._get_kwargs())


def csv_to_markdown_table(csv_file: str) -> str:
    """
    Convert a CSV file to a markdown table.

    Parameters:
        csv_file (str): The path to the CSV file to be converted.

    Returns:
        str: The markdown table as a string.
    """
    with open(csv_file, "r") as file:
        import csv
        from itertools import repeat

        reader = csv.reader(file)
        table: list[str] = []
        for i, row in enumerate(reader):
            row = [item.strip() for item in row]
            table.append("| " + " | ".join(row) + " |")
            if i == 0:
                separators = repeat("-", len(row))
                table.append("| " + " | ".join(separators) + " |")
        return "\n".join(table)


if __name__ == "__main__":
    main()
