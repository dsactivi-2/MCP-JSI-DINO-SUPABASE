#!/usr/bin/env python3

import os
import signal
import subprocess
import tempfile
import time
from pathlib import Path

from gate_b1_test_support import (
    STREAM_GUARD_PATH,
    fail,
    guard_arguments,
    guard_environment,
    wait_for_pid_exit,
)

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

    environment = guard_environment(test_root)
    process = subprocess.Popen(
        ["/opt/homebrew/bin/python3", "-B", *guard_arguments(test_root, fake_psql)],
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

    if not wait_for_pid_exit(child_pid):
        os.killpg(child_pid, signal.SIGKILL)
        fail("SIGTERM left fake psql running")

print("PASS: SIGTERM terminates fake psql")
