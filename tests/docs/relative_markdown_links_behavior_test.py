#!/usr/bin/env python3
"""Exercise the checker through a synthetic file tree and process exit status."""

import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


CHECKER = Path(__file__).with_name("relative_markdown_links_test.py")


class MarkdownLinksTest(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory(prefix="crm-links-")
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.script = self.root / "tests/docs/relative_markdown_links_test.py"
        self.script.parent.mkdir(parents=True)
        shutil.copy2(CHECKER, self.script)
        subprocess.run(["git", "init", "-q", str(self.root)], check=True)
        (self.root / "README.md").write_text("# Start\n")
        subprocess.run(["git", "-C", str(self.root), "add", "."], check=True)

    def check(self, *args):
        return subprocess.run(
            [sys.executable, str(self.script), *args],
            capture_output=True, text=True, check=False,
        )

    def test_unstaged_and_new_documents_are_checked(self):
        (self.root / "README.md").write_text("# Start\n\n[Broken](missing.md)\n")
        (self.root / "new.md").write_text("# New\n\n[Broken](absent.md)\n")
        result = self.check()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("README.md:3", result.stdout + result.stderr)
        self.assertIn("new.md:3", result.stdout + result.stderr)

    def test_index_is_an_explicit_snapshot(self):
        (self.root / "README.md").write_text("# Start\n\n[Broken](missing.md)\n")
        result = self.check("--source", "index")
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_new_target_and_duplicate_unicode_heading(self):
        (self.root / "new.md").write_text("# Prüfung\n\n# Prüfung\n")
        (self.root / "README.md").write_text(
            "# Start\n\n[New](new.md#prüfung-1)\n"
        )
        self.assertEqual(self.check().returncode, 0)
        (self.root / "README.md").write_text("# Start\n\n[Wrong](new.md#prufung)\n")
        result = self.check()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("missing fragment", result.stdout + result.stderr)

    def test_heading_punctuation_preserves_adjacent_hyphens(self):
        (self.root / "README.md").write_text(
            "# Q10 – Übergang\n\n[Here](#q10--übergang)\n"
        )
        result = self.check()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
