#!/usr/bin/env python3

import os
import signal
import tempfile
import time
from pathlib import Path
from unittest import mock

from gate_b1_test_support import fail, guard_runtime, load_stream_guard, wait_for_pid_exit

stream_guard = load_stream_guard()

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

    try:
        with guard_runtime(test_root, fake_psql):
            with mock.patch.object(stream_guard.os, "open", side_effect=open_with_broken_raw):
                try:
                    stream_guard.main()
                except OSError:
                    pass
    finally:
        os.close(write_fd)

    for _ in range(100):
        if pid_path.exists():
            break
        time.sleep(0.01)
    if not pid_path.exists():
        fail("fake psql did not start before the I/O failure")

    process_id = int(pid_path.read_text(encoding="utf-8").strip())
    if not wait_for_pid_exit(process_id):
        os.killpg(process_id, signal.SIGKILL)
        fail("unexpected I/O failure left fake psql running")

print("PASS: unexpected I/O failure terminates fake psql")
