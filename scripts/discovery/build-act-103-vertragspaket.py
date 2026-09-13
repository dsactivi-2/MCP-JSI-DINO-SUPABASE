#!/usr/bin/env python3
"""Build the ACT-103 evidence pack. Does not close ACT-103 or promote JSON."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
INVENTORY = ROOT / "docs/discovery/crm-work-inventory.md"
DRAFT = ROOT / "docs/discovery/crm-json-filter-draft.md"
ADR = ROOT / "docs/decisions/0002-search-design-interview.md"
OUT = ROOT / "docs/discovery/act-103-vertragspaket.md"


def fail(message: str) -> None:
    raise SystemExit("FAIL: " + message)


def require(text: str, name: str, markers: tuple[str, ...]) -> None:
    for marker in markers:
        if marker not in text:
            fail(name + " missing required marker: " + marker)


def section_between(text: str, start: str, end: str, name: str) -> str:
    if start not in text:
        fail(name + ": start not found: " + start)
    body = text.split(start, 1)[1]
    if end not in body:
        fail(name + ": end not found: " + end)
    return body.split(end, 1)[0]


def parse_pipe_rows(block: str) -> list[list[str]]:
    rows: list[list[str]] = []
    for line in block.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if not cells or set(cells[0]) <= {"-", ":"}:
            continue
        if cells[0] in {"ID", "Thema", "Luecke", "JSON", "PHP", "Feld", "Regel"}:
            continue
        rows.append(cells)
    return rows


def md_table(headers: list[str], rows: list[list[str]]) -> str:
    out = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        padded = row + [""] * (len(headers) - len(row))
        out.append("| " + " | ".join(padded[: len(headers)]) + " |")
    return "\n".join(out)


def main() -> None:
    inventory = INVENTORY.read_text(encoding="utf-8")
    draft = DRAFT.read_text(encoding="utf-8")
    adr = ADR.read_text(encoding="utf-8")
    require(
        inventory,
        "inventory",
        (
            "JSON-Filter ist Entwurf, kein Vertrag.",
            "INNER JOIN: nicht übernehmen, ohne Gruppe/Bearbeitung sichtbar.",
            "Punkt 2 **Ja:** Archiv-Satz bleibt (Zählfehler nicht kopieren).",
            "Punkt 3 **Ja:** JSON bleibt Entwurf, kein Vertrag.",
        ),
    )
    require(
        draft,
        "json-draft",
        (
            "Status: **ENTWURF**",
            "kein abgenommener Vertrag",
            "ohne Gruppe/Bearbeitung bleiben sie sichtbar",
            "R1 übernimmt den PHP-Zählfehler nicht",
        ),
    )
    require(
        adr,
        "adr-0002",
        (
            "INNER JOIN Gruppe/Status in R1:",
            "Punkt 3 **Ja:** JSON bleibt Entwurf, kein Vertrag.",
            "Punkt 2 (Archiv-Satz) **Ja:**",
            "JMBG in der internen Trefferliste:",
            "Ranking R1:",
            "**Q15.6",
        ),
    )
    q_block = section_between(
        inventory,
        "## 3. Entscheidungen, die nicht neu aufgerollt werden",
        "## 4. Gemappte Daten",
        "inventory Q table",
    )
    q_rows = [row[:3] for row in parse_pipe_rows(q_block) if row]
    if len(q_rows) < 8:
        fail("inventory Q table too small: %s" % len(q_rows))
    open_block = section_between(
        draft,
        "## Offen, ehrlich",
        "## Nächster Schritt",
        "json-draft open table",
    )
    open_rows = [row[:2] for row in parse_pipe_rows(open_block) if row]
    if len(open_rows) < 6:
        fail("json-draft open table too small: %s" % len(open_rows))
    conflicts = []
    if any("Ranking" in row[0] and "OFFEN" in row[1] for row in open_rows):
        conflicts.append(
            "JSON-Entwurf: Ranking/Cursor OFFEN. ADR-0002 Q18: Ranking R1 bestätigt, kandidat_id absteigend."
        )
    if any("JMBG" in row[0] and "unbestätigt" in row[1] for row in open_rows):
        conflicts.append(
            "JSON-Entwurf: JMBG-Ausgabe unbestätigt. ADR-0002 Q18: JMBG intern bestätigt ja, kein Filter."
        )
    conflict_md = "Keine. Quellen sind auf den geprueften Markern gleich."
    if conflicts:
        conflict_md = "\n".join("- " + item for item in conflicts)
    q_table = md_table(["ID", "Stand", "Kern"], q_rows)
    open_table = md_table(["Thema", "Stand im JSON-Entwurf"], open_rows)
    parts = [
        "<!-- markdownlint-disable MD013 -->",
        "# ACT-103 Vertragspaket",
        "",
        "Stand der Quellen: 2026-09-13",
        "",
        "Status: **PACK / KEIN VERTRAG**. Dieses Dokument schließt",
        "[ACT-103](https://linear.app/activi/issue/ACT-103/pflichtartefakt-des-scans-festlegen)",
        "nicht. Es macht den JSON-Filter nicht zum Vertrag. Es startet keinen MCP.",
        "Erzeugt von scripts/discovery/build-act-103-vertragspaket.py.",
        "Bei Konflikt gilt die neueste ausdrückliche Antwort in",
        "[ADR-0002](../decisions/0002-search-design-interview.md).",
        "",
        "## Wozu das Paket da ist",
        "",
        "ACT-103 fragt, welches Scan-Stück die Wayfinder-Karte beenden darf:",
        "redigiertes Data Dictionary, Mapping auf den Suchvertrag, JSON-Filter- und",
        "RPC-Allowlist-Vorschlag, oder eine andere Kombination. Ein Runtime-MCP, ein",
        "ER-Diagramm oder ein 1:1-Dump der Datenbank zählen nicht.",
        "",
        "Die drei ACT-103-Fragen sind 2026-09-13 gekreuzt. JSON bleibt Entwurf.",
        "",
        "Lokal 2026-09-13 gekreuzt: **1A 2A 3A**. Linear-Kommentar gesetzt;",
        "Issue-Status Done. JSON bleibt Entwurf.",
        "",
        "## Quellen",
        "",
        "| Datei | Rolle |",
        "| --- | --- |",
        "| [crm-work-inventory.md](crm-work-inventory.md) | PHP-Scan-Landkarte |",
        "| [crm-json-filter-draft.md](crm-json-filter-draft.md) | R1 JSON-Entwurf |",
        "| [ADR-0002](../decisions/0002-search-design-interview.md) | neueste ausdrückliche Antworten |",
        "| [issue-tracker.md](../agents/issue-tracker.md) | Linear ACT-103 Status Done |",
        "",
        "## Schon bestätigt — nicht neu aufrollen",
        "",
        q_table,
        "",
        "Zusätzlich aus ADR-0002 Q18 / Bericht-Audit 2026-09-13:",
        "",
        "- INNER JOIN Gruppe/Status in R1: **nicht** kopieren. Ohne Gruppe/Bearbeitung sichtbar.",
        "- Archiv-Satz: PHP-Zählfehler kennen, in R1 nicht kopieren. Punkt 2 **Ja**.",
        "- JSON bleibt Entwurf, kein Vertrag. Punkt 3 **Ja**.",
        "- Vorbericht-PASS zählt nicht. Punkt 1 **Ja**.",
        "- Struke/Smjer = Ausbildungsberuf; JSON-Namen bleiben struke / smjer.",
        "- Jahresfilter R1 Q8.5.9: von–bis, Job + Jobgruppe. Alte UI bleibt ja/nein.",
        "- Ranking R1: größte kandidat_id zuerst.",
        "- JMBG intern in der Trefferliste ja, kein Filter, Discovery ohne Werte.",
        "",
        "## Bleibt Entwurf oder OFFEN — nicht hier schließen",
        "",
        open_table,
        "",
        "- JSON-Filter R1: **ENTWURF**, geprüft, kein Vertrag.",
        "- Q15.6 Export: siehe ADR-0002. Nicht eine der drei ACT-103-Fragen unten.",
        "- Auth, Hosting, SDK, Tenant: nicht gewählt. Nicht ACT-103.",
        "- RPC-Allowlist / redigiertes Data Dictionary: in den Scan-Dateien nicht als abgenommenes Pflichtartefakt geführt.",
        "",
        "## Quellenkonflikt",
        "",
        conflict_md,
        "",
        "Neueste ausdrückliche Antwort in ADR-0002 gewinnt. Der JSON-Entwurf wird",
        "dadurch nicht still zum Vertrag.",
        "",
        "## Drei Fragen — nur du kreuzt",
        "",
        "Gekreuzt 2026-09-13 im Chat. Das Script schreibt nur diese bestätigten",
        "Buchstaben; es erfindet keine Kreuze.",
        "",
        "| # | Frage | Option A | Option B | Option C | Dein Kreuz |",
        "| --- | --- | --- | --- | --- | --- |",
        "| 1 | Welches Pflichtartefakt beendet ACT-103? | Inventar + Codebefunde + JSON-Entwurf reichen | Zusätzlich redigiertes Data Dictionary oder Mapping auf den kanonischen Vertrag | Zusätzlich RPC-Allowlist, bevor die Karte endet | 1A |",
        "| 2 | INNER JOIN und Archiv-Satz | Für ACT-103 geschlossen (Antworten 2026-09-13 in ADR-0002 / Inventar / Entwurf) | Bleiben offen, bis sie im JSON-Vertrag stehen | Linear-Text anpassen, Inhalt bleibt bestätigt | 2A |",
        "| 3 | Darf ACT-103 Done werden, solange JSON ENTWURF ist? | Ja; Pflichtartefakt ist der geprüfte Entwurf, Vertrag kommt später (AUTO-02) | Nein; erst JSON zum Vertrag, dann ACT-103 Done | Ja, aber nur zusammen mit Option 1A und 2A | 3A |",
        "",
        "Antwort 2026-09-13 (Nutzer, dieser Chat): **1A 2A 3A**.",
        "Linear-Kommentar gesetzt; Issue-Status Done.",
        "",
        "Nicht ankreuzen und nicht in dieser Runde entscheiden: MCP-Bau, Tool-Namen,",
        "Eval-MCP, Produktions-Apply, Q15.6, Auth.",
        "",
        "## Was dieses Paket nicht tut",
        "",
        "- JSON nicht zum Vertrag erklären",
        "- Pack erzeugt keine Linear-Writes; der Kommentar kam separat",
        "- keinen MCP scaffolden",
        "- keine Schema-Tatsachen erfinden",
        "",
    ]
    OUT.write_text("\n".join(parts), encoding="utf-8")
    print("PASS: wrote " + str(OUT.relative_to(ROOT)))


if __name__ == "__main__":
    main()
