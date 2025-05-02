# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///

"""
Check if the Pull Request's title consists of only ascii character.

This script is intended to be used in GitHub Actions.
The Pull Request's title is captured by "PR_TITLE" env var.

Usage:
    python check_pr_title

This script originates from the following repo:
https://github.com/whisperpine/check_pr_title

MIT License.
"""

import os
import re
import sys


def print_in_red(text: str) -> None:
    """Print text in red color."""
    print(f"\033[91m{text}\033[0m")


def check_character_set(text: str) -> bool:
    """Check if input text contains only ASCII chars."""
    ascii_chars = re.compile(r"[^\x00-\x7F]")
    non_ascii_chars = ascii_chars.findall(text)

    if non_ascii_chars:
        non_ascii_chars = list(dict.fromkeys(non_ascii_chars))
        print_in_red(f"error: non-ASCII chars found: {non_ascii_chars}")
        return False
    return True


def check_pr_title():
    ENV_VAR_NAME = "PR_TITLE"
    mr_title = os.environ.get(ENV_VAR_NAME)
    if mr_title is None:
        print_in_red(f"error: cannot get env var {ENV_VAR_NAME}")
        exit(1)

    title_valid = check_character_set(mr_title)
    if not title_valid:
        sys.exit(1)


if __name__ == "__main__":
    check_pr_title()
