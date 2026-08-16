#!/usr/bin/env python3
"""Behavioral tests for branch_name_check.py."""

from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "branch_name_check.py"


class BranchNameCheckTests(unittest.TestCase):
    def run_checker(self, *args: str, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), *args],
            cwd=cwd or ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

    def test_accepts_supported_branch_names(self) -> None:
        for branch in (
            "main",
            "master",
            "feat/branch-name-check",
            "fix/issue-42",
            "chore/python-demo",
            "epic/python-demo",
            "release/v1-0",
        ):
            with self.subTest(branch=branch):
                result = self.run_checker("--branch", branch)
                self.assertEqual(result.returncode, 0)
                self.assertIn(f"ok: {branch}", result.stdout)
                self.assertEqual(result.stderr, "")

    def test_rejects_invalid_branch_names(self) -> None:
        for branch in ("", "Feat/foo", "feat/", "feature/foo", "feat/foo_bar", "feat/foo/bar"):
            with self.subTest(branch=branch):
                result = self.run_checker("--branch", branch)
                self.assertEqual(result.returncode, 1)
                self.assertIn("FAIL: invalid branch name", result.stderr)
                self.assertEqual(result.stdout, "")

    def test_reads_current_branch_when_argument_is_omitted(self) -> None:
        result = self.run_checker()
        self.assertEqual(result.returncode, 0)
        self.assertIn("ok: feat/issue-14-branch-name-check", result.stdout)
        self.assertEqual(result.stderr, "")

    def test_reports_git_read_failure_with_exit_two(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            result = self.run_checker(cwd=Path(directory))
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")
        self.assertIn("FAIL: unable to determine current branch", result.stderr)


if __name__ == "__main__":
    unittest.main()
