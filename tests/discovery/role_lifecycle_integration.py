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
            "gaps": (["password authentication and production compatibility not proven"]
                     if args.owner_compatible_draft else
                     ["non-superuser owner cannot satisfy current SET ROLE and zero-membership policy"]),
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
