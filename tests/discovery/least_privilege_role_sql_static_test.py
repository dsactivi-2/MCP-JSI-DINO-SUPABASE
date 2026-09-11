#!/usr/bin/env python3

import re
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
SETUP_PATH = (
    REPO_ROOT
    / "docs/discovery/sql/01-create-least-privilege-discovery-role-v1.sql"
)
ROLLBACK_PATH = (
    REPO_ROOT
    / "docs/discovery/sql/01-drop-least-privilege-discovery-role-v1.sql"
)
ROLE = "dino_crm_discovery_ro_v1"


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


setup = SETUP_PATH.read_text(encoding="utf-8")
rollback = ROLLBACK_PATH.read_text(encoding="utf-8")

required_setup_fragments = (
    "\\set ON_ERROR_STOP on",
    "BEGIN;",
    "SET LOCAL statement_timeout = '5s';",
    "SET LOCAL lock_timeout = '1s';",
    "SET LOCAL idle_in_transaction_session_timeout = '15s';",
    f"CREATE ROLE {ROLE}",
    "NOINHERIT",
    "NOSUPERUSER",
    "NOCREATEDB",
    "NOCREATEROLE",
    "NOREPLICATION",
    "NOBYPASSRLS",
    "CONNECTION LIMIT 1",
    "PASSWORD NULL",
    f"\\password {ROLE}",
    "default_transaction_read_only = 'on'",
    "has_database_privilege",
    "has_schema_privilege",
    "has_table_privilege",
    "has_column_privilege",
    "has_sequence_privilege",
    "has_function_privilege",
    "pg_auth_members",
    "COMMIT;",
)
for fragment in required_setup_fragments:
    if fragment not in setup:
        fail(f"setup fragment missing: {fragment}")

for forbidden in (
    "GRANT SELECT",
    "GRANT USAGE ON SCHEMA",
    "REVOKE TEMP FROM PUBLIC",
    "REVOKE TEMPORARY FROM PUBLIC",
    "SECURITY DEFINER",
    "DROP OWNED",
    "REASSIGN OWNED",
    "CASCADE",
):
    if re.search(rf"\b{re.escape(forbidden)}\b", setup, flags=re.IGNORECASE):
        fail(f"forbidden setup operation present: {forbidden}")

if setup.count("CREATE ROLE") != 1 or setup.count("COMMIT;") != 1:
    fail("setup must contain exactly one role creation and one commit")

required_rollback_fragments = (
    "\\set ON_ERROR_STOP on",
    "BEGIN;",
    "SET LOCAL statement_timeout = '5s';",
    f"DROP ROLE {ROLE};",
    "COMMIT;",
)
for fragment in required_rollback_fragments:
    if fragment not in rollback:
        fail(f"rollback fragment missing: {fragment}")

for forbidden in ("CASCADE", "DROP OWNED", "REASSIGN OWNED"):
    statements_only = re.sub(r"--[^\n]*", "", rollback)
    if re.search(rf"\b{re.escape(forbidden)}\b", statements_only, flags=re.IGNORECASE):
        fail(f"forbidden rollback operation present: {forbidden}")

rollback_statements = re.sub(r"--[^\n]*", "", rollback)
if rollback_statements.count("DROP ROLE") != 1 or rollback_statements.count("COMMIT;") != 1:
    fail("rollback must contain exactly one role removal and one commit")

print("PASS: least-privilege role SQL static checks")
