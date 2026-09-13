#!/usr/bin/env python3

from pathlib import Path
import subprocess
import sys


REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "scripts/discovery/build-act-103-vertragspaket.py"
OUT = REPO_ROOT / "docs/discovery/act-103-vertragspaket.md"


def fail(message: str) -> None:
    raise SystemExit("FAIL: " + message)


first = subprocess.run(
    [sys.executable, str(SCRIPT)],
    cwd=REPO_ROOT,
    check=False,
    capture_output=True,
    text=True,
)
if first.returncode != 0:
    fail("builder failed: " + first.stdout + first.stderr)

text = OUT.read_text(encoding="utf-8")
second = subprocess.run(
    [sys.executable, str(SCRIPT)],
    cwd=REPO_ROOT,
    check=False,
    capture_output=True,
    text=True,
)
if second.returncode != 0:
    fail("second builder run failed")
if OUT.read_text(encoding="utf-8") != text:
    fail("builder is not idempotent")

required = (
    "Status: **PACK / KEIN VERTRAG**",
    "Dieses Dokument schließt",
    "nicht. Es macht den JSON-Filter nicht zum Vertrag.",
    "Welches Pflichtartefakt beendet ACT-103?",
    "INNER JOIN und Archiv-Satz",
    "Darf ACT-103 Done werden, solange JSON ENTWURF ist?",
    "JSON-Filter R1: **ENTWURF**",
    "Quellenkonflikt",
)
for marker in required:
    if marker not in text:
        fail("pack missing marker: " + marker)

for forbidden in (
    "ACT-103 ist Done",
    "JSON ist Vertrag",
    "MCP-Bau ist freigegeben",
    "Linear-Write ausgeführt",
):
    if forbidden in text:
        fail("pack contains forbidden claim: " + forbidden)

print("PASS: ACT-103 pack is generated, idempotent, and not a contract")
