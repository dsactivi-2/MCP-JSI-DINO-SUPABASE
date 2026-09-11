# Append-only Arbeitsbericht: Security- und Read-only-Discovery-Gate

Regel: Bestehende Einträge werden nicht geändert oder entfernt. Korrekturen
werden als neuer Eintrag mit Verweis auf den betroffenen Eintrag angehängt.

## Sitzungsprotokoll

### [2026-09-11T02:50:42+02:00] Phase 0 – Orientierung und Evidenzbasis

- Intent: Projekt aktivieren, Pflichtdokumente und Skill-Regeln vollständig
  lesen, ohne Datenbank- oder externe Schreibzugriffe.
- Aktionen:
  - Serena-Anleitung gelesen und bestehendes Projekt aktiviert.
  - Serena-Memory \`core\` gelesen.
  - \`/wayfinder\` im verfügbaren Skill-Katalog nicht gefunden.
  - Fallback-Skills \`grilling\`, \`domain-modeling\` und
    \`file-driven-multi-session-supervision\` vollständig gelesen.
  - Alle zehn vom Nutzer genannten Projektdateien vollständig gelesen.
- Evidenz:
  - Aktives Serena-Projekt:
    \`/Users/activi/Documents/ChatGPT/Dino problem baza crm\`.
  - Pflichtlektüre umfasst AGENTS.md, Projektstatus, CONTEXT, Brief, drei ADRs,
    Discovery-Runbook, historischen Audit und Korrekturmatrix.
- Ergebnis: Der korrigierte Stand trennt bestätigte Entscheidungen,
  Vorschläge, Annahmen und offene Punkte. Q4.5 und Q8.5 bleiben offen.
- Assessment: \`PASS\`
- Nächste Aktion: Tatsächlichen Git-Arbeitsbaum und Diff read-only prüfen.

### [2026-09-11T02:52:36+02:00] Phase 1 – Git- und Korrekturprüfung

- Intent: Aktuellen Arbeitsbaum gegen die Korrekturmatrix prüfen.
- Aktionen:
  - Git-Status, unstaged Diff und staged Diff über den globalen Git-MCP gelesen.
  - README und lokale Regeln für Domänendokumentation gelesen.
  - Keine Datei gestaged, committed, gepusht, gelöscht oder zurückgesetzt.
- Evidenz:
  - Branch \`main\`.
  - Vier getrackte Dateien geändert: AGENTS.md, Implementierungsbrief,
    ADR-0001 und Projektstatus.
  - Governance-Dokumente einschließlich CONTEXT, README, ADR-0002, ADR-0003,
    Research und Reviews sind unversioniert.
  - Staged Diff ist leer.
  - Inhaltliche Korrekturen entsprechen den zentralen F1-F9-Grenzen:
    Q8.5 offen, Q8.4-Grundsatz erhalten, Release 1 kontaktfrei,
    Bestätigungsablauf und Operatoren vorläufig, physische Fakten ungeprüft.
- Ergebnis: Kein neuer inhaltlicher Widerspruch in den geprüften Grenzen
  festgestellt. Der historische Audit bleibt korrekt als früheres FAIL
  gekennzeichnet; die Korrekturmatrix meldet PASS_WITH_GAPS.
- Assessment: \`PASS_WITH_GAPS\`
- Nächste Aktion: Entscheidungskarte und Discovery-Gate entwerfen.

### [2026-09-11T02:52:36+02:00] Phase 2 – Entscheidungskarte

- Intent: Abhängigkeiten des Gesamtprojekts sichtbar machen, ohne offene
  Nutzerentscheidungen zu schließen.
- Aktionen:
  - \`docs/discovery/project-decision-map.md\` neu angelegt.
  - Fakten, akzeptierte Entscheidungen, Vorschläge, Annahmen, offene Punkte und
    Gates getrennt.
  - Kritischen Pfad von Governance über Discovery bis Rollout abgebildet.
- Evidenz:
  - Q4.5 und Q8.5 bleiben explizit offen.
  - Profilverwaltungs-MCP und Runtime-Such-MCP bleiben getrennt.
  - Kontaktphase bleibt außerhalb von Release 1.
- Ergebnis: Abhängige Entscheidungskarte liegt als nicht normatives
  Arbeitsdokument vor.
- Assessment: \`PASS\`
- Nächste Aktion: Exakte SQL-Allowlist, Stop-Kriterien, Ausgaberichtlinie und
  Artefaktliste erstellen.

### [2026-09-11T02:52:36+02:00] Phase 3 – Discovery-Gate-Entwurf

- Intent: Den ersten Blocker vollständig für eine getrennte Freigabesitzung
  vorbereiten.
- Aktionen:
  - Offizielle PostgreSQL-Dokumentation zu READ ONLY, Katalogen, RLS-Policies
    und Privilegiensichten read-only geprüft.
  - Identity-/Privilege-Allowlist mit acht festen Query-IDs erstellt.
  - Metadaten-Allowlist mit sechzehn festen Query-IDs erstellt.
  - Preflight mit Rollenprofil, Scope, Stop-Kriterien, Ausgaberichtlinie,
    Artefaktliste, Ablauf und Freigabepunkt erstellt.
- Evidenz:
  - \`docs/discovery/sql/00-identity-and-privilege-gate.sql\`
  - \`docs/discovery/sql/10-metadata-inventory.sql\`
  - \`docs/discovery/security-read-only-discovery-preflight.md\`
- Ergebnis: Nur Katalogmetadaten sind vorgeschlagen. Kandidatenzeilen,
  Fachdatenaggregate, Funktionen, RPCs, EXPLAIN ANALYZE und Mutationen sind
  ausdrücklich nicht allowlistet.
- Assessment: \`PASS_WITH_GAPS\`
- Nächste Aktion: Lokale Syntax-, Link-, Markdown- und Git-Diff-Prüfungen
  ausführen; keine SQL-Ausführung.

### [2026-09-11T02:58:27+02:00] Phase 4 – Markdown-Strukturkorrektur

- Intent: Den einzigen Befund des ersten Markdown-Lint-Laufs beheben.
- Aktionen:
  - Vor den unveränderten Protokolleinträgen die Sammelüberschrift
    \`Sitzungsprotokoll\` ergänzt.
  - Keinen bestehenden Eintrag geändert oder entfernt.
- Evidenz:
  - Erster Lint-Lauf: ein MD001-Befund in Zeile 6; Ebene 3 ohne
    vorangehende Ebene 2.
- Ergebnis: Struktureller Container ergänzt; erneute Prüfung steht aus.
- Assessment: \`PASS_WITH_GAPS\`
- Nächste Aktion: Gesamte lokale Verifikation erneut ausführen.

### [2026-09-11T03:00:02+02:00] Phase 5 – Verifikation und Übergabe

- Intent: Dokumentation, Links, Allowlist-Struktur, Entscheidungsgrenzen und
  Git-Arbeitsbaum frisch prüfen.
- Aktionen:
  - Markdown-Lint über Root und \`docs/**/*.md\` ausgeführt.
  - 25 Markdown-Dateien und 201 relative Links einschließlich Fragmenten geprüft.
  - SQL-Dateien statisch in Statements zerlegt und auf erlaubte
    Statement-Anfänge, READ ONLY, ROLLBACK, Query-ID-Anzahl und verbotene
    DDL-/DML-Tokens geprüft.
  - Neun kritische Entscheidungsgrenzen automatisiert geprüft.
  - \`rtk git diff --check\`, \`rtk git status --short\` und
    \`rtk git diff --stat\` ausgeführt.
  - SHA-256 der beiden SQL-Allowlist-Dateien ermittelt.
- Evidenz:
  - Markdown-Lint: \`PASS\`, 19 Dateien, null Befunde.
  - Relative Links: \`PASS\`, 201 Links, null Fehler.
  - SQL-Struktur: \`PASS\`; Gate-Datei 14 Statements und 8 Query-IDs,
    Metadaten-Datei 23 Statements und 16 Query-IDs; keine verbotenen
    Statement-Anfänge oder DDL-/DML-Tokens außerhalb von Kommentaren/Stringwerten.
  - Entscheidungsgrenzen: \`PASS\`, neun Prüfungen, null fehlend.
  - \`git diff --check\`: \`PASS\`, keine Ausgabe.
  - Getrackter Diff: vier Dateien, 344 Einfügungen und 83 Entfernungen.
  - Nichts gestaged; neue Discovery- und Worklog-Verzeichnisse sind unversioniert.
  - SHA-256 Gate:
    \`291bda2bac355ea298766b2f9b9410589be662e3dd30140e5da9923ff39250b9\`.
  - SHA-256 Metadaten:
    \`ad3ce70c457ee37501944d05a268e3f7e6da7b241eb8edeaef79226f5795a84f\`.
- Ergebnis: Dokumentations- und statische Allowlist-Prüfungen sind grün. SQL
  wurde nicht gegen einen PostgreSQL-Parser oder Server validiert und nicht
  ausgeführt; Versionskompatibilität und tatsächliche Rechte bleiben
  absichtlich Teil der getrennten Discovery-Sitzung.
- Assessment: \`PASS_WITH_GAPS\`
- Nächste Aktion: Auf ausdrückliche Nutzerfreigabe von
  \`DISCOVERY-GATE-2026-09-11-A\` warten. Datenbankzugriff erst in einer
  getrennten Sitzung.

### [2026-09-11T03:19:51+02:00] Phase 6 – Gate-Version B

- Intent: Den weiterhin mit \`NO-GO\` bewerteten Discovery-Preflight in drei
  getrennt freizugebende Stufen überführen.
- Aktionen:
  - Nicht geheimen Ziel-Alias \`dino_crm_discovery_target_01\` festgelegt und
    lokale Zielattestierung für erwarteten Datenbanknamen sowie normalisierten
    Host-/Projektkennungs-Hash spezifiziert.
  - Gate B1 auf Identity-/Privilege-Prüfungen begrenzt und um beide
    PostgreSQL-Identitäten, Rollenwechsel, vollständige Rollenvererbung,
    Spaltenrechte, Sequenzrechte/-Ownership und eindeutige TEMP-Behandlung
    erweitert.
  - Gate B2 auf einfache Katalog- und Strukturmetadaten begrenzt.
  - Definitionen, Enum-Labels und datenabgeleitete Statistiken in einen nicht
    freigegebenen Gate-B3-Entwurf verschoben und nach Sensitivitätsrisiko
    gekennzeichnet.
  - Ein-Verbindungs-Mechanismus, Fehlerabbruch, externe Restricted-Raw-Ablage,
    Byte-/Zeilenlimits, LIMIT-Stop, Retention und Pflichtfelder späterer
    Freigabetexte dokumentiert.
  - Exakten, noch nicht erteilten Freigabetext ausschließlich für Gate B1
    erstellt.
- Evidenz:
  - \`docs/discovery/security-read-only-discovery-preflight-b.md\`
  - \`docs/discovery/gate-b-change-matrix.md\`
  - \`docs/discovery/gate-b1-approval-text.md\`
  - \`docs/discovery/sql/00-identity-and-privilege-gate-b1.sql\`
  - \`docs/discovery/sql/10-catalog-structure-gate-b2.sql\`
  - \`docs/discovery/sql/20-definitions-statistics-gate-b3-draft.sql\`
- Ergebnis: Gate B ist dokumentarisch vorbereitet. B1, B2 und B3 sind nicht
  freigegeben; die Ausführungsumgebung und der begrenzende Launcher sind noch
  nicht lokal attestiert beziehungsweise verifiziert.
- Assessment: \`PASS_WITH_GAPS / NO-GO\`
- Nächste Aktion: Ausschließlich statische Dokument-, SQL-Allowlist-, Link-,
  Hash- und Git-Diff-Prüfungen ausführen.

### [2026-09-11T03:26:10+02:00] Phase 7 – Statische Gate-B-Verifikation

- Intent: Gate B ohne Datenbankverbindung und ohne SQL-Ausführung gegen die
  dokumentierten Sicherheits- und Vollständigkeitsgrenzen prüfen.
- Aktionen:
  - Alle erlaubten PostgreSQL-Hilfsfunktionsaufrufe in den B-SQL-Dateien
    explizit mit \`pg_catalog\` qualifiziert; die dadurch geänderten Hashes in
    Preflight und B1-Freigabetext neu gebunden.
  - Den B1-Freigabetext mit wörtlichen Pflichtfeldnamen und festen externen
    Restricted-Raw-Pfaden präzisiert; interaktive Passwortabfrage verboten.
  - Die Discovery-Artefaktliste um Zielattest, Raw-Ausgaben, Laufmanifeste,
    Allowlists und Sanitized Review ergänzt.
  - Markdown-Lint, relative Linkprüfung, statische SQL-Statement- und
    Gate-Invariantenprüfung, Hilfsfunktionsprüfung und \`git diff --check\`
    ausgeführt.
  - Ein erster Ad-hoc-Checker-Lauf meldete fünf False Positives wegen einer
    unzutreffenden Query-ID-Regel und abweichender Überschriftenbegriffe; die
    Prüfregel wurde korrigiert. Daraus wurde kein SQL- oder Datenbanklauf.
- Evidenz:
  - Markdown-Lint: \`PASS\`, 22 Dateien, null Befunde.
  - Relative Links: \`PASS\`, 22 Dateien, 213 relative Links, null Fehler.
  - SQL-Textprüfung: \`PASS\`, 11 B1-, 14 B2- und 10 B3-Query-IDs;
    nur BEGIN/SET/SELECT/WITH/ROLLBACK als Statement-Anfänge.
  - Gate-Invarianten: \`PASS\`; B2 enthält keine verschobenen Definitionen,
    Enum-Labels oder Statistikquellen, B3 enthält die vorgesehenen Entwürfe.
  - Unqualifizierte geprüfte Hilfsfunktionsaufrufe: null Treffer.
  - \`git diff --check\`: \`PASS\`, keine Ausgabe. Unversionierte Dateien
    werden davon nicht erfasst und wurden zusätzlich durch Markdown-, Link-,
    Hash- und statische SQL-Prüfungen abgedeckt.
  - B1 SHA-256:
    \`fb013e94827516cdee2ffd7bf6059c4ad000e04c6bb1e115073b89b6fc9aecb1\`.
  - B2 SHA-256:
    \`88652862e75934b0348f0b1bdcd101eae318be3f1700df9c1efe9f73f0deac88\`.
  - B3-Entwurf SHA-256:
    \`fa6e0e518d9e659b4c97ff9b58eb7891012897032acb44c35a3d758da518abff\`.
- Ergebnis: Die statisch prüfbaren Gate-B-Dokumente sind konsistent. Keine
  PostgreSQL-Parser-/Servervalidierung, lokale Zielattestation,
  Launcher-Verifikation oder Ergebnisprüfung wurde durchgeführt.
- Assessment: \`PASS_WITH_GAPS / NO-GO\`
- Nächste Aktion: NO-GO beibehalten. Gate B1 darf erst in einer getrennten
  Sitzung nach Schließen der lokalen Preflight-Gaps und ausdrücklicher
  Bestätigung des hashgebundenen B1-Freigabetextes beginnen.

### [2026-09-11T04:20:41+02:00] Phase 8 – Lokaler B1-V2-Launcher mit Fake-psql

- Intent: Die lokale Launcher-Lücke test-first schließen, ohne Zielattest,
  Connection Service, Credentials, Netzwerk, Datenbankverbindung oder
  PostgreSQL-Ausführung zu verwenden.
- Aktionen:
  - Matt-Skill \`/tdd\` einschließlich Test- und Mocking-Referenzen gelesen;
    öffentlicher Seam ist die Launcher-CLI, Fake-\`psql\` die Systemgrenze.
  - Fail-closed Bash-Launcher und Python-Stream-Guard implementiert.
  - B1 V2 mit tokengebundenen Query-Markern ergänzt; ursprüngliche B1-SQL und
    ihr nicht erteilter Freigabetext unverändert als historische Entwürfe
    erhalten.
  - Fake-\`psql\`-Tests für Hash, Alias, Attestmodus, Symlink, Owner,
    Ziel-Fingerprint, unbekannte Konfigurationsfelder, eingebettetes Passwort,
    Raw-Pfad, Zeitfenster, Lock, SQL-/Clientfehler, Timeout, Query-/Gesamtbytes,
    Sentinel 5001, null Ergebniszeilen, No-Retry und Output-Minimierung erstellt.
  - Preflight, Änderungsmatrix, Entscheidungskarte, README und neuen weiterhin
    nicht erteilten B1-V2-Freigabetext konsistent fortgeschrieben.
- Evidenz:
  - B1-V2-SQL SHA-256:
    \`e63a5eea418f48b1d912d2777b0e27fd9ca93a71980bd5dd8eeff56e970f7223\`.
  - Launcher SHA-256:
    \`28fb3e4251e6ae45447c5ed570b1b0b02bf8e38948b7efc81ebec7d122fdc812\`.
  - Stream-Guard SHA-256:
    \`fb6713fe56dc5b4f165f0893c964c683155df06792329bce2dd0df94f0be77f0\`.
  - Launcher-Testmatrix: \`PASS\`, neun Gruppen, kein Retry und keine Ausgabe
    synthetischer Raw-Werte.
  - Statische B1-V2-SQL-/Dokumentprüfung: \`PASS\`.
  - Bash-Syntax: \`PASS\`.
  - Markdown-Lint: \`PASS\`, 23 Dateien, null Befunde.
  - Relative Links: \`PASS\`, 218 lokale Verweise.
- Ergebnis: Die lokal testbaren Launcher-Grenzen sind umgesetzt. Es erfolgte
  kein Aufruf eines realen \`psql\`, kein DNS-/Netzwerkzugriff und keine
  Datenbankverbindung oder SQL-Ausführung gegen PostgreSQL.
- Gaps: \`shellcheck\`, \`shfmt\`, \`sqlfluff\`, \`pg_format\` und ein
  PostgreSQL-Parser sind lokal nicht verfügbar. Zielattest, Freigabeattest,
  Connection Service, Credentialweg, Raw-Retention/Löschmechanismus und reale
  PostgreSQL-Kompatibilität sind nicht eingerichtet oder geprüft.
- Assessment: \`PASS_WITH_GAPS / NO-GO\`
- Nächste Aktion: Separaten, geheimnisfreien Handoff für eine spätere Sitzung
  erstellen. B1 V2 bleibt bis zu neuem Setup-Auftrag und ausdrücklicher
  hashgebundener Freigabe vollständig gesperrt.

### [2026-09-11T04:22:29+02:00] Phase 9 – Abschlussverifikation und Handoff

- Intent: Lokale Vorbereitungsphase ohne Datenbankzugriff abschließen und den
  nächsten Freigabepunkt eindeutig dokumentieren.
- Aktionen:
  - Matt-Skill \`/handoff\` vollständig gelesen.
  - Geheimnisfreien Folgesitzungs-Handoff unter
    \`/private/tmp/supabase-crm-gate-b1-v2-execution-handoff.md\` erstellt.
  - Launcher-Matrix, statische Gate-Prüfung, relative Links, Bash-Syntax,
    Markdown-Lint, Artefakthashes, \`git diff --check\` und Git-Status frisch
    ausgeführt.
- Evidenz:
  - Alle ausführbaren lokalen Prüfungen: \`PASS\`.
  - 23 Markdown-Dateien ohne Lintbefund; 218 relative Links ohne Fehler.
  - Keine Python-Cacheverzeichnisse unter \`scripts/\` oder \`tests/\`.
  - Staged Diff weiterhin leer; bestehender Dirty Worktree erhalten.
- Ergebnis: Lokaler Launcher-Preflight abgeschlossen; keine Datenbankverbindung,
  kein echter \`psql\`-Aufruf, kein SQL gegen PostgreSQL und kein externer Write.
- Assessment: \`PASS_WITH_GAPS / NO-GO\`
- Nächster Freigabepunkt: Erst separater Nutzerauftrag für lokale Setup-Schritte,
  danach neue ausdrückliche Bestätigung des vollständigen B1-V2-Freigabetexts.

### [2026-09-11T04:57:34+02:00] Phase 10 – Review-Korrekturlauf mit TDD

- Intent: Alle Befunde des Launcher-Reviews ohne Datenbankzugriff test-first
  korrigieren und den zukünftigen Commit aus einem sauberen Git-Index-Export
  verifizieren.
- RED-Evidenz:
  - Ein semantischer Rollen-Finding-Row endete fälschlich mit Erfolg.
  - Realistische `psql`-Statuszeilen verursachten einen Protokollfehler.
  - Multi-Host wurde akzeptiert und ein falscher Launcher-Hash nicht passend
    erkannt.
  - Ein unerwarteter I/O-Fehler ließ den Fake-`psql`-Prozess weiterlaufen.
  - Der versionierte Preflight verlinkte ein unversioniertes Ziel und bezeichnete
    den vorhandenen Launcher widersprüchlich als fehlend.
- Korrekturen:
  - Finding-Queries `SQL-GATE-B1-003` bis `SQL-GATE-B1-010` stoppen bei jeder
    Ergebniszeile; Query 003 liefert nur administrative Rollenbefunde.
  - `psql` läuft mit `--quiet`; unerwartete Fehler beenden die Prozessgruppe.
  - Multi-Host-Listen sind verboten. Freigabeattest, tatsächlicher Launcher und
    Stream-Guard werden hashgebunden verglichen.
  - Doppelte Konfigurations-Leselogik wurde zusammengeführt.
  - Linkprüfung arbeitet gegen den Git-Index; die Lint-Konfiguration ist Teil des
    vorgesehenen Commits.
- Neue SHA-256-Werte:
  - B1-V2-SQL:
    `0f586d02a663f9df543a7b7c1b8efde876c2b96d6079cd79e02c3a7359710317`.
  - Launcher:
    `638e4713370f7a2499e2543656334da97f1e245d3a8385d6914f0f137fbabf3d`.
  - Stream-Guard:
    `acfc52daf4773be1034d52f5bed1acd61f73a2ec6ae6768c872b86876406e190`.
- Sauberer Index-Export unter `/private/tmp`: 13 Launcher-Gruppen, separater
  I/O-Test, statische Gate-Prüfung, 39 versionierte Links, Bash-Syntax und
  Markdownlint bestanden.
- Sicherheitsgrenze: Kein reales `psql`, kein Netzwerk, keine
  Datenbankverbindung und kein SQL gegen PostgreSQL.
- Assessment: `PASS_WITH_GAPS / NO-GO`; Freigabestatus bleibt `NICHT ERTEILT`.

### [2026-09-11T05:14:07+02:00] Phase 11 – Review-Follow-up mit TDD

- Intent: Die Befunde des ersten Matt-`/code-review` test-first schließen und
  den exakten Korrekturstand in einem echten sauberen Git-Checkout prüfen.
- RED-Evidenz:
  - SIGTERM ließ die gestartete Fake-`psql`-Prozessgruppe weiterlaufen.
  - Ein Fehler bei der Selector-Initialisierung ließ Fake-`psql` weiterlaufen.
  - Fehlende Service-Werte meldeten eine Attestationsdiagnose.
  - Der Preflight behauptete trotz geänderter Query-003-Semantik, dass keine
    SELECT-Semantik geändert wurde.
- Korrekturen:
  - Der Stream-Guard installiert lokale Handler für SIGINT, SIGTERM und SIGHUP;
    Initialisierung, Protokolllauf und Cleanup teilen einen Fail-Closed-Pfad.
  - Konfigurationsdiagnosen unterscheiden Attestation und Connection Service.
  - Fake-`psql` deckt Findings für Queries 003 bis 010 einzeln ab; duplizierte
    Protokoll-Fixtures wurden zusammengeführt.
  - Die Markdownlint-Ausnahme wurde vom Repository-Root in eine ausschließlich
    für die Gate-B-Prüfung angegebene Testkonfiguration verschoben.
- Finale SHA-256-Werte:
  - B1-V2-SQL:
    `0f586d02a663f9df543a7b7c1b8efde876c2b96d6079cd79e02c3a7359710317`.
  - Launcher:
    `735dd6e5ad63ec6e211b0df027dea19286181060f50ceda64d80f1c51f15dce7`.
  - Stream-Guard:
    `c7628f48c5487202d0db3279753030be73a749664fb45b4e0f03103777158b7c`.
- Sauberer Checkout: Lokaler Clone unter
  `/private/tmp/gate-b1-clean-clone.rMc0TP/repo`; 14 Launcher-Gruppen,
  I/O-, Signal- und Selector-Cleanup, statische Gate-Prüfung, 39 versionierte
  Links, Bash-Syntax, Markdownlint und `git diff --check` bestanden.
  `git status --short` blieb nach den Tests leer.
- Sicherheitsgrenze: Kein reales `psql`, kein Netzwerk, keine
  Datenbankverbindung und kein SQL gegen PostgreSQL.
- Assessment: `PASS_WITH_GAPS / NO-GO`; Freigabestatus bleibt `NICHT ERTEILT`.

### [2026-09-11T05:25:41+02:00] Phase 12 – Signal-Race-Review-Follow-up

- Intent: Den verbliebenen harten Standards-Befund des Matt-`/code-review`
  test-first schließen und den Test-Harness ohne Verhaltensänderung bündeln.
- Review-Ausgang: Spec-Achse `PASS` mit null Befunden; Standards-Achse `FAIL`
  wegen eines Signals im `Popen`-Zuweisungsfenster, eines zweiten Signals
  während Cleanup und dupliziertem Python-Test-Harness.
- RED-Evidenz:
  - Ein deterministisches SIGTERM zwischen Child-Start und `Popen`-Zuweisung
    ließ Fake-`psql` weiterlaufen.
  - Nach dessen Minimalfix ließ ein deterministisches zweites SIGTERM während
    Cleanup Fake-`psql` weiterlaufen.
- Korrekturen:
  - Signale im Spawn-Fenster werden vorgemerkt und unmittelbar nach sicherer
    Prozesszuweisung als `launcher_interrupted` verarbeitet.
  - Während Child-Terminierung und Selector-Cleanup bleibt der Guard aktiv;
    frühere Signalhandler werden erst danach wiederhergestellt.
  - Gemeinsame Guard-Argumente, Umgebung, Import- und Prozess-Wartehilfen liegen
    in `tests/discovery/gate_b1_test_support.py`.
- Finale SHA-256-Werte:
  - B1-V2-SQL:
    `0f586d02a663f9df543a7b7c1b8efde876c2b96d6079cd79e02c3a7359710317`.
  - Launcher:
    `fdceaa1503d01c0149ac12062a9a19cf90b5997fcf04ca14614533da672b0690`.
  - Stream-Guard:
    `b3c4fbe8053641ef93e70c126dbc7e5fe10892af3cc41743e5c7c9c0ce5252b7`.
- Sauberer Checkout: Lokaler Clone unter
  `/private/tmp/gate-b1-race-clean-clone.HrAms7/repo`; 14 Launcher-Gruppen,
  fünf Guard-/Cleanup-Prüfungen einschließlich beider Signal-Races, statische
  Gate-Prüfung, 39 Links, Bash-Syntax, Markdownlint und `git diff --check`
  bestanden. `git status --short` blieb nach den Tests leer.
- Sicherheitsgrenze: Kein reales `psql`, kein Netzwerk, keine
  Datenbankverbindung und kein SQL gegen PostgreSQL.
- Assessment: `PASS_WITH_GAPS / NO-GO`; Freigabestatus bleibt `NICHT ERTEILT`.

### [2026-09-11T08:44:33+02:00] Phase 13 – Supabase-Plugin- und Skills-Integration

- Intent: Die installierten Supabase-Plugin-Distributionen und beide
  projektlokalen Skills bewerten und ihre sichere Nutzung in Governance,
  Discovery-Planung und Aktualisierungsablauf verankern.
- Befunde:
  - Beide Skill-Verzeichnisse sind vollständig und stimmen mit der vorhandenen
    Community-Distribution überein; sie helfen sofort bei Planung und statischem
    Review, stellen aber keine Datenbankverbindung und keine Evidenz dar.
  - Zwei installierte Plugin-Distributionen verwenden denselben Supabase
    app/MCP. Sie schaffen keine getrennten Identitäten oder Trust Boundaries.
  - Die aktive Verbindung ist nicht auf das CRM-Projekt begrenzt; read-only und
    minimale Feature-Gruppen sind nicht attestiert. Live-Zugriffe bleiben daher
    blockiert.
  - Gate B bleibt an den geprüften lokalen `psql`-Launcher gebunden. Ein
    Supabase-MCP-Pfad benötigt eine eigene Gate-Version und Freigabe.
- Änderungen:
  - Verbindliche Agentenregeln, Projektstatus, Discovery-Runbook, Gate-B-
    Preflight, Implementierungsbrief und Entscheidungskarte wurden um diese
    Trennung ergänzt.
  - `docs/agents/supabase-tooling.md` dokumentiert Routing, MCP-Gate und den
    reproduzierbaren Skills-Updateablauf.
  - Die beiden Rechercheberichte dokumentieren Installationsstand, Nutzen,
    Grenzen und aktuelle Vendor-Signale.
  - `.gitignore` schließt lokale Environment- und `pgpass`-Dateien aus; es wurde
    keine MCP-Verbindungskonfiguration in das Repository geschrieben.
- Evidenz:
  - Relative Markdown-Links: `PASS`, 39 Links.
  - Gate-B1-V2-Statikprüfung: `PASS`.
  - Geänderte Zieldokumente mit der bestehenden Gate-B-Stilkonfiguration:
    `PASS`, 10 Dateien und null Befunde.
  - `git diff --check`: `PASS`.
  - Die diagnostische Standardprüfung des gesamten Repositories meldet 431
    MD013-/MD060-Stilbefunde in 14 Dateien, weil die beabsichtigten Regeln für
    Zeilenlänge und Tabellen nicht als allgemeines Projektprofil konfiguriert
    sind. Es existiert bewusst kein allgemeines `.markdownlint.json`; die README
    benennt diese Lücke jetzt korrekt.
- Sicherheitsgrenze: Keine Tabellen-, Schema-, Kandidaten-, Kontakt- oder
  CV-Daten gelesen; kein SQL, keine Migration, kein Deployment und keine
  externe Berechtigung geändert.
- Assessment: `PASS_WITH_GAPS / NO-GO`; Skills sind freigegeben für Planung und
  Review, Live-Plugin-Zugriffe bleiben `BLOCKED`.
