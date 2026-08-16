#!/usr/bin/env python3
"""Validate a supplied branch name or the current Git branch."""

from __future__ import annotations

import argparse
import subprocess


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--branch", help="branch name to validate; defaults to the current Git branch")
    return parser.parse_args()


def current_branch() -> str:
    return subprocess.run(
        ["git", "branch", "--show-current"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def main() -> int:
    args = parse_args()
    branch = args.branch if args.branch is not None else current_branch()
    print(branch)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
