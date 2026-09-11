#!/usr/bin/env python3
"""Test the extended audit's external privacy boundary without a database."""

import copy
import json
from pathlib import Path
import runpy
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = runpy.run_path(str(Path(__file__).with_name("definer_audit_guard_test.py")))
TOKEN = FIXTURE["TOKEN"]


def document():
    audit = FIXTURE["document"]()
    audit["functions"].append(copy.deepcopy(audit["functions"][0]))
    audit["functions"][1]["oid"] += 1
    audit["total_count"] = 2
    return {"audit": audit, "paths": {"total": 1, "frontier_count": 0,
            "other_root_dependency_count": 0, "nodes": [{
                "oid": 23456, "class": "relation", "kind": "v", "depth": 1,
                "public_lookup": True, "public_access": True}]},
            "helpers": [{"name": "lo_create", "oid": 34567, "public_execute": True,
                         "public_lookup": True, "security_definer": False}]}


class GuardTest(unittest.TestCase):
    def run_guard(self, doc):
        return subprocess.run([sys.executable, "-B",
                               str(ROOT / "scripts/discovery/audit-public-paths.py"),
                               "--validate-stdin", TOKEN], input=json.dumps(doc),
                              text=True, capture_output=True, timeout=5)

    def test_only_fixed_labels_leave_extended_boundary(self):
        result = self.run_guard(document())
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn(FIXTURE["SECRET"], result.stdout + result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["paths"]["nodes"][0]["alias"], "D001")
        self.assertEqual(report["paths"]["status"], "CATALOG_ONLY_INCOMPLETE")
        self.assertTrue(report["helpers"][0]["public_execute"])

    def test_partial_or_scope_changed_reports_fail_without_raw_output(self):
        for mutate in [
            lambda d: d["audit"].update(total_count=1),
            lambda d: d["paths"].update(total=257),
            lambda d: d["paths"]["nodes"][0].update(kind=FIXTURE["SECRET"]),
            lambda d: d["helpers"][0].update(name=FIXTURE["SECRET"]),
            lambda d: d["helpers"][0].update(public_execute="true"),
            lambda d: d.update(unexpected=FIXTURE["SECRET"]),
        ]:
            doc = document()
            mutate(doc)
            result = self.run_guard(doc)
            self.assertEqual(result.returncode, 1)
            self.assertEqual(result.stdout, "")
            self.assertRegex(result.stderr,
                             r"^STOP: extended audit rejected at (json|envelope|root_scope|roots|paths|helpers); no raw output or retry\n$")
            self.assertNotIn(FIXTURE["SECRET"], result.stderr)


if __name__ == "__main__":
    unittest.main()
