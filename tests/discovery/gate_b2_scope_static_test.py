#!/usr/bin/env python3

import hashlib
import re
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
SQL_PATH = REPO_ROOT / "docs/discovery/sql/10-catalog-structure-gate-b2.sql"
PREFLIGHT_PATH = REPO_ROOT / "docs/discovery/security-read-only-discovery-preflight-b.md"
EXPECTED_HASH = "53a7eb35b3d3c49e6901c3ad12dc418955be44f88eae4cd3fbe0cb7ae1376200"
EXPECTED_QUERY_IDS = [f"SQL-GATE-B2-{number:03d}" for number in range(1, 15)]
SCOPE_CLAUSE = "IN ('crm', 'crm_api', 'crm_auth')"


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


sql_bytes = SQL_PATH.read_bytes()
sql_text = sql_bytes.decode("utf-8")
if hashlib.sha256(sql_bytes).hexdigest() != EXPECTED_HASH:
    fail("B2 SQL hash mismatch")

query_ids = re.findall(r"'(?P<id>SQL-GATE-B2-\d{3})'\s+AS\s+query_id", sql_text)
if query_ids != EXPECTED_QUERY_IDS:
    fail("B2 query IDs are missing, duplicated, or reordered")
if sql_text.count(SCOPE_CLAUSE) < 13:
    fail("not every schema-bearing B2 query is restricted to the approved scope")
if "NOT IN ('pg_catalog', 'information_schema')" in sql_text:
    fail("broad non-system schema inventory remains present")
if "BEGIN TRANSACTION READ ONLY" not in sql_text or not sql_text.rstrip().endswith("ROLLBACK;"):
    fail("B2 transaction guard or rollback is missing")

preflight_text = PREFLIGHT_PATH.read_text(encoding="utf-8")
if EXPECTED_HASH not in preflight_text:
    fail("B2 hash is inconsistent with the preflight")
for schema in ("crm", "crm_api", "crm_auth"):
    if f"\\`{schema}\\`" not in preflight_text:
        fail(f"preflight does not document the {schema} scope")
if "B2 ist nicht freigegeben" not in preflight_text:
    fail("preflight does not preserve the B2 approval boundary")

print("PASS: B2 SQL remains read-only and restricted to crm, crm_api, crm_auth")
