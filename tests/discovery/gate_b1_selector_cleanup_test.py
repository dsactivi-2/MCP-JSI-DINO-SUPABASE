#!/usr/bin/env python3

import signal
import subprocess
import tempfile
from pathlib import Path
from unittest import mock

from gate_b1_test_support import fail, guard_runtime, load_stream_guard, wait_for_process_exit

class FailingSelector:
    def register(self, *_arguments: object) -> None:
        raise OSError("synthetic selector registration failure")

    def close(self) -> None:
        pass


stream_guard = load_stream_guard()

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

    real_popen = stream_guard.subprocess.Popen
    started_processes: list[subprocess.Popen[bytes]] = []

    def capturing_popen(*arguments: object, **keywords: object) -> subprocess.Popen[bytes]:
        process = real_popen(*arguments, **keywords)
        started_processes.append(process)
        return process

    with guard_runtime(test_root, fake_psql):
        with (
            mock.patch.object(stream_guard.subprocess, "Popen", side_effect=capturing_popen),
            mock.patch.object(stream_guard.selectors, "DefaultSelector", return_value=FailingSelector()),
        ):
            try:
                stream_guard.main()
            except OSError:
                pass

    if len(started_processes) != 1:
        fail("selector case did not start exactly one fake psql process")
    child_process = started_processes[0]
    if not wait_for_process_exit(child_process):
        os.killpg(child_process.pid, signal.SIGKILL)
        fail("selector initialization failure left fake psql running")

print("PASS: selector initialization failure terminates fake psql")
