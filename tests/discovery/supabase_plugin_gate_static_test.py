#!/usr/bin/env python3

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
GATE_PATH = REPO_ROOT / "docs/discovery/supabase-plugin-read-only-gate-draft.md"
README_PATH = REPO_ROOT / "README.md"
PROJECT_PATH = REPO_ROOT / "docs/project.md"
TOOLING_PATH = REPO_ROOT / "docs/agents/supabase-tooling.md"
DECISION_MAP_PATH = REPO_ROOT / "docs/discovery/project-decision-map.md"


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


gate_text = GATE_PATH.read_text(encoding="utf-8")

required_gate_markers = (
    "Status: **DRAFT / NO-GO**",
    "USER-ATTESTED PASS",
    "Gesamtbewertung: **NO-GO**",
    "NICHT ERTEILT",
    "project_ref=${SUPABASE_PROJECT_REF}",
    "read_only=true",
    "features=database,docs",
    "Read-only ist eine Schreibschutzschicht, keine PII- oder Mandantengrenze.",
    "Ziel ist Produktion mit echten Kandidatendaten",
    "FAIL / BLOCKED – Ziel ist Produktion mit echten Kandidatendaten.",
    "darf der Plugin nicht direkt mit dem bestätigten Produktionsprojekt",
    "Getrenntes Development-/Testprojekt ohne echte Personen.",
    "`search_docs`",
    "`list_extensions`",
    "`list_tables`",
    "`verbose=false`",
    "`execute_sql`, auch für `SELECT`",
    "`list_projects` erraten",
)
for marker in required_gate_markers:
    if marker not in gate_text:
        fail(f"required gate marker missing: {marker}")

for forbidden_literal in (
    'project_id: "',
    "Status: **PASS**",
    "Gesamtbewertung: **GO**",
    "Live-Zugriff ist freigegeben",
    "Ist das Ziel ein Development-/Testprojekt",
):
    if forbidden_literal in gate_text:
        fail(f"unsafe or contradictory gate text found: {forbidden_literal}")

references = {
    README_PATH: "docs/discovery/supabase-plugin-read-only-gate-draft.md",
    PROJECT_PATH: "discovery/supabase-plugin-read-only-gate-draft.md",
    TOOLING_PATH: "../discovery/supabase-plugin-read-only-gate-draft.md",
    DECISION_MAP_PATH: "supabase-plugin-read-only-gate-draft.md",
}
for path, expected_reference in references.items():
    if expected_reference not in path.read_text(encoding="utf-8"):
        fail(f"gate reference missing from {path.relative_to(REPO_ROOT)}")

print("PASS: Supabase Plugin Gate P remains a non-executable NO-GO draft")
