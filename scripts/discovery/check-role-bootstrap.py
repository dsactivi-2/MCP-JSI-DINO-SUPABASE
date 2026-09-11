#!/usr/bin/env python3
"""One bounded read-only connection; output only bootstrap capability flags."""

import configparser
import hashlib
import json
import os
from pathlib import Path
import signal
import stat
import subprocess
import sys


ALIAS = "dino_crm_discovery_target_01"
CONFIG_ROOT = Path("/Users/activi/Library/Application Support/Activi/discovery-targets")
QUERY = """
BEGIN READ ONLY;
SELECT (current_database() = :'expected_database_name'
  AND session_user = :'expected_user')::int,
  current_setting('server_version_num')::int / 10000,
  r.rolsuper::int, r.rolcreaterole::int,
  (d.datdba = r.oid)::int,
  EXISTS(SELECT 1 FROM pg_roles
    WHERE rolname = 'dino_crm_discovery_ro_v1')::int,
  EXISTS(SELECT 1 FROM aclexplode(COALESCE(d.datacl, acldefault('d', d.datdba))) a
    WHERE a.grantee = 0 AND a.privilege_type = 'TEMPORARY')::int,
  EXISTS(SELECT 1 FROM aclexplode(COALESCE(d.datacl, acldefault('d', d.datdba))) a
    WHERE a.grantee = 0 AND a.privilege_type = 'CREATE')::int
FROM pg_roles r JOIN pg_database d ON d.datname = current_database()
WHERE r.rolname = session_user;
ROLLBACK;
"""

PUBLIC_QUERY = """
BEGIN READ ONLY;
WITH public_schemas AS (
  SELECT n.oid, a.privilege_type FROM pg_namespace n,
    LATERAL aclexplode(COALESCE(n.nspacl, acldefault('n', n.nspowner))) a
  WHERE a.grantee = 0
), public_relations AS (
  SELECT c.oid, c.relkind, a.privilege_type FROM pg_class c,
    LATERAL aclexplode(COALESCE(c.relacl,
      acldefault(CASE WHEN c.relkind='S' THEN 's'::"char" ELSE 'r'::"char" END,
        c.relowner))) a
  WHERE a.grantee = 0 AND c.relkind IN ('r','p','v','m','f','S')
), public_columns AS (
  SELECT a.attrelid, x.privilege_type FROM pg_attribute a,
    LATERAL aclexplode(a.attacl) x
  WHERE x.grantee=0 AND a.attnum>0 AND NOT a.attisdropped
), public_definers AS (
  SELECT p.pronamespace FROM pg_proc p,
    LATERAL aclexplode(COALESCE(p.proacl, acldefault('f', p.proowner))) a
  WHERE p.prosecdef AND a.grantee=0 AND a.privilege_type='EXECUTE'
)
SELECT (current_database() = :'expected_database_name'
  AND session_user = :'expected_user')::int,
  EXISTS(SELECT 1 FROM public_schemas WHERE privilege_type='CREATE')::int,
  EXISTS(SELECT 1 FROM public_relations WHERE relkind<>'S'
    AND (privilege_type IN ('INSERT','DELETE','TRUNCATE','REFERENCES','TRIGGER','MAINTAIN')
      OR (privilege_type='UPDATE' AND oid<>'pg_catalog.pg_settings'::regclass)))::int,
  EXISTS(SELECT 1 FROM public_columns WHERE privilege_type='INSERT'
    OR (privilege_type='UPDATE' AND attrelid<>'pg_catalog.pg_settings'::regclass))::int,
  EXISTS(SELECT 1 FROM public_relations WHERE relkind='S'
    AND privilege_type IN ('USAGE','UPDATE'))::int,
  EXISTS(SELECT 1 FROM public_definers)::int,
  EXISTS(SELECT 1 FROM public_definers p JOIN public_schemas n
    ON n.oid=p.pronamespace AND n.privilege_type='USAGE')::int;
ROLLBACK;
"""


def secure(path):
    entry = path.lstat()
    if not (stat.S_ISREG(entry.st_mode) and stat.S_IMODE(entry.st_mode) == 0o600
            and entry.st_uid == os.getuid() and path.resolve() == path):
        raise ValueError("restricted configuration metadata failed")


def main():
    public_scope = sys.argv[1:] == ["--read-only-public-preflight"]
    if not public_scope and sys.argv[1:] != ["--read-only-owner-preflight"]:
        raise ValueError("explicit read-only owner-preflight argument required")
    target = CONFIG_ROOT / (ALIAS + ".target")
    service = CONFIG_ROOT / (ALIAS + ".pg_service.conf")
    credential = CONFIG_ROOT / (ALIAS + ".pgpass")
    identity = CONFIG_ROOT / (ALIAS + ".role-bootstrap.identity.json")
    for path in (target, service, credential, identity):
        secure(path)
    evidence = json.loads(identity.read_text())
    if evidence.get("target_alias") != ALIAS:
        raise ValueError("independent identity evidence alias mismatch")
    attest = {}
    for line in target.read_text().splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        key, value = (part.strip() for part in line.split("=", 1))
        if key in attest:
            raise ValueError("duplicate target key")
        attest[key] = value
    config = configparser.ConfigParser(interpolation=None, strict=True)
    config.read_string(service.read_text())
    if config.sections() != [ALIAS] or config.defaults():
        raise ValueError("connection section mismatch")
    settings = dict(config[ALIAS])
    if set(settings) != {"host", "dbname", "user", "sslmode", "connect_timeout"}:
        raise ValueError("connection fields mismatch")
    expected_role = evidence.get("expected_database_role", "")
    transport_hash = hashlib.sha256(settings["user"].encode()).hexdigest()
    if (not expected_role or
            evidence.get("transport_user_sha256") != transport_hash):
        raise ValueError("independently confirmed transport-user and database-role binding missing")
    if (attest.get("target_alias") != ALIAS
            or attest.get("connection_service") != ALIAS
            or attest.get("expected_database_name") != settings["dbname"]
            or hashlib.sha256(settings["host"].strip().lower().encode()).hexdigest()
            != attest.get("target_fingerprint_sha256")
            or settings["sslmode"] not in {"require", "verify-ca", "verify-full"}
            or settings["connect_timeout"] != "5"
            or "," in settings["host"]):
        raise ValueError("target binding failed")
    env = {
        "PATH": "/opt/homebrew/bin:/usr/bin:/bin", "LC_ALL": "C",
        "PGSERVICE": ALIAS, "PGSERVICEFILE": str(service),
        "PGPASSFILE": str(credential), "PGSYSCONFDIR": "/private/tmp",
        "PSQL_HISTORY": "/dev/null", "PGAPPNAME": "dino-role-bootstrap-readonly",
        "PGOPTIONS": "-c default_transaction_read_only=on -c statement_timeout=5000 "
                     "-c lock_timeout=1000 -c idle_in_transaction_session_timeout=15000 "
                     "-c search_path=pg_catalog",
    }
    command = ["/opt/homebrew/bin/psql", "-X", "-qAt", "-w", "-v", "ON_ERROR_STOP=1",
               "-v", "VERBOSITY=sqlstate", "-v", "SHOW_CONTEXT=never",
               "-v", "expected_database_name=" + settings["dbname"],
               "-v", "expected_user=" + expected_role]
    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                               stderr=subprocess.DEVNULL, text=True, env=env,
                               start_new_session=True)
    try:
        output, _ = process.communicate(PUBLIC_QUERY if public_scope else QUERY, timeout=12)
    except subprocess.TimeoutExpired:
        raise ValueError("owner preflight timed out; no retry") from None
    finally:
        if process.poll() is None:
            try:
                os.killpg(process.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            process.communicate()
    if process.returncode != 0:
        raise ValueError("owner preflight connection/query failed; no retry")
    fields = output.strip().split("|")
    if (len(output) > 100 or len(fields) != (7 if public_scope else 8)
            or fields[0] != "1" or not fields[1].isdigit()
            or any(value not in {"0", "1"} for value in fields[1 if public_scope else 2:])):
        raise ValueError("owner preflight response rejected")
    names = ["target_identity_matches", "server_major", "actor_superuser",
             "actor_createrole", "actor_database_owner", "role_already_exists",
             "public_temp", "public_create"]
    if public_scope:
        names = ["target_identity_matches", "public_schema_create",
                 "public_relation_write", "public_column_write",
                 "public_sequence_write", "public_definer_execute",
                 "public_definer_execute_with_schema_usage"]
    report = dict(zip(names, (int(value) for value in fields)))
    report.update({"status": "READ_ONLY_EVIDENCE", "database_mutated": False,
                   "candidate_data_read": False, "connections": 1})
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, configparser.Error):
        print("STOP: bootstrap preflight failed; no raw connection output or retry", file=sys.stderr)
        raise SystemExit(1) from None
