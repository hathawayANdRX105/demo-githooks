#!/usr/bin/env python3
"""Validate a supplied branch name or the current Git branch."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--branch", help="branch name to validate; defaults to the current Git branch")
    return parser.parse_args()


def current_branch() -> str:
    result = subprocess.run(
        ["git", "branch", "--show-current"],
        check=True,
        capture_output=True,
        text=True,
    )
    branch = result.stdout.strip()
    if not branch:
        raise RuntimeError("Git has no current branch")
    return branch


BRANCH_PATTERN = re.compile(r"^(?:main|master|(?:feat|fix|chore|epic|release)/[a-z0-9]+(?:-[a-z0-9]+)*)$")


def is_valid_branch_name(branch: str) -> bool:
    return BRANCH_PATTERN.fullmatch(branch) is not None


def main() -> int:
    args = parse_args()
    if args.branch is None:
        try:
            branch = current_branch()
        except (OSError, RuntimeError, subprocess.CalledProcessError):
            print("FAIL: unable to determine current branch", file=sys.stderr)
            return 2
    else:
        branch = args.branch

    if not is_valid_branch_name(branch):
        print(f"FAIL: invalid branch name: {branch}", file=sys.stderr)
        return 1

    print(f"ok: {branch}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
