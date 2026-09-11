#!/usr/bin/env python3
"""Read-only rights inventory and deterministic, unapplied SQL plan generation."""

import configparser
import json
from pathlib import Path
import re
import runpy
import secrets
import subprocess
import sys

from definer_audit import MAX_BYTES, need, reject_duplicates

BASE = runpy.run_path(str(Path(__file__).with_name("check-public-definers.py")))
ROLE = "dino_crm_discovery_ro_v1"


def sha(expression):
    return "encode(sha256(convert_to((" + expression + ")::text,'UTF8')),'hex')"


def acl(expression):
    return ("COALESCE((SELECT jsonb_agg(jsonb_build_array(a.grantor::bigint,"
            "a.grantee::bigint,a.privilege_type,a.is_grantable) ORDER BY "
            "a.grantor,a.grantee,a.privilege_type,a.is_grantable) FROM aclexplode(" +
            expression + ") a),'[]'::jsonb)")


ROLE_HASH = sha("jsonb_build_array(r.oid::bigint,r.rolname,r.rolsuper,r.rolinherit,"
                "r.rolcreaterole,r.rolcreatedb,r.rolcanlogin,r.rolreplication,r.rolbypassrls)")
FUNCTION_HASH = sha("jsonb_build_array(p.oid::bigint,n.nspname,p.proname,"
                    "pg_get_function_identity_arguments(p.oid),p.proowner::bigint,"
                    "p.prosrc,p.prosqlbody::text,p.proconfig,p.prosecdef,p.prolang::bigint,"
                    "p.probin,p.prokind,p.provolatile,p.proleakproof,p.prosupport::oid::bigint,"
                    "p.proargtypes::text,p.prorettype::bigint)")
FUNCTION_ACL = acl("COALESCE(p.proacl,acldefault('f',p.proowner))")
DATABASE_HASH = sha("jsonb_build_array(d.oid::bigint,d.datname,d.datdba::bigint)")
DATABASE_ACL = acl("COALESCE(d.datacl,acldefault('d',d.datdba))")
MEMBERSHIP_HASH = sha("COALESCE((SELECT jsonb_agg(jsonb_build_array(roleid::bigint,"
                      "member::bigint,grantor::bigint,admin_option,inherit_option,set_option)"
                      " ORDER BY roleid,member,grantor) FROM pg_auth_members),'[]'::jsonb)")


def ids_sql(ids):
    need(isinstance(ids, list) and 1 <= len(ids) <= 32 and len(set(ids)) == len(ids))
    need(all(type(i) is int and 0 < i < 2**32 for i in ids))
    return ",".join(str(i) for i in sorted(ids))


def query(ids):
    selected = ids_sql(ids)
    source_hash = sha("CASE WHEN p.prosqlbody IS NOT NULL THEN pg_get_functiondef(p.oid) ELSE p.prosrc END")
    return f"""
BEGIN ISOLATION LEVEL REPEATABLE READ READ ONLY;
SELECT jsonb_build_object(
 'token', :'audit_token',
 'identity_matches', current_database()=:'expected_database_name' AND session_user=:'expected_user',
 'server_major', current_setting('server_version_num')::int/10000,
 'actor_oid', (SELECT oid::bigint FROM pg_roles WHERE rolname=session_user),
 'new_role_exists', EXISTS(SELECT 1 FROM pg_roles WHERE rolname='{ROLE}'),
 'role_count', (SELECT count(*) FROM pg_roles),
 'membership_hash', {MEMBERSHIP_HASH},
 'roles', (SELECT jsonb_agg(jsonb_build_object(
   'oid',r.oid::bigint,'fingerprint',{ROLE_HASH},'login',r.rolcanlogin,
   'superuser',r.rolsuper) ORDER BY r.oid)
   FROM (SELECT * FROM pg_roles ORDER BY oid LIMIT 257) r),
 'functions', (SELECT jsonb_agg(jsonb_build_object(
   'oid',p.oid::bigint,'fingerprint',{FUNCTION_HASH},'source_hash',{source_hash},
   'owner',p.proowner::bigint,'owner_set',pg_has_role(session_user,p.proowner,'SET'),
   'grant_option',has_function_privilege(session_user,p.oid,'EXECUTE WITH GRANT OPTION'),
   'acl',{FUNCTION_ACL}) ORDER BY p.oid)
   FROM pg_proc p JOIN pg_namespace n ON n.oid=p.pronamespace WHERE p.oid IN ({selected})),
 'database', (SELECT jsonb_build_object(
   'oid',d.oid::bigint,'fingerprint',{DATABASE_HASH},'owner',d.datdba::bigint,
   'owner_set',pg_has_role(session_user,d.datdba,'SET'),
   'grant_option',has_database_privilege(session_user,d.oid,'TEMP WITH GRANT OPTION'),
   'acl',{DATABASE_ACL}) FROM pg_database d WHERE d.datname=current_database()),
 'unplanned_public_definers', (SELECT count(*) FROM pg_proc p
   WHERE p.prosecdef AND p.oid NOT IN ({selected}) AND EXISTS(
     SELECT 1 FROM aclexplode(COALESCE(p.proacl,acldefault('f',p.proowner))) a
     WHERE a.grantee=0 AND a.privilege_type='EXECUTE')),
 'public_maintain', EXISTS(SELECT 1 FROM pg_class c,
   LATERAL aclexplode(COALESCE(c.relacl,acldefault('r',c.relowner))) a
   WHERE c.relkind IN ('r','p','v','m','f') AND a.grantee=0 AND a.privilege_type='MAINTAIN')
);
ROLLBACK;
"""


def integer(value):
    need(type(value) is int and 0 < value < 2**32)


def digest(value):
    need(isinstance(value, str) and re.fullmatch("[0-9a-f]{64}", value))


def validate(payload, token, ids):
    need(len(payload) <= MAX_BYTES)
    d = json.loads(payload, object_pairs_hook=reject_duplicates)
    need(isinstance(d, dict) and set(d) == {
        "token", "identity_matches", "server_major", "actor_oid", "new_role_exists",
        "role_count", "membership_hash", "roles", "functions", "database",
        "unplanned_public_definers", "public_maintain"})
    need(d["token"] == token and re.fullmatch("[0-9a-f]{32}", token))
    need(d["identity_matches"] is True and type(d["server_major"]) is int and d["server_major"] == 17)
    integer(d["actor_oid"])
    for key in ("new_role_exists", "public_maintain"):
        need(type(d[key]) is bool)
    need(type(d["unplanned_public_definers"]) is int and 0 <= d["unplanned_public_definers"] <= 100000)
    need(type(d["role_count"]) is int and 1 <= d["role_count"] <= 256)
    digest(d["membership_hash"])
    need(isinstance(d["roles"], list) and len(d["roles"]) == d["role_count"])
    roleids = set()
    for r in d["roles"]:
        need(isinstance(r, dict) and set(r) == {"oid", "fingerprint", "login", "superuser"})
        integer(r["oid"])
        digest(r["fingerprint"])
        need(r["oid"] not in roleids and type(r["login"]) is bool and type(r["superuser"]) is bool)
        roleids.add(r["oid"])
    need(d["actor_oid"] in roleids)
    need(isinstance(d["functions"], list) and len(d["functions"]) == len(ids))
    seen = set()
    for item, privileges in [(f, {"EXECUTE"}) for f in d["functions"]] + [
            (d["database"], {"TEMPORARY", "CREATE", "CONNECT"})]:
        expected = {"oid", "fingerprint", "owner", "owner_set", "grant_option", "acl"}
        if privileges == {"EXECUTE"}:
            expected.add("source_hash")
        need(isinstance(item, dict) and set(item) == expected)
        integer(item["oid"])
        integer(item["owner"])
        need(item["owner"] in roleids)
        digest(item["fingerprint"])
        if "source_hash" in item:
            digest(item["source_hash"])
            need(item["oid"] in ids and item["oid"] not in seen)
            seen.add(item["oid"])
        need(type(item["owner_set"]) is bool and type(item["grant_option"]) is bool)
        need(isinstance(item["acl"], list) and len(item["acl"]) <= 2048)
        entries = set()
        for a in item["acl"]:
            need(isinstance(a, list) and len(a) == 4)
            integer(a[0])
            need(type(a[1]) is int and (a[1] == 0 or a[1] in roleids))
            need(a[0] in roleids and a[2] in privileges and type(a[3]) is bool)
            need(tuple(a) not in entries)
            entries.add(tuple(a))
    need(seen == set(ids))
    d.pop("token")
    return d


def proposals(snapshot):
    output = []
    for item, kind, privilege in [(f, "function", "EXECUTE") for f in snapshot["functions"]] + [
            (snapshot["database"], "database", "TEMPORARY")]:
        public = [a for a in item["acl"] if a[1] == 0 and a[2] == privilege]
        need(len(public) == 1 and public[0][0] == item["owner"] and not public[0][3])
        direct = {a[1] for a in item["acl"] if a[2] == privilege}
        added = [r["oid"] for r in snapshot["roles"] if r["oid"] not in direct]
        after = [a for a in item["acl"] if a not in public] + [
            [item["owner"], oid, privilege, False] for oid in added]
        output.append({"kind": kind, "oid": item["oid"], "fingerprint": item["fingerprint"],
                       "owner": item["owner"], "privilege": privilege,
                       "before_acl": sorted(item["acl"]), "after_acl": sorted(after),
                       "added_grantees": sorted(added),
                       "actor_can_change": item["owner_set"] and item["grant_option"]})
    return output


def select_changes(snapshot, scope="full"):
    changes = proposals(snapshot)
    executable = [c for c in changes if c["actor_can_change"]]
    residual = [c for c in changes if not c["actor_can_change"]]
    if scope == "full":
        need(executable and not residual and all(c["actor_can_change"] for c in executable))
        return executable, []
    if scope == "q10_2l_a":
        need(executable and residual)
        need(all(c["actor_can_change"] for c in executable))
        need(any(c["kind"] == "database" and c["privilege"] == "TEMPORARY" for c in executable))
        need(any(c["kind"] == "function" and c["privilege"] == "EXECUTE" for c in executable))
        need(all(c["kind"] == "function" and c["privilege"] == "EXECUTE" for c in residual))
        return executable, residual
    raise ValueError("unknown rights plan scope")


def generate_sql(snapshot, rollback=False, *, scope="full", finish="commit",
                 statement_timeout="5s"):
    """Generate a bound transaction, never connect or execute it."""
    need(not snapshot["new_role_exists"] and not snapshot["public_maintain"]
         and snapshot["unplanned_public_definers"] == 0)
    need(finish in {"commit", "rollback"})
    need(isinstance(statement_timeout, str) and statement_timeout in {"5s", "30s", "60s"})
    changes, residual = select_changes(snapshot, scope)
    manifest = {"actor_oid": snapshot["actor_oid"], "membership_hash": snapshot["membership_hash"],
                "roles": [[r["oid"], r["fingerprint"]] for r in sorted(snapshot["roles"], key=lambda r:r["oid"])],
                "changes": changes,
                "residual": [{"kind": c["kind"], "oid": c["oid"], "fingerprint": c["fingerprint"],
                              "acl": c["before_acl"]} for c in residual]}
    selected = ids_sql([f["oid"] for f in snapshot["functions"]])
    public_guard = f"""
  IF EXISTS(SELECT 1 FROM pg_proc p WHERE p.prosecdef AND p.oid NOT IN ({selected})
      AND EXISTS(SELECT 1 FROM aclexplode(COALESCE(p.proacl,acldefault('f',p.proowner))) a
        WHERE a.grantee=0 AND a.privilege_type='EXECUTE'))
    OR EXISTS(SELECT 1 FROM pg_class c,
      LATERAL aclexplode(COALESCE(c.relacl,acldefault('r',c.relowner))) a
      WHERE c.relkind IN ('r','p','v','m','f') AND a.grantee=0 AND a.privilege_type='MAINTAIN') THEN
    RAISE EXCEPTION USING MESSAGE='rights plan additional PUBLIC risk drift';
  END IF;
"""
    encoded = json.dumps(manifest, sort_keys=True, separators=(",", ":")).replace("'", "''")
    before = "after_acl" if rollback else "before_acl"
    after = "before_acl" if rollback else "after_acl"
    action = "REVOKE" if rollback else "GRANT"
    direction = "FROM" if rollback else "TO"
    public_action = "GRANT" if rollback else "REVOKE"
    public_direction = "TO" if rollback else "FROM"
    suffix = " RESTRICT" if rollback else ""
    public_suffix = "" if rollback else " RESTRICT"
    ending = "COMMIT;" if finish == "commit" else "ROLLBACK;"
    header = ("-- APPLY: separately approved production rights change."
              if finish == "commit"
              else "-- DRY-RUN: identical body, transaction rolled back.")
    return f"""{header}
-- Preserves canonical ACL entries, not NULL-versus-default catalog representation.
\\set ON_ERROR_STOP on
BEGIN;
SET LOCAL statement_timeout='{statement_timeout}';
SET LOCAL lock_timeout='2s';
SET LOCAL idle_in_transaction_session_timeout='90s';
SET LOCAL search_path=pg_catalog;
SELECT 1 / ((current_database()=:'expected_database_name'
  AND session_user=:'expected_user')::int) AS identity_guard
\\gset
DO $rights_plan$
DECLARE
  manifest jsonb := '{encoded}'::jsonb;
  item jsonb;
  role_oid oid;
  role_name name;
  object_name text;
  privilege text;
  object_type text;
  actual_hash text;
  actual_acl jsonb;
  role_state jsonb;
BEGIN
  IF current_setting('server_version_num')::int NOT BETWEEN 170000 AND 179999
    OR (SELECT oid FROM pg_roles WHERE rolname=current_user) <> (manifest->>'actor_oid')::oid
    OR EXISTS(SELECT 1 FROM pg_roles WHERE rolname='{ROLE}') THEN
    RAISE EXCEPTION USING MESSAGE='rights plan actor/version/role guard failed';
  END IF;
  SELECT jsonb_agg(jsonb_build_array(r.oid::bigint,{ROLE_HASH}) ORDER BY r.oid)
    INTO role_state FROM pg_roles r;
  IF role_state IS DISTINCT FROM manifest->'roles'
    OR {MEMBERSHIP_HASH} IS DISTINCT FROM manifest->>'membership_hash' THEN
    RAISE EXCEPTION USING MESSAGE='rights plan role-state drift';
  END IF;
{public_guard}
  FOR item IN SELECT value FROM jsonb_array_elements(COALESCE(manifest->'residual','[]'::jsonb)) LOOP
    IF item->>'kind'='function' THEN
      SELECT {FUNCTION_HASH}, {FUNCTION_ACL}
        INTO actual_hash,actual_acl FROM pg_proc p JOIN pg_namespace n ON n.oid=p.pronamespace
        WHERE p.oid=(item->>'oid')::oid;
    ELSE
      SELECT {DATABASE_HASH}, {DATABASE_ACL}
        INTO actual_hash,actual_acl FROM pg_database d
        WHERE d.oid=(item->>'oid')::oid AND d.datname=current_database();
    END IF;
    IF actual_hash IS DISTINCT FROM item->>'fingerprint'
      OR actual_acl IS DISTINCT FROM item->'acl' THEN
      RAISE EXCEPTION USING MESSAGE='rights plan residual ACL drift';
    END IF;
  END LOOP;
  FOR item IN SELECT value FROM jsonb_array_elements(manifest->'changes') LOOP
    IF item->>'kind'='function' THEN
      SELECT {FUNCTION_HASH}, {FUNCTION_ACL}
        INTO actual_hash,actual_acl FROM pg_proc p JOIN pg_namespace n ON n.oid=p.pronamespace
        WHERE p.oid=(item->>'oid')::oid;
    ELSE
      SELECT {DATABASE_HASH}, {DATABASE_ACL}
        INTO actual_hash,actual_acl FROM pg_database d
        WHERE d.oid=(item->>'oid')::oid AND d.datname=current_database();
    END IF;
    IF actual_hash IS DISTINCT FROM item->>'fingerprint'
      OR actual_acl IS DISTINCT FROM item->'{before}'
      OR NOT pg_has_role(current_user,(item->>'owner')::oid,'SET') THEN
      RAISE EXCEPTION USING MESSAGE='rights plan object/ACL/authority drift';
    END IF;
  END LOOP;
  FOR item IN SELECT value FROM jsonb_array_elements(manifest->'changes') LOOP
    SELECT rolname INTO STRICT role_name FROM pg_roles WHERE oid=(item->>'owner')::oid;
    EXECUTE format('SET LOCAL ROLE %I',role_name);
    IF item->>'kind'='function' THEN
      SELECT p.oid::regprocedure::text INTO STRICT object_name
        FROM pg_proc p WHERE p.oid=(item->>'oid')::oid;
      object_type := 'FUNCTION';
      privilege := 'EXECUTE';
    ELSE
      object_name := quote_ident(current_database());
      object_type := 'DATABASE';
      privilege := 'TEMPORARY';
    END IF;
    FOR role_oid IN SELECT value::text::oid
      FROM jsonb_array_elements(item->'added_grantees') LOOP
      SELECT rolname INTO STRICT role_name FROM pg_roles WHERE oid=role_oid;
      EXECUTE format('{action} %s ON %s %s {direction} %I{suffix}',
                     privilege,object_type,object_name,role_name);
    END LOOP;
    EXECUTE format('{public_action} %s ON %s %s {public_direction} PUBLIC{public_suffix}',
                   privilege,object_type,object_name);
    EXECUTE 'RESET ROLE';
  END LOOP;
  FOR item IN SELECT value FROM jsonb_array_elements(manifest->'changes') LOOP
    IF item->>'kind'='function' THEN
      SELECT {FUNCTION_HASH}, {FUNCTION_ACL}
        INTO actual_hash,actual_acl FROM pg_proc p JOIN pg_namespace n ON n.oid=p.pronamespace
        WHERE p.oid=(item->>'oid')::oid;
    ELSE
      SELECT {DATABASE_HASH}, {DATABASE_ACL}
        INTO actual_hash,actual_acl FROM pg_database d
        WHERE d.oid=(item->>'oid')::oid AND d.datname=current_database();
    END IF;
    IF actual_hash IS DISTINCT FROM item->>'fingerprint'
      OR actual_acl IS DISTINCT FROM item->'{after}' THEN
      RAISE EXCEPTION USING MESSAGE='rights plan postcondition failed';
    END IF;
    FOR role_oid IN SELECT (value->>0)::oid FROM jsonb_array_elements(manifest->'roles') LOOP
      IF item->>'kind'='function' THEN
        IF NOT has_function_privilege(role_oid,(item->>'oid')::oid,'EXECUTE') THEN
          RAISE EXCEPTION USING MESSAGE='existing function access lost';
        END IF;
      ELSE
        IF NOT has_database_privilege(role_oid,(item->>'oid')::oid,'TEMP') THEN
          RAISE EXCEPTION USING MESSAGE='existing TEMP access lost';
        END IF;
      END IF;
    END LOOP;
  END LOOP;
  SELECT jsonb_agg(jsonb_build_array(r.oid::bigint,{ROLE_HASH}) ORDER BY r.oid)
    INTO role_state FROM pg_roles r;
  IF role_state IS DISTINCT FROM manifest->'roles'
    OR {MEMBERSHIP_HASH} IS DISTINCT FROM manifest->>'membership_hash' THEN
    RAISE EXCEPTION USING MESSAGE='rights plan concurrent role-state drift';
  END IF;
  FOR item IN SELECT value FROM jsonb_array_elements(COALESCE(manifest->'residual','[]'::jsonb)) LOOP
    IF item->>'kind'='function' THEN
      SELECT {FUNCTION_HASH}, {FUNCTION_ACL}
        INTO actual_hash,actual_acl FROM pg_proc p JOIN pg_namespace n ON n.oid=p.pronamespace
        WHERE p.oid=(item->>'oid')::oid;
    ELSE
      SELECT {DATABASE_HASH}, {DATABASE_ACL}
        INTO actual_hash,actual_acl FROM pg_database d
        WHERE d.oid=(item->>'oid')::oid AND d.datname=current_database();
    END IF;
    IF actual_hash IS DISTINCT FROM item->>'fingerprint'
      OR actual_acl IS DISTINCT FROM item->'acl' THEN
      RAISE EXCEPTION USING MESSAGE='rights plan residual ACL drift';
    END IF;
  END LOOP;
{public_guard}
END
$rights_plan$;
{ending}
"""


def main():
    need(len(sys.argv) == 3 and sys.argv[1] == "--read-only-from-evidence")
    evidence = json.loads(Path(sys.argv[2]).read_text())
    need(evidence.get("scope", "").startswith("Q10.2h:") and evidence["count"] == 2)
    ids = [f["routine_oid"] for f in evidence["functions"]] + [
        h["oid"] for h in evidence["helpers"] if h["public_execute"]]
    need(len(ids) == 10)
    ids_sql(ids)
    bootstrap = runpy.run_path(str(Path(__file__).with_name("check-role-bootstrap.py")))
    command, env = bootstrap["connection_parameters"]()
    token = secrets.token_hex(16)
    command += ["-v", "audit_token=" + token]
    env["PGAPPNAME"] = "dino-rights-plan-readonly"
    snapshot = validate(BASE["collect"](command, env, query(ids), diagnose=True), token, ids)
    source_hashes = {f["routine_oid"]: f["source_sha256"] for f in evidence["functions"]}
    need(all(f["source_hash"] == source_hashes[f["oid"]] for f in snapshot["functions"]
             if f["oid"] in source_hashes))
    changes = proposals(snapshot)
    report = {"status": "PREPARATION_ONLY", "database_mutated": False,
              "candidate_data_read": False, "connections": 1,
              "snapshot": snapshot, "changes": changes}
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    try:
        main()
    except (ValueError, TypeError, KeyError, UnicodeError, RecursionError, OSError,
            configparser.Error, subprocess.TimeoutExpired, KeyboardInterrupt):
        print("STOP: rights inventory rejected; no raw output or retry", file=sys.stderr)
        raise SystemExit(1) from None
