#!/usr/bin/env python3

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "scripts/wizards/crm-wiring-01-locate-and-scan.sh"
HITS = REPO_ROOT / "docs/discovery/crm-php-hits"
AGENTS = REPO_ROOT / "AGENTS.md"
CAPTURE = REPO_ROOT / "docs/runbooks/crm-source-wiring-capture.md"


def fail(message: str) -> None:
    raise SystemExit("FAIL: " + message)


script = SCRIPT.read_text(encoding="utf-8")
for line in script.splitlines():
    stripped = line.strip()
    if stripped.startswith("rg ") or stripped.startswith("grep "):
        if "head" in stripped:
            fail("wizard 01 scan must not pipe through head: " + stripped)

if 'HIT_TABLES" == "200"' not in script or 'HIT_UI" == "200"' not in script:
    fail("wizard 01 must reject a 200-line tables/ui list")

expected = {
    "hits-rpc.txt": 21,
    "hits-tables.txt": 1732,
    "hits-ui.txt": 2487,
}
for name, count in expected.items():
    path = HITS / name
    n = path.read_bytes().count(b"\n")
    if n == 200:
        fail(name + " is the old 200-line cap, not the complete list")
    if n != count:
        fail(f"{name} has {n} lines, expected {count} complete fundstellen")

agents = AGENTS.read_text(encoding="utf-8")
for marker in (
    "Finish every sentence",
    "wc -l",
    "1732",
    "2487",
    "failed truncated run",
):
    if marker not in agents:
        fail("AGENTS.md missing evidence rule: " + marker)

capture = CAPTURE.read_text(encoding="utf-8")
for marker in (
    'hits-tables.txt',
    "wc -l",
    "1732",
    "2487",
):
    if marker not in capture:
        fail("capture runbook missing complete-scan rule: " + marker)
if "head -200" in capture:
    fail("capture runbook must not use head -200 on hit lists")

print("PASS: Wizard 01 hit lists stay complete; 200-line cap stays rejected")
