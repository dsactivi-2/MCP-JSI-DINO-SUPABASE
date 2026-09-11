#!/usr/bin/env python3
"""Exercise minimized plan input and fail-closed SQL generation."""

import copy
import json
from pathlib import Path
import runpy
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/discovery"))
MODULE = runpy.run_path(str(ROOT / "scripts/discovery/rights_plan.py"))
TOKEN = "a"*32
HASH = "b"*64


def document():
    return {"token": TOKEN, "identity_matches": True, "server_major": 17,
            "actor_oid": 10, "new_role_exists": False, "role_count": 2,
            "membership_hash": HASH,
            "roles": [{"oid": 10, "fingerprint": HASH, "login": True, "superuser": True},
                      {"oid": 20, "fingerprint": HASH, "login": False, "superuser": False}],
            "functions": [{"oid": 100, "fingerprint": HASH, "source_hash": HASH,
                           "owner": 10, "owner_set": True, "grant_option": True,
                           "acl": [[10, 0, "EXECUTE", False], [10, 10, "EXECUTE", True]]}],
            "database": {"oid": 200, "fingerprint": HASH, "owner": 10,
                         "owner_set": True, "grant_option": True,
                         "acl": [[10, 0, "CONNECT", False], [10, 0, "TEMPORARY", False],
                                 [10, 10, "CONNECT", False], [10, 10, "CREATE", False],
                                 [10, 10, "TEMPORARY", False]]},
            "unplanned_public_definers": 0, "public_maintain": False}


class PlanTest(unittest.TestCase):
    def test_preserves_other_acl_entries_and_adds_only_missing_direct_grants(self):
        d = MODULE["validate"](json.dumps(document()).encode(), TOKEN, [100])
        changes = MODULE["proposals"](d)
        self.assertEqual(changes[0]["added_grantees"], [20])
        self.assertIn([10, 10, "EXECUTE", True], changes[0]["after_acl"])
        self.assertIn([10, 20, "EXECUTE", False], changes[0]["after_acl"])
        self.assertIn([10, 0, "CONNECT", False], changes[1]["after_acl"])
        self.assertNotIn([10, 0, "TEMPORARY", False], changes[1]["after_acl"])

    def test_unexpected_raw_fields_and_invalid_oids_are_rejected(self):
        for mutate in [lambda d: d["roles"][0].update(name="private"),
                       lambda d: d["functions"][0].update(oid="100; DROP ROLE"),
                       lambda d: d["functions"][0]["acl"].append([10, 999, "EXECUTE", False]),
                       lambda d: d.update(role_count=257)]:
            d = document()
            mutate(d)
            with self.assertRaises((ValueError, TypeError)):
                MODULE["validate"](json.dumps(d).encode(), TOKEN, [100])

    def test_generated_psql_stops_on_errors(self):
        d = MODULE["validate"](json.dumps(document()).encode(), TOKEN, [100])
        self.assertIn("\\set ON_ERROR_STOP on", MODULE["generate_sql"](d))
        sql = MODULE["generate_sql"](d)
        self.assertTrue(sql.strip().endswith("COMMIT;"))
        dry = MODULE["generate_sql"](d, finish="rollback")
        self.assertTrue(dry.strip().endswith("ROLLBACK;"))
        self.assertIn("statement_timeout='5s'", sql)

    def test_generation_rejects_unavailable_authority_or_existing_discovery_role(self):
        d = MODULE["validate"](json.dumps(document()).encode(), TOKEN, [100])
        for mutate in [lambda s: s.update(new_role_exists=True),
                       lambda s: s.update(public_maintain=True),
                       lambda s: s.update(unplanned_public_definers=1),
                       lambda s: s["functions"][0].update(owner_set=False)]:
            changed = copy.deepcopy(d)
            mutate(changed)
            with self.assertRaises(ValueError):
                MODULE["generate_sql"](changed)


    def mixed_document(self):
        d = document()
        d["functions"].append({
            "oid": 101, "fingerprint": HASH, "source_hash": HASH,
            "owner": 10, "owner_set": False, "grant_option": False,
            "acl": [[10, 0, "EXECUTE", False], [10, 10, "EXECUTE", True]]})
        return d

    def test_reduced_scope_omits_unchangeable_function_from_grants(self):
        d = MODULE["validate"](json.dumps(self.mixed_document()).encode(), TOKEN, [100, 101])
        with self.assertRaises(ValueError):
            MODULE["generate_sql"](d)
        sql = MODULE["generate_sql"](d, scope="q10_2l_a")
        self.assertIn('"oid":100', sql)
        self.assertIn('"oid":101', sql)
        self.assertIn('"residual"', sql)
        changes = MODULE["select_changes"](d, "q10_2l_a")[0]
        self.assertEqual([c["oid"] for c in changes if c["kind"] == "function"], [100])
        self.assertTrue(any(c["kind"] == "database" for c in changes))

    def test_reduced_scope_rejects_full_changeable_snapshot(self):
        d = MODULE["validate"](json.dumps(document()).encode(), TOKEN, [100])
        with self.assertRaises(ValueError):
            MODULE["generate_sql"](d, scope="q10_2l_a")

if __name__ == "__main__":
    unittest.main()
