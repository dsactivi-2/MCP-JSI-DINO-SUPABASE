# Security- und Read-only-Discovery-Gate B

Gate-Familie: DISCOVERY-GATE-B

Ziel-Alias: **dino_crm_discovery_target_01**

Status: **PASS_WITH_GAPS / NO-GO**

Version A bleibt als historischer Entwurf erhalten. Version B ersetzt keine
fehlende Nutzerfreigabe. Es besteht keine Erlaubnis für eine
Datenbankverbindung, SQL-Ausführung oder Ausgabe von Datenbankresultaten.

## 1. Zielbindung ohne Repository-Geheimnisse

Der Ziel-Alias ist eindeutig und nicht geheim. Er bezeichnet nur den erwarteten
Discovery-Gegenstand; er enthält weder Host, URL, Projektkennung,
Datenbanknamen noch Credentials.

Vor jeder Verbindung muss ein lokales Zielattest verwendet werden:

\`/Users/activi/Library/Application Support/Activi/discovery-targets/dino_crm_discovery_target_01.target\`

Das Attest liegt außerhalb des Repositories, hat Modus \`0600\` und enthält:

- den Ziel-Alias;
- den erwarteten Datenbanknamen;
- SHA-256 der kanonisch normalisierten Host-/Projektkennung;
- zulässige lokale Connection-Service-Kennung;
- Erstellungszeit und verantwortliche Person.

B1 V2 verwendet zusätzlich ausschließlich folgende feste lokale Dateien:

- Freigabeattest:
  \`/Users/activi/Library/Application Support/Activi/discovery-targets/dino_crm_discovery_target_01.approval\`
- Connection Service:
  \`/Users/activi/Library/Application Support/Activi/discovery-targets/dino_crm_discovery_target_01.pg_service.conf\`
- Credential-Datei:
  \`/Users/activi/Library/Application Support/Activi/discovery-targets/dino_crm_discovery_target_01.pgpass\`

Alle drei Dateien müssen regulär, symlinkfrei, Eigentum des ausführenden
lokalen Nutzers und Modus \`0600\` sein. Der Connection Service erlaubt nur
\`host\`, \`dbname\`, \`user\`, \`sslmode\` und \`connect_timeout=5\` in genau
einem Abschnitt mit dem Ziel-Alias. Ein eingebettetes Passwort oder ein
unbekanntes Feld ist STOP. Die Credential-Datei wird nur an libpq übergeben und
vom Launcher weder gelesen noch ausgegeben. Das Freigabeattest darf erst aus
einer neuen ausdrücklichen Freigabe erstellt werden; es existiert in dieser
Sitzung nicht.

Die rohe Host-/Projektkennung, URL und der Datenbankname werden nicht in
Repository, Arbeitsbericht oder Chat kopiert. Der lokale Launcher:

1. prüft Eigentümer und Modus \`0600\` des Zielattests;
2. vergleicht den Alias bytegenau;
3. normalisiert die lokal gelesene Host-/Projektkennung als UTF-8,
   Kleinschreibung, außen getrimmt, ohne abschließenden Zeilenumbruch;
4. vergleicht deren SHA-256 bytegenau mit dem lokalen Attest;
5. übergibt den erwarteten Datenbanknamen nur als lokale
   \`psql\`-Variable \`expected_database_name\`;
6. lässt SQL-GATE-B1-002 den verbundenen Datenbanknamen serverseitig prüfen.

Alias-, Fingerprint- oder Datenbanknamenabweichung ist ein sofortiger STOP.
Die tatsächlichen Werte werden nicht ausgegeben.

## 2. Drei getrennte Freigabestufen

| Gate | Inhalt | Voraussetzung | Status |
| --- | --- | --- | --- |
| B1 V2 | Nur Ziel-, Identity- und effektive Privilege-Prüfung mit streambaren Query-Grenzen. | Neuer exakter B1-V2-Freigabetext. | NO-GO, Freigabe fehlt. |
| B2 | Nur einfache Katalog- und Strukturmetadaten. | B1 PASS, Review des B1-Raw-Outputs und neue B2-Freigabe. | BLOCKED. |
| B3 | Definitionen und daten-/workload-abgeleitete Statistiken. | B2 PASS, Sensitivitätsreview und neue B3-Freigabe. | DRAFT / BLOCKED. |

Keine Freigabe überträgt sich auf eine spätere Stufe. Jede Stufe verwendet eine
neue, separat genehmigte Sitzung und genau eine Verbindung.

## 3. Gate B1 – Identity und Privileges

Die ursprüngliche B1-Datei bleibt als historischer, nicht freigegebener Entwurf
erhalten:

Allowlist:
[00-identity-and-privilege-gate-b1.sql](sql/00-identity-and-privilege-gate-b1.sql)

SHA-256:
\`fb013e94827516cdee2ffd7bf6059c4ad000e04c6bb1e115073b89b6fc9aecb1\`

Der lokal getestete Launcher ist ausschließlich an die neue B1-V2-Datei
gebunden:

- Allowlist:
  [00-identity-and-privilege-gate-b1-v2.sql](sql/00-identity-and-privilege-gate-b1-v2.sql)
- SHA-256:
  \`0f586d02a663f9df543a7b7c1b8efde876c2b96d6079cd79e02c3a7359710317\`
- Launcher-SHA-256:
  \`638e4713370f7a2499e2543656334da97f1e245d3a8385d6914f0f137fbabf3d\`
- Stream-Guard-SHA-256:
  \`acfc52daf4773be1034d52f5bed1acd61f73a2ec6ae6768c872b86876406e190\`
- Gate-ID: \`DISCOVERY-GATE-B1-V2-2026-09-11\`
- Freigabestatus: \`NICHT ERTEILT\`

B1 V2 ändert keine SELECT-, Transaktions- oder Timeout-Semantik. Es ergänzt
nur launcher-generierte, tokengebundene \`BEGIN\`/\`END\`-Marker um jede der elf
Queries. Dadurch bleiben Query-Grenzen auch bei null Ergebniszeilen eindeutig.
Die folgende Allowlist und fail-closed Bewertung gilt inhaltlich unverändert
für B1 V2.

### Erlaubte Inhalte

- beobachteter Datenbankname ausschließlich im Restricted-Raw-Output;
- \`session_user\` und \`current_user\`;
- Serverversion, READ-ONLY- und Replikaflag;
- Rollenattribute beider Identitäten;
- vollständige direkte und geerbte Rollenpfade beider Identitäten;
- Datenbank-, Schema-, Relations-, Spalten-, Sequenz- und Routine-Ownership;
- effektive CREATE-, TEMP-, Tabellen- und Spalten-Write-Rechte;
- Sequenzrechte UPDATE und USAGE;
- ausführbare SECURITY-DEFINER-Routinen;
- angewandte Sessionlimits.

### Fail-closed Bewertung

| Query | PASS | STOP |
| --- | --- | --- |
| B1-001/002 | Alias/Fingerprint vor Verbindung passend; erwarteter Datenbankname und Identitäten passen. | Jede Abweichung oder fehlende lokale Attestation. |
| B1-003 | Beide Identitäten vorhanden; keine Admin-/BYPASSRLS-Flags. | SUPERUSER, CREATEROLE, CREATEDB, REPLICATION oder BYPASSRLS. |
| B1-004 | Null Rollenmitgliedschaften. | Jede direkte oder geerbte Rolle; sie gilt konservativ als möglicher Rollenwechsel. |
| B1-005 | Null Treffer. | Owner, CREATE oder TEMP. TEMP ist eindeutig STOP, keine Warnung. |
| B1-006 | Null Treffer. | Schema-Owner oder Schema-CREATE. |
| B1-007 | Null Treffer. | Relations-Owner oder Tabellen-Write-/TRIGGER-Recht. |
| B1-008 | Null Treffer. | Effektives Spaltenrecht INSERT oder UPDATE. |
| B1-009 | Null Treffer. | Sequenz-Owner, USAGE oder UPDATE. |
| B1-010 | Null Treffer. | Routine-Owner oder ausführbare SECURITY-DEFINER-Routine. |
| B1-011 | Ziel und Identität unverändert; Limits aktiv. | Abweichung, Rollenwechsel oder inaktives Limit. |

Jeder Treffer in B1-004 bis B1-010 ist STOP. Es gibt in Gate B1 kein
automatisches Akzeptieren vermeintlich harmloser Treffer. Eine Ausnahme braucht
eine neue Gate-Version und neue Nutzerfreigabe.

## 4. Gate B2 – einfache Strukturmetadaten

Allowlist:
[10-catalog-structure-gate-b2.sql](sql/10-catalog-structure-gate-b2.sql)

SHA-256:
\`88652862e75934b0348f0b1bdcd101eae318be3f1700df9c1efe9f73f0deac88\`

B2 ist nicht freigegeben. Nach B1 PASS müssen B1-Ergebnis, Zielbindung,
Dateihash, Größen und Stopstatus geprüft werden. Erst danach darf der Nutzer
einen eigenständigen B2-Freigabetext bestätigen.

B2 erlaubt ausschließlich:

- Schema-, Relations-, Spalten-, Constraint-, Index-, Trigger-, Routine-,
  Extension- und Publication-Namen;
- Datentypen und strukturelle Flags;
- PK/FK-/Constraint-Beziehungen über Metadaten;
- RLS-Enabled-/Forced-Flags und Anzahl Policies, keine Ausdrücke;
- Grantnamen und Grantflags;
- Größenklassen, keine exakten Größen;
- \`reltuples\` als geschätzte Zeilenzahl;
- Routine-Signaturen und Sicherheitsflags ohne Body;
- Index- und Triggerstatus ohne Definition.

B2 enthält ausdrücklich nicht:

- RLS-Ausdrücke;
- View-, Trigger- oder Indexdefinitionen;
- Enum-Labels;
- \`pg_stats\`, \`pg_stat_user_tables\` oder andere
  daten-/workload-abgeleitete Statistiken;
- Kandidatenzeilen oder Aggregate über Anwendungstabellen.

Erreicht irgendeine B2-Abfrage \`LIMIT 5001\`, ist das Inventar möglicherweise
unvollständig: sofortiger STOP, kein PASS und keine B3-Vorbereitung auf Basis
des unvollständigen Inventars.

## 5. Gate B3 – nicht freigegebener Entwurf

Entwurf:
[20-definitions-statistics-gate-b3-draft.sql](sql/20-definitions-statistics-gate-b3-draft.sql)

SHA-256 des aktuellen, **nicht freigegebenen** Entwurfs:
\`fa6e0e518d9e659b4c97ff9b58eb7891012897032acb44c35a3d758da518abff\`

| Querygruppe | Inhalt | Mögliche Sensitivität |
| --- | --- | --- |
| B3-001 | RLS-Ausdrücke | Literale, Rollenlogik, Tenant-Mechanismen, Spalten- und Funktionsnamen. |
| B3-002 | Viewdefinitionen | Literale, Joins, private Objektnamen und Geschäftslogik. |
| B3-003 | Triggerdefinitionen | Literalargumente, Routinenamen und Eventlogik. |
| B3-004 | Indexdefinitionen | Ausdrucksliterale, partielle Prädikate und Suchstruktur. |
| B3-005 | Enum-Labels | Internes Vokabular, Status- und Taxonomiewerte. |
| B3-006 | \`pg_stats\` ohne Wertarrays | Datenabgeleitete Sparsität, Selektivität, Breite und Korrelation. |
| B3-007 | \`pg_stat_user_tables\` | Workload, Wartungszeiten und approximative Live-/Dead-Zahlen. |
| B3-008 | Exakte Objektgrößen | Interne Skalierung, Wachstum und Datenkonzentration. |
| B3-009 | Policy-Rollen | Interne Autorisierungsstruktur. |

\`most_common_vals\`, \`most_common_freqs\`, \`histogram_bounds\`,
Kandidatenzeilen und Anwendungstabellen-Aggregate sind auch im B3-Entwurf nicht
enthalten. B3 benötigt vor jeder Ausführung einen neuen Sensitivitätsreview,
eine neue Hashprüfung und einen eigenen Freigabetext.

## 6. Exakter Ausführungsmechanismus

### Verbindungs- und Prozessgrenze

- Pro freigegebenem Gate genau ein lokaler \`psql\`-Prozess und genau eine
  Datenbankverbindung.
- Keine Parallelität, Wiederholung, automatische Retry-Logik oder Kombination
  von B1, B2 und B3.
- \`psql -X --no-psqlrc --no-password --quiet --set=ON_ERROR_STOP=on --csv
  --tuples-only\`; jeder SQL- oder Clientfehler beendet den Lauf.
- Jede SQL-Datei startet \`BEGIN TRANSACTION READ ONLY\`, setzt lokale Timeouts
  und endet mit \`ROLLBACK\`.
- Der lokale Connection Service entspricht dem Ziel-Alias. Credentials werden
  getrennt lokal bezogen und erscheinen in keinem Argument, Output oder Log.

Der weiterhin nicht freigegebene Launcher-Aufruf für B1 V2 besitzt keine freien
Ziel-, SQL- oder Raw-Pfadparameter. Zielwerte werden ausschließlich aus den
lokalen, nicht protokollierten Attest-, Connection-Service- und Credential-
Dateien bezogen. Der Restricted-Raw-Pfad ist fest vorgegeben:

\`\`\`bash
/Users/activi/Documents/ChatGPT/Dino\ problem\ baza\ crm/scripts/discovery/run-gate-b1.sh
\`\`\`

Der Launcher darf den Prozess nur starten, wenn:

- Zielattest und lokaler Connection Service bytegenau zum Alias gehören;
- der Connection Service genau einen Hostwert ohne Multi-Host-Liste enthält;
- der Host-/Projektfingerprint lokal übereinstimmt;
- der Restricted-Raw-Ordner außerhalb des Repositories neu ist und Modus
  \`0700\` hat;
- SQL-Datei, Launcher und Stream-Guard jeweils den im Freigabeattest gebundenen
  SHA-256 besitzen;
- der aktuelle Zeitstempel im freigegebenen Zeitfenster liegt;
- kein anderer Discovery-Prozess oder keine andere Verbindung aktiv ist.

Der in der Freigabe genannte B1-V2-Raw-Ordner muss unmittelbar vor dem Lauf neu
angelegt, auf Modus \`0700\` geprüft und nach dem Lauf unverändert als einziger
Restricted-Raw-Ausgabeort behandelt werden. Seine bloße Nennung autorisiert
weder seine Anlage noch den Lauf.

### Ausgabebegrenzung

| Grenze | B1 | B2 | B3-Entwurf |
| --- | --- | --- | --- |
| SQL-Zeilensentinel | \`LIMIT 5001\`; 5001 Treffer = STOP | Gleich | Gleich |
| Erlaubte Nutzzeilen | Höchstens 5000 je Query | Höchstens 5000 je Query | Höchstens 5000 je Query |
| Bytes je Query | 2 MiB | 5 MiB | 5 MiB |
| Gesamte Sitzung | 12 MiB | 40 MiB | 40 MiB |
| Verbindungen | 1 | 1 | 1 |
| Parallelität | 0 weitere | 0 weitere | 0 weitere |

Der lokale Launcher begrenzt den CSV-Stream anhand tokengebundener Query-Marker
während des Schreibens. Er prüft Reihenfolge, Query-ID, CSV-Grenzen, Query- und
Gesamtbytes sowie den 5001-Zeilensentinel. Beim Überschreiten einer Grenze
beendet er die Prozessgruppe und damit die einzige Verbindung, markiert STOP
und startet keinen Retry. Fehlende Marker oder ein nullzeiliger Abschnitt ohne
korrektes Marker-Paar sind ebenfalls STOP.

Die Launcher-Implementierung ist ausschließlich mit Fake-\`psql\` lokal
verifiziert. Zielattest, Connection Service, Credentialweg, echte
PostgreSQL-Kompatibilität und Freigabe fehlen weiterhin. Deshalb bleibt der
Gesamtstatus NO-GO.

### Ausgabe- und Retention-Regel

- Keine SQL-Ausgabe, Rollen-, Objekt-, Datenbank- oder Hostinformation im Chat.
- Restricted Raw ausschließlich außerhalb des Repositories in einem neuen
  Verzeichnis mit Modus \`0700\`.
- Kein \`tee\`, Clipboard, Terminal-Mitschnitt, Ticket, Prompt, Commit oder
  unredigierter Bericht.
- Restricted Raw maximal 24 Stunden nach Verbindungsende aufbewahren.
- Die Freigabe autorisiert keine unprotokollierte Löschung. Vor Ablauf muss eine
  dokumentierte lokale Löschfreigabe vorliegen; fehlt sie, darf die Verbindung
  gar nicht begonnen werden.
- Sanitized Artefakte dürfen erst nach Security-/Privacy-Review und eigener
  Dokumentationsfreigabe ins Repository.

## 7. Erlaubte PostgreSQL-Hilfsfunktionen

Nur die in der jeweils freigegebenen SQL-Datei wörtlich enthaltenen
\`pg_catalog\`-Hilfsfunktionen sind erlaubt.

### B1

- \`current_database\`, \`pg_is_in_recovery\`, \`current_setting\`;
- \`has_database_privilege\`, \`has_schema_privilege\`;
- \`has_table_privilege\`, \`has_column_privilege\`;
- \`has_sequence_privilege\`, \`has_function_privilege\`;
- \`pg_get_function_identity_arguments\`.

### B2

- \`current_database\`, \`current_setting\`, \`pg_get_userbyid\`, \`format_type\`;
- \`pg_total_relation_size\`, \`pg_relation_size\`;
- \`pg_get_function_identity_arguments\`, \`pg_get_function_result\`;
- Katalog-Aggregat \`count\` ausschließlich über \`pg_policy\`.

### B3-Entwurf

- \`current_database\`, \`current_setting\`, \`pg_get_expr\`, \`pg_get_viewdef\`;
- \`pg_get_triggerdef\`, \`pg_get_indexdef\`;
- \`pg_relation_size\`, \`pg_total_relation_size\`;
- \`unnest\` ausschließlich über \`pg_policy.polroles\`.

Anwendungsfunktionen, Supabase-RPCs, Triggerfunktionen, gespeicherte
Prozeduren, SECURITY-DEFINER-Ausführung und dynamisches SQL bleiben verboten.
Das Inventarisieren einer Signatur ist kein Funktionsaufruf.

## 8. Globale Stop-Kriterien

Jede Stufe stoppt fail-closed, wenn:

1. Gate-ID, Alias, Zeitfenster, Pfad, SHA-256 oder lokales Zielattest abweicht.
2. Host-/Projektfingerprint oder erwarteter Datenbankname nicht passt.
3. \`session_user\` und \`current_user\` abweichen oder sich während des Laufs
   ändern.
4. B1 einen Rollen-, TEMP-, Ownership-, Write-, Sequenz- oder kritischen
   Routinetreffer liefert.
5. READ ONLY, Fehlerabbruch oder ein Timeout nicht aktiv ist.
6. eine Abfrage, Funktion oder ein Identifier nicht wörtlich allowlistet ist.
7. eine Anwendungstabelle, Kandidatenzeile, ein RPC oder dynamisches SQL
   aufgerufen würde.
8. SQL-\`LIMIT 5001\`, Query-Bytegrenze oder Gesamtgrößenlimit erreicht wird.
9. mehr als eine Verbindung, Parallelität oder Retry entsteht.
10. Restricted Raw den \`0700\`-Ordner verlässt oder SQL-Ausgabe im Chat
    erscheinen würde.
11. Secret, URL, Credential, Kontakt, CV-Text, Geburtsdatum,
    Identifikationsnummer oder unerwarteter PII erscheint.
12. Retention und spätere Löschung vor Verbindungsbeginn nicht geklärt sind.
13. die vorherige Stufe nicht geprüft und ausdrücklich als PASS freigegeben ist.
14. der Nutzer die Freigabe widerruft oder der Scope sich ändert.

## 9. Pflichtfelder jedes späteren Freigabetextes

Jeder Gate-Freigabetext muss vollständig nennen:

- Gate-ID;
- Ziel-Alias;
- exaktes Zeitfenster;
- absolute Dateipfade;
- SHA-256 jeder freigegebenen SQL-Datei;
- erlaubte Inhalte;
- verbotene Inhalte;
- vollständige Stop-Kriterien;
- Retention-Regel.

Fehlt ein Feld oder ändert sich ein Hash, ist der Text unwirksam.

## 10. Status

| Prüfung | Status |
| --- | --- |
| Ziel-Alias definiert | PASS |
| Lokale Zielattestation spezifiziert | PASS_WITH_GAPS – noch nicht lokal geprüft |
| B1 V1 SQL erhalten | PASS – historischer Entwurf, nicht freigegeben |
| B1 V2 SQL entworfen | PASS – nur statisch und mit Fake-Protokoll getestet |
| B2 SQL getrennt und reduziert | PASS – nur statisch |
| B3 sensitiv klassifiziert | PASS – DRAFT, nicht freigegeben |
| Kontrollierter Launcher verifiziert | PASS_WITH_GAPS – ausschließlich Fake-\`psql\`, keine DB-Verbindung |
| Datenbankname und Host-/Projektkennung geprüft | SKIPPED – keine Verbindung erlaubt |
| SQL ausgeführt | SKIPPED – verboten |
| Gate B1 freigegeben | BLOCKED |
| Gate B2 freigegeben | BLOCKED |
| Gate B3 freigegeben | BLOCKED |

**Gesamtstatus: PASS_WITH_GAPS / NO-GO.**

## 11. Discovery-Artefaktliste

| Artefakt | Ort | Klassifikation | Gate-Status |
| --- | --- | --- | --- |
| Zielattest | Lokaler absoluter Pfad aus Abschnitt 1 | Restricted Config; nie kopieren oder ausgeben. | B1-Voraussetzung, nicht geprüft. |
| B1-V1-Allowlist | Historischer Repository-Pfad und SHA-256 aus Abschnitt 3 | Reviewable SQL; keine Ergebnisdaten. | Historischer Entwurf, nicht freigegeben. |
| B1-V2-Allowlist | Aktueller Repository-Pfad und SHA-256 aus Abschnitt 3 | Reviewable SQL mit Query-Markern; keine Ergebnisdaten. | Entwurf, nicht freigegeben. |
| B1-V2-Raw-Ausgabe | Absoluter externer Pfad aus Abschnitt 6 | Restricted Raw; Modus \`0700\`, maximal 24 Stunden. | Darf in dieser Sitzung nicht entstehen. |
| B1-Laufmanifest | Neben B1-Raw-Ausgabe, ohne Zielwerte oder Resultset-Inhalte | Restricted Metadata; Gate-ID, Alias, Zeiten, SQL-Hash, Byte-/Zeilenzähler und STOP/PASS. | Launcher lokal mit Fake-`psql` verifiziert; reales Manifest darf ohne Freigabe nicht entstehen. |
| B2-Allowlist | Repository-Pfad und SHA-256 aus Abschnitt 4 | Reviewable SQL; keine Ergebnisdaten. | BLOCKED. |
| B2-Raw-Ausgabe und Manifest | Erst in eigenem B2-Freigabetext exakt festzulegen | Restricted Raw/Metadata. | Nicht freigegeben. |
| B3-Entwurf | Repository-Pfad und SHA-256 aus Abschnitt 5 | Sensitiver SQL-Entwurf; mögliche Literale/interne Informationen. | DRAFT / BLOCKED. |
| B3-Raw-Ausgabe und Manifest | Erst in eigenem B3-Freigabetext exakt festzulegen | Restricted Raw/Metadata mit erhöhtem Sensitivitätsrisiko. | Nicht freigegeben. |
| Sanitized Review | Noch kein Pfad | Nur nach Security-/Privacy-Review und separater Schreibfreigabe. | Nicht freigegeben. |

## 12. Zugehörige Dokumente

- [Änderungsmatrix A zu B](gate-b-change-matrix.md)
- [Historischer, nicht erteilter B1-Freigabetext](gate-b1-approval-text.md)
- [Exakter, nicht erteilter B1-V2-Freigabetext](gate-b1-v2-approval-text.md)
- [Append-only Arbeitsbericht](../worklogs/2026-09-11-security-read-only-discovery-gate.md)
