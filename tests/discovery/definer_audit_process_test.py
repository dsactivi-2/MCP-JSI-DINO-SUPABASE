#!/usr/bin/env python3
"""Verify bounded collection and process cleanup using synthetic children."""

import os
from pathlib import Path
import runpy
import sys
import tempfile
import time
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/discovery"))
COLLECT = runpy.run_path(str(ROOT / "scripts/discovery/check-public-definers.py"))["collect"]


class ProcessTest(unittest.TestCase):
    def test_diagnostic_errors_emit_only_fixed_classes(self):
        cases = [
            ("psql: error: private_host password authentication failed for private_user",
             "authentication_failed"),
            ("ERROR:  42501\nCONTEXT: private_source", "catalog_privilege_denied"),
            ("psql: private unknown error", "unclassified"),
        ]
        for message, expected in cases:
            with self.subTest(expected=expected):
                with self.assertRaisesRegex(ValueError, "^audit failure " + expected + "$"):
                    COLLECT([sys.executable, "-c", "import sys; sys.stderr.write(" +
                             repr(message) + "); sys.exit(2)"], {}, "", diagnose=True, timeout=2)

    def test_selector_failure_cannot_leave_a_started_child(self):
        with mock.patch("selectors.DefaultSelector", side_effect=OSError("synthetic")), \
                mock.patch("subprocess.Popen") as start:
            with self.assertRaises(OSError):
                COLLECT(["unused"], {}, "query")
            start.assert_not_called()

    def test_collects_one_complete_response(self):
        self.assertEqual(COLLECT([sys.executable, "-c",
                                  "import sys; sys.stdout.write(sys.stdin.read())"],
                                 {}, "synthetic", limit=10, timeout=2), b"synthetic")

    def test_query_larger_than_pipe_capacity_is_fully_delivered(self):
        query = "synthetic query\n" * 10000
        output = COLLECT([sys.executable, "-c",
                          "import sys,time; time.sleep(0.05); "
                          "print(len(sys.stdin.read()))"], {}, query, diagnose=True, timeout=2)
        self.assertEqual(output.strip(), str(len(query)).encode())

    def test_failure_stderr_and_stdout_are_not_reported(self):
        with self.assertRaisesRegex(ValueError, "^audit process failed$"):
            COLLECT([sys.executable, "-c",
                     "import sys; print('private'); print('private',file=sys.stderr); sys.exit(2)"],
                    {}, "", timeout=2)

    def test_output_flood_and_blocked_child_are_killed(self):
        for code, limit, timeout in [("os.write(1,b'x'*10000); time.sleep(30)", 128, 2),
                                     ("time.sleep(30)", 128, 0.3)]:
            with self.subTest(code=code), tempfile.TemporaryDirectory() as directory:
                pidfile = Path(directory) / "pid"
                script = ("import os,time; from pathlib import Path; Path(" +
                          repr(str(pidfile)) + ").write_text(str(os.getpid())); " + code)
                start = time.monotonic()
                with self.assertRaises(ValueError):
                    COLLECT([sys.executable, "-c", script], {}, "SELECT synthetic;",
                            limit=limit, timeout=timeout)
                self.assertLess(time.monotonic()-start, 3)
                with self.assertRaises(ProcessLookupError):
                    os.kill(int(pidfile.read_text()), 0)

    def test_diagnostic_stderr_flood_is_bounded(self):
        with tempfile.TemporaryDirectory() as directory:
            pidfile = Path(directory) / "pid"
            script = ("import os,time; from pathlib import Path; Path(" +
                      repr(str(pidfile)) + ").write_text(str(os.getpid())); " +
                      "os.write(2,b'private'*10000); time.sleep(30)")
            with self.assertRaisesRegex(ValueError, "^audit output limit exceeded$"):
                COLLECT([sys.executable, "-c", script], {}, "", diagnose=True, timeout=2)
            with self.assertRaises(ProcessLookupError):
                os.kill(int(pidfile.read_text()), 0)

    def test_early_stdin_close_still_produces_safe_diagnostic(self):
        with self.assertRaisesRegex(ValueError, "^audit failure authentication_failed$"):
            COLLECT([sys.executable, "-c",
                     "import os,sys; os.close(0); sys.stderr.write("
                     "'password authentication failed for private_user'); sys.exit(2)"],
                    {}, "synthetic " * 100000, diagnose=True, timeout=2)


if __name__ == "__main__":
    unittest.main()
