# Projekt-, Dokumentations- und Planaudit

Prüfdatum: 2026-09-11. Sprache: Deutsch entsprechend dem Auftrag.

**Gesamturteil: FAIL für „vollständig, aktuell und fehlerfrei“.
Die Grundarchitektur ist geeignet; ihre optimale Ausgestaltung ist ohne
Discovery und repräsentative Messungen noch nicht bewiesen.**

Der Plan benötigt gezielte Korrekturen und eine schlankere Arbeitsaufteilung,
keinen grundsätzlichen Architekturwechsel. Die folgenden Änderungen sind
Reviewvorschläge. Dieser Bericht ändert keine akzeptierte Entscheidung,
Freigabe oder vorhandene Projektdatei.

## Umfang und Beweisgrenzen

Geprüft wurde der aktuelle Arbeitsstand auf
`codex/supabase-crm-auth-discovery`, einschließlich vorhandener Änderungen und
unversionierter Entwürfe. Git HEAD beim Audit: `0d755ccecec10ead988e5553271acdbb41b450e0`.

- 39 Projekt-Markdown-Dateien im Root und unter `docs/` vor den neuen Berichten:
  Kontext, Projektstatus, Brief, vier ADRs, Agentenregeln, Planung, Runbooks,
  Discovery-Unterlagen, sieben Forschungsberichte, Reviews und Worklogs.
- Acht SQL-Dateien als statische Entwürfe und die vorhandenen lokalen
  Dokumentations-/Discovery-Prüfungen; keine vollständige Anwendung existiert.
- Ergänzend Serena-Memories, lokale Skill-Anweisungen und Routingregeln.
- Live-Abgleich des dedizierten Linear-Projekts und Teams: **0 Issues**, auch
  unter Einschluss archivierter Issues, **0 Dokumente, 0 Meilensteine,
  0 Projektkommentare und 0 Statusupdates**. Team und fünf kanonische
  Triage-Labels stimmen mit den lokalen Unterlagen überein.
- Aktuelle offizielle technische Quellen und Forschungsabgleich sind im
  [Best-Practice-Bericht](../research/2026-09-11-plan-best-practice-verification.md)
  dokumentiert.

Es wurde keine Supabase-/PostgreSQL-Verbindung aufgebaut. Keine Rohexporte,
Credentials oder Backupinhalte wurden geöffnet, keine SQL-Datei ausgeführt und
kein externer Write vorgenommen. Exporttreue, tatsächlicher Datenbestand,
RLS-Wirksamkeit, Restore und Produktionsleistung sind deshalb nicht neu bewiesen.
Der vollständige historische Originalchat liegt nicht als Primärquelle vor;
die dokumentierten Rekonstruktionslücken bleiben offen.

## Was fachlich erhalten bleiben sollte

Der kontrollierte Weg aus
[ADR-0001](../decisions/0001-controlled-query-boundary.md) und
[ADR-0004](../decisions/0004-automated-database-development.md) ist eine
plausible, schlanke Ausgangsbasis:

1. Sprachmodell strukturiert die Suchabsicht; strikt validierte Filter werden
   über einen kleinen MCP-Vertrag ausgeführt.
2. PostgreSQL entscheidet über Berechtigung, Filterung, Ranking und Pagination.
3. Höchstens 50 Kandidaten pro Suchseite; Release 1 bleibt auf allen Wegen
   kontaktfrei, ohne erfundene Werte oder automatische Filterlockerung.
4. Berufssuchprofile bleiben versioniert und nicht exklusiv. Ihre Verwaltung
   behält die getrennte Identität, Rechte und Veröffentlichung aus ADR-0003.
5. Additiver Aufbau A mit kompatiblen Bausteinen für D statt frühem Vollumbau.
6. Lokale synthetische Daten, versionierte Migrationen und reproduzierbare
   Tests/CI; Optimierung zunächst mit PostgreSQL-/Supabase-eigenen Werkzeugen.

Die Zahl von ungefähr 200.000 Kandidaten allein rechtfertigt weder einen
externen Suchdienst noch Cache, Replika oder Vektorbackend. Diese Auswahl
benötigt tatsächliche Datenverteilung, Query-Pläne und Qualitätsmessung.
Keine separate gehostete Staging-Instanz zu wollen widerspricht nicht den
bereits akzeptierten lokalen synthetischen Tests.

## Korrekturbedarf

P1 bedeutet: vor dem betroffenen Ausführungs- oder Implementierungsschritt
beheben. P2 bedeutet: vor Spezifikations-/Releasefreigabe konsolidieren.
P3 bezeichnet Wartbarkeit und Format. Historische Berichte werden nicht
rückwirkend umgeschrieben.

### A01 — Zugangsplan hat eine ungelöste Bootstrap-Abhängigkeit · P1

[Rollenpaket, offene Voraussetzungen](../discovery/least-privilege-discovery-role-v1.md#vor-einer-ausführung-zwingend-offen)
verlangt Restore-Nachweis und eine eigene Mutationsfreigabe für die neue Rolle.
[ADR-0002 Q10.2a](../decisions/0002-search-design-interview.md#q10--datenbank-zielzustand-und-übergang)
verlangt wiederum Audit vor jeder Produktionsänderung. Für diesen Audit soll
erst die Rolle entstehen. Die
[Entscheidungskarte](../discovery/project-decision-map.md#offene-punkte-und-gates)
bildet die Auflösung dieses Zirkels nicht ab.

Erforderlich ist ein ausdrücklich begrenzter Bootstrap-Plan mit Evidenzweg,
verantwortlichem Akteur, Restore-Voraussetzung und eigener Freigabe. Keine
stillschweigende Nutzung eines privilegierten Zugangs als Ersatz. Abgelehnte
Backup-Prüfungen werden durch diesen Bericht nicht erneut autorisiert.

### A02 — Rollen-Setup und Rollback sind nicht ausführbar verifiziert · P1

Im [Setup-SQL](../discovery/sql/01-create-least-privilege-discovery-role-v1.sql)
stehen ab Zeile 63 qualifizierte Ausdrücke `pg_catalog.current_user`.
`CURRENT_USER` ist ein spezieller SQL-Ausdruck; die verwendete Form ist ein
qualifizierter Spaltenverweis, kein Nachweis der aktuellen Rolle.

Das Setup erteilt außerdem `CONNECT`, während der
[Rollback](../discovery/sql/01-drop-least-privilege-discovery-role-v1.sql)
nur `DROP ROLE` vorsieht und die eigene Grant-Abhängigkeit nicht entfernt.
Damit fehlt ein vollständiger Rückweg bereits für den vorgesehenen Setupzustand.
Unerwartete Abhängigkeiten müssen weiterhin zum Abbruch führen.

Der existierende statische Test besteht trotz dieser Befunde, weil er
Textfragmente prüft. Vor Ausführung sind Korrektur und eine echte synthetische
PostgreSQL-Probe von Setup, Fehlerabbruch und Rückweg nötig. Dieser Audit
hat keine solche Datenbankprobe durchgeführt. Primärquellen siehe
[technische Verifikation](../research/2026-09-11-plan-best-practice-verification.md).

### A03 — Rechteinventar kann Sichtbarkeitslücken als leere Befunde liefern · P1

[B2-SQL](../discovery/sql/10-catalog-structure-gate-b2.sql), Zeilen 142 und 177,
verwendet rollenabhängige `information_schema`-Rechtesichten. Die neue Rolle
soll ausschließlich `CONNECT` erhalten. Ein leeres Resultat beweist dadurch
nicht das Fehlen von Grants anderer Rollen. Ebenso sind `pg_stats`-Befunde
an Zugriffsrechte gebunden.

Vollständigkeit und Berechtigungsscope müssen pro Query ausdrücklich belegt
werden. Ein gesondert genehmigter Katalog-/Attestweg ist einer pauschalen
Erweiterung der Leserechte vorzuziehen. Vorhandene Texttests beweisen diese
Sichtbarkeit nicht.

### A04 — Sprachtest erwartet erfundene, nicht genannte Filter · P1

Die [Testmatrix](../SUPABASE_CRM_MCP_IMPLEMENTATION_BRIEF.md#test-matrica),
Zeilen 824–826, fordert identische Filter für L-BS-01, L-DE-01 und L-EN-01.
Im deutschen Beispiel fehlen Alter und Sprachanforderung; im englischen
fehlt der Altersbereich. Dies widerspricht der bestätigten Regel, dass
ungenannte Filter inaktiv bleiben.

Die Beispiele müssen wirklich bedeutungsgleich sein. Zusätzlich braucht es
einen Negativfall, der das Weglassen einer Kategorie ausdrücklich prüft.
Erwartete Filter fachlich unabhängig definieren, nicht aus der zu testenden
Implementierung generieren.

### A05 — Aktueller Discovery-Status ist nicht synchronisiert · P2

Das [Rollenpaket](../discovery/least-privilege-discovery-role-v1.md) verlangt
nach dem Setup einen B1-V3-Preflight. [Projektstatus](../project.md) und
[kritischer Pfad](../discovery/project-decision-map.md#kritischer-pfad)
zeigen weiterhin B1 V2 als nächsten Lauf. Die Karte enthält außerdem noch
keine Übernahme der akzeptierten ADR-0004-Automatisierung.

Der [Gate-B-Preflight](../discovery/security-read-only-discovery-preflight-b.md)
behauptet stellenweise weiterhin fehlende Ziel-/Servicedateien, während der
neuere Worklog ihre Existenz und Dateimetadaten dokumentiert. Existenz,
inhaltliche Zielprüfung, wirksame Rechte und Freigabe getrennt führen.

### A06 — B2/B3 und nachgelagerte Discovery sind noch keine fertige Pipeline · P2

Es existiert nur ein ausführungsgebundener B1-Launcher. Die B2-/B3-Entwürfe
besitzen noch keine entsprechend implementierten und getesteten Streammarker,
Launcher und eigenen Freigabepakete. B3 ist zudem breiter als der aktuelle
B2-Scope; es braucht vor Weiterverwendung eine neue objektgebundene Allowlist.

In [B3](../discovery/sql/20-definitions-statistics-gate-b3-draft.sql) fehlt die
explizite Behandlung der PUBLIC-Rollenkennung in der Policy-Auswertung.
Funktionskörper, sicherheitsrelevante Funktionskonfiguration und
View-`security_invoker`-Einstellungen sind nicht vollständig abgedeckt.
Aggregierte DQ- und Query-Plan-Nachträge liegen ebenfalls hinter eigenen Gates.

Die dokumentierten BLOCKED-/DRAFT-Status verhindern einen aktuellen Zugriff.
Der Fehler liegt in fehlenden Arbeitspaketen und Vollständigkeitsnachweisen,
nicht in einer hier beobachteten Datenfreigabe.

### A07 — Must-have und optionale Liste widersprechen sich · P2

Im [Brief](../SUPABASE_CRM_MCP_IMPLEMENTATION_BRIEF.md#good-to-have-zahtjevi)
stehen Cursor, Ranking-Spezifikation, Vertragsversionierung, sichere Fehler
und Health/Observability unter Good-to-have, obwohl andere Abschnitte sie
verbindlich für die Abnahme verlangen. Reproduzierbare Entwicklungsdaten sind
sogar als Nice-to-have gelistet, inzwischen aber Bestandteil von ADR-0004.

Jede Anforderung braucht genau einen aktuellen Release-/Pflichtstatus.
Optionale LLM-Neusortierung von 50–100 Ergebnissen im Nice-to-have-Abschnitt
benötigt zudem eine ausdrückliche Abgrenzung zur autoritativen DB-Rangfolge
aus ADR-0001; sie ist kein stillschweigend freigegebener Runtime-Pfad.

### A08 — Acht lokale Ticketzeilen sind kein vollständiger Umsetzungsplan · P2

Der [Ticketplan](../planning/release-1-automation-tickets.md) bezeichnet sich
korrekt als Automatisierungsentwurf. Er deckt nicht alle Produktarbeiten mit
eigenen überprüfbaren Arbeitspaketen ab: drei Runtime-Tools, Taxonomie und
Profile, getrennte Profilverwaltung, vollständige Autorisierung,
Bootstrap/Restore, B2/B3, Mehrclient-Abnahme und Rollout fehlen als
selbstständige, nachverfolgbare Liefergegenstände.

Eigene Verantwortliche, konkrete Evidenzartefakte und saubere Akzeptanzfälle
fehlen pro Ticket; ADR-0004 verlangte zudem eigene CLI-/Promptfoo-Diagnosetickets.
AUTO-02 soll den Designvertrag abschließen, nennt denselben Interviewabschluss
aber bereits als Blocker. Diese Zuständigkeit muss entwirrt werden.
`AUTO-01` bis `AUTO-03` werden im Brief zusätzlich für andere Testfälle benutzt.
Getrennte Namensräume vermeiden falsche Zuordnungen.

AUTO-07 hängt außerdem am bereits erfolgten Rollout. Betriebsbereite
Minimalalarme und Monitoring müssen gemäß den Releasekriterien vor dem
Rollout nachgewiesen werden; ihre spätere Verfeinerung kann danach folgen.

Linear ist tatsächlich leer; dies ist keine fehlerhafte Synchronisierung
bereits bestehender Tickets. Die spätere Erstellung bleibt ein eigener
externer Write. Die heutige Prüfung erstellt keine Tickets.

### A09 — Automatische Gates benötigen konkrete Fehler- und Restore-Semantik · P1

Der [Automatisierungsrunbook](../runbooks/database-development-automation.md)
nennt Lint, Reset, Tests und Dry-run, spezifiziert aber nicht alle Bedingungen,
die einen falschen Erfolg verhindern:

- SQL-Lint muss bei vereinbarten Findings mit Fehlercode abbrechen; bloßes
  `db lint` ist laut aktueller CLI-Referenz kein verlässlicher Fehler-Gate.
- `db push --dry-run` listet geplante Migrationen. Es ist weder eine echte
  Ausführungsprobe noch ein Lock-, RLS-, Datenintegritäts- oder Restore-Test.
- Frischaufbau aus Null und Upgrade vom letzten freigegebenen Stand sind
  verschiedene Testpfade. Beide sind für spätere Migrationen erforderlich.
- Fachlich gezielte negative Kontrollfälle müssen beweisen, dass der Gate
  eine absichtlich fehlerhafte Änderung tatsächlich stoppt.
- Tatsächlich installierte Erweiterungsversionen und explizite Grants müssen
  geprüft werden; generierter Schema-Diff allein reicht nicht als Sicherheitsbeweis.

Das sind Kriterien für den späteren Scaffold, keine hier ausgeführten
CLI-/Datenbankbefehle. Quellen und Details stehen im
[Best-Practice-Bericht](../research/2026-09-11-plan-best-practice-verification.md).

### A10 — Aktueller Linktest prüft den falschen Arbeitsstand · P2

[relative_markdown_links_test.py](../../tests/docs/relative_markdown_links_test.py),
Zeilen 24–37, liest über `git show :datei` den Index und berücksichtigt nur
getrackte Dateien. Unstaged Änderungen und neue ADR-/Planungsdateien fehlen.
Heute meldet er 281 gültige Links; der zusätzliche Arbeitsdatei-Check prüft
332. Beide bestehen, aber nur letzterer erfasst die aktuellen Dokumente.

Künftig Indexprüfung für Commit-Artefakte und Working-Tree-Prüfung für den
aktiven Audit ausdrücklich auswählen; neue Dateien einschließen. Die lokale
Zusatzprüfung dieses Audits verwendet einen begrenzten Markdown-Linkparser,
keinen vollständigen CommonMark-Renderer.

### A11 — Forschungs- und Umgebungsstatus brauchen präzisere Zeitbezüge · P2

Ältere Tool-Recherche beschreibt noch `Allow low-risk` und einen späteren
produktiven Developer-MCP-Pfad. Neuere Projektregeln bestätigen `Always ask`
und verbieten diesen Zugriff auf das Produktionsprojekt. Aktuelle
Herstelleroptionen und eure strengere Projektentscheidung getrennt darstellen.

Die frische Supabase-Versionsprüfung scheitert konkret an einem vom Sandbox
verweigerten Telemetrie-Dateischreibzugriff. Das beweist keine defekte
CLI-Installation. Promptfoo scheitert erneut am nativen Modul-ABI-Konflikt.
Beide sind in dieser Sitzung nicht einsatzbereit, die Ursachen sind verschieden.
Keine Neuinstallation, Reparatur oder globale Konfigurationsänderung erfolgte.

### A12 — Dokumentationshygiene ist nicht vollständig erfüllt · P2/P3

Der Brief enthält in Zeile 5 weiterhin einen konkreten Projektendpoint,
obwohl dessen Dokumentationsfreigabe offen ist und die aktuellen Regeln
private Projektkennungen im Repository ausschließen. Hier wird nur die
Fundstelle genannt, der Wert nicht wiederholt. Alias verwenden; eine mögliche
Historienbereinigung wäre eine separate Git-Entscheidung.

Markdownlint meldet **611 Befunde in 17 von 39 Dateien**: 553 Zeilenlängen-
und 58 Tabellenformat-Befunde. Das ist dokumentierter Formatierungsbedarf,
kein Beleg für 611 fachliche Fehler. Die Serena-Memory `suggested_commands`
behauptet außerdem noch, es gebe keine Lint-/Testkommandos, obwohl README und
Testverzeichnis solche bereits enthalten. Historische PASS-Berichte sind
Zeitpunktnachweise und keine heutige Vollprüfung.

## Kürzerer Ablauf mit denselben Qualitätsanforderungen

Die Verbesserung liegt in weniger Doppelpflege, echten Abhängigkeiten und
einem frühen vollständigen Durchstich. Sie besteht nicht im Weglassen von
Funktionen, Security, Restore oder Nutzerentscheidungen.

<!-- markdownlint-disable MD013 -->

| Arbeit | Vorschlag | Erhaltener Qualitätsnachweis |
| --- | --- | --- |
| Dokumentpflege | Ein Anforderungsregister mit stabiler ID, Release, Status, ADR, Test und späterem Linear-Link; Übersichten daraus ableiten. | Jede Pflichtfunktion und jede offene Entscheidung bleibt nachvollziehbar. |
| Vorbereitungen | Dokumentchecks, Tooldiagnose und synthetische Testfallplanung unabhängig von späteren fachlichen Entscheidungen vorbereiten. | Keine produktive Verbindung und keine vorweggenommene Schemazusage. |
| Discovery | Bestehende Exporte zur Eingrenzung nutzen; einen wiederverwendbaren Ausgabeschutz entwerfen, aber B1/B2/B3 weiterhin getrennt freigeben. | Identische Ziel-, Hash-, Scope-, Größen- und Redaktionskontrollen je Gate. |
| Vertragsarbeit | Nach Discovery die entscheidenden Release-1-Fragen zuerst abschließen; spätere Kontakt-/Export-/Vektorentscheidungen als eigene Frontier führen. | Q8.5, Auth, Filtersemantik und andere echte R1-Blocker bleiben zwingend. |
| Implementierung | Nach Scaffold/Gates einen vertikalen Durchstich aus Validator, RPC, Auth und MCP-Tool bauen; danach alle vorgesehenen Tools und Filter vollständig ergänzen. | Durchgängige Tests beginnen früh; der erste kleine Durchstich ist noch kein freigabefähiger Release. |
| Profilverwaltung | Gemeinsame versionierte Vertrags-/Testbibliothek nutzen, fachliche Funktionen nach ADR-0003 implementieren. | Getrennte Identitäten, Rechte, Deployments und Veröffentlichungsbestätigung bleiben bestehen. |
| CI | Ein reproduzierbarer Ablauf; kurze lokale Auswahl beim Editieren, vollständiger relevanter Gate vor Merge/Release. | Frischaufbau, Upgrade, negative RLS-/Grant-Tests, Contract, Datenschutz und Rückweg bleiben abgedeckt. |
| Leistung | Repräsentative Queries und vorab definierte Qualitäts-/Budgetgrenzen früh; schwere Last-/Soakläufe gezielt vor Release oder bei relevanten Änderungen. | Keine nachträgliche Anpassung der Ziele, nur damit ein langsamer Build besteht. |
| Zusatzwerkzeuge | Native Diagnostik zuerst; Zusatztool nur für einen belegten Diagnose-/Qualitätsengpass. | Kein zusätzlicher Dienst allein wegen Kalenderablauf oder Herstellerwerbung. |

<!-- markdownlint-enable MD013 -->

Die Entkopplung späterer Entscheidungen vom Release-1-Abschluss und ein
ereignisabhängiger statt starrer 4–8-Wochen-Trigger für pganalyze wären
ausdrückliche Änderungen an ADR-0002 beziehungsweise ADR-0004. Sie gelten
hier nur als Vorschläge. Bestehende Gates werden nicht automatisch verkürzt.

Ein einziger kanonischer Eingabe-/Ausgabevertrag kann Validatoren, Toolschemas,
Typen und Dokumentation versorgen. Die fachlichen Sollwerte des mehrsprachigen
Referenzsets müssen unabhängig davon gepflegt werden. Andernfalls bestätigen
automatisch erzeugte Tests nur denselben Fehler wie die Implementierung.

## Reihenfolge der Nacharbeit

1. A01–A04 klären beziehungsweise korrigieren; besonders Zugangsbootstrap,
   Rollen-SQL, Metadatensichtbarkeit und widersprüchliche Sprachtests.
2. A05–A12 konsolidieren und ein vollständiges lokales
   Anforderung-zu-Test-zu-Arbeitspaket-Mapping erstellen.
3. Bootstrap/Discovery separat freigeben und durchführen; danach die noch
   offenen Release-1-Verträge abschließen.
4. Scaffold und automatische Gates etablieren; vollständige Funktionalität
   in kleinen durchgängigen Schritten bauen und prüfen.
5. Erst mit tatsächlichen Qualitäts-, Last- und Restore-Nachweisen die
   konkrete Produktionseinführung freigeben.

Es gibt keine belastbare Prozentzahl zur Zeitersparnis. Rework, Durchlaufzeit,
manuelle Prüfschritte, Fehlerquote und Kosten müssen vor/nach der Umstellung
gemessen werden. Funktions- und Qualitätsgleichheit ist ein Abnahmekriterium,
keine durch Werkzeugwahl garantierte Eigenschaft.

## Tatsächlich ausgeführte Verifikation

Lokaler Prüfzeitpunkt: 2026-09-11 ab 10:29 UTC.

<!-- markdownlint-disable MD013 -->

| Prüfung | Ergebnis und Grenze |
| --- | --- |
| Root-/docs-Markdown im Arbeitsverzeichnis | 39 Dateien, 332 lokale Ziele/Fragmente, keine fehlenden Ziele und keine offenen Code-Fences. Vor Erstellung der beiden neuen Auditberichte. |
| Bestehender relativer Linktest | PASS, 281 Links; Git-Index, nicht aktueller Working Tree. |
| Markdownlint | FAIL, 611 Befunde: MD013 553, MD060 58; 17 betroffene Dateien. |
| Neun weitere Python-Prüfdateien | PASS: Schema-Taskliste, Plugin-Gate, B1-Statik, B2-Scope, Rollen-Statik und vier Prozess-/Stream-/Signalprüfungen. |
| Fake-psql-Launcher | 14 benannte Testgruppen PASS; synthetische Prozesse, keine Datenbankverbindung. |
| Bash-Syntax | Beide Shell-Dateien einzeln mit `bash -n` erfolgreich geprüft. |
| Aktuelle Hashbindungen | Fünf aktuelle Gate-Hashes stimmen; historische Hashstände bleiben historisch. |
| Git-Diff-Whitespace | PASS; erfasst vorhandene getrackte Änderungen. |
| Supabase CLI `--version` | Exit 1: EPERM beim lokalen Telemetrieschreiben im Sandbox. Kein Beweis eines installierten Versions-/Programmfehlers. |
| Promptfoo `--version` | Exit 1: `better-sqlite3` ABI 141 statt benötigter 147. |
| Anwendung, Live-RLS, SQL-Ausführung, Last und Restore | Nicht durchgeführt; fehlender Scaffold beziehungsweise nicht freigegebener Datenbank-/Backupzugriff. |

<!-- markdownlint-enable MD013 -->

Keine konfigurierte pytest-, Ruff-, mypy- oder Anwendungspipeline wurde
gefunden. Statt erfundener Projektkommandos wurden die tatsächlich vorhandenen
direkt ausführbaren Testdateien verwendet. Serena konnte ohne konfigurierte
Language Server keine Python-Symbole liefern; lokales Lesen war der
dokumentierte Fallback.

Das reproduzierbare zusätzliche Prüfscript liegt lokal unter
`/private/tmp/dino_document_audit_20260911.py`; timestamped Ergebnisse und
Ausgangs-Hashes unter `/private/tmp/dino-document-audit-20260911/`.
Diese temporären Dateien sind keine dauerhaft etablierte Projektpipeline.

Der Audit ergänzt ausschließlich diesen Bericht und den verlinkten
Best-Practice-Bericht. Bestehende Änderungen bleiben erhalten. Kein Commit,
keine Ticketanlage, keine Datenbankmutation und kein Deployment erfolgten.

Abschließender Check nach Erstellung der Berichte: **41 Markdown-Dateien,
360 gültige lokale Verweise**, keine veränderte der 39 zuvor erfassten
Markdown-Dateien laut SHA-256-Vergleich. Beide neuen Berichte bestehen
Markdownlint mit null Befunden. `git diff --check` ist weiterhin erfolgreich;
die 611 zuvor gemessenen Formatbefunde der vorhandenen Dokumente sind
dadurch nicht behoben.
