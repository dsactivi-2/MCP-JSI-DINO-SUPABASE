#!/usr/bin/env python3
"""Approved catalog-only audit with bounded in-memory output and no raw logs."""

import configparser
import json
import os
from pathlib import Path
import runpy
import re
import secrets
import selectors
import signal
import subprocess
import sys
import time

from definer_audit import MAX_BYTES, summarize


QUERY = """
BEGIN ISOLATION LEVEL REPEATABLE READ READ ONLY;
WITH selected AS MATERIALIZED (
  SELECT p.*, n.nspname, r.rolname, r.rolsuper, r.rolbypassrls,
    r.rolcreaterole, l.lanname
  FROM pg_proc p JOIN pg_namespace n ON n.oid=p.pronamespace
    JOIN pg_roles r ON r.oid=p.proowner JOIN pg_language l ON l.oid=p.prolang
  WHERE p.prosecdef
    AND EXISTS (SELECT 1 FROM aclexplode(COALESCE(p.proacl,
      acldefault('f',p.proowner))) a
      WHERE a.grantee=0 AND a.privilege_type='EXECUTE')
    AND EXISTS (SELECT 1 FROM aclexplode(COALESCE(n.nspacl,
      acldefault('n',n.nspowner))) a
      WHERE a.grantee=0 AND a.privilege_type='USAGE')
), bounded AS (
  SELECT * FROM selected WHERE (SELECT count(*) FROM selected)<=256
    AND current_database()=:'expected_database_name'
    AND session_user=:'expected_user'
  ORDER BY oid LIMIT 256
)
SELECT json_build_object(
  'token', :'audit_token',
  'identity_matches', current_database()=:'expected_database_name'
    AND session_user=:'expected_user',
  'server_major', current_setting('server_version_num')::int/10000,
  'total_count', (SELECT count(*) FROM selected),
  'functions', COALESCE((SELECT json_agg(json_build_object(
    'oid', p.oid::bigint, 'schema', p.nspname, 'name', p.proname,
    'arguments', pg_get_function_identity_arguments(p.oid),
    'owner', p.rolname, 'owner_superuser', p.rolsuper,
    'owner_bypassrls', p.rolbypassrls, 'owner_createrole', p.rolcreaterole,
    'language', p.lanname, 'kind', p.prokind, 'volatility', p.provolatile,
    'source', CASE WHEN p.prosqlbody IS NOT NULL
      THEN pg_get_functiondef(p.oid) ELSE p.prosrc END,
    'sql_standard', p.prosqlbody IS NOT NULL,
    'config', COALESCE(p.proconfig, ARRAY[]::text[]),
    'extension', (SELECT e.extname FROM pg_depend d
      JOIN pg_extension e ON e.oid=d.refobjid
      WHERE d.classid='pg_proc'::regclass AND d.objid=p.oid
        AND d.refclassid='pg_extension'::regclass AND d.deptype='e'),
    'acl', (SELECT json_agg(json_build_object(
      'role', CASE WHEN a.grantee=0 THEN 'PUBLIC' ELSE r.rolname END,
      'grantable', a.is_grantable))
      FROM aclexplode(COALESCE(p.proacl, acldefault('f',p.proowner))) a
      LEFT JOIN pg_roles r ON r.oid=a.grantee
      WHERE a.privilege_type='EXECUTE')
  ) ORDER BY p.oid) FROM bounded p), '[]'::json));
ROLLBACK;
"""

RECONCILE_QUERY = """
BEGIN ISOLATION LEVEL REPEATABLE READ READ ONLY;
WITH public_schemas AS (
  SELECT DISTINCT n.oid FROM pg_namespace n,
    LATERAL aclexplode(COALESCE(n.nspacl, acldefault('n', n.nspowner))) a
  WHERE a.grantee=0 AND a.privilege_type='USAGE'
), public_definers AS (
  SELECT DISTINCT p.oid, p.pronamespace, p.proowner, p.prolang FROM pg_proc p,
    LATERAL aclexplode(COALESCE(p.proacl, acldefault('f', p.proowner))) a
  WHERE p.prosecdef AND a.grantee=0 AND a.privilege_type='EXECUTE'
), reachable AS (
  SELECT DISTINCT p.* FROM public_definers p JOIN public_schemas n ON n.oid=p.pronamespace
)
SELECT (current_database()=:'expected_database_name'
  AND session_user=:'expected_user')::int,
  (SELECT count(*) FROM public_definers),
  (SELECT count(*) FROM reachable),
  (SELECT count(*) FROM reachable p JOIN pg_roles r ON r.oid=p.proowner
    JOIN pg_language l ON l.oid=p.prolang);
ROLLBACK;
"""


def summarize_coverage(payload):
    fields = payload.decode("ascii").strip().split("|")
    if (len(payload)>100 or len(fields)!=4 or fields[0]!="1"
            or any(not v.isdecimal() or len(v)>10 for v in fields)):
        raise ValueError("coverage response rejected")
    values = [int(v) for v in fields]
    if not values[1] >= values[2] >= values[3]:
        raise ValueError("inconsistent coverage response")
    return {"status": "READ_ONLY_EVIDENCE", "connections": 1,
            "database_mutated": False, "candidate_data_read": False,
            "definitions_read": False, "target_identity_matches": True,
            "public_definer_count": values[1], "direct_schema_lookup_count": values[2],
            "direct_lookup_with_owner_language_count": values[3],
            "catalog_join_complete": values[2] == values[3]}


ERROR_CLASSES = {"authentication_failed", "target_rejected", "startup_rejected",
                 "host_resolution_failed", "transport_refused", "transport_closed",
                 "catalog_privilege_denied", "statement_timeout", "sql_syntax",
                 "undefined_relation", "unsupported_feature", "unclassified"}


def classify_error(payload):
    message = payload.decode("utf-8", errors="replace").lower()
    for needle, category in [
        ("password authentication failed", "authentication_failed"),
        ("tenant or user not found", "target_rejected"),
        ("unsupported startup parameter", "startup_rejected"),
        ("could not translate host name", "host_resolution_failed"),
        ("connection refused", "transport_refused"),
        ("server closed the connection", "transport_closed"),
    ]:
        if needle in message:
            return category
    codes = {"42501": "catalog_privilege_denied", "57014": "statement_timeout",
             "42601": "sql_syntax", "42p01": "undefined_relation", "0a000": "unsupported_feature"}
    match = re.search(r"(?:error|fatal):\s+([a-z0-9]{5})(?:\s|$)", message)
    return codes.get(match[1], "unclassified") if match else "unclassified"


def collect(command, env, query, limit=MAX_BYTES, timeout=15, diagnose=False):
    """Read at most limit+1 bytes; kill/reap the process group on every exit."""
    selector = selectors.DefaultSelector()
    try:
        process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE if diagnose else subprocess.DEVNULL,
                                   env=env, start_new_session=True)
    except BaseException:
        selector.close()
        raise
    payload = bytearray()
    errors = bytearray()
    deadline = time.monotonic() + timeout
    try:
        pending = memoryview(query.encode())
        os.set_blocking(process.stdin.fileno(), False)
        os.set_blocking(process.stdout.fileno(), False)
        selector.register(process.stdin, selectors.EVENT_WRITE)
        selector.register(process.stdout, selectors.EVENT_READ)
        if diagnose:
            os.set_blocking(process.stderr.fileno(), False)
            selector.register(process.stderr, selectors.EVENT_READ)
        while selector.get_map():
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise ValueError("audit timed out")
            for key, _ in selector.select(remaining):
                if key.fileobj is process.stdin:
                    try:
                        written = os.write(process.stdin.fileno(), pending[:4096])
                    except BlockingIOError:
                        continue
                    except BrokenPipeError:
                        selector.unregister(process.stdin)
                        process.stdin.close()
                        continue
                    pending = pending[written:]
                    if not pending:
                        selector.unregister(process.stdin)
                        process.stdin.close()
                else:
                    target = errors if key.fileobj is process.stderr else payload
                    budget = 8192 if key.fileobj is process.stderr else limit
                    try:
                        chunk = os.read(key.fileobj.fileno(), min(65536, budget + 1 - len(target)))
                    except BlockingIOError:
                        continue
                    if not chunk:
                        selector.unregister(key.fileobj)
                        key.fileobj.close()
                    else:
                        target.extend(chunk)
                        if len(target) > budget:
                            raise ValueError("audit output limit exceeded")
        process.wait(timeout=max(0.001, deadline-time.monotonic()))
        if process.returncode:
            if diagnose:
                raise ValueError("audit failure " + classify_error(errors))
            raise ValueError("audit process failed")
        return bytes(payload)
    finally:
        selector.close()
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        process.wait()
        for stream in (process.stdin, process.stdout, process.stderr):
            if stream is not None and not stream.closed:
                stream.close()


def main():
    coverage = sys.argv[1:] == ["--approved-read-only-coverage-reconciliation"]
    if not coverage and sys.argv[1:] != ["--approved-read-only-definer-audit"]:
        raise ValueError("explicit approved scope required")
    bootstrap = runpy.run_path(str(Path(__file__).with_name("check-role-bootstrap.py")))
    command, env = bootstrap["connection_parameters"]()
    token = secrets.token_hex(16)
    command += ["-v", "audit_token=" + token]
    env["PGAPPNAME"] = "dino-public-definer-audit-readonly"
    if coverage:
        report = summarize_coverage(collect(command, env, RECONCILE_QUERY, limit=100))
    else:
        report = summarize(collect(command, env, QUERY), token)
    report["connections"] = 1
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    try:
        main()
    except (ValueError, TypeError, KeyError, UnicodeError, RecursionError,
            OSError, configparser.Error, subprocess.TimeoutExpired, KeyboardInterrupt):
        print("STOP: protected audit failed; no raw output or retry", file=sys.stderr)
        raise SystemExit(1) from None
