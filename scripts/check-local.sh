#!/bin/bash
set -euo pipefail
export PYTHONDONTWRITEBYTECODE=1

cd "$(dirname "${BASH_SOURCE[0]}")/.."

for test_file in tests/docs/*_test.py tests/discovery/*_test.py; do
  rtk proxy python3 "$test_file"
done
rtk proxy /bin/bash tests/discovery/gate_b1_launcher_test.sh
for shell_file in scripts/check-local.sh scripts/discovery/run-gate-b1.sh tests/discovery/gate_b1_launcher_test.sh \
  scripts/wizards/crm-wiring-01-locate-and-scan.sh \
  scripts/wizards/crm-wiring-02-map-search.sh \
  scripts/wizards/crm-wiring-03-accept.sh \
  scripts/wizards/crm-wiring-04-status-and-triggers.sh; do
  rtk proxy /bin/bash -n "$shell_file"
done

# Frozen evidence skips lint; append-only lock is tests/docs/historical_append_only_test.py.
rtk proxy python3 - <<'PY'
from pathlib import Path
import subprocess
import sys

frozen = {
    'docs/discovery/crm-schema-static-analysis.md',
    'docs/discovery/crm-auth-schema-static-analysis.md',
    'docs/discovery/security-read-only-discovery-preflight.md',
    'docs/discovery/gate-b-change-matrix.md',
    'docs/discovery/gate-b1-approval-text.md',
    'docs/research/berufssuchprofile-q8-4-2.md',
    'docs/research/2026-09-11-plan-best-practice-verification.md',
    'docs/reviews/2026-09-11-project-plan-audit.md',
    'docs/reviews/decision-reconstruction-audit-prompt.md',
    'docs/reviews/decision-reconstruction-audit.md',
    'docs/reviews/decision-reconstruction-corrections.md',
    'docs/worklogs/2026-09-11-automation-plan-adoption.md',
    'docs/worklogs/2026-09-11-security-read-only-discovery-gate.md',

}
paths = sorted(Path('.').glob('*.md')) + sorted(Path('docs').rglob('*.md'))
active = [str(p) for p in paths if str(p) not in frozen]
result = subprocess.run(['markdownlint-cli2', *active], check=False)
sys.exit(result.returncode)
PY
rtk proxy git diff --check
rtk git status --short
printf '%s\n' 'PASS: local documentation and synthetic process checks; no database proof'
