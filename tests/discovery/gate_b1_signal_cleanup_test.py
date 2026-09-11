#!/usr/bin/env python3

import os
import signal
import subprocess
import tempfile
import time
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
STREAM_GUARD = REPO_ROOT / "scripts/discovery/gate_b1_stream_guard.py"


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def process_exists(pid: int) -> bool:
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    return True


with tempfile.TemporaryDirectory(prefix="gate-b1-signal-test.") as temp_dir:
    test_root = Path(temp_dir)
    fake_psql = test_root / "fake-psql"
    pid_path = test_root / "fake-psql.pid"
    sql_path = test_root / "gate.sql"
    raw_path = test_root / "raw.out"
    manifest_path = test_root / "manifest.json"

    sql_path.write_text("synthetic SQL\n", encoding="utf-8")
    fake_psql.write_text(
        "#!/bin/bash\n"
        "set -euo pipefail\n"
        f"printf '%s\\n' \"$$\" >{pid_path!s}\n"
        "trap 'exit 0' TERM HUP INT\n"
        "sleep 30\n",
        encoding="utf-8",
    )
    fake_psql.chmod(0o700)

    environment = {
        "GATE_B1_EXPECTED_DATABASE_NAME": "TEST_DATABASE",
        "PGSERVICE": "dino_crm_discovery_target_01",
        "PGSERVICEFILE": str(test_root / "service.conf"),
        "PGPASSFILE": str(test_root / "pgpass"),
    }
    process = subprocess.Popen(
        [
            "/opt/homebrew/bin/python3",
            str(STREAM_GUARD),
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
        ],
        env=environment,
    )

    for _ in range(200):
        if pid_path.exists():
            break
        if process.poll() is not None:
            fail("stream guard exited before fake psql started")
        time.sleep(0.01)
    if not pid_path.exists():
        process.kill()
        fail("fake psql did not start")

    child_pid = int(pid_path.read_text(encoding="utf-8").strip())
    process.send_signal(signal.SIGTERM)
    process.wait(timeout=5)

    for _ in range(200):
        if not process_exists(child_pid):
            break
        time.sleep(0.01)
    if process_exists(child_pid):
        os.killpg(child_pid, signal.SIGKILL)
        fail("SIGTERM left fake psql running")

print("PASS: SIGTERM terminates fake psql")
