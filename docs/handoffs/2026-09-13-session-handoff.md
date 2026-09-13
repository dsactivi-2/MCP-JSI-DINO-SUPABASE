<!-- markdownlint-disable MD013 -->
# Handoff: Session 2026-09-13 — live nach Doku-Hygiene

Stand: 2026-09-13, nach Korrektur der alten „Jahre nicht R1“-Sätze.

Kompakte Recovery (nicht ins Repo nötig; /tmp kann verschwinden):
`/private/tmp/dino-crm-unified-handoff-2026-09-13.md`
Kopie: `/private/tmp/dino-crm-session-handoff-2026-09-13.md`

Paste-Prompt: [2026-09-13-aktueller-session-prompt.md](2026-09-13-aktueller-session-prompt.md).
Landkarte: [crm-work-inventory.md](../discovery/crm-work-inventory.md).
Interview: [ADR-0002](../decisions/0002-search-design-interview.md).
Testdatei: [crm-json-filter-draft.md](../discovery/crm-json-filter-draft.md).
Projekt: [docs/project.md](../project.md).
Tracker: [issue-tracker.md](../agents/issue-tracker.md).

## Auftrag der nächsten Session

JSON-Filter bleibt ENTWURF. Kein MCP-Scaffold, bis der Nutzer das
ausdrücklich startet. Hosting/SDK-Version offen. Cloudflare möglich,
nicht gewählt. Antworten in ADR-0002 nicht neu aufrollen.
Commit der aktuellen Doku-Hygiene nur wenn der Nutzer es sagt.

## Quellen (lesen, nicht abschreiben)

- PHP nur `/Users/activi/Downloads/crm-master-3/src/crm`
- Dump nur `databaseDump/dump_20260226_081150.sql` — keine INSERT, keine Personenwerte
- Nicht `2024_10_28.sql`, nicht `/Users/activi/Projects/jobstep-crm`
- Eval-MCP (synthetisch, nicht Submodul): `/Users/activi/Code/eval-crm-mcp-option1`

## Schon bestätigt (ADR-0002)

Q4 intern Pool + Kontakte. Kunde nie ganzer Pool.
Hauptsuche `list_ajax` → `lista_kandidata`.
Bericht-Audit: Vorbericht-PASS zählt nicht. Archiv-Zählfehler nicht nachbauen.
Struke/Smjer = Ausbildungsberuf; JSON-Namen `struke` / `smjer`.
Jahresfilter R1: Q8.5.9 von–bis, Job + Jobgruppe. Overlap nicht addieren.
Aktueller Job bis heute. Ohne genannten Job ist das Jahresfeld ungültig.
INNER JOIN: PHP-Ist in `lista_kandidata` (Gruppe + Status obrade).
R1 nicht kopieren; ohne Gruppe/Bearbeitung sichtbar.
JMBG intern in der Trefferliste, kein Filter.
Ranking: größte `kandidat_id` zuerst.
Erst Filter zeigen, dann eine Suche.
Ein Such-MCP, Tokens je Rolle. Profil-MCP getrennt (ADR-0003).
Export: Blättern und CSV/Excel, max. 500, inkl. JMBG/Kontakt, nicht Kunde.
Gate B1/B2/B3 V3 PASS als `dino_crm_discovery_ro_v1`. Gate P NO-GO.
Kein Redis/Iris in R1. Worker-RAM für Jobnamen erst nach RPC.

## Linear (live)

ACT-103 Done (1A 2A 3A). ACT-101–109 Done. ACT-100 In Progress, weil JSON
kein Vertrag ist (AUTO-02). Linear-Beschreibung ACT-100 ist 2026-09-13
nachgezogen (Kommentar `18d4c8a3-a194-4d8a-a86c-f6d113ec9c42`).
Worklog: [2026-09-13-act-100-linear-sync.md](../worklogs/2026-09-13-act-100-linear-sync.md).

## Doku-Hygiene 2026-09-13

Live-Sätze „godine nisu R1 filter“ / „Q8.5 bleibt offen“ / Q16 „Overlap OPEN“
sind an ADR-0002 Q8.5.9 angeglichen. Historische Audit-Prompts bleiben
Audit-Stand; sie sind kein Live-Vertrag.

## Offen (nicht erfinden)

JSON bleibt Entwurf; Vertrag = AUTO-02.
JSON-Feld für den genannten Job (`struke` ist Schule, nicht Lebenslauf-Zeile).
Von/bis-Spaltennamen und physische Jobgruppe: Discovery.
Hosting/SDK-Version, Tenant, SLOs, Auth-Token.
Export-Schutz, wenn die Datei den Chat verlässt.
Phase 0 / AUTO-01 (Restore, wirksames RLS).
Ganzer Bestand ohne Filter: nein.

## Git

Branch `codex/supabase-crm-auth-discovery`.
Letzter Push: `ca1caae`. Danach lokale Hygiene plus ACT-100-Worklog,
nicht committet bis der Nutzer es sagt.
Nicht stashen, nicht resetten.
