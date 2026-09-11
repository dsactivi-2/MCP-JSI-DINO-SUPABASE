#!/usr/bin/env python3
"""Run only in a newly created, networkless synthetic Docker container."""

import argparse
import hashlib
import json
from pathlib import Path
import re
import runpy
import secrets
import subprocess
import sys
import time
import uuid


ROOT = Path(__file__).resolve().parents[2]
SQL_ROOT = ROOT / "docs/discovery/sql"
ROLE = "dino_crm_discovery_ro_v1"
IMAGE = "sha256:18cfe3ef5e6815560c98237d6216d1e5119702fb0f3894c8785dd58b8bbe5d73"


def docker(*args, input=None, timeout=30):
    return subprocess.run(
        ["docker", *args], input=input, text=True, capture_output=True,
        timeout=timeout, check=False,
    )


def require(condition, label):
    if not condition:
        raise RuntimeError(label)


def verify_public_execution_boundaries(sql):
    """Reproduce PostgreSQL privilege limits using only disposable fixtures."""
    fixture = """
CREATE ROLE synthetic_boundary_reader LOGIN;
ALTER ROLE synthetic_boundary_reader SET default_transaction_read_only=on;
CREATE TABLE public.synthetic_boundary_probe(id integer);
CREATE SCHEMA synthetic_boundary_private;
CREATE FUNCTION synthetic_boundary_private.writer() RETURNS integer
LANGUAGE plpgsql SECURITY DEFINER AS $$BEGIN
  INSERT INTO public.synthetic_boundary_probe VALUES(1); RETURN 1;
END$$;
CREATE VIEW public.synthetic_boundary_view AS SELECT synthetic_boundary_private.writer();
GRANT SELECT ON public.synthetic_boundary_view TO PUBLIC;
CREATE VIEW public.synthetic_boundary_view2 AS SELECT * FROM public.synthetic_boundary_view;
GRANT SELECT ON public.synthetic_boundary_view2 TO PUBLIC;
CREATE FUNCTION synthetic_boundary_private.second() RETURNS integer
LANGUAGE sql SECURITY DEFINER AS 'SELECT 1';
"""
    require(sql(fixture).returncode == 0, "public boundary fixtures failed")
    sys.path.insert(0, str(ROOT / "scripts/discovery"))
    extended = runpy.run_path(str(ROOT / "scripts/discovery/audit-public-paths.py"))
    query = "\\set expected_user postgres\n\\set audit_token " + "a"*32 + "\n" + extended["QUERY"]
    audited = sql(query)
    require(audited.returncode == 0, "extended audit SQL failed")
    report = extended["summarize_extended"](audited.stdout.encode(), "a"*32)
    require(report["count"] == 2 and any(f["write_indicators"] == ["INSERT"]
            for f in report["functions"]), "extended source summary failed")
    require(any(n["depth"] == 2 and n["public_access"] for n in report["paths"]["nodes"]),
            "extended audit missed indirect view chain")
    require(any(h["name"] == "lo_create" and h["public_execute"]
                and not h["security_definer"] for h in report["helpers"]),
            "extended helper ACL audit incorrect")
    untouched = sql("SELECT count(*) FROM public.synthetic_boundary_probe;")
    require(untouched.returncode == 0 and untouched.stdout.strip() == "0",
            "extended audit executed writer")
    require(sql("CREATE FUNCTION synthetic_boundary_private.third() RETURNS integer "
                "LANGUAGE sql SECURITY DEFINER AS 'SELECT 1';").returncode == 0,
            "extended scope-change fixture failed")
    changed = sql(query)
    require(changed.returncode == 0, "scope-change audit SQL failed")
    try:
        extended["summarize_extended"](changed.stdout.encode(), "a"*32)
    except ValueError:
        pass
    else:
        raise RuntimeError("expanded root scope was silently accepted")
    require(sql("DROP FUNCTION synthetic_boundary_private.third();").returncode == 0,
            "extended scope-change fixture cleanup failed")
    direct = sql("SET default_transaction_read_only=off; "
                 "SELECT synthetic_boundary_private.writer();", user="synthetic_boundary_reader")
    require(direct.returncode != 0, "expected schema lookup denial missing")
    indirect = sql("SET default_transaction_read_only=off; "
                   "SELECT * FROM public.synthetic_boundary_view;", user="synthetic_boundary_reader")
    require(indirect.returncode == 0 and indirect.stdout.strip() == "1",
            "indirect definer counterexample not reproduced")
    effect = sql("SELECT count(*) FROM public.synthetic_boundary_probe;")
    require(effect.returncode == 0 and effect.stdout.strip() == "1",
            "indirect definer write effect not reproduced")
    persistent = sql("SET default_transaction_read_only=off; SELECT pg_catalog.lo_create(0);",
                     user="synthetic_boundary_reader")
    require(persistent.returncode == 0 and persistent.stdout.strip().isdigit(),
            "persistent large-object counterexample not reproduced")
    cleanup = """
SELECT lo_unlink(oid) FROM pg_largeobject_metadata
WHERE lomowner=(SELECT oid FROM pg_roles WHERE rolname='synthetic_boundary_reader');
DROP VIEW public.synthetic_boundary_view2;
DROP VIEW public.synthetic_boundary_view;
DROP FUNCTION synthetic_boundary_private.writer();
DROP FUNCTION synthetic_boundary_private.second();
DROP SCHEMA synthetic_boundary_private;
DROP TABLE public.synthetic_boundary_probe;
DROP ROLE synthetic_boundary_reader;
"""
    require(sql(cleanup).returncode == 0, "public boundary fixture cleanup failed")


def verify_rights_plan(sql):
    """Test forward change, exact canonical rollback, drift and new-login denial."""
    sys.path.insert(0, str(ROOT / "scripts/discovery"))
    module = runpy.run_path(str(ROOT / "scripts/discovery/rights_plan.py"))
    require(sql("""
CREATE ROLE synthetic_existing LOGIN;
CREATE ROLE synthetic_group NOLOGIN;
GRANT synthetic_group TO synthetic_existing;
CREATE FUNCTION public.synthetic_rights_one() RETURNS integer
LANGUAGE sql SECURITY DEFINER AS 'SELECT 1';
CREATE FUNCTION public.synthetic_rights_two() RETURNS integer
LANGUAGE sql SECURITY DEFINER AS 'SELECT 2';
CREATE VIEW public.synthetic_rights_view AS SELECT public.synthetic_rights_two() AS value;
GRANT SELECT ON public.synthetic_rights_view TO PUBLIC;
GRANT EXECUTE ON FUNCTION public.synthetic_rights_one() TO synthetic_group WITH GRANT OPTION;
SET ROLE synthetic_group;
GRANT EXECUTE ON FUNCTION public.synthetic_rights_one() TO synthetic_existing WITH GRANT OPTION;
RESET ROLE;
""").returncode == 0, "rights-plan fixtures failed")
    listed = sql("""
SELECT oid FROM pg_proc
WHERE oid IN ('public.synthetic_rights_one()'::regprocedure,
              'public.synthetic_rights_two()'::regprocedure)
  OR (pronamespace='pg_catalog'::regnamespace AND proname IN
      ('lo_create','lo_creat','lo_from_bytea','lo_put','lowrite','lo_unlink','lo_truncate','lo_truncate64'))
ORDER BY oid;
""")
    require(listed.returncode == 0, "rights-plan target enumeration failed")
    ids = [int(value) for value in listed.stdout.splitlines()]
    query = "\\set expected_user postgres\n\\set audit_token " + "a"*32 + "\n" + module["query"](ids)

    def snapshot():
        result = sql(query)
        require(result.returncode == 0, "rights inventory SQL failed")
        return module["validate"](result.stdout.encode(), "a"*32, ids)

    before = snapshot()
    require(len(ids) == 10 and not before["public_maintain"], "rights inventory scope mismatch")
    forward = "\\set expected_user postgres\n" + module["generate_sql"](before)
    reverse = "\\set expected_user postgres\n" + module["generate_sql"](before, rollback=True)
    require(sql("CREATE FUNCTION public.synthetic_unplanned() RETURNS int "
                "LANGUAGE sql SECURITY DEFINER AS 'SELECT 3';").returncode == 0,
            "unplanned function fixture failed")
    require(sql(forward).returncode != 0, "unplanned PUBLIC definer drift accepted")
    require(sql("DROP FUNCTION public.synthetic_unplanned();").returncode == 0,
            "unplanned function cleanup failed")
    require(sql("CREATE TABLE public.synthetic_maintain(id int); "
                "GRANT MAINTAIN ON public.synthetic_maintain TO PUBLIC;").returncode == 0,
            "MAINTAIN drift fixture failed")
    require(sql(forward).returncode != 0, "PUBLIC MAINTAIN drift accepted")
    require(sql("DROP TABLE public.synthetic_maintain;").returncode == 0,
            "MAINTAIN drift cleanup failed")
    broken = forward.replace("EXECUTE 'RESET ROLE';",
                             "EXECUTE 'RESET ROLE'; RAISE EXCEPTION 'synthetic injected failure';", 1)
    require(sql(broken).returncode != 0, "injected mid-transaction failure did not fail")
    aborted = snapshot()
    require(aborted["database"]["acl"] == before["database"]["acl"]
            and [f["acl"] for f in aborted["functions"]] == [f["acl"] for f in before["functions"]],
            "failed transaction left partial ACL changes")
    require(sql(forward).returncode == 0, "rights forward transaction failed")
    after = snapshot()
    for change in module["proposals"](before):
        actual = after["database"] if change["kind"] == "database" else next(
            f for f in after["functions"] if f["oid"] == change["oid"])
        require(actual["acl"] == change["after_acl"], "rights forward ACL mismatch")
    require(sql(forward).returncode != 0, "repeated rights apply accepted")
    require(sql("CREATE ROLE synthetic_new_reader LOGIN; "
                "GRANT CONNECT ON DATABASE role_test TO synthetic_new_reader;").returncode == 0,
            "new-reader fixture failed")
    denied = sql("SELECT lo_create(0);", user="synthetic_new_reader")
    require(denied.returncode != 0, "new reader created large object")
    denied = sql("SELECT public.synthetic_rights_one();", user="synthetic_new_reader")
    require(denied.returncode != 0, "new reader executed definer")
    denied = sql("SELECT * FROM public.synthetic_rights_view;", user="synthetic_new_reader")
    require(denied.returncode != 0, "new reader executed definer indirectly through PUBLIC view")
    require(sql("SELECT * FROM public.synthetic_rights_view;", user="synthetic_existing").returncode == 0,
            "existing indirect view access lost")
    denied = sql("CREATE TEMP TABLE synthetic_temp(id int);", user="synthetic_new_reader")
    require(denied.returncode != 0, "new reader obtained TEMP")
    require(sql("SELECT public.synthetic_rights_one();", user="synthetic_existing").returncode == 0,
            "existing application function access lost")
    require(sql("CREATE TEMP TABLE synthetic_temp(id int);", user="synthetic_existing").returncode == 0,
            "existing application TEMP access lost")
    require(sql(reverse).returncode != 0, "rollback ignored changed role roster")
    require(sql("REVOKE CONNECT ON DATABASE role_test FROM synthetic_new_reader; "
                "DROP ROLE synthetic_new_reader;").returncode == 0,
            "new-reader fixture cleanup failed")
    require(sql(reverse).returncode == 0, "rights rollback failed")
    restored = snapshot()
    require(restored["database"]["acl"] == before["database"]["acl"]
            and [f["acl"] for f in restored["functions"]] == [f["acl"] for f in before["functions"]],
            "canonical ACL rollback mismatch")
    require(sql("GRANT EXECUTE ON FUNCTION public.synthetic_rights_two() TO synthetic_existing;").returncode == 0,
            "ACL drift fixture failed")
    changed = snapshot()
    require(sql(forward).returncode != 0, "ACL drift not rejected")
    require(snapshot()["functions"] == changed["functions"], "failed plan changed ACLs")
    require(sql("""
REVOKE EXECUTE ON FUNCTION public.synthetic_rights_two() FROM synthetic_existing;
DROP VIEW public.synthetic_rights_view;
DROP FUNCTION public.synthetic_rights_one();
DROP FUNCTION public.synthetic_rights_two();
REVOKE synthetic_group FROM synthetic_existing;
DROP ROLE synthetic_existing;
DROP ROLE synthetic_group;
""").returncode == 0, "rights-plan fixtures cleanup failed")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--allow-new-isolated-container", action="store_true")
    parser.add_argument("--owner-compatible-draft", action="store_true")
    args = parser.parse_args()
    require(args.allow_new_isolated_container, "explicit test-container opt-in required")
    name = "dino-role-test-" + uuid.uuid4().hex
    container = None
    checks = []
    started = time.monotonic()
    try:
        result = docker(
            "run", "--detach", "--pull=never", "--name", name,
            "--label", "activi.test=" + name,
            "--network", "none", "--read-only",
            "--memory", "512m", "--cpus", "1", "--pids-limit", "128",
            "--security-opt", "no-new-privileges",
            "--tmpfs", "/var/lib/postgresql/data:rw,nosuid,size=256m",
            "--tmpfs", "/var/run/postgresql:rw,nosuid,size=16m",
            "--tmpfs", "/tmp:rw,nosuid,size=16m",
            "--env", "POSTGRES_HOST_AUTH_METHOD=trust",
            "--env", "POSTGRES_DB=role_test", IMAGE,
            "-c", "listen_addresses=", "-c", "log_statement=none",
        )
        require(result.returncode == 0, "isolated container creation failed")
        container = result.stdout.strip()
        require(re.fullmatch(r"[0-9a-f]{64}", container), "invalid created container ID")
        inspected = docker("inspect", container)
        require(inspected.returncode == 0, "container isolation inspection failed")
        state = json.loads(inspected.stdout)[0]
        require(state["Config"]["Labels"]["activi.test"] == name, "wrong test owner")
        require(state["HostConfig"]["NetworkMode"] == "none", "network isolation missing")
        require(state["HostConfig"]["ReadonlyRootfs"], "read-only root missing")
        require(not state["HostConfig"].get("PortBindings"), "host port exposed")
        require(all(m["Type"] == "tmpfs" for m in state["Mounts"]), "persistent mount found")
        for _ in range(40):
            ready = docker("exec", container, "sh", "-c",
                           'test "$(cat /proc/1/comm)" = postgres && '
                           'pg_isready -U postgres -d role_test')
            if ready.returncode == 0:
                break
            time.sleep(0.25)
        else:
            raise RuntimeError("synthetic database readiness timeout")

        def sql(statement, user="postgres", expected="role_test"):
            return docker(
                "exec", "-i", container, "psql", "-X", "-qAt", "-w",
                "-U", user, "-d", "role_test", "-v", "ON_ERROR_STOP=1",
                "-v", "expected_database_name=" + expected, input=statement,
            )

        def expect_value(statement, value, label):
            result = sql(statement)
            require(result.returncode == 0 and result.stdout.strip() == value, label)

        def run_file(content, expected="role_test", user="postgres"):
            uploaded = docker(
                "exec", "-i", container, "sh", "-c", "cat > /tmp/role-test.sql",
                input=content,
            )
            require(uploaded.returncode == 0, "synthetic SQL transfer failed")
            # Test credentials exist only in memory and anonymous stdin pipes.
            password = secrets.token_urlsafe(32)
            result = docker(
                "exec", "-i", container, "psql", "-X", "-qAt", "-w",
                "-U", user, "-d", "role_test", "-v", "ON_ERROR_STOP=1",
                "-v", "expected_database_name=" + expected,
                "-f", "/tmp/role-test.sql", input=password + "\n" + password + "\n",
            )
            return result

        verify_public_execution_boundaries(sql)
        checks.append("extended audit reads two roots and view dependencies without execution; scope drift rejected")
        checks.append("counterexample: hidden-schema definer executes through a PUBLIC SELECT view")
        checks.append("counterexample: PUBLIC invoker function creates a persistent large object")
        verify_rights_plan(sql)
        checks.append("rights transfer preserves existing access and blocks new-login known write paths")
        checks.append("rights rollback restores canonical ACLs and rejects roster or ACL drift")

        exists = f"SELECT count(*) FROM pg_roles WHERE rolname='{ROLE}';"
        setup_file = ("02-create-least-privilege-discovery-role-v2-draft.sql"
                      if args.owner_compatible_draft else
                      "01-create-least-privilege-discovery-role-v1.sql")
        setup = (SQL_ROOT / setup_file).read_text()
        rollback = (SQL_ROOT / "01-drop-least-privilege-discovery-role-v1.sql").read_text()
        version = sql("SHOW server_version;")
        require(version.returncode == 0, "test version unavailable")
        public_query = runpy.run_path(str(ROOT / "scripts/discovery/check-role-bootstrap.py"))["PUBLIC_QUERY"]
        public_probe = "\\set expected_user postgres\n" + public_query
        expect_value(public_probe, "1|0|0|0|0|0|0", "PUBLIC baseline flags incorrect")
        require(sql("CREATE FUNCTION public.synthetic_definer() RETURNS integer "
                    "LANGUAGE sql SECURITY DEFINER AS 'SELECT 1';").returncode == 0,
                "definer fixture failed")
        expect_value(public_probe, "1|0|0|0|0|1|1", "PUBLIC definer exposure not detected")
        require(sql("DROP FUNCTION public.synthetic_definer();").returncode == 0,
                "definer fixture cleanup failed")
        checks.append("read-only PUBLIC preflight distinguishes baseline and callable definer")
        sys.path.insert(0, str(ROOT / "scripts/discovery"))
        audit = runpy.run_path(str(ROOT / "scripts/discovery/check-public-definers.py"))
        audit_query = ("\\set expected_user postgres\n\\set audit_token " + "a"*32 +
                       "\n" + audit["QUERY"])
        baseline = sql(audit_query)
        require(baseline.returncode == 0, "definer audit SQL baseline failed")
        require(audit["summarize"](baseline.stdout.encode(), "a"*32)["count"] == 0,
                "definer audit baseline nonempty")
        require(sql("CREATE TABLE public.synthetic_audit_probe(id integer); "
                    "CREATE FUNCTION public.synthetic_audit_writer() RETURNS void "
                    "LANGUAGE plpgsql SECURITY DEFINER AS $$BEGIN INSERT INTO "
                    "public.synthetic_audit_probe VALUES(1); END$$; "
                    "CREATE FUNCTION public.synthetic_audit_sql() RETURNS integer "
                    "LANGUAGE sql SECURITY DEFINER RETURN 1; "
                    "CREATE FUNCTION public.synthetic_audit_window() RETURNS integer "
                    "LANGUAGE sql WINDOW SECURITY DEFINER AS 'SELECT 1'; "
                    "CREATE FUNCTION public.synthetic_audit_hidden() RETURNS integer "
                    "LANGUAGE sql SECURITY DEFINER AS 'SELECT 1'; "
                    "REVOKE EXECUTE ON FUNCTION public.synthetic_audit_hidden() FROM PUBLIC; "
                    "CREATE SCHEMA synthetic_private; "
                    "CREATE FUNCTION synthetic_private.synthetic_audit_hidden() RETURNS integer "
                    "LANGUAGE sql SECURITY DEFINER AS 'SELECT 1';").returncode == 0,
                "definer audit fixtures failed")
        audited = sql(audit_query)
        require(audited.returncode == 0, "definer audit SQL fixtures failed")
        audit_report = audit["summarize"](audited.stdout.encode(), "a"*32)
        reconciled = sql("\\set expected_user postgres\n" + audit["RECONCILE_QUERY"])
        require(reconciled.returncode == 0, "definer coverage reconciliation failed")
        coverage = audit["summarize_coverage"](reconciled.stdout.encode())
        require(coverage["public_definer_count"] == 4 and coverage["direct_schema_lookup_count"] == 3
                and coverage["catalog_join_complete"], "definer coverage mismatch")
        require(audit_report["count"] == 3 and
                any(f["routine_kind"] == "window" for f in audit_report["functions"]) and
                any(f["source_representation"] == "create_definition_including_wrapper"
                    for f in audit_report["functions"]) and
                any(f["write_indicators"] == ["INSERT"] for f in audit_report["functions"]),
                "definer audit selection or write indicator incorrect")
        expect_value("SELECT count(*) FROM public.synthetic_audit_probe;", "0",
                     "definer audit executed fixture")
        require(sql("DROP FUNCTION public.synthetic_audit_writer(); "
                    "DROP FUNCTION public.synthetic_audit_sql(); "
                    "DROP FUNCTION public.synthetic_audit_window(); "
                    "DROP FUNCTION public.synthetic_audit_hidden(); "
                    "DROP FUNCTION synthetic_private.synthetic_audit_hidden(); "
                    "DROP SCHEMA synthetic_private; "
                    "DROP TABLE public.synthetic_audit_probe;").returncode == 0,
                "definer audit fixture cleanup failed")
        checks.append("definer audit selects only PUBLIC-reachable routines without executing them")
        checks.append("definer audit handles SQL-standard bodies and labels synthetic INSERT")
        require(sql("REVOKE TEMP ON DATABASE role_test FROM PUBLIC;").returncode == 0,
                "synthetic fixture initialization failed")

        old = sql("SELECT pg_catalog.current_user;")
        require(old.returncode != 0, "original current_user error not reproduced")
        checks.append("original qualified current_user fails")
        require(run_file(setup).returncode == 0, "corrected setup failed")
        expect_value(exists, "1", "role was not created")
        identity = sql("SELECT current_user; SHOW default_transaction_read_only;", user=ROLE)
        require(identity.returncode == 0 and identity.stdout.strip() == ROLE + "\non",
                "new login or read-only default failed")
        expect_value(
            f"SELECT has_database_privilege('{ROLE}', 'role_test', 'CONNECT') "
            f"AND NOT has_database_privilege('{ROLE}', 'role_test', 'CREATE,TEMP');",
            "t", "unexpected database privileges",
        )
        checks.append("setup creates role with CONNECT and read-only login defaults")
        require(run_file(setup).returncode != 0, "existing role not rejected")
        expect_value(exists, "1", "existing role was lost")
        checks.append("existing role rejected without removal")
        require(run_file(rollback).returncode == 0, "corrected rollback failed")
        expect_value(exists, "0", "rollback left role behind")
        checks.append("rollback removes own CONNECT and role")
        require(run_file(setup, expected="wrong_target").returncode != 0,
                "wrong target not rejected")
        expect_value(exists, "0", "wrong target left a role")
        checks.append("wrong database rejected atomically")
        require(sql("GRANT TEMP ON DATABASE role_test TO PUBLIC;").returncode == 0,
                "TEMP fixture failed")
        require(run_file(setup).returncode != 0, "PUBLIC TEMP was not rejected")
        expect_value(exists, "0", "PUBLIC TEMP failure left a role")
        checks.append("PUBLIC TEMP rejected atomically")
        require(sql("REVOKE TEMP ON DATABASE role_test FROM PUBLIC;").returncode == 0,
                "TEMP fixture cleanup failed")
        require(sql("CREATE TABLE public.synthetic_probe(id integer); "
                    "GRANT INSERT ON public.synthetic_probe TO PUBLIC;").returncode == 0,
                "write fixture failed")
        require(run_file(setup).returncode != 0, "PUBLIC write was not rejected")
        expect_value(public_probe, "1|0|1|0|0|0|0", "PUBLIC write exposure not detected")
        expect_value(exists, "0", "PUBLIC write failure left a role")
        checks.append("PUBLIC write rejected atomically")
        require(sql("REVOKE INSERT ON public.synthetic_probe FROM PUBLIC;").returncode == 0,
                "write fixture cleanup failed")
        require(sql("CREATE VIEW public.pg_settings AS SELECT id FROM public.synthetic_probe; "
                    "GRANT UPDATE ON public.pg_settings TO PUBLIC;").returncode == 0,
                "same-name view fixture failed")
        require(run_file(setup).returncode != 0, "application view UPDATE not rejected")
        expect_value(exists, "0", "application view failure left a role")
        checks.append("same-named application view is not exempt from UPDATE checks")
        require(sql("DROP VIEW public.pg_settings;").returncode == 0,
                "same-name view cleanup failed")
        for privilege in ("UPDATE", "UPDATE(id)", "MAINTAIN"):
            require(sql(f"GRANT {privilege} ON public.synthetic_probe TO PUBLIC;").returncode == 0,
                    "UPDATE fixture failed")
            require(run_file(setup).returncode != 0, "PUBLIC UPDATE not rejected")
            if privilege == "MAINTAIN":
                expect_value(public_probe, "1|0|1|0|0|0|0", "PUBLIC maintenance privilege not detected")
            expect_value(exists, "0", "PUBLIC UPDATE failure left a role")
            require(sql(f"REVOKE {privilege} ON public.synthetic_probe FROM PUBLIC;").returncode == 0,
                    "UPDATE fixture cleanup failed")
            checks.append(f"PUBLIC {privilege} rejected atomically")
        require(run_file(setup).returncode == 0, "second setup failed")
        require(sql(f"GRANT SELECT ON public.synthetic_probe TO {ROLE};").returncode == 0,
                "dependency fixture failed")
        require(run_file(rollback).returncode != 0, "unexpected dependency not rejected")
        expect_value(exists, "1", "failed rollback lost role")
        expect_value(
            f"SELECT has_database_privilege('{ROLE}','role_test','CONNECT') "
            f"AND has_table_privilege('{ROLE}','public.synthetic_probe','SELECT');",
            "t", "failed rollback lost grants",
        )
        checks.append("unexpected dependency preserves role and grants on rollback failure")
        require(sql(f"REVOKE SELECT ON public.synthetic_probe FROM {ROLE};").returncode == 0,
                "dependency fixture cleanup failed")
        require(run_file(rollback).returncode == 0, "final rollback failed")
        expect_value(exists, "0", "final rollback left role")
        require(sql("CREATE ROLE synthetic_owner LOGIN CREATEROLE; "
                    "ALTER DATABASE role_test OWNER TO synthetic_owner;").returncode == 0,
                "non-superuser owner fixture failed")
        owner_result = run_file(setup, user="synthetic_owner")
        if args.owner_compatible_draft:
            require(owner_result.returncode == 0, "owner-compatible setup failed")
            expect_value(exists, "1", "owner-compatible setup left no role")
            expect_value(
                f"SELECT count(*) FROM pg_auth_members WHERE member=(SELECT oid FROM pg_roles WHERE rolname='{ROLE}');",
                "0", "discovery role gained membership in another role",
            )
            expect_value(
                f"SELECT count(*) FROM pg_auth_members WHERE roleid=(SELECT oid FROM pg_roles WHERE rolname='{ROLE}') "
                "AND admin_option AND NOT inherit_option AND NOT set_option;",
                "1", "expected single admin-only creator grant missing",
            )
            require(run_file(rollback, user="synthetic_owner").returncode == 0,
                    "non-superuser owner rollback failed")
            expect_value(exists, "0", "non-superuser owner rollback left role")
            checks.append("non-superuser owner setup and rollback with only admin-only creator grant")
            probes = {
                "creator SET": f"GRANT {ROLE} TO postgres WITH ADMIN TRUE, SET TRUE, INHERIT FALSE;",
                "creator INHERIT": f"GRANT {ROLE} TO postgres WITH ADMIN TRUE, SET FALSE, INHERIT TRUE;",
                "different administrator": f"GRANT {ROLE} TO synthetic_owner WITH ADMIN TRUE, SET FALSE, INHERIT FALSE;",
                "outgoing membership": f"GRANT synthetic_owner TO {ROLE};",
            }
            marker = "-- Evaluate the fixed new role explicitly; the creator need not SET ROLE."
            require(setup.count(marker) == 1, "test grant insertion point missing")
            for label, grant in probes.items():
                probe = setup.replace(marker, grant + "\n" + marker)
                require(run_file(probe).returncode != 0, label + " unexpectedly accepted")
                expect_value(exists, "0", label + " left a partial role")
                checks.append(label + " rejected atomically")
        else:
            require(owner_result.returncode != 0, "unsupported owner unexpectedly succeeded")
            expect_value(exists, "0", "unsupported owner left a partial role")
            checks.append("unsupported non-superuser owner fails without a partial role")
        report = {
            "status": "PASS_WITH_GAPS", "scope": "synthetic only; no production connection",
            "gaps": (["password authentication and production compatibility not proven",
                      "PUBLIC routine effects need separate review; role defaults are not enforced read-only"]
                     if args.owner_compatible_draft else
                     ["non-superuser owner cannot satisfy current SET ROLE and zero-membership policy",
                      "PUBLIC routine effects need separate review; role defaults are not enforced read-only"]),
            "setup_file": setup_file,
            "authentication_scope": "local trust: password authentication not proven",
            "image": IMAGE, "server_version": version.stdout.strip(), "checks": checks,
            "sql_sha256": {
                "setup": hashlib.sha256(setup.encode()).hexdigest(),
                "rollback": hashlib.sha256(rollback.encode()).hexdigest(),
            },
            "elapsed_seconds": round(time.monotonic() - started, 2),
        }
    finally:
        if not container:
            # A timed-out Docker client may still have created the named container.
            inspection = docker("inspect", name)
            if inspection.returncode == 0:
                candidate = json.loads(inspection.stdout)[0]
                require(candidate["Config"]["Labels"].get("activi.test") == name,
                        "refusing cleanup of container without exact owner label")
                container = candidate["Id"]
            else:
                remaining = docker("container", "ls", "--all", "--filter",
                                   "name=^/" + name + "$", "--format", "{{.ID}}")
                require(remaining.returncode == 0 and not remaining.stdout.strip(),
                        "cleanup_unverified: cannot prove created container absent")
        if container:
            removed = docker("rm", "--force", container)
            require(removed.returncode == 0, "created test container cleanup failed")
    report["created_container_removed"] = True
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
