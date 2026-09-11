#!/usr/bin/env python3

import hashlib
import re
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
SQL_PATH = REPO_ROOT / "docs/discovery/sql/00-identity-and-privilege-gate-b1-v2.sql"
LAUNCHER_PATH = REPO_ROOT / "scripts/discovery/run-gate-b1.sh"
PREFLIGHT_PATH = REPO_ROOT / "docs/discovery/security-read-only-discovery-preflight-b.md"
APPROVAL_PATH = REPO_ROOT / "docs/discovery/gate-b1-v2-approval-text.md"
EXPECTED_HASH = "0f586d02a663f9df543a7b7c1b8efde876c2b96d6079cd79e02c3a7359710317"
EXPECTED_LAUNCHER_HASH = "638e4713370f7a2499e2543656334da97f1e245d3a8385d6914f0f137fbabf3d"
EXPECTED_STREAM_GUARD_HASH = "acfc52daf4773be1034d52f5bed1acd61f73a2ec6ae6768c872b86876406e190"
EXPECTED_QUERY_IDS = [f"SQL-GATE-B1-{number:03d}" for number in range(1, 12)]
FORBIDDEN_SQL_TOKENS = {
    "ALTER",
    "CALL",
    "COPY",
    "CREATE",
    "DELETE",
    "DO",
    "DROP",
    "EXECUTE",
    "GRANT",
    "INSERT",
    "MERGE",
    "REVOKE",
    "TRUNCATE",
    "UPDATE",
}


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


sql_bytes = SQL_PATH.read_bytes()
sql_text = sql_bytes.decode("utf-8")
actual_hash = hashlib.sha256(sql_bytes).hexdigest()
if actual_hash != EXPECTED_HASH:
    fail("B1 V2 SQL hash mismatch")

query_ids = re.findall(r"'(?P<id>SQL-GATE-B1-\d{3})'\s+AS\s+query_id", sql_text)
begin_ids = re.findall(
    r"^\\echo __GATE_B1_BOUNDARY__\|:boundary_token\|BEGIN\|(SQL-GATE-B1-\d{3})$",
    sql_text,
    flags=re.MULTILINE,
)
end_ids = re.findall(
    r"^\\echo __GATE_B1_BOUNDARY__\|:boundary_token\|END\|(SQL-GATE-B1-\d{3})$",
    sql_text,
    flags=re.MULTILINE,
)
if query_ids != EXPECTED_QUERY_IDS:
    fail("query IDs are missing, duplicated, or reordered")
if begin_ids != EXPECTED_QUERY_IDS or end_ids != EXPECTED_QUERY_IDS:
    fail("query boundary markers are missing, duplicated, or reordered")

without_line_comments = re.sub(r"--[^\n]*", "", sql_text)
without_meta_commands = re.sub(r"^\\[^\n]*$", "", without_line_comments, flags=re.MULTILINE)
without_strings = re.sub(r"'(?:''|[^'])*'", "''", without_meta_commands)
statements = [statement.strip() for statement in without_strings.split(";") if statement.strip()]
statement_starts = [statement.split(None, 1)[0].upper() for statement in statements]
if statement_starts != ["BEGIN", "SET", "SET", "SET", "SET"] + [
    "SELECT",
    "SELECT",
    "WITH",
    "WITH",
    "WITH",
    "WITH",
    "WITH",
    "WITH",
    "WITH",
    "WITH",
    "SELECT",
] + ["ROLLBACK"]:
    fail("unexpected SQL statement structure")
if not re.search(r"\bBEGIN\s+TRANSACTION\s+READ\s+ONLY\b", without_strings, re.IGNORECASE):
    fail("READ ONLY transaction guard missing")
if statement_starts[-1] != "ROLLBACK":
    fail("final ROLLBACK missing")

tokens = set(re.findall(r"\b[A-Z]+\b", without_strings.upper()))
forbidden_present = sorted(tokens & FORBIDDEN_SQL_TOKENS)
if forbidden_present:
    fail("forbidden SQL token present")

launcher_text = LAUNCHER_PATH.read_text(encoding="utf-8")
preflight_text = PREFLIGHT_PATH.read_text(encoding="utf-8")
approval_text = APPROVAL_PATH.read_text(encoding="utf-8")
actual_launcher_hash = hashlib.sha256(LAUNCHER_PATH.read_bytes()).hexdigest()
actual_stream_guard_hash = hashlib.sha256(
    (REPO_ROOT / "scripts/discovery/gate_b1_stream_guard.py").read_bytes()
).hexdigest()
if actual_launcher_hash != EXPECTED_LAUNCHER_HASH:
    fail("launcher hash mismatch")
if actual_stream_guard_hash != EXPECTED_STREAM_GUARD_HASH:
    fail("stream guard hash mismatch")
if f"readonly PROD_SQL_SHA256='{EXPECTED_HASH}'" not in launcher_text:
    fail("launcher is not bound to the B1 V2 SQL hash")
if EXPECTED_HASH not in preflight_text or EXPECTED_HASH not in approval_text:
    fail("B1 V2 hash is inconsistent across gate documents")
for bound_hash in (EXPECTED_LAUNCHER_HASH, EXPECTED_STREAM_GUARD_HASH):
    if bound_hash not in preflight_text or bound_hash not in approval_text:
        fail("launcher component hash is inconsistent across gate documents")
if "Status: **NICHT ERTEILT**" not in approval_text:
    fail("B1 V2 approval text is not marked as ungranted")
if "**Gesamtstatus: PASS_WITH_GAPS / NO-GO.**" not in preflight_text:
    fail("preflight status is not PASS_WITH_GAPS / NO-GO")
if "Launcher fehlt" in preflight_text:
    fail("preflight contradicts the present launcher")

print("PASS: B1 V2 static SQL and gate-document checks")
