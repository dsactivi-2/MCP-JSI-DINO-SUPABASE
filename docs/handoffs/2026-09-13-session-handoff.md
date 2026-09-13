<!-- markdownlint-disable MD013 -->
# Handoff: Session 2026-09-13 — einheitlich (live)

Stand: 2026-09-13 (nach Prüfung beider Session-Handoffs)

Kompakte Recovery (nicht ins Repo nötig; /tmp kann verschwinden):
`/private/tmp/dino-crm-unified-handoff-2026-09-13.md`
Kopie gleicher Bytes:
`/private/tmp/dino-crm-session-handoff-2026-09-13.md`

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
Commit nur wenn der Nutzer es sagt.

## Quellen (lesen, nicht abschreiben)

- PHP nur `/Users/activi/Downloads/crm-master-3/src/crm`
- Dump nur `databaseDump/dump_20260226_081150.sql` — keine INSERT, keine Personenwerte
- Nicht `2024_10_28.sql`, nicht `/Users/activi/Projects/jobstep-crm`
- CRM-Code nicht ins Doku-Repo kopieren
- Eval-MCP (synthetisch, nicht Submodul): `/Users/activi/Code/eval-crm-mcp-option1`

## Schon bestätigt (ADR-0002)

Q4 intern Pool + Kontakte. Kunde nie ganzer Pool.
Hauptsuche `list_ajax` → `lista_kandidata`.
Bericht-Audit: Vorbericht-PASS zählt nicht. Archiv-Zählfehler nicht nachbauen.
Struke/Smjer = Ausbildungsberuf; JSON-Namen `struke` / `smjer`.
Jahresfilter R1: Q8.5.9 von–bis, Job + Jobgruppe.
INNER JOIN nicht kopieren; ohne Gruppe/Bearbeitung sichtbar.
JMBG intern in der Trefferliste, kein Filter.
Ranking: größte `kandidat_id` zuerst.
Erst Filter zeigen, dann eine Suche.
Ein Such-MCP, Tokens je Rolle. Profil-MCP getrennt (ADR-0003).
Export: Blättern und CSV/Excel, max. 500, inkl. JMBG/Kontakt, nicht Kunde.
Gate B1/B2/B3 V3 PASS als `dino_crm_discovery_ro_v1`. Gate P NO-GO.
Kein Redis/Iris in R1. Worker-RAM für Jobnamen erst nach RPC.

## Linear (live)

ACT-103 Done (1A 2A 3A). ACT-101–109 Done. ACT-100 In Progress.
Linear-Text von ACT-100 ist alt (Jahre nicht in R1, INNER JOIN offen).
Kein Linear-Write auf ACT-100 ohne neuen Auftrag.

## Offen

JSON bleibt Entwurf; Vertrag = AUTO-02.
JSON-Feld für den genannten Job bei Jahresfilter (`struke` ist Schule).
Von/bis-Spalten und physische Jobgruppe: Discovery.
Hosting/SDK-Version. Tenant. SLOs. Ganzer Bestand ohne Filter: nein.
Drei Doku-Sätze noch alt: `docs/project.md`, Brief, Inventar §4.5
sagen noch "Jahre nicht R1".
Phase 0 / AUTO-01 Discovery-Bericht unvollständig.

## Git und Checks

Branch `codex/supabase-crm-auth-discovery`.
HEAD `777fbd4`, origin gleich. Working Tree dirty (33 Dateien).
Nicht stashen, nicht resetten. Commit/Push nur auf Auftrag.
`scripts/check-local.sh` 2026-09-13: Exit 0, 753 Links.
Kein Beweis für Produktion-SQL, RLS oder Restore.
