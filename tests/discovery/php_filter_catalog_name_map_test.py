#!/usr/bin/env python3

from pathlib import Path
import subprocess
import sys
import tempfile


REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "scripts/discovery/build-php-filter-catalog-name-map.py"
FIXTURE = REPO_ROOT / "tests/discovery/fixtures/gate-b2-names-only.out"


def fail(message: str) -> None:
    raise SystemExit("FAIL: " + message)


with tempfile.TemporaryDirectory() as tmp:
    out = Path(tmp) / "map.md"
    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--b2-out",
            str(FIXTURE),
            "--output",
            str(out),
        ],
        cwd=REPO_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        fail("builder failed: " + result.stdout + result.stderr)
    text = out.read_text(encoding="utf-8")

if "NAMEN ONLY" not in text:
    fail("missing NAMEN ONLY")
if "struke" not in text:
    fail("missing struke")
if "idk_struke: ja (crm)" not in text:
    fail("fixture did not confirm idk_struke")
for forbidden in ("@gmail", "Bearer ", "postgres://", "kandidat_email"):
    if forbidden in text:
        fail("forbidden token in name map: " + forbidden)

print("PASS: PHP filter catalog name map stays names-only")
