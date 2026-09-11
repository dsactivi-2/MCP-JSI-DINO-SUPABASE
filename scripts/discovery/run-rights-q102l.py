#!/usr/bin/env python3
"""Dry-run then apply Q10.2l-A PUBLIC rights cut. One try, no retry, no candidate data."""

import hashlib
import json
import os
from pathlib import Path
import runpy
import secrets
import stat
import sys
import time

sys.path.insert(0, str(Path(__file__).parent))
PLAN = runpy.run_path(str(Path(__file__).parent / "rights_plan.py"))
BOOT = runpy.run_path(str(Path(__file__).parent / "check-role-bootstrap.py"))

ALIAS = "dino_crm_discovery_target_01"
GATE_ID = "RIGHTS-Q10-2L-A-2026-09-11"
CONFIG_ROOT = Path("/Users/activi/Library/Application Support/Activi/discovery-targets")
APPROVAL = CONFIG_ROOT / f"{ALIAS}.rights-q102l.approval"
EVIDENCE = Path("/private/tmp/crm-public-paths-20260911/final-sanitized-report.json")
OUT_DIR = Path("/private/tmp/crm-rights-plan-q102l")
WINDOW_SECONDS = 1800
TIMEOUT = "60s"


def need(ok, message="rights apply rejected"):
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
        "scope=q10_2l_a",
        "window_start_epoch=" + str(start),
        "window_end_epoch=" + str(end),
        "sql_sha256=" + sql_hash,
        "launcher_sha256=" + launcher_hash,
        "",
    ])
    secure_write(APPROVAL, body)


def mutate_env(env):
    env = dict(env)
    env["PGAPPNAME"] = "dino-rights-q102l-mutate"
    env["PGOPTIONS"] = (
        "-c default_transaction_read_only=off -c statement_timeout=60000 "
        "-c lock_timeout=2000 -c idle_in_transaction_session_timeout=90000 "
        "-c search_path=pg_catalog"
    )
    return env


def inventory(command, env, evidence):
    ids = [f["routine_oid"] for f in evidence["functions"]] + [
        h["oid"] for h in evidence["helpers"] if h["public_execute"]]
    PLAN["ids_sql"](ids)
    token = secrets.token_hex(16)
    cmd = list(command) + ["-v", "audit_token=" + token]
    env = dict(env)
    env["PGAPPNAME"] = "dino-rights-q102l-readonly"
    snapshot = PLAN["validate"](
        PLAN["BASE"]["collect"](cmd, env, PLAN["query"](ids), diagnose=True, timeout=30),
        token, ids)
    source_hashes = {f["routine_oid"]: f["source_sha256"] for f in evidence["functions"]}
    PLAN["need"](all(f["source_hash"] == source_hashes[f["oid"]]
                     for f in snapshot["functions"] if f["oid"] in source_hashes))
    return snapshot


def public_priv(acl, privilege):
    return [a for a in acl if a[1] == 0 and a[2] == privilege]


def summarize(snapshot, executable, residual):
    functions = {f["oid"]: f for f in snapshot["functions"]}
    exec_public = [bool(public_priv(functions[c["oid"]]["acl"], "EXECUTE"))
                   for c in executable if c["kind"] == "function"]
    resid_public = [bool(public_priv(functions[c["oid"]]["acl"], "EXECUTE"))
                    for c in residual]
    temp_public = bool(public_priv(snapshot["database"]["acl"], "TEMPORARY"))
    return {
        "new_role_exists": snapshot["new_role_exists"],
        "role_count": snapshot["role_count"],
        "executable_public_execute": exec_public,
        "residual_public_execute": resid_public,
        "public_temp": temp_public,
    }


def run_sql(command, env, sql, timeout):
    payload = PLAN["BASE"]["collect"](
        command, env, sql, limit=4096, timeout=timeout, diagnose=True)
    need(len(payload) <= 4096)
    return payload


def main():
    need(sys.argv[1:] == ["--apply-q10-2l-a"], "explicit apply argument required")
    need(EVIDENCE.is_file())
    evidence = json.loads(EVIDENCE.read_text())
    need(evidence.get("scope", "").startswith("Q10.2h:") and evidence["count"] == 2)
    launcher_hash = digest_file(Path(__file__))
    command, env = BOOT["connection_parameters"]()
    snapshot = inventory(command, env, evidence)
    executable, residual = PLAN["select_changes"](snapshot, "q10_2l_a")
    before = summarize(snapshot, executable, residual)
    need(before["executable_public_execute"] == [True, True])
    need(all(before["residual_public_execute"]) and len(before["residual_public_execute"]) == 8)
    need(before["public_temp"] is True and before["new_role_exists"] is False)
    apply_sql = PLAN["generate_sql"](
        snapshot, scope="q10_2l_a", finish="commit", statement_timeout=TIMEOUT)
    dry_sql = PLAN["generate_sql"](
        snapshot, scope="q10_2l_a", finish="rollback", statement_timeout=TIMEOUT)
    sql_hash = hashlib.sha256(apply_sql.encode()).hexdigest()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out_sql = OUT_DIR / "forward.apply.sql"
    out_sql.write_text(apply_sql)
    os.chmod(out_sql, 0o600)
    start = int(time.time())
    end = start + WINDOW_SECONDS
    write_approval(sql_hash, launcher_hash, start, end)
    approval = read_approval()
    now = int(time.time())
    need(approval["status"] == "GRANTED")
    need(approval["gate_id"] == GATE_ID)
    need(approval["target_alias"] == ALIAS)
    need(approval["scope"] == "q10_2l_a")
    need(approval["sql_sha256"] == sql_hash)
    need(approval["launcher_sha256"] == launcher_hash)
    need(int(approval["window_start_epoch"]) <= now <= int(approval["window_end_epoch"]))
    mutate = mutate_env(env)
    run_sql(command, mutate, dry_sql, 90)
    run_sql(command, mutate, apply_sql, 90)
    after_snap = inventory(command, env, evidence)
    after = summarize(after_snap, executable, residual)
    need(after["executable_public_execute"] == [False, False], "PUBLIC EXECUTE remained")
    need(all(after["residual_public_execute"]), "LO residual lost")
    need(after["public_temp"] is False, "PUBLIC TEMP remained")
    need(after["new_role_exists"] is False)
    need(after["role_count"] == before["role_count"])
    print(json.dumps({
        "status": "APPLIED",
        "gate_id": GATE_ID,
        "scope": "q10_2l_a",
        "database_mutated": True,
        "candidate_data_read": False,
        "dry_run": "rolled_back",
        "connections": 4,
        "sql_sha256": sql_hash,
        "after_public_temp": False,
        "executable_public_execute_after": after["executable_public_execute"],
        "residual_public_execute_kept": True,
        "new_role_exists": False,
        "role_count": after["role_count"],
    }, indent=2))


if __name__ == "__main__":
    try:
        main()
    except (ValueError, TypeError, KeyError, UnicodeError, RecursionError, OSError):
        print("STOP: Q10.2l apply rejected; no retry", file=sys.stderr)
        raise SystemExit(1) from None
