<!-- markdownlint-disable MD013 -->
# Handoff: Session 2026-09-13 — nach Bericht-Audit

Stand: 2026-09-13

Kompakte Recovery-Kopie (nicht ins Repo nötig):
`/private/tmp/dino-crm-session-handoff-2026-09-13.md`

Paste-Prompt: [2026-09-13-aktueller-session-prompt.md](2026-09-13-aktueller-session-prompt.md).
Landkarte: [crm-work-inventory.md](../discovery/crm-work-inventory.md).
Testdatei: [crm-json-filter-draft.md](../discovery/crm-json-filter-draft.md).

## Auftrag der nächsten Session

Nicht Tool-Namen. Nicht Eval. Nicht MCP. Erst Nutzer liest das Verdict
des Bericht-Audits. Keine OPEN-Lücke schließen. Kein Commit, außer der
Nutzer sagt es.

## Was schon steht (nicht von vorn scannen)

- CRM-Code nur `/Users/activi/Downloads/crm-master-3`.
- Dump nur `databaseDump/dump_20260226_081150.sql`. Nicht `2024_10_28.sql`.
- Nicht `/Users/activi/Projects/jobstep-crm`.
- Q4 intern: ganzer Pool + Kontakte. Kunde nie ganzer Pool. Zwei Freigaben.
- Hauptsuche: `kandidati.php?page=list_ajax` → `lista_kandidata`.
- JSON-Entwurf bleibt ENTWURF. Archiv-Satz getrennt: Klassen an Liste-SQL
  und Zähl-SQL; `search[value]` nur Liste-SQL. R1 übernimmt den PHP-Zählfehler
  nicht (Q21). INNER JOIN bleibt OFFEN.
- Commit `e288d3d` ist auf origin. Danach lokale Doku uncommittet.

## Was der Bericht-Audit ergeben hat

Vorbericht-PASS nicht haltbar (A3/A4). Chat „Tree nicht angefasst“ und
alte check-local-Zahlen 723/726 falsch. `lista_kandidata_dn` nicht R1.
Worklog: [2026-09-13-json-filter-audit.md](../worklogs/2026-09-13-json-filter-audit.md).

## Dirty Tree (nicht resetten)

Doku-Updates zum Audit plus bereits vorhandene uncommittete Dateien.
Nicht stashen, nicht resetten, nicht branchen, nicht pushen, außer der
Nutzer sagt es.
