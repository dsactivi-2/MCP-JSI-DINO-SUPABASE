#!/usr/bin/env python3
"""Create a separate login service/pgpass for dino_crm_discovery_ro_v1. Never touch owner files."""

import configparser
import getpass
import os
from pathlib import Path
import stat
import subprocess
import sys

ALIAS_OWNER = "dino_crm_discovery_target_01"
ALIAS_RO = "dino_crm_discovery_ro_v1"
ROLE = "dino_crm_discovery_ro_v1"
CONFIG_ROOT = Path("/Users/activi/Library/Application Support/Activi/discovery-targets")
OWNER_SERVICE = CONFIG_ROOT / f"{ALIAS_OWNER}.pg_service.conf"
OWNER_PGPASS = CONFIG_ROOT / f"{ALIAS_OWNER}.pgpass"
RO_SERVICE = CONFIG_ROOT / f"{ALIAS_RO}.pg_service.conf"
RO_PGPASS = CONFIG_ROOT / f"{ALIAS_RO}.pgpass"
PSQL = "/opt/homebrew/bin/psql"


def need(ok, message):
    if not ok:
        raise SystemExit("STOP: " + message)


def secure_existing(path):
    entry = path.lstat()
    need(stat.S_ISREG(entry.st_mode) and stat.S_IMODE(entry.st_mode) == 0o600
         and entry.st_uid == os.getuid() and path.resolve() == path
         and not path.is_symlink(), "restricted file invalid")


def secure_write(path, text):
    path.write_text(text)
    os.chmod(path, 0o600)
    secure_existing(path)


def owner_settings():
    secure_existing(OWNER_SERVICE)
    secure_existing(OWNER_PGPASS)
    cfg = configparser.ConfigParser(interpolation=None, strict=True)
    cfg.read_string(OWNER_SERVICE.read_text())
    need(cfg.sections() == [ALIAS_OWNER], "owner service section mismatch")
    settings = dict(cfg[ALIAS_OWNER])
    need(set(settings) == {"host", "dbname", "user", "sslmode", "connect_timeout"},
         "owner service fields mismatch")
    need("." in settings["user"], "owner pooler user shape unexpected")
    line = OWNER_PGPASS.read_text().splitlines()[0]
    parts = line.split(":", 4)
    need(len(parts) == 5, "owner pgpass shape unexpected")
    return settings, parts


def write_service():
    settings, _parts = owner_settings()
    suffix = settings["user"].split(".", 1)[1]
    body = "\n".join([
        f"[{ALIAS_RO}]",
        "host=" + settings["host"],
        "dbname=" + settings["dbname"],
        "user=" + ROLE + "." + suffix,
        "sslmode=" + settings["sslmode"],
        "connect_timeout=" + settings["connect_timeout"],
        "",
    ])
    secure_write(RO_SERVICE, body)
    return settings, suffix


def write_pgpass(password):
    need(password and "\n" not in password and ":" not in password, "password rejected")
    settings, parts = owner_settings()
    suffix = settings["user"].split(".", 1)[1]
    user = ROLE + "." + suffix
    line = ":".join([parts[0], parts[1], settings["dbname"], user, password]) + "\n"
    secure_write(RO_PGPASS, line)


def smoke_test():
    secure_existing(RO_SERVICE)
    secure_existing(RO_PGPASS)
    env = {
        "PATH": "/opt/homebrew/bin:/usr/bin:/bin",
        "LC_ALL": "C",
        "PGSERVICE": ALIAS_RO,
        "PGSERVICEFILE": str(RO_SERVICE),
        "PGPASSFILE": str(RO_PGPASS),
        "PGSYSCONFDIR": "/private/tmp",
        "PSQL_HISTORY": "/dev/null",
        "PGAPPNAME": "dino-ro-login-smoke",
        "PGOPTIONS": "-c default_transaction_read_only=on -c statement_timeout=5000 "
                     "-c search_path=pg_catalog",
    }
    query = ("BEGIN READ ONLY; SELECT session_user, current_user, "
             "current_setting('transaction_read_only'); ROLLBACK;\n")
    proc = subprocess.run(
        [PSQL, "-X", "-qAt", "-w", "-v", "ON_ERROR_STOP=1"],
        input=query, env=env, text=True, capture_output=True, timeout=20)
    need(proc.returncode == 0, "login smoke test failed")
    fields = proc.stdout.strip().split("|")
    need(len(fields) == 3, "smoke output rejected")
    need(fields[0] == ROLE, "session_user is not the discovery role")
    need(fields[1] == ROLE, "current_user is not the discovery role")
    print('{"status":"LOGIN_OK","role":"%s","read_only":"%s"}' % (ROLE, fields[2]))


def main():
    need(sys.argv[1:] in (["--write-service"], ["--write-pgpass"], ["--smoke-test"],
                          ["--setup-interactive"]), "explicit mode required")
    mode = sys.argv[1]
    if mode in {"--write-service", "--setup-interactive", "--write-pgpass"}:
        write_service()
        print('{"status":"SERVICE_WRITTEN","alias":"%s"}' % ALIAS_RO)
    if mode in {"--write-pgpass", "--setup-interactive"}:
        password = getpass.getpass("Password for dino_crm_discovery_ro_v1: ")
        write_pgpass(password)
        print('{"status":"PGPASS_WRITTEN"}')
    if mode in {"--smoke-test", "--setup-interactive"}:
        smoke_test()


if __name__ == "__main__":
    try:
        main()
    except (ValueError, TypeError, KeyError, OSError, subprocess.TimeoutExpired):
        print("STOP: discovery-role login setup rejected", file=sys.stderr)
        raise SystemExit(1) from None
