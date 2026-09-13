#!/usr/bin/env python3
"""Historical docs are photos: add a new dated file, never edit an old one."""

from pathlib import Path
import subprocess
import tempfile
import unittest


REPO_ROOT = Path(__file__).resolve().parents[2]

LOCKED_PREFIXES = (
    "docs/reviews/",
    "docs/worklogs/",
    "docs/handoffs/",
    "docs/research/",
)

# Keep in sync with the lint-skip set in scripts/check-local.sh.
LOCKED_FILES = {
    "docs/discovery/crm-schema-static-analysis.md",
    "docs/discovery/crm-auth-schema-static-analysis.md",
    "docs/discovery/security-read-only-discovery-preflight.md",
    "docs/discovery/gate-b-change-matrix.md",
    "docs/discovery/gate-b1-approval-text.md",
    "docs/research/berufssuchprofile-q8-4-2.md",
    "docs/research/2026-09-11-plan-best-practice-verification.md",
    "docs/reviews/2026-09-11-project-plan-audit.md",
    "docs/reviews/decision-reconstruction-audit-prompt.md",
    "docs/reviews/decision-reconstruction-audit.md",
    "docs/reviews/decision-reconstruction-corrections.md",
    "docs/worklogs/2026-09-11-automation-plan-adoption.md",
    "docs/worklogs/2026-09-11-security-read-only-discovery-gate.md",
}


def is_locked(path: str) -> bool:
    posix = path.replace("\\", "/")
    if posix in LOCKED_FILES:
        return True
    return posix.startswith(LOCKED_PREFIXES)


def forbidden_changes(repo: Path) -> list[str]:
    result = subprocess.run(
        [
            "git",
            "-C",
            str(repo),
            "diff",
            "--diff-filter=MDR",
            "--name-only",
            "HEAD",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    changed = {
        line.strip().replace("\\", "/")
        for line in result.stdout.splitlines()
        if line.strip()
    }
    return sorted(path for path in changed if is_locked(path))


class HistoricalAppendOnlyTest(unittest.TestCase):
    def setUp(self) -> None:
        self.directory = tempfile.TemporaryDirectory(prefix="crm-hist-")
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        subprocess.run(["git", "init", "-q", str(self.root)], check=True)
        subprocess.run(
            ["git", "-C", str(self.root), "config", "user.email", "test@example.com"],
            check=True,
        )
        subprocess.run(
            ["git", "-C", str(self.root), "config", "user.name", "Test"],
            check=True,
        )
        worklog = self.root / "docs/worklogs/2026-09-11-old.md"
        worklog.parent.mkdir(parents=True)
        worklog.write_text("# Old\n", encoding="utf-8")
        frozen = self.root / "docs/discovery/crm-schema-static-analysis.md"
        frozen.parent.mkdir(parents=True)
        frozen.write_text("# Frozen\n", encoding="utf-8")
        project = self.root / "docs/project.md"
        project.parent.mkdir(parents=True, exist_ok=True)
        project.write_text("# Live\n", encoding="utf-8")
        subprocess.run(["git", "-C", str(self.root), "add", "."], check=True)
        subprocess.run(
            ["git", "-C", str(self.root), "commit", "-qm", "seed"],
            check=True,
        )

    def test_new_worklog_is_allowed(self) -> None:
        path = self.root / "docs/worklogs/2026-09-13-new.md"
        path.write_text("# New\n", encoding="utf-8")
        subprocess.run(["git", "-C", str(self.root), "add", str(path)], check=True)
        self.assertEqual(forbidden_changes(self.root), [])

    def test_edit_worklog_is_blocked(self) -> None:
        path = self.root / "docs/worklogs/2026-09-11-old.md"
        path.write_text("# Changed\n", encoding="utf-8")
        self.assertEqual(
            forbidden_changes(self.root),
            ["docs/worklogs/2026-09-11-old.md"],
        )

    def test_edit_project_md_is_allowed(self) -> None:
        path = self.root / "docs/project.md"
        path.write_text("# Updated live status\n", encoding="utf-8")
        self.assertEqual(forbidden_changes(self.root), [])

    def test_edit_frozen_discovery_is_blocked(self) -> None:
        path = self.root / "docs/discovery/crm-schema-static-analysis.md"
        path.write_text("# Rewritten\n", encoding="utf-8")
        self.assertEqual(
            forbidden_changes(self.root),
            ["docs/discovery/crm-schema-static-analysis.md"],
        )

    def test_this_repo_has_no_locked_edits(self) -> None:
        violations = forbidden_changes(REPO_ROOT)
        self.assertEqual(
            violations,
            [],
            "do not edit historical files; add a new dated file instead: "
            + ", ".join(violations),
        )

    def test_locked_files_match_check_local_frozen_set(self) -> None:
        text = (REPO_ROOT / "scripts/check-local.sh").read_text(encoding="utf-8")
        start = text.index("frozen = {")
        end = text.index("}", start)
        quoted = {
            line.strip().strip(",").strip("'").strip('"')
            for line in text[start:end].splitlines()
            if ".md" in line
        }
        self.assertEqual(quoted, LOCKED_FILES)


if __name__ == "__main__":
    unittest.main()
