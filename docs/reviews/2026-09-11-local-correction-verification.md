# Prüfbericht: lokale Korrektur und Konsolidierung

Datum: 2026-09-11. Status: **PASS_WITH_GAPS für die lokale Korrekturrunde**.
Der gemeinsame Gesamtgate bleibt wegen eines fremden Whitespace-Befunds rot.

## Vergleichsbasis und Umfang

Verglichen wird ausschließlich gegen den zu Sitzungsbeginn erfassten lokalen
Snapshot `/private/tmp/crm-correction-20260911-baseline`, einschließlich
unversionierter Dateien. Kein Commitvergleich und kein Hilfscommit.
Die noch unveränderte Serena-Memory wurde vor ihrem ersten Edit nacherfasst.
Vorhandene Nutzeränderungen sind nicht als Änderungen dieser Runde ausgewiesen.

<!-- markdownlint-disable-next-line MD013 -->
Die [Abschlussmatrix](../planning/audit-correction-matrix.md) beschreibt A01–A12;
das [Register](../planning/release-1-requirements.md) und der
<!-- markdownlint-disable-next-line MD013 -->
[Arbeitsplan](../planning/release-1-automation-tickets.md) bilden die konsolidierte
<!-- markdownlint-disable-next-line MD013 -->
lokale Spezifikation. Der [Zugangsplan](../discovery/access-plan-consolidated.md)
bereitet die nächste konkrete Entscheidung vor.

## Verhalten und SQL-Nachweis

Der neue Dateibaum-Repro zeigte zuerst einen falschen Exitcode 0 für fehlende
Links in unstaged/neuen Dokumenten. Nach dem minimalen Fix meldet der Default
den Working Tree; der Index ist separat wählbar. Weitere Red/Green-Fälle prüfen
Unicode-Fragmente und Überschriften mit Satzzeichen. Fachliche Sprach-Sollwerte
im Brief sind von der noch nicht vorhandenen Implementierung unabhängig.

Die Rollenentwürfe korrigieren `current_user` und den eigenen CONNECT-Cleanup.
Es gibt keinen ausgeführten SQL-Red/Green-Nachweis: keine bereits vorhandene,
eindeutig isolierte synthetische Datenbank ist nachgewiesen. `psql` auf PATH
ist keine solche Evidenz. Die konkreten Lifecycle-Repros stehen im
[Rollenpaket](../discovery/least-privilege-discovery-role-v1.md). Textchecks
belegen keine SQL-Ausführbarkeit. B2/B3-Launcher, Marker und Objekt-Coverage
bleiben als konkrete spätere Arbeitspakete offen.

## Verifikation

Letzter vollständiger lokaler Lauf: `20260911T111207Z`.
Zeitbezogene Logs liegen ausschließlich unter
`/private/tmp/crm-correction-20260911-checks`.

<!-- markdownlint-disable MD013 -->

| Prüfung | Tatsächliches Ergebnis | Grenze |
| --- | --- | --- |
| Python-Prüfdateien | 11 direkt ausführbare Prüfdateien erfolgreich, darunter vier neue Dateibaum-Verhaltenstests. | Keine konfigurierte pytest/Ruff/mypy- oder Anwendungspipeline; statische SQL-Prüfungen sind keine SQL-Laufzeittests. |
| Fake-psql-Launcher | Alle 14 benannten Testgruppen PASS; Stream-/Signal-/Cleanup-Negativfälle ebenfalls erfolgreich. | Nur synthetische Prozesse; kein produktiver Launcher-Aufruf. Erwartete STOP-Ausgaben sind Testfälle. |
| Bash-Syntax | Drei Shell-Dateien jeweils separat mit `bash -n` erfolgreich. | Syntaxprüfung führt keinen Launcher aus. |
| Working-Tree-Link-/Fragmentprüfung | PASS: 406 lokale Referenzen im abschließenden vollständigen Lauf. | Begrenzter Parser für Inline-Links und ATX-Überschriften; kein vollständiger CommonMark-Renderer oder Webtest. |
| Explizite Index-Linkprüfung | PASS: 281 Referenzen. | Absichtlich staged Snapshot, kein Ersatz des Working Trees. |
| Aktives Markdownlint | PASS: 33 Dateien, null Befunde. | Nur explizit benannte historische Belege ausgenommen; neue aktive Reviews/Worklogs bleiben im Gate. MD013-Ausnahmen nur lokal für lange Tabellen/Einzelzeilen, keine globale Abschaltung. |
| Vollständiges Markdownlint | FAIL: 301 Befunde in 8 historischen Dateien. | Historische Beweise werden nicht rückwirkend formatiert. Früherer Audit hatte 611 Befunde insgesamt; das ist kein heutiger Erfolg des vollständigen Lints. |
| Hashbindungen | B1 V1/V2, Launcher, Stream-Guard, B2, B3 und Rollenentwürfe geprüft; korrigierte B2/B3-Entwurfshashes synchronisiert. | Keine Hashänderung erzeugt eine Freigabe. |
| Anforderungs-/Paketprüfung | 48 eindeutige Anforderungen, 39 eindeutige Pakete; zugeordnete Pakete vorhanden, keine zyklischen Blocking-Kanten. | Inhaltliche Abnahme ist noch nicht implementiert. |
| Eigener Diff: Whitespace | `git diff --check -- <eigene Pfade>` PASS; neue Dateien zusätzlich gegen Snapshot geprüft, keine Whitespace-Diagnosen. | Fremde Änderungen sind nicht Teil der Reviewbasis. |
| Gesamtes `git diff --check` | FAIL / Exit 2: `.agents/skills/supabase-postgres-best-practices/references/_contributing.md:30`, nachlaufendes Leerzeichen. | Außerhalb unseres Diffs; unverändert gelassen. `rtk git` unterdrückte den Fehltext; der Wrapper verwendet dafür jetzt `rtk proxy git`. |
| Gemeinsamer lokaler Gate | Exit 2, blockiert korrekt am globalen Git-Whitespace-Schritt. | Vorherige Python-/Fake-/Bash-/Lintschritte grün; kein falscher Gesamt-PASS. |
| Historische Beweise | 13 erfasste Audit-/Worklog-/Exportanalyse-/Altgate-Dateien byteidentisch zum Snapshot. | Keine Rohdaten oder Backupinhalte geöffnet. |
| SQL, RLS, Load, Restore, echte Clients | NICHT AUSGEFÜHRT. | Keine nachgewiesene zulässige vorhandene synthetische DB; Anwendung fehlt; keine Produktions-/Backupfreigabe. |

<!-- markdownlint-enable MD013 -->

Reproduktion: `rtk proxy /bin/bash scripts/check-local.sh`; vollständiges Lint
und expliziter Indexmodus gemäß README. Erwarteter Gesamtstatus bleibt FAIL,
solange der fremde Whitespace-Befund besteht. Keine Toolinstallation oder
Reparatur globaler Konfiguration wurde vorgenommen.

## Skills und Anwendung

- `/ask-matt`: nach Projektregeln zur Einordnung in die vorhandene
  Korrekturrunde.
- `/implement`: nach beiden Audits als Arbeitsspezifikation; ohne Skill-Commit.
- `/domain-modeling`: vor Begriff-/ADR-Änderungen; Status und Entwürfe getrennt,
  keine neuen Fachentscheidungen und kein zusätzliches ADR-Verzeichnis.
- `supabase` und `supabase-postgres-best-practices`: vor SQL-/Zugangsarbeit;
  relevante Privilegienreferenz, vorhandene Auditprimärquellen, keine
  Verbindung.
- `/tdd`: vor Prüferskriptänderungen; genehmigte Dateibaum-/Exitcode-Grenze,
  relevante fehlgeschlagene Repros und minimale Korrektur.
- `/code-review`: nach lokalen Prüfungen, unabhängige Achsen Standards und Spec
  ausschließlich gegen den Sitzungssnapshot.

`/diagnosing-bugs`, `/research` und `/grill-with-docs` waren nicht nötig:
die Ursachen und technischen Primärquellen lagen im Audit; keine neue
Geschäftsentscheidung wurde abgeleitet. Die beiden materiellen Änderungen
stehen als [ENTWURF](../planning/decision-drafts.md), nicht als beschlossen.

## Grenzen und nächster Schritt

Keine Produktionsverbindung, SQL-Ausführung, Rollenanlage, Migration,
Deployment, Credential-/Backupöffnung, globale Änderung, Linear-Write,
Commit, Push oder Branchwechsel. Q8.5 bleibt vollständig OFFEN, Q4.5 wird
nicht rekonstruiert. Allgemeine Suchbestätigung ist vorläufig, Q7 verbindlich.

Als Nächstes den Bootstrap-Evidenzweg prüfen und entscheiden: vorhandene
geeignete Identität belegen oder begrenzten Owner-/Restore-Prüfweg autorisieren.
Danach erst Identitäts-/SQL-Lifecycle-Nachweise, das passende B1-Paket und seine
separate Ausführungsfreigabe. Die Freigabe dieser lokalen Korrektur und neue
SQL-Hashes autorisieren keinen dieser Schritte.

## Standards

Erstprüfung: drei konkrete Befunde – GOV-01 zog Geschäftsentscheidungen vor
Discovery, der Lintgate schloss ganze Review-/Worklog-Verzeichnisse aus und
beim Formatieren war ein Shellpfad umgebrochen worden. Alle drei korrigiert.
Unabhängige Nachprüfung: Scope auf Discovery begrenzt, historische Dateien
explizit benannt, Launcherpfad korrekt quotiert; Bash-Syntax erfolgreich,
Launcher nicht ausgeführt. Keine neuen relevanten Befunde in der Nachprüfung.

## Spec

Erstprüfung: zwei konkrete Befunde – dieselbe GOV/Q9-Abhängigkeit und fehlende
explizite Zuordnungen für TLS/Secrets, regelmäßige Zugriffsprüfung und menschliche
Entscheidungsprüfung. Alle korrigiert; drei REQ-Einträge samt Paketzuordnung
ergänzt. Unabhängige Nachprüfung bestätigt beide Korrekturen; keine weiteren
relevanten Lücken innerhalb dieser gezielten Prüfung.

Standards: 3 behoben, 0 offen. Spec: 2 behoben, 0 offen. Beide Achsen verwendeten
nur den redigierten Sitzungssnapshot, ohne Commit-/Branchvergleich.

## Tatsächlich geänderte Dateien

Die Liste umfasst ausschließlich unsere 31 geänderten oder neuen Dateien.
Vorhandene weitere Worktree-Änderungen und `skills-lock.json` werden nicht
unserer Arbeit zugerechnet. Die technische Memory-Korrektur verweist auf README
als maßgebliche Quelle statt nicht existente Tests zu behaupten.

- `.serena/memories/suggested_commands.md`
- `CONTEXT.md`
- `README.md`
- `docs/SUPABASE_CRM_MCP_IMPLEMENTATION_BRIEF.md`
- `docs/agents/supabase-tooling.md`
- `docs/agents/triage-labels.md`
- `docs/decisions/0002-search-design-interview.md`
- `docs/decisions/0004-automated-database-development.md`
- `docs/discovery/access-plan-consolidated.md`
- `docs/discovery/least-privilege-discovery-role-v1.md`
- `docs/discovery/project-decision-map.md`
- `docs/discovery/security-read-only-discovery-preflight-b.md`
- `docs/discovery/sql/01-create-least-privilege-discovery-role-v1.sql`
- `docs/discovery/sql/01-drop-least-privilege-discovery-role-v1.sql`
- `docs/discovery/sql/10-catalog-structure-gate-b2.sql`
- `docs/discovery/sql/20-definitions-statistics-gate-b3-draft.sql`
- `docs/discovery/supabase-plugin-read-only-gate-draft.md`
- `docs/planning/audit-correction-matrix.md`
- `docs/planning/decision-drafts.md`
- `docs/planning/release-1-automation-tickets.md`
- `docs/planning/release-1-requirements.md`
- `docs/project.md`
- `docs/research/supabase-agent-skills-einfach-erklaert.md`
- `docs/research/supabase-werkzeuge-fuer-crm-mcp.md`
- `docs/reviews/2026-09-11-local-correction-verification.md`
- `docs/runbooks/database-development-automation.md`
- `docs/runbooks/schema-discovery.md`
- `scripts/check-local.sh`
- `tests/discovery/gate_b2_scope_static_test.py`
- `tests/docs/relative_markdown_links_behavior_test.py`
- `tests/docs/relative_markdown_links_test.py`
