#!/usr/bin/env python3

import importlib.util
import os
import signal
import sys
import tempfile
import time
from pathlib import Path
from unittest import mock


REPO_ROOT = Path(__file__).resolve().parents[2]
STREAM_GUARD_PATH = REPO_ROOT / "scripts/discovery/gate_b1_stream_guard.py"


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def process_exists(pid: int) -> bool:
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    return True


spec = importlib.util.spec_from_file_location("gate_b1_stream_guard", STREAM_GUARD_PATH)
if spec is None or spec.loader is None:
    fail("stream guard could not be imported")
stream_guard = importlib.util.module_from_spec(spec)
spec.loader.exec_module(stream_guard)

with tempfile.TemporaryDirectory(prefix="gate-b1-stream-guard-test.") as temp_dir:
    test_root = Path(temp_dir)
    fake_psql = test_root / "fake-psql"
    sql_path = test_root / "gate.sql"
    manifest_path = test_root / "manifest.json"
    raw_path = test_root / "raw.out"
    pid_path = test_root / "fake-psql.pid"

    sql_path.write_text("synthetic SQL\n", encoding="utf-8")
    fake_psql.write_text(
        "#!/bin/bash\n"
        "set -euo pipefail\n"
        f"printf '%s\\n' \"$$\" >{pid_path!s}\n"
        "boundary_token=\n"
        "for argument in \"$@\"; do\n"
        "  case \"${argument}\" in\n"
        "    --set=boundary_token=*) boundary_token=\"${argument#--set=boundary_token=}\" ;;\n"
        "  esac\n"
        "done\n"
        "printf '__GATE_B1_BOUNDARY__|%s|BEGIN|SQL-GATE-B1-001\\n' \"${boundary_token}\"\n"
        "printf 'SQL-GATE-B1-001,TEST_DATABASE,TEST_IDENTITY,TEST_IDENTITY,150000,on,f\\n'\n"
        "sleep 30\n",
        encoding="utf-8",
    )
    fake_psql.chmod(0o700)

    read_fd, write_fd = os.pipe()
    os.close(read_fd)
    real_open = os.open

    def open_with_broken_raw(path: object, flags: int, mode: int = 0o777) -> int:
        if Path(path) == raw_path:
            return os.dup(write_fd)
        return real_open(path, flags, mode)

    old_argv = sys.argv
    old_environment = os.environ.copy()
    try:
        sys.argv = [
            str(STREAM_GUARD_PATH),
            "--psql",
            str(fake_psql),
            "--sql",
            str(sql_path),
            "--raw",
            str(raw_path),
            "--manifest",
            str(manifest_path),
            "--gate-id",
            "DISCOVERY-GATE-B1-V2-2026-09-11",
            "--target-alias",
            "dino_crm_discovery_target_01",
            "--sql-sha256",
            "0" * 64,
            "--window-end-epoch",
            str(int(time.time()) + 60),
            "--timeout-seconds",
            "60",
        ]
        os.environ.update(
            {
                "GATE_B1_EXPECTED_DATABASE_NAME": "TEST_DATABASE",
                "PGSERVICE": "dino_crm_discovery_target_01",
                "PGSERVICEFILE": str(test_root / "service.conf"),
                "PGPASSFILE": str(test_root / "pgpass"),
            }
        )
        with mock.patch.object(stream_guard.os, "open", side_effect=open_with_broken_raw):
            try:
                stream_guard.main()
            except OSError:
                pass
    finally:
        sys.argv = old_argv
        os.environ.clear()
        os.environ.update(old_environment)
        os.close(write_fd)

    for _ in range(100):
        if pid_path.exists():
            break
        time.sleep(0.01)
    if not pid_path.exists():
        fail("fake psql did not start before the I/O failure")

    process_id = int(pid_path.read_text(encoding="utf-8").strip())
    for _ in range(100):
        if not process_exists(process_id):
            break
        time.sleep(0.01)
    if process_exists(process_id):
        os.killpg(process_id, signal.SIGKILL)
        fail("unexpected I/O failure left fake psql running")

print("PASS: unexpected I/O failure terminates fake psql")
