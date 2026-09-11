#!/usr/bin/env python3

import os
import signal
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from unittest import mock

from gate_b1_test_support import (
    STREAM_GUARD_PATH,
    fail,
    guard_arguments,
    guard_environment,
    guard_runtime,
    load_stream_guard,
    process_exists,
    wait_for_process_exit,
)

def run_double_signal_driver(test_root: Path) -> int:
    stream_guard = load_stream_guard()
    fake_psql = test_root / "fake-psql"
    real_terminate = stream_guard.terminate

    def terminate_after_second_signal(process: subprocess.Popen[bytes]) -> None:
        os.kill(os.getpid(), signal.SIGTERM)
        real_terminate(process)

    stream_guard.terminate = terminate_after_second_signal
    sys.argv = guard_arguments(test_root, fake_psql)
    os.environ.update(guard_environment(test_root))
    return stream_guard.main()


if os.environ.get("GATE_B1_DOUBLE_SIGNAL_DRIVER") == "1":
    raise SystemExit(run_double_signal_driver(Path(os.environ["GATE_B1_SIGNAL_TEST_ROOT"])))


with tempfile.TemporaryDirectory(prefix="gate-b1-spawn-signal-test.") as temp_dir:
    test_root = Path(temp_dir)
    fake_psql = test_root / "fake-psql"
    (test_root / "gate.sql").write_text("synthetic SQL\n", encoding="utf-8")
    fake_psql.write_text("#!/bin/bash\nset -euo pipefail\nsleep 30\n", encoding="utf-8")
    fake_psql.chmod(0o700)
    stream_guard = load_stream_guard()
    real_popen = stream_guard.subprocess.Popen
    started_processes: list[subprocess.Popen[bytes]] = []
    def interrupted_popen(*arguments: object, **keywords: object) -> subprocess.Popen[bytes]:
        process = real_popen(*arguments, **keywords)
        started_processes.append(process)
        os.kill(os.getpid(), signal.SIGTERM)
        return process

    with guard_runtime(test_root, fake_psql):
        with mock.patch.object(stream_guard.subprocess, "Popen", side_effect=interrupted_popen):
            stream_guard.main()

    if len(started_processes) != 1:
        fail("spawn race did not start exactly one fake psql process")
    child_process = started_processes[0]
    if not wait_for_process_exit(child_process):
        os.killpg(child_process.pid, signal.SIGKILL)
        fail("signal during Popen assignment left fake psql running")


with tempfile.TemporaryDirectory(prefix="gate-b1-double-signal-test.") as temp_dir:
    test_root = Path(temp_dir)
    fake_psql = test_root / "fake-psql"
    pid_path = test_root / "fake-psql.pid"
    (test_root / "gate.sql").write_text("synthetic SQL\n", encoding="utf-8")
    fake_psql.write_text(
        "#!/bin/bash\n"
        "set -euo pipefail\n"
        f"printf '%s\\n' \"$$\" >{pid_path!s}\n"
        "sleep 30\n",
        encoding="utf-8",
    )
    fake_psql.chmod(0o700)
    environment = os.environ.copy()
    environment.update(guard_environment(test_root))
    environment.update(
        {
            "GATE_B1_DOUBLE_SIGNAL_DRIVER": "1",
            "GATE_B1_SIGNAL_TEST_ROOT": str(test_root),
        }
    )
    driver = subprocess.Popen(["/opt/homebrew/bin/python3", "-B", str(Path(__file__).resolve())], env=environment)
    for _ in range(200):
        if pid_path.exists():
            break
        if driver.poll() is not None:
            fail("double-signal driver exited before fake psql started")
        time.sleep(0.01)
    if not pid_path.exists():
        driver.kill()
        fail("double-signal fake psql did not start")

    child_pid = int(pid_path.read_text(encoding="utf-8").strip())
    driver.send_signal(signal.SIGTERM)
    driver.wait(timeout=5)
    try:
        os.kill(child_pid, 0)
    except ProcessLookupError:
        pass
    else:
        os.killpg(child_pid, signal.SIGKILL)
        fail("second cleanup signal left fake psql running")


print("PASS: spawn-window and repeated cleanup signals terminate fake psql")
