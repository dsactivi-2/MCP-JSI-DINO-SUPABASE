<!-- markdownlint-disable MD013 -->
# Worklog: Doku-Pointer-Plan (Freigabe 2026-09-13)

Datum: 2026-09-13

Status: **ausgeführt**. `scripts/check-local.sh` PASS. Kein Commit ohne
Extra-Auftrag. Kein Ordner-Move, keine Frozen-Dateien, kein MCP, kein
Linear-Write.

Chef-Skill: `update-md-files` (Project). Dazu: `writing-for-agents`,
`agents-md-builder`, `agents-md-toolkit`, `context-engineering`.
Welle 2 zusätzlich `domain-modeling` nur für ADR-0002-Offenblock.
Nach den Edits: `markdown-documentation` plus `scripts/check-local.sh`.

Nicht: `create-project-md-files`, `grill-with-docs`, `wayfinder`,
`file-organizer`, `start-matt-wizard`.

Live-Stand für Korrekturen (nicht raten):

- Q8.5 in [ADR-0002](../decisions/0002-search-design-interview.md):
  `TEILWEISE BESTÄTIGT`; 8.5.1 und 8.5.3–8 stehen; 8.5.2 ignoriert;
  Jahre sind kein R1-Filter.
- Gate B in ADR-0002 Q10.2p-q: Rolle `dino_crm_discovery_ro_v1` existiert;
  B1 V3 PASS; B2 V3 PASS; B3 V3 PASS; Rohdaten außerhalb Git;
  keine Kandidatenzeilen. Der Satz zu fehlenden B2/B3-Launchern
  in `docs/project.md` ist alt.
- Nächster Fachschritt bleibt beim Nutzer; in Linear ist ACT-103 offen.

## Welle 1

1. [AGENTS.md](../../AGENTS.md): auf etwa 90-120 Zeilen. Phase kurz plus
   Zeiger. Working sequence nach Aufgabe, Brief nicht immer zuerst.
   Interview-Q-Kopie raus, Verfahren bleibt.
2. [README.md](../../README.md): Rollenkarte statt ~40 Dateizeilen.
   Start: zuerst `docs/project.md`.
3. [docs/project.md](../project.md): Katalog kürzen; Q8.5-Satz an ADR-0002;
   einen Gate-B-Satz nach Q10.2p-q; alten Launcher-Satz entfernen.
4. [docs/handoffs/2026-09-13-aktueller-session-prompt.md](../handoffs/2026-09-13-aktueller-session-prompt.md):
   Banner historisch; Struke/Smjer, 5 Jahre, INNER JOIN an Inventar.

## Welle 2

1. [docs/project.md](../project.md): Q10.2-Chronik in Trenutno stanje
   durch kurzen Live-Block plus Zeiger ersetzen.
2. [docs/SUPABASE_CRM_MCP_IMPLEMENTATION_BRIEF.md](../SUPABASE_CRM_MCP_IMPLEMENTATION_BRIEF.md):
   drei Q8.5-Stellen (ca. Zeilen 71, 344, 1119).
3. [docs/decisions/0002-search-design-interview.md](../decisions/0002-search-design-interview.md):
   nur Block Offene Fragen / Q8 nachziehen.
4. [docs/handoffs/2026-09-13-scan-to-mcp.md](../handoffs/2026-09-13-scan-to-mcp.md):
   Q8.5-Sätze „vollständig OFFEN“ korrigieren.

## Nicht anfassen

Frozen-Liste in `scripts/check-local.sh`. Research, Reviews, PHP-Hits,
Runbooks, Linear, Serena-Memories, `CONTEXT.md` (Glossar passt),
[role-version-register.md](../discovery/role-version-register.md) (Stand
2026-09-11, bekannt veraltet, nicht in dieser Freigabe).

## Prüfung

`rtk proxy /bin/bash scripts/check-local.sh`, dann `rtk git status --short`.
