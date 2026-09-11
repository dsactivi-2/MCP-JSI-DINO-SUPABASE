# Exakter Freigabetext für Gate B1 V2

Status: **NICHT ERTEILT**

Dieser Text ist ausschließlich für eine neue, getrennte Sitzung bestimmt. Seine
Ablage im Repository ist keine Freigabe. Die frühere B1-Fassung und ihr
Freigabetext bleiben historische, nicht erteilte Entwürfe.

## Zu bestätigender Wortlaut

> Gate-ID: \`DISCOVERY-GATE-B1-V2-2026-09-11\`.
>
> Ziel-Alias: \`dino_crm_discovery_target_01\`.
>
> Ich erteile ausschließlich für dieses Gate B1 die nachstehend begrenzte
> Freigabe.
>
> Zeitfenster: Es beginnt mit dem Zeitstempel dieser Freigabenachricht in der
> getrennten Sitzung und endet exakt 30 Minuten später. Es erlaubt genau einen
> Verbindungsversuch, einen lokalen \`psql\`-Prozess und eine
> Datenbankverbindung; keine Parallelität und keinen Retry.
>
> Dateipfade:
>
> - Preflight:
>   \`/Users/activi/Documents/ChatGPT/Dino problem baza crm/docs/discovery/security-read-only-discovery-preflight-b.md\`
> - SQL:
>   \`/Users/activi/Documents/ChatGPT/Dino problem baza crm/docs/discovery/sql/00-identity-and-privilege-gate-b1-v2.sql\`
> - Launcher:
>   \`/Users/activi/Documents/ChatGPT/Dino problem baza crm/scripts/discovery/run-gate-b1.sh\`
> - Stream-Guard:
>   \`/Users/activi/Documents/ChatGPT/Dino problem baza crm/scripts/discovery/gate_b1_stream_guard.py\`
> - Lokales Zielattest:
>   \`/Users/activi/Library/Application Support/Activi/discovery-targets/dino_crm_discovery_target_01.target\`
> - Lokales Freigabeattest:
>   \`/Users/activi/Library/Application Support/Activi/discovery-targets/dino_crm_discovery_target_01.approval\`
> - Lokaler Connection Service:
>   \`/Users/activi/Library/Application Support/Activi/discovery-targets/dino_crm_discovery_target_01.pg_service.conf\`
> - Lokale Credential-Datei:
>   \`/Users/activi/Library/Application Support/Activi/discovery-targets/dino_crm_discovery_target_01.pgpass\`
> - Restricted-Raw-Verzeichnis:
>   \`/Users/activi/Library/Application Support/Activi/discovery-raw/dino_crm_discovery_target_01/DISCOVERY-GATE-B1-V2-2026-09-11\`
> - Restricted-Raw-Ausgabe:
>   \`/Users/activi/Library/Application Support/Activi/discovery-raw/dino_crm_discovery_target_01/DISCOVERY-GATE-B1-V2-2026-09-11/gate-b1.out\`
> - Minimiertes Laufmanifest:
>   \`/Users/activi/Library/Application Support/Activi/discovery-raw/dino_crm_discovery_target_01/DISCOVERY-GATE-B1-V2-2026-09-11/gate-b1-manifest.json\`
>
> SHA-256 der einzigen freigegebenen SQL-Datei:
> \`0f586d02a663f9df543a7b7c1b8efde876c2b96d6079cd79e02c3a7359710317\`.
>
> SHA-256 des Launchers:
> \`638e4713370f7a2499e2543656334da97f1e245d3a8385d6914f0f137fbabf3d\`.
>
> SHA-256 des Stream-Guards:
> \`acfc52daf4773be1034d52f5bed1acd61f73a2ec6ae6768c872b86876406e190\`.
>
> Bei Hashabweichung einer dieser drei Dateien ist die Freigabe unwirksam.
>
> Erlaubte Inhalte: Nur die in dieser SQL-Datei enthaltenen Identity- und
> Privilege-Prüfungen: Vergleich des lokal attestierten Ziels und erwarteten
> Datenbanknamens, \`session_user\` und \`current_user\`, Rollenattribute,
> vollständige direkte und geerbte Rollen, Datenbank-/Schema-/Relations-/
> Spalten-/Sequenz-/Routine-Ownership, CREATE, TEMP, Tabellen- und
> Spaltenrechte für INSERT/UPDATE, weitere Tabellen-Write-Rechte,
> Sequenzrechte UPDATE/USAGE, ausführbare SECURITY-DEFINER-Routinen sowie
> READ-ONLY- und Timeout-Status.
>
> Erlaubt sind ausschließlich die wörtlich in der SQL-Datei enthaltenen
> \`pg_catalog\`-Hilfsfunktionen:
> \`current_database\`, \`pg_is_in_recovery\`, \`current_setting\`,
> \`has_database_privilege\`, \`has_schema_privilege\`,
> \`has_table_privilege\`, \`has_column_privilege\`,
> \`has_sequence_privilege\`, \`has_function_privilege\` und
> \`pg_get_function_identity_arguments\`.
>
> Verbotene Inhalte: Gate B2 und B3, jede zusätzliche oder veränderte
> SQL-Anweisung,
> Anwendungsfunktionen, RPCs, Triggerfunktionsaufrufe, gespeicherte Prozeduren,
> dynamisches SQL, Kandidaten- oder Fachdaten, Katalogdefinitionen,
> RLS-Ausdrücke, View-/Trigger-/Indexdefinitionen, Enum-Labels,
> datenabgeleitete Statistiken, EXPLAIN/EXPLAIN ANALYZE, DDL, DML,
> Funktionsausführung, Kontakte, CVs, Geburtsdaten, Identifikationsnummern,
> Secrets, URLs und Credentials.
>
> \`psql\` muss mit
> \`-X --no-psqlrc --no-password --quiet --set=ON_ERROR_STOP=on --csv
> --tuples-only\` laufen. Der Launcher setzt zusätzlich einen zufälligen,
> nicht geheimen \`boundary_token\` und den lokal attestierten erwarteten
> Datenbanknamen als \`psql\`-Variablen. Die
> SQL-Datei muss \`BEGIN TRANSACTION READ ONLY\`, die dokumentierten lokalen
> Timeouts und abschließendes \`ROLLBACK\` unverändert enthalten.
>
> Jede Query wird im Raw-Stream durch genau ein tokengebundenes
> \`BEGIN\`/\`END\`-Markerpaar begrenzt. Fehlende, vertauschte oder zusätzliche
> Marker, eine falsche Query-ID oder ein unvollständiger CSV-Datensatz sind STOP.
> Jede Ergebniszeile der Finding-Queries SQL-GATE-B1-003 bis
> SQL-GATE-B1-010 ist ebenfalls sofort STOP.
>
> Stop-Kriterien: Es gilt sofortiger fail-closed STOP bei abweichender Gate-ID,
> Ziel-Alias,
> Zeit, Datei, SHA-256 oder Zielattestation; abweichendem
> Host-/Projektfingerprint oder Datenbanknamen; abweichendem oder wechselndem
> \`session_user\`/\`current_user\`; jedem administrativen Rollenflag; jeder
> direkten oder geerbten Rolle; jedem TEMP-, Ownership-, CREATE-, Tabellen-,
> Spalten-Write-, Sequenz-USAGE-/UPDATE- oder kritischen Routinetreffer;
> fehlendem READ ONLY, Fehlerabbruch oder Timeout; jeder nicht wörtlich
> allowlisteten Query/Funktion; Anwendungstabellen-, Kandidaten-, RPC- oder
> dynamischem SQL-Zugriff; \`LIMIT 5001\`; mehr als 2 MiB je Query oder
> 12 MiB Gesamtausgabe; mehr als einer Verbindung, Parallelität oder Retry;
> einer Multi-Host-Liste im Connection Service;
> SQL-Ausgabe im Chat oder außerhalb des Restricted-Raw-Ordners; Auftreten
> verbotener Inhalte; ungeklärter Retention/Löschung; Scopeänderung oder
> Widerruf.
>
> SQL-Ausgabe darf nicht im Chat erscheinen. Restricted Raw darf nur außerhalb
> des Repositories in einem neuen Verzeichnis mit Modus \`0700\` gespeichert
> werden. Es gibt kein \`tee\`, Clipboard, Terminal-Mitschnitt, Ticket, Prompt
> oder Commit mit Raw-Inhalten.
>
> Retention-Regel: Restricted Raw darf höchstens 24 Stunden nach Verbindungsende
> bestehen. Vor der Verbindung muss ein dokumentierter, autorisierter lokaler
> Löschmechanismus feststehen; andernfalls ist STOP. Sanitized Inhalte dürfen
> erst nach separatem Security-/Privacy-Review und eigener
> Dokumentationsfreigabe in das Repository.
>
> Diese Freigabe endet nach Gate B1. Gate B2 und Gate B3 benötigen jeweils nach
> Review der vorherigen Stufe eine neue ausdrückliche Nutzerfreigabe.
