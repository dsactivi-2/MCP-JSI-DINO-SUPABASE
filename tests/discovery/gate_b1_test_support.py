#!/usr/bin/env python3

import importlib.util
import os
import subprocess
import sys
import time
from contextlib import contextmanager
from pathlib import Path
from types import ModuleType
from typing import Iterator


REPO_ROOT = Path(__file__).resolve().parents[2]
STREAM_GUARD_PATH = REPO_ROOT / "scripts/discovery/gate_b1_stream_guard.py"


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def load_stream_guard() -> ModuleType:
    spec = importlib.util.spec_from_file_location("gate_b1_stream_guard", STREAM_GUARD_PATH)
    if spec is None or spec.loader is None:
        fail("stream guard could not be imported")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def guard_arguments(test_root: Path, fake_psql: Path) -> list[str]:
    return [
        str(STREAM_GUARD_PATH),
        "--psql",
        str(fake_psql),
        "--sql",
        str(test_root / "gate.sql"),
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


def guard_environment(test_root: Path) -> dict[str, str]:
    return {
        "GATE_B1_EXPECTED_DATABASE_NAME": "TEST_DATABASE",
        "PGSERVICE": "dino_crm_discovery_target_01",
        "PGSERVICEFILE": str(test_root / "service.conf"),
        "PGPASSFILE": str(test_root / "pgpass"),
    }


@contextmanager
def guard_runtime(test_root: Path, fake_psql: Path) -> Iterator[None]:
    old_argv = sys.argv
    old_environment = os.environ.copy()
    try:
        sys.argv = guard_arguments(test_root, fake_psql)
        os.environ.update(guard_environment(test_root))
        yield
    finally:
        sys.argv = old_argv
        os.environ.clear()
        os.environ.update(old_environment)


def process_exists(pid: int) -> bool:
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    return True


def wait_for_process_exit(process: subprocess.Popen[bytes]) -> bool:
    for _ in range(200):
        if process.poll() is not None:
            return True
        time.sleep(0.01)
    return process.poll() is not None


def wait_for_pid_exit(pid: int) -> bool:
    for _ in range(200):
        if not process_exists(pid):
            return True
        time.sleep(0.01)
    return not process_exists(pid)
