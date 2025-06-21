# /// script
# requires-python = ">=3.13"
# dependencies = []
# ///

"""
Generate CHANGELOG.md according to current repo's git history.

Git commit messages must be in accordance with Conventional Commits:
https://www.conventionalcommits.org/en/v1.0.0/

The CHANGELOG.md format is inspired by the following initiative:
https://keepachangelog.com/en/1.1.0/

Usage:
    python keep_a_changelog.py

This script originates from the following repo:
https://github.com/whisperpine/python-scripts

MIT License.
"""

import os
import re
import subprocess
from dataclasses import dataclass


@dataclass
class CommitInfo:
    """
    A dataclass representing metadata for a git commit.

    Attributes:
        commit_hash (str): The full SHA-1 hash of the commit.
        message (str): The commit message, typically following Conventional Commits.
        date_str (str): The commit date in ISO format (YYYY-MM-DD).
        tags (list[str]): A list of tags associated with the commit,
            filtered to include only Semantic Versioning tags.
    """

    commit_hash: str
    message: str
    date_str: str
    tags: list[str]


def is_semver_tag(tag: str) -> bool:
    """
    Check if a string adheres to Semantic Versioning.

    Note: the prefix "v" is optional.
    """

    SEMVER_PATTERN = re.compile(
        r"^v?(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$"
    )
    return bool(SEMVER_PATTERN.match(tag))


def get_git_logs() -> list[str]:
    """
    Retrieve a list of git commits.

    Returns:
        list[str]: A list of str, each representing a git log line.

    Raises:
        subprocess.CalledProcessError: If the git command fails to execute.
    """
    try:
        # git log format: hash | message | date | tags
        LOG_FORMAT = "--pretty=format:%H|%s|%ad|%d"
        result = subprocess.run(
            ["git", "log", LOG_FORMAT, "--date=iso"],
            capture_output=True,
            text=True,
            check=True,
        )
    except subprocess.CalledProcessError as err:
        print(f"Error executing git command: {err}")
        raise err

    return result.stdout.strip().split("\n")


def parse_git_logs(lines: list[str]) -> list[CommitInfo]:
    """
    Parse raw git logs into structured data.

    Args:
        lines (list[str]): A list of str, each representing a git log line.

    Returns:
        list[CommitInfo]: A list of CommitInfo objects,
            each representing a commit with its metadata.

    Raises:
        ValueError: If the commit date string cannot be parsed into a datetime object.
    """
    from datetime import datetime

    commits: list[CommitInfo] = []
    for line in lines:
        if not line:
            continue

        # get separated parts of one line of git log
        parts = line.split("|")

        commit_hash: str = parts[0]
        message: str = parts[1]
        date_str: str = parts[2]
        tags: list[str] = []

        # process datetime
        try:
            commit_date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S %z")
        except ValueError as err:
            err.add_note(f"failed to parse '{date_str}' to datetime")
            raise err

        # process tags
        if len(parts) > 3 and parts[3]:
            tag_str = parts[3].strip()
            if tag_str:
                # remove parentheses and the prefix "tag: "
                tag_str = re.sub(r"^\s*\(|\)\s*$", "", tag_str)
                tags = [
                    tag.strip().replace("tag: ", "")
                    for tag in tag_str.split(",")
                    if tag.strip()
                ]
                # retain tags that match semantic versioning
                tags = [tag for tag in tags if is_semver_tag(tag)]

        commit_info = CommitInfo(
            commit_hash=commit_hash,
            message=message,
            date_str=str(commit_date.date()),
            tags=tags,
        )
        commits.append(commit_info)

    return commits


def print_commits(commits: list[CommitInfo]) -> None:
    """
    Print a list of CommitInfo.

    This function is for debugging purporse.
    """
    if not commits:
        print("No commits found or error occurred.")
        return
    for commit in commits:
        print(f"\nCommit: {commit.commit_hash[:8]}")
        print(f"Message: {commit.message}")
        print(f"Date: {commit.date_str}")
        if len(commit.tags) > 0:
            print(f"Tags: {', '.join(commit.tags)}")
        print("-" * 50)


def write_changelog(commits: list[CommitInfo]) -> None:
    """
    Write the changelog to a file.
    """

    if not commits:
        _ = print("No commits found or error occurred.")
        return

    changelog_path = os.path.join(get_git_root(), "CHANGELOG.md")
    with open(changelog_path, "w") as f:
        _ = f.write("# CHANGELOG\n\n")
        if len(commits[0].tags) == 0:
            _ = f.write("## Unreleased\n\n")
        for commit in commits:
            if len(commit.tags) > 0:
                heading = "\n## " + ",".join(commit.tags) + f" - {commit.date_str}\n\n"
                _ = f.write(heading)
            _ = f.write(f"- {commit.message}\n")


def get_git_root() -> str:
    """Return the absolute path of the repo's root directory."""
    git_root = (
        subprocess.check_output(
            ["git", "rev-parse", "--show-toplevel"], stderr=subprocess.STDOUT
        )
        .decode("utf-8")
        .strip()
    )
    return os.path.abspath(git_root)


def main() -> None:
    lines: list[str] = get_git_logs()
    commits: list[CommitInfo] = parse_git_logs(lines)
    # print_commits(commits)  # for debugging
    write_changelog(commits)


if __name__ == "__main__":
    main()
