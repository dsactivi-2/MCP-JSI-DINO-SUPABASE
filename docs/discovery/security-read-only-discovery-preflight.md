# Security- und Read-only-Discovery-Gate

Gate-ID: DISCOVERY-GATE-2026-09-11-A

Status: **NO-GO – VORLÄUFIGER VORSCHLAG, ausdrückliche Freigabe ausstehend**

Dieses Dokument bereitet den ersten Blocker vollständig vor. Es autorisiert
weder eine Datenbankverbindung noch SQL-Ausführung, Kandidatendatenzugriff,
Migrationen oder sonstige Änderungen.

## 1. Freigabegegenstand

Die vorgeschlagene Freigabe gilt ausschließlich für eine getrennte Sitzung und
genau zwei aufeinanderfolgende read-only Stufen:

1. Prüfung der aktiven Identität und ihrer effektiven Rechte mit
   [00-identity-and-privilege-gate.sql](sql/00-identity-and-privilege-gate.sql).
2. Nur wenn Stufe 1 ohne STOP endet: Kataloginventar mit
   [10-metadata-inventory.sql](sql/10-metadata-inventory.sql).

Nicht umfasst sind Kandidatenzeilen, exakte Zählungen über Fachtabellen,
Data-Quality-Abfragen auf Fachdaten, CVs, Kontakte, freie Textfelder,
EXPLAIN ANALYZE, Funktionsaufrufe, RPCs oder dynamisch erzeugtes SQL. Dafür wäre
nach Sichtung des Metadateninventars eine neue exakte Query-Allowlist und eine
separate Freigabe erforderlich.

## 2. Getrennte Zustände

### Fakten

- Der Nutzer übernimmt derzeit Product, Data, Security, Privacy/Legal,
  Operations und Discovery.
- Eine zweite prüfende Person ist nicht verpflichtend.
- Die Datenbank wurde nicht auditiert; physische Struktur, RLS und Tenant-Modell
  sind unbekannt.
- Discovery-Repository-Artefakte bleiben ohne Kontaktwerte. Produkt R1 intern sieht Kontakte (Q4).
- Die SQL-Dateien wurden in dieser Sitzung nur geschrieben und lokal geprüft,
  nicht ausgeführt.

### Akzeptierte Entscheidungen

- Q9 verlangt zuerst dieses Sicherheitsgate, danach read-only Discovery und erst
  anschließend die Fortsetzung des Designinterviews.
- Runtime-SQL bleibt kontrolliert; die Discovery-Ausnahme gilt nur für vorher
  geprüfte read-only Auditabfragen.
- Unbekannte Tabellen, Spalten, Beziehungen oder RLS-Eigenschaften werden nicht
  als Fakten behandelt.

### Vorschläge zur Freigabe

| Parameter | Vorgeschlagener Wert |
| --- | --- |
| Identität | Dedizierte, zeitlich begrenzte Login-Rolle; kein gemeinsam genutzter Benutzer. |
| Versionsbereich | PostgreSQL 15 bis 18; andere Version führt zu STOP und Review. |
| Zeitfenster | Ein beaufsichtigtes Fenster von höchstens 45 Minuten. |
| Statement timeout | 5 Sekunden je Gate- oder Metadatenabfrage. |
| Lock timeout | 1 Sekunde. |
| Idle-in-transaction timeout | 15 Sekunden. |
| Parallelität | Genau eine Datenbankverbindung, keine parallelen Abfragen. |
| Transaktion | Explizit READ ONLY; Abschluss immer mit ROLLBACK. |
| Ergebnisgrenze | In SQL festgelegte Limits; zusätzlich höchstens 10 MiB pro Abfrageausgabe. |
| Rohdatenort | Neuer lokaler temporärer Ordner außerhalb des Git-Arbeitsbaums, Modus 0700. |
| Repository-Ausgabe | Nur manuell redigierte und geprüfte Markdown-/CSV-Zusammenfassungen. |
| Retention | Rohdaten nach abgenommener Redaktion nach separater Löschfreigabe entfernen. |

### Arbeitsannahmen

- Eine dedizierte Identität mit den vorgeschlagenen Rechten kann bereitgestellt
  werden.
- Der Server liegt im freigegebenen Versionsbereich.
- Die Katalogabfragen sind mit der tatsächlich eingesetzten Version kompatibel.
- Metadaten reichen aus, um eine zweite, objektgebundene Auditstufe zu entwerfen.

### Offene Punkte vor Ausführung

- Ausdrückliche Freigabe von Gate-ID, Scope, SQL-Dateien und Grenzwerten.
- Sicherer Übergabeweg für die Identität; keine Credentials im Chat, Repository,
  Shell-Verlauf, Bericht oder Diff.
- Exakter Beginn und Ende des 45-Minuten-Fensters.
- Verantwortliche Entscheidung, falls TEMP-Recht oder unerwartete
  SECURITY-DEFINER-Ausführbarkeit gefunden wird.
- Löschfreigabe und Retention für die späteren Rohmetadaten.

## 3. Rollen- und Rechteprofil

Die Discovery-Identität soll ausschließlich verbinden, Metadaten lesen und
ausgewählte Katalogsichten abfragen können. Sie soll keine Datenbank, Schemas,
Relationen oder Routinen besitzen.

### Sofortiger STOP

- Superuser, BYPASSRLS, CREATEROLE, CREATEDB oder REPLICATION ist aktiv.
- Die Identität ist Datenbank-, Schema-, Relations- oder Routine-Owner.
- Direkte oder geerbte Rolle gewährt administrative, Owner-, Migration- oder
  Write-Rechte.
- Effektives INSERT, UPDATE, DELETE, TRUNCATE oder TRIGGER besteht auf einem
  nicht-systemischen Objekt.
- CREATE besteht auf Datenbank oder nicht-systemischem Schema.
- Eine ausführbare SECURITY-DEFINER-Routine ist nicht vorab einzeln bewertet.
- Der Server oder die Datenbank ist nicht die ausdrücklich freigegebene
  Zielumgebung.

### WARN mit Entscheidung vor Fortsetzung

- TEMP ist aktiv. Das ist kein Zugriff auf Kandidatenzeilen, erweitert aber die
  Schreibfähigkeit der Sitzung und soll für diese Identität möglichst entzogen
  werden.
- Die Identität erbt zusätzliche reine Leserechte, deren Scope breiter als die
  geplante Discovery ist.
- Katalogausgabe überschreitet die Zeilen- oder 10-MiB-Grenze.
- Eine Abfrage läuft in einen Timeout oder benötigt Sperren über dem Lock-Limit.

Ein WARN wird im Arbeitsbericht dokumentiert und vor der nächsten Stufe vom
Discovery-/Security-Verantwortlichen entschieden. Ein STOP beendet die Sitzung
ohne Metadateninventar.

## 4. Überprüfbare SQL-Allowlist

Die beiden Dateien sind die vollständige Allowlist für die erste
Datenbanksitzung. Erlaubt ist nur der unveränderte Dateiinhalt. Vor Ausführung
werden SHA-256, Git-Diff und Dateipfad geprüft. Es gibt keine freie
SQL-Eingabemöglichkeit und keine Identifier-Substitution.

### Stufe 1: Identitätsgate

| ID | Zweck | Erfolgsbedingung |
| --- | --- | --- |
| SQL-GATE-001 | Ziel, Rolle, Version und READ ONLY prüfen. | Freigegebenes Ziel; Version 15-18; transaction_read_only = on. |
| SQL-GATE-002 | Gefährliche Rollenattribute prüfen. | Alle administrativen/BYPASSRLS-Attribute false. |
| SQL-GATE-003 | Direkte und geerbte Rollen ermitteln. | Keine administrative, Owner-, Migration- oder Write-Rolle. |
| SQL-GATE-004 | Datenbankeigentum, CREATE und TEMP prüfen. | Kein Owner/CREATE; TEMP höchstens WARN. |
| SQL-GATE-005 | Schemaeigentum und CREATE prüfen. | Keine Treffer mit Owner oder CREATE. |
| SQL-GATE-006 | Effektive Objekt-Write-Rechte prüfen. | Null Treffer. |
| SQL-GATE-007 | Ausführbare SECURITY-DEFINER-Routinen prüfen. | Null Treffer oder vorherige Einzelbewertung; sonst STOP. |
| SQL-GATE-008 | Angewandte Sessionlimits prüfen. | Alle vorgeschlagenen Limits sind aktiv. |

### Stufe 2: Metadateninventar

| ID | Inhalt | Persistenzklasse |
| --- | --- | --- |
| SQL-META-001 | Nicht-systemische Schemas. | Restricted raw; redigierte Zusammenfassung. |
| SQL-META-002 | Relationen, RLS-Flags, Schätzzeilen und Größen. | Restricted raw; redigierter Inventarbericht. |
| SQL-META-003 | Spalten, Typen, Nullability und Default-Flags ohne Defaultausdrücke. | Restricted raw; Data Dictionary nach Review. |
| SQL-META-004 | Constraints und Schlüsselbeziehungen ohne Datenwerte. | Restricted raw; ER-Übersicht nach Review. |
| SQL-META-005 | RLS-Policies und Ausdrücke. | Restricted raw; nur sicherheitsgeprüfte Zusammenfassung. |
| SQL-META-006 | Sichtbare Tabellen- und View-Grants. | Restricted raw; pseudonymisiertes Grant-Inventar. |
| SQL-META-007 | Routinen, Signaturen und Sicherheitsflags ohne Quelltext. | Restricted raw; Routine-Inventar. |
| SQL-META-008 | Sichtbare Routine-Grants. | Restricted raw; pseudonymisierte Zusammenfassung. |
| SQL-META-009 | Indexstatus, Größe und Definition. | Restricted raw; Index-Inventar. |
| SQL-META-010 | Nicht-interne Triggerdefinitionen. | Restricted raw; Trigger-Inventar. |
| SQL-META-011 | Aggregierte Relationsaktivitätsstatistik. | Restricted raw; Größen-/Nutzungsbaseline. |
| SQL-META-012 | Extensionname und Version ohne Konfiguration. | Restricted raw; Extension-Inventar. |
| SQL-META-013 | Viewdefinitionen. | Besonders restricted; nur nach Redaktionsreview. |
| SQL-META-014 | Plannerstatistik ohne common values oder Histogrammwerte. | Restricted raw; aggregierte DQ-Hinweise. |
| SQL-META-015 | Enumlabels ohne Kandidatenzeilen. | Restricted raw; nur freigegebene Taxonomiehinweise. |
| SQL-META-016 | Publication-Metadaten ohne replizierte Inhalte. | Restricted raw; Replikationsübersicht. |

### Explizit nicht allowlistet

- SELECT gegen fachliche oder Kandidatentabellen;
- COUNT, SAMPLE, DISTINCT, MIN/MAX oder sonstige Aggregate auf Fachdaten;
- pg_stats.most_common_vals, most_common_freqs oder histogram_bounds;
- Funktions- oder RPC-Aufrufe;
- INSERT, UPDATE, DELETE, MERGE, COPY, CREATE, ALTER, DROP, TRUNCATE, GRANT,
  REVOKE, COMMENT, VACUUM, ANALYZE oder REFRESH;
- EXPLAIN ANALYZE sowie dynamisches SQL;
- Zugriff auf CV-, Kontakt-, Geburts-, Identifikations- oder freie Textwerte;
- Secret-, FDW-Options-, Connection-String- oder Vault-Abfragen.

## 5. Vollständige Stop-Kriterien

Die Sitzung stoppt sofort und fail-closed, wenn mindestens eines gilt:

1. Eine Gate-Abfrage schlägt fehl oder ergibt ein STOP-Signal.
2. Das Ziel, die Rolle, der Hash, die SQL-Datei oder das Zeitfenster weicht von
   der Freigabe ab.
3. READ ONLY oder eines der Sessionlimits ist nicht nachweislich aktiv.
4. Eine Abfrage ist nicht exakt in den zwei freigegebenen Dateien enthalten.
5. Ein Tool schlägt Identifier, SQL-Fragmente oder zusätzliche Queries vor.
6. Kandidatenzeilen oder andere Fachdaten würden gelesen.
7. Kontakt, CV-Text, Geburtsdatum, Identifikationsnummer, Secret, Token oder
   private Verbindungsinformation erscheint in der Ausgabe.
8. RLS- oder Tenant-Grenzen sind unerwartet, nicht sichtbar oder widersprüchlich.
9. Zeilen-, Größen-, Timeout-, Sperr- oder Parallelitätsgrenze wird überschritten.
10. Der Scope weicht vom Metadateninventar ab oder eine Mutation wird versucht.
11. Redaktions- oder Persistenzregeln können nicht eingehalten werden.
12. Die verantwortliche Person widerruft die Freigabe oder fordert Pause.

Bei möglichem Datenleck werden keine weiteren Abfragen gestartet. Es werden nur
minimierte technische Fakten ohne PII dokumentiert; Incident- und
Privacy/Legal-Entscheidungen folgen außerhalb dieser Allowlist.

## 6. Ausgaberichtlinie

| Klasse | Beispiele | Zulässiger Ort | Git |
| --- | --- | --- | --- |
| Verboten | Secrets, Tokens, Connection Strings, Kontakte, CV-Text, Geburtsdaten, Identifikationsnummern, Kandidatenzeilen. | Nirgends speichern; bei Sichtung STOP. | Nie. |
| Restricted raw | Objekt-/Rollennamen, Policy-, View-, Trigger- oder Indexdefinitionen, Katalogausgabe. | Temporärer Ordner außerhalb des Arbeitsbaums, Modus 0700. | Nie unverändert. |
| Sanitized review | Pseudonymisierte Rollen, minimierte Objektmetadaten, Aggregate ohne kleine Gruppen oder Wertverteilungen. | Freigegebener Discovery-Artefaktordner. | Erst nach manueller Security-/Privacy-Prüfung. |
| Public project fact | Bestätigte, nicht sensible Struktur- und Entscheidungszusammenfassung. | Versionierte Projektdokumentation. | Nach ausdrücklicher Dokumentationsfreigabe. |

Zusätzliche Regeln:

- Rohoutputs erhalten Session-ID, Query-ID, UTC-Zeit, Toolversion und SHA-256,
  aber keine Credentials oder freien Benutzertexte.
- Rollennamen werden außerhalb des Restricted-Ordners durch stabile
  sitzungsspezifische Pseudonyme ersetzt.
- Policy-, View-, Trigger- und Indexdefinitionen werden vor Repository-Ablage
  auf Literale, private Namen und unerwartete Daten geprüft.
- Null-/Distinct-/Histogrammwerte werden erst in der zweiten, separat
  allowlisteten Stufe erhoben; kleine Gruppen werden unterdrückt.
- Kein Rohoutput wird in Prompts, Tickets, Logs, Chatnachrichten oder Commits
  kopiert.
- Ein Sanitization-Review prüft auch den Git-Diff vor jeder Persistenz.

## 7. Discovery-Artefaktliste

Die erste freigegebene Sitzung soll folgende minimierte Nachweise erzeugen:

| Artefakt | Inhalt | Status nach erster Sitzung |
| --- | --- | --- |
| 00-session-manifest | Gate-ID, Zeitfenster, Query-Datei-Hashes, Tool- und Serverversion, Identitätspseudonym. | Erwartet. |
| 01-privilege-gate-report | PASS/WARN/FAIL je SQL-GATE-ID; keine Credentialwerte. | Erwartet. |
| 02-schema-relation-inventory | Schemas, Relationsarten, Größenklassen, Schätzzeilen und RLS-Flags. | Erwartet, redigiert. |
| 03-data-dictionary-draft | Spalten, Typen, Nullability, Identity-/Generated-Flags; keine Datenwerte. | Erwartet, redigiert. |
| 04-relationship-map | PK/FK/Unique/Check-Metadaten und ER-Übersicht ohne Kandidatenwerte. | Erwartet, redigiert. |
| 05-security-inventory | RLS-, Grant-, Rollen-, Routine- und SECURITY-DEFINER-Befunde. | Erwartet, besonders geschützt. |
| 06-index-trigger-view-inventory | Index-, Trigger- und View-Metadaten. | Erwartet, besonders geschützt. |
| 07-extension-replication-inventory | Extensions und Publication-Metadaten ohne Konfiguration oder Inhalte. | Erwartet, redigiert. |
| 08-relevant-object-shortlist | Begründete Auswahl für spätere fachliche Tiefenprüfung. | Vorschlag zur Nutzerprüfung. |
| 09-open-facts-risks-decisions | Fakten, Risiken, Annahmen und offene Entscheidungen getrennt. | Erwartet. |
| 10-deep-discovery-query-proposal | Exakte objektgebundene SQL-Allowlist für Aggregate, DQ und sichere Planprüfung. | Entwurf; neue Freigabe nötig. |

Spätere, noch nicht freigegebene Artefakte sind ein aggregierter
Data-Quality-Bericht, sichere Query-Plan-Baselines, die Zuordnung zum kanonischen
Modell sowie JSON-/MCP-/RPC-Vertragsvorschläge.

## 8. Ausführungsprotokoll für die getrennte Sitzung

1. Freigabetext und Gate-ID abgleichen; bei Abweichung STOP.
2. SQL-Dateien und SHA-256 gegen den freigegebenen Git-Diff prüfen.
3. Restriktiven temporären Rohdatenordner außerhalb des Repositories erzeugen.
4. Credentials über einen lokalen, nicht protokollierten Mechanismus beziehen.
5. Nur die Identity-Gate-Datei in einer READ-ONLY-Transaktion ausführen.
6. Resultat gegen alle STOP-/WARN-Kriterien auswerten und protokollieren.
7. Nur bei PASS beziehungsweise ausdrücklich entschiedenem WARN die
   Metadaten-Datei ausführen.
8. Ausgaben lokal redigieren; verbotene Inhalte führen zu STOP.
9. Sanitized Artefakte und offene Befunde prüfen; noch nichts committen.
10. Verbindung schließen und Rohdaten-Retention beziehungsweise spätere
    Löschung dokumentieren.
11. Den nächsten objektgebundenen Query-Nachtrag vorlegen; keine Tiefenprüfung
    ohne neue Freigabe.

## 9. Preflight-Ergebnis

| Prüfung | Status |
| --- | --- |
| Dokumentationsstand und Entscheidungsgrenzen gelesen | PASS |
| Abhängige Entscheidungskarte erstellt | PASS |
| Exakte Identity-/Privilege-Allowlist entworfen | PASS |
| Exakte Metadaten-Allowlist entworfen | PASS |
| Kandidaten- und Fachdatenzugriff ausgeschlossen | PASS |
| Stop-Kriterien und Ausgaberichtlinie definiert | PASS |
| Discovery-Artefakte definiert | PASS |
| SQL gegen Projektdatenbank ausgeführt | SKIPPED – ausdrücklich verboten |
| Identität und tatsächliche Rechte verifiziert | BLOCKED – benötigt freigegebene getrennte Sitzung |
| Gate vom Nutzer ausdrücklich freigegeben | BLOCKED |

**Gesamtstatus: PASS_WITH_GAPS / NO-GO.** Die Vorbereitung ist vollständig; die
operativen Fakten und die Nutzerfreigabe fehlen absichtlich. Datenbankzugriff
darf erst nach ausdrücklicher Freigabe dieses Gate-Scopes in einer getrennten
Sitzung beginnen.

## 10. Freigabepunkt

Eine wirksame Freigabe muss mindestens Gate-ID
DISCOVERY-GATE-2026-09-11-A nennen und ausdrücklich bestätigen:

- nur die zwei verlinkten, unveränderten SQL-Dateien;
- nur Identity-/Privilege- und Katalogmetadaten;
- die vorgeschlagenen Zeit-, Timeout-, Größen- und Parallelitätsgrenzen;
- die Stop-Kriterien und Ausgaberichtlinie;
- keine Kandidatenzeilen, Kontakte, CVs, Fachdatenaggregate oder Mutationen;
- Ausführung erst in einer getrennten Sitzung.

Jede Änderung dieser Punkte erzeugt eine neue Gate-Version und erfordert eine
neue Freigabe.

## Technische Referenzen

- [PostgreSQL: SET TRANSACTION](https://www.postgresql.org/docs/current/sql-set-transaction.html)
- [PostgreSQL: Systemkataloge](https://www.postgresql.org/docs/current/catalogs.html)
- [PostgreSQL: pg_policy](https://www.postgresql.org/docs/current/catalog-pg-policy.html)
- [PostgreSQL: table_privileges](https://www.postgresql.org/docs/current/infoschema-table-privileges.html)
- [PostgreSQL: routine_privileges](https://www.postgresql.org/docs/current/infoschema-routine-privileges.html)
