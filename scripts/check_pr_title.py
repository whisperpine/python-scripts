# /// script
# requires-python = ">=3.13"
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

ENV_VAR_NAME = "PR_TITLE"


def print_in_red(text: str) -> None:
    """Print text in red color."""
    print(f"\033[91m{text}\033[0m")


def is_ascii(text: str) -> bool:
    """Check if input text contains only ASCII chars."""
    ascii_chars: re.Pattern[str] = re.compile(r"[^\x00-\x7F]")
    non_ascii_chars: list[str] = ascii_chars.findall(text)

    if non_ascii_chars:
        non_ascii_chars: set[str] = set(dict.fromkeys(non_ascii_chars))
        print_in_red(f"error: non-ASCII chars found: {non_ascii_chars}")
        return False
    return True


def main() -> None:
    mr_title: str | None = os.environ.get(ENV_VAR_NAME)
    if not mr_title:
        print_in_red(f"error: cannot get env var {ENV_VAR_NAME}")
        sys.exit(1)
    elif not is_ascii(mr_title):
        sys.exit(1)


if __name__ == "__main__":
    main()
