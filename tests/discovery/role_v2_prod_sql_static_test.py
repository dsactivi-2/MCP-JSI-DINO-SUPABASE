#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SQL = ROOT / "docs/discovery/sql/03-create-least-privilege-discovery-role-v2-prod.sql"
ROLE = "dino_crm_discovery_ro_v1"


def fail(message):
    raise SystemExit("FAIL: " + message)


text = SQL.read_text(encoding="utf-8")
for fragment in (
    "\\set ON_ERROR_STOP on",
    "BEGIN;",
    "identity_guard",
    "expected_user",
    f"CREATE ROLE {ROLE}",
    "PASSWORD NULL",
    "GRANT CONNECT",
    "NOINHERIT",
    "has_function_privilege",
    "COMMIT;",
):
    if fragment not in text:
        fail("missing " + fragment)
if "\\password" in text:
    fail("interactive password must not be in automated SQL")
if text.count("CREATE ROLE") != 1 or text.count("COMMIT;") != 1:
    fail("exactly one CREATE ROLE and COMMIT required")
print("PASS: v2 prod role SQL static checks")
