#!/usr/bin/env python3
"""Exercise the audit's JSON-pipe privacy boundary without a database."""

import json
from pathlib import Path
import subprocess
import sys
import unittest
import copy


ROOT = Path(__file__).resolve().parents[2]
GUARD = ROOT / "scripts/discovery/definer_audit.py"
TOKEN = "a" * 32
SECRET = "synthetic_private_canary_7341"


def document(source="BEGIN UPDATE private_table SET note='hidden'; END;"):
    return {"token": TOKEN, "identity_matches": True, "server_major": 17,
            "total_count": 1, "functions": [{
                "oid": 12345, "schema": SECRET, "name": SECRET,
                "arguments": SECRET, "owner": SECRET, "owner_superuser": False,
                "owner_bypassrls": True, "owner_createrole": False,
                "language": "plpgsql", "kind": "f", "volatility": "v",
                "source": source, "sql_standard": False,
                "config": ["search_path=pg_catalog," + SECRET],
                "extension": None,
                "acl": [{"role": "PUBLIC", "grantable": False},
                        {"role": SECRET, "grantable": False}]}]}


class GuardTest(unittest.TestCase):
    def run_guard(self, payload):
        return subprocess.run([sys.executable, str(GUARD), "--token", TOKEN],
                              input=payload, text=True, capture_output=True, timeout=5)

    def test_report_never_exposes_source_identifiers_literals_or_acl_names(self):
        result = self.run_guard(json.dumps(document(
            "BEGIN /* " + SECRET + " */ UPDATE private_table SET note='" + SECRET + "'; END;")))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn(SECRET, result.stdout + result.stderr)
        self.assertNotIn("private_table", result.stdout + result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["functions"][0]["write_indicators"], ["UPDATE"])
        self.assertEqual(report["functions"][0]["safety_status"], "NOT_PROVEN_READ_ONLY")

    def test_literals_comments_and_quoted_identifiers_are_not_write_evidence(self):
        source = "BEGIN /* UPDATE /* DELETE */ INSERT */ PERFORM 'DROP'; -- COPY\n"
        source += 'PERFORM $$TRUNCATE$$; PERFORM "MERGE"(); END;'
        result = self.run_guard(json.dumps(document(source)))
        self.assertEqual(result.returncode, 0, result.stderr)
        function = json.loads(result.stdout)["functions"][0]
        self.assertEqual(function["write_indicators"], [])
        self.assertEqual(function["ddl_indicators"], [])
        self.assertTrue(function["unresolved_call_syntax"])
        self.assertEqual(function["safety_status"], "NOT_PROVEN_READ_ONLY")

    def test_dynamic_sql_and_external_calls_remain_unresolved(self):
        result = self.run_guard(json.dumps(document(
            "BEGIN EXECUTE 'DELETE " + SECRET + "'; PERFORM http_post('private'); END;")))
        self.assertEqual(result.returncode, 0, result.stderr)
        function = json.loads(result.stdout)["functions"][0]
        self.assertTrue(function["dynamic_sql"])
        self.assertEqual(function["external_indicators"], ["HTTP_POST"])
        self.assertNotIn(SECRET, result.stdout + result.stderr)

    def test_invalid_or_incomplete_envelopes_never_emit_partial_results(self):
        base = document()
        variants = []
        for key, value in [("token", "b"*32), ("identity_matches", False),
                           ("server_major", 16), ("total_count", 2),
                           ("total_count", 257), ("total_count", True)]:
            item = copy.deepcopy(base)
            item[key] = value
            variants.append(json.dumps(item))
        item = copy.deepcopy(base)
        item["functions"][0]["source"] = "x" * (256*1024+1)
        variants.append(json.dumps(item))
        for source in ["BEGIN '"+SECRET, "/*"+SECRET, "$tag$"+SECRET]:
            variants.append(json.dumps(document(source)))
        variants += ['{"token":"'+SECRET+'","token":"duplicate"}',
                     json.dumps(base)[:-3], "x" * (4*1024*1024+1)]
        for payload in variants:
            with self.subTest(length=len(payload)):
                result = self.run_guard(payload)
                self.assertEqual(result.returncode, 1)
                self.assertEqual(result.stdout, "")
                self.assertEqual(result.stderr,
                                 "STOP: protected audit input rejected; no raw output\n")

    def test_opaque_language_is_never_classified_read_only(self):
        item = document(SECRET)
        item["functions"][0]["language"] = "c"
        result = self.run_guard(json.dumps(item))
        self.assertEqual(result.returncode, 0, result.stderr)
        function = json.loads(result.stdout)["functions"][0]
        self.assertFalse(function["source_analyzed_lexically"])
        self.assertTrue(function["unresolved_call_syntax"])
        self.assertNotIn(SECRET, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
