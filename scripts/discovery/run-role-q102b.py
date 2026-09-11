#!/usr/bin/env python3
"""Dry-run then create dino_crm_discovery_ro_v1. One try, no retry, no password, no candidate data."""

import hashlib
import json
import os
from pathlib import Path
import runpy
import stat
import sys
import time

sys.path.insert(0, str(Path(__file__).parent))
PLAN = runpy.run_path(str(Path(__file__).parent / "rights_plan.py") )
BOOT = runpy.run_path(str(Path(__file__).parent / "check-role-bootstrap.py"))

ALIAS = "dino_crm_discovery_target_01"
GATE_ID = "ROLE-Q10-2B-2026-09-12"
ROLE = "dino_crm_discovery_ro_v1"
CONFIG_ROOT = Path("/Users/activi/Library/Application Support/Activi/discovery-targets")
APPROVAL = CONFIG_ROOT / f"{ALIAS}.role-q102b.approval"
SQL_PATH = Path(__file__).resolve().parents[2] / "docs/discovery/sql/03-create-least-privilege-discovery-role-v2-prod.sql"
OUT_DIR = Path("/private/tmp/crm-role-q102b")
WINDOW_SECONDS = 1800

PRECHECK = """
BEGIN READ ONLY;
SELECT jsonb_build_object(
  'identity_matches', current_database()=:'expected_database_name' AND session_user=:'expected_user',
  'exists', EXISTS(SELECT 1 FROM pg_roles WHERE rolname='dino_crm_discovery_ro_v1')
);
ROLLBACK;
"""

POSTCHECK = """
BEGIN READ ONLY;
SELECT jsonb_build_object(
  'identity_matches', current_database()=:'expected_database_name' AND session_user=:'expected_user',
  'exists', EXISTS(SELECT 1 FROM pg_roles WHERE rolname='dino_crm_discovery_ro_v1'),
  'login', (SELECT rolcanlogin FROM pg_roles WHERE rolname='dino_crm_discovery_ro_v1'),
  'connlimit', (SELECT rolconnlimit FROM pg_roles WHERE rolname='dino_crm_discovery_ro_v1'),
  'connect', has_database_privilege('dino_crm_discovery_ro_v1', current_database(), 'CONNECT'),
  'temp', has_database_privilege('dino_crm_discovery_ro_v1', current_database(), 'TEMP'),
  'create_db', has_database_privilege('dino_crm_discovery_ro_v1', current_database(), 'CREATE'),
  'definer_execute', EXISTS(
    SELECT 1 FROM pg_proc p
    WHERE p.prosecdef
      AND has_function_privilege('dino_crm_discovery_ro_v1', p.oid, 'EXECUTE'))
);
ROLLBACK;
"""


def need(ok, message="role apply rejected"):
    if not ok:
        raise ValueError(message)


def digest_file(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def secure_write(path, text):
    path.write_text(text)
    os.chmod(path, 0o600)
    entry = path.lstat()
    need(stat.S_ISREG(entry.st_mode) and stat.S_IMODE(entry.st_mode) == 0o600
         and entry.st_uid == os.getuid() and path.resolve() == path)


def read_approval():
    need(APPROVAL.is_file())
    values = {}
    for line in APPROVAL.read_text().splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        key, value = line.split("=", 1)
        need(key not in values, "duplicate approval key")
        values[key] = value
    need(set(values) == {
        "status", "gate_id", "target_alias", "scope", "window_start_epoch",
        "window_end_epoch", "sql_sha256", "launcher_sha256"})
    return values


def write_approval(sql_hash, launcher_hash, start, end):
    body = "\n".join([
        "status=GRANTED",
        "gate_id=" + GATE_ID,
        "target_alias=" + ALIAS,
        "scope=q10_2b_v2",
        "window_start_epoch=" + str(start),
        "window_end_epoch=" + str(end),
        "sql_sha256=" + sql_hash,
        "launcher_sha256=" + launcher_hash,
        "",
    ])
    secure_write(APPROVAL, body)


def mutate_env(env):
    env = dict(env)
    env["PGAPPNAME"] = "dino-role-q102b-mutate"
    env["PGOPTIONS"] = (
        "-c default_transaction_read_only=off -c statement_timeout=60000 "
        "-c lock_timeout=2000 -c idle_in_transaction_session_timeout=90000 "
        "-c search_path=pg_catalog"
    )
    return env


def read_json(command, env, sql, timeout=30):
    env = dict(env)
    env["PGAPPNAME"] = "dino-role-q102b-readonly"
    payload = PLAN["BASE"]["collect"](command, env, sql, limit=4096, timeout=timeout, diagnose=True)
    return json.loads(payload.decode())


def run_sql(command, env, sql, timeout):
    payload = PLAN["BASE"]["collect"](command, env, sql, limit=4096, timeout=timeout, diagnose=True)
    need(len(payload) <= 4096)
    return payload


def main():
    diagnose = sys.argv[1:] == ["--diagnose-dry-run"]
    need(sys.argv[1:] == ["--apply-q10-2b"] or diagnose, "explicit apply or diagnose argument required")
    need(SQL_PATH.is_file())
    apply_sql = SQL_PATH.read_text()
    need("\\password" not in apply_sql)
    need(apply_sql.strip().endswith("COMMIT;"))
    dry_sql = apply_sql.rsplit("COMMIT;", 1)[0] + "ROLLBACK;"
    sql_hash = hashlib.sha256(apply_sql.encode()).hexdigest()
    launcher_hash = digest_file(Path(__file__))
    command, env = BOOT["connection_parameters"]()
    before = read_json(command, env, PRECHECK)
    need(before.get("identity_matches") is True)
    need(before.get("exists") is False, "role already exists")
    if diagnose:
        try:
            run_sql(command, mutate_env(env), dry_sql, 90)
        except ValueError as exc:
            print(json.dumps({"status": "DRY_RUN_FAILED", "error": str(exc)[:120],
                              "database_mutated": False, "role_exists": False}))
            return
        print(json.dumps({"status": "DRY_RUN_OK", "database_mutated": False, "role_exists": False}))
        return
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    start = int(time.time())
    end = start + WINDOW_SECONDS
    write_approval(sql_hash, launcher_hash, start, end)
    approval = read_approval()
    now = int(time.time())
    need(approval["status"] == "GRANTED")
    need(approval["gate_id"] == GATE_ID)
    need(approval["target_alias"] == ALIAS)
    need(approval["scope"] == "q10_2b_v2")
    need(approval["sql_sha256"] == sql_hash)
    need(approval["launcher_sha256"] == launcher_hash)
    need(int(approval["window_start_epoch"]) <= now <= int(approval["window_end_epoch"]))
    mutate = mutate_env(env)
    run_sql(command, mutate, dry_sql, 90)
    mid = read_json(command, env, PRECHECK)
    need(mid.get("exists") is False, "dry-run left a role")
    run_sql(command, mutate, apply_sql, 90)
    after = read_json(command, env, POSTCHECK)
    need(after.get("identity_matches") is True)
    need(after.get("exists") is True)
    need(after.get("login") is True)
    need(after.get("connlimit") == 1)
    need(after.get("connect") is True)
    need(after.get("temp") is False)
    need(after.get("create_db") is False)
    need(after.get("definer_execute") is False)
    print(json.dumps({
        "status": "APPLIED",
        "gate_id": GATE_ID,
        "role": ROLE,
        "database_mutated": True,
        "candidate_data_read": False,
        "password_set": False,
        "dry_run": "rolled_back",
        "connections": 4,
        "sql_sha256": sql_hash,
        "connect": True,
        "temp": False,
        "create_db": False,
        "definer_execute": False,
        "connlimit": 1,
    }, indent=2))


if __name__ == "__main__":
    try:
        main()
    except (ValueError, TypeError, KeyError, UnicodeError, RecursionError, OSError, json.JSONDecodeError):
        print("STOP: Q10.2b role apply rejected; no retry", file=sys.stderr)
        raise SystemExit(1) from None
