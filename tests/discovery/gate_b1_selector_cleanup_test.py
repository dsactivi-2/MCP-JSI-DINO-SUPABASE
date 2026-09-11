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


class FailingSelector:
    def register(self, *_arguments: object) -> None:
        raise OSError("synthetic selector registration failure")

    def close(self) -> None:
        pass


spec = importlib.util.spec_from_file_location("gate_b1_stream_guard", STREAM_GUARD_PATH)
if spec is None or spec.loader is None:
    fail("stream guard could not be imported")
stream_guard = importlib.util.module_from_spec(spec)
spec.loader.exec_module(stream_guard)

with tempfile.TemporaryDirectory(prefix="gate-b1-selector-test.") as temp_dir:
    test_root = Path(temp_dir)
    fake_psql = test_root / "fake-psql"
    sql_path = test_root / "gate.sql"

    sql_path.write_text("synthetic SQL\n", encoding="utf-8")
    fake_psql.write_text(
        "#!/bin/bash\n"
        "set -euo pipefail\n"
        "sleep 30\n",
        encoding="utf-8",
    )
    fake_psql.chmod(0o700)

    old_argv = sys.argv
    old_environment = os.environ.copy()
    real_popen = stream_guard.subprocess.Popen
    started_processes: list[object] = []

    def capturing_popen(*arguments: object, **keywords: object) -> object:
        process = real_popen(*arguments, **keywords)
        started_processes.append(process)
        return process

    try:
        sys.argv = [
            str(STREAM_GUARD_PATH),
            "--psql",
            str(fake_psql),
            "--sql",
            str(sql_path),
            "--raw",
            str(test_root / "raw.out"),
            "--manifest",
            str(test_root / "manifest.json"),
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
        with (
            mock.patch.object(stream_guard.subprocess, "Popen", side_effect=capturing_popen),
            mock.patch.object(stream_guard.selectors, "DefaultSelector", return_value=FailingSelector()),
        ):
            try:
                stream_guard.main()
            except OSError:
                pass
    finally:
        sys.argv = old_argv
        os.environ.clear()
        os.environ.update(old_environment)

    if len(started_processes) != 1:
        fail("selector case did not start exactly one fake psql process")
    child_process = started_processes[0]
    for _ in range(200):
        if child_process.poll() is not None:
            break
        time.sleep(0.01)
    if child_process.poll() is None:
        os.killpg(child_process.pid, signal.SIGKILL)
        fail("selector initialization failure left fake psql running")

print("PASS: selector initialization failure terminates fake psql")
