# Änderungsmatrix: Discovery-Gate A zu B

Datum: 2026-09-11

Status: Dokumentierte Überarbeitung ohne Datenbankzugriff oder Freigabe.

Version A und ihre SQL-Dateien bleiben als historischer Entwurf unverändert
erhalten. Nur die B-Dateien beschreiben den neuen Vorschlag.

Die ursprüngliche B1-SQL und ihr nicht erteilter Freigabetext bleiben ebenfalls
historisch erhalten. B1 V2 ergänzt ausschließlich das lokal getestete
Launcher-Protokoll; auch dafür besteht keine Ausführungsfreigabe.

| Bereich | Gate A | Gate B | Wirkung |
| --- | --- | --- | --- |
| Gate-ID | Eine gemeinsame Gate-ID A. | Gate-Familie B mit getrennten Freigaben B1, B2 und B3. | Keine implizite Weitergabe einer Freigabe. |
| Zielbindung | Zielumgebung und Datenbankname waren nur allgemeine Stopkriterien. | Eindeutiger Alias \`dino_crm_discovery_target_01\`, lokales Attest, Host-/Projektfingerprint und erwarteter Datenbankname. | Fail-closed Schutz gegen falsches Ziel ohne URL/Credentials im Repository. |
| Verbindung | Identity und Metadaten als aufeinanderfolgende Stufen beschrieben. | Pro Gate genau ein Prozess, eine Verbindung und ein Versuch; jede Stufe in separater Sitzung. | B2/B3 können nicht durch eine B1-Freigabe mitlaufen. |
| B1-Identitäten | Aktive Rolle und Sessionrolle wurden angezeigt. | \`session_user\` und \`current_user\` werden verglichen, beide Rollenattribute geprüft und am Ende erneut kontrolliert. | Rollenwechsel oder Identitätsabweichung ist STOP. |
| Rollenpfade | Mitgliedschaften der aktiven Rolle. | Vollständige direkte und geerbte Rollen beider Identitäten. | Jede erreichbare Rolle wird konservativ als möglicher Rollenwechsel behandelt. |
| Spaltenrechte | Tabellenrechte, keine eigene Spaltenprüfung. | Effektive INSERT-/UPDATE-Rechte je Spalte. | Verdeckte Spalten-Write-Rechte führen zu STOP. |
| Sequenzen | Nicht separat geprüft. | Sequenz-Ownership sowie UPDATE-/USAGE-Rechte beider Identitäten. | Sequenzseitige Schreibfähigkeit wird fail-closed erkannt. |
| TEMP | WARN mit Entscheidungsmöglichkeit. | Jeder TEMP-Treffer ist STOP. | Eindeutige konservative Behandlung. |
| Trefferbewertung | Teilweise WARN oder Einzelreview. | Alle B1-Finding-Queries sind fail-closed; Ausnahmen brauchen neue Gate-Version. | Kein stilles Akzeptieren. |
| Strukturinventar | Metadaten, Definitionen und Statistiken gemeinsam. | B2 enthält nur Namen, Typen, Beziehungen, Flags, Größenklassen und \`reltuples\`. | Sensitivität und Datenableitung werden aus B2 entfernt. |
| RLS | Flags und Policy-Ausdrücke gemeinsam. | B2 nur Enabled/Forced/Policy-Anzahl; Ausdrücke in B3. | RLS-Logik wird separat freigegeben. |
| Definitionen | View-, Trigger- und Indexdefinitionen in der Metadatenstufe. | Ausschließlich im nicht freigegebenen B3-Entwurf. | Mögliche Literale und interne Logik bleiben hinter eigenem Gate. |
| Enum-Labels | In der Metadatenstufe. | B3-Entwurf mit Sensitivitätskennzeichnung. | Internes Vokabular wird nicht in B2 erhoben. |
| Statistiken | \`pg_stats\` und Relationsaktivität in der Metadatenstufe. | B3-Entwurf; daten-/workload-abgeleitet markiert. | Keine datenabgeleiteten Werte in B2. |
| Outputmechanismus | Restricted Raw und allgemeine Größenlimits. | Genaues \`psql\`-Profil, \`ON_ERROR_STOP\`, keine Chatausgabe, 0700-Raw-Ordner, Query- und Sitzungslimits. | Reproduzierbarer fail-closed Ablauf. |
| SQL-LIMIT | Normales Ergebnislimit. | \`LIMIT 5001\` ist Sentinel; 5001 Zeilen bedeuten unvollständiges Inventar und STOP. | Ein abgeschnittenes Inventar kann nicht PASS werden. |
| Hilfsfunktionen | Anwendungs-/RPC-Aufrufe allgemein ausgeschlossen. | Pro Gate vollständige Liste der einzig erlaubten \`pg_catalog\`-Hilfsfunktionen. | Kein impliziter Funktionsaufruf. |
| Retention | Rohdaten maximal bis zur späteren Löschentscheidung. | Maximal 24 Stunden; autorisierter Löschmechanismus muss vor Verbindung feststehen. | Fehlende Retention/Löschung blockiert B1. |
| Freigabetext | Gemeinsamer Text für beide damaligen Stufen. | Neuer exakter Text ausschließlich für B1 mit Gate-ID, Alias, Zeitfenster, Pfaden, Hash, Scope, Verboten, Stops und Retention. | B2/B3 bleiben ausdrücklich unfreigegeben. |
| B1-V2-Query-Grenzen | Nur konstante \`query_id\`-Spalten; bei null Zeilen kein Stream-Marker. | Tokengebundene \`BEGIN\`/\`END\`-Marker um jede Query, CSV ohne Kopfzeile. | Query-Grenzen bleiben auch bei null Zeilen eindeutig und streamend prüfbar. |
| B1-V2-Launcher | Nur dokumentiert. | Feste Produktionspfade, Hash-, Attest-, Owner-, Modus-, Symlink-, Zeit-, Lock-, Byte-, Sentinel- und Ein-Prozess-Prüfungen. | Lokal ausschließlich mit Fake-\`psql\` getestet; reale Ausführung bleibt NO-GO. |

## Neue Dateien

- [Gate-B-Preflight](security-read-only-discovery-preflight-b.md)
- [Gate-B1-SQL](sql/00-identity-and-privilege-gate-b1.sql)
- [Gate-B2-SQL](sql/10-catalog-structure-gate-b2.sql)
- [Gate-B3-Entwurf](sql/20-definitions-statistics-gate-b3-draft.sql)
- [Exakter Gate-B1-Freigabetext](gate-b1-approval-text.md)
- [B1-V2-SQL](sql/00-identity-and-privilege-gate-b1-v2.sql)
- [Exakter Gate-B1-V2-Freigabetext](gate-b1-v2-approval-text.md)
- [Lokaler B1-V2-Launcher](../../scripts/discovery/run-gate-b1.sh)

## Erhaltene Grenzen

- Status bleibt PASS_WITH_GAPS / NO-GO.
- Keine Datenbankverbindung und keine SQL-Ausführung.
- Keine Kandidaten- oder Fachdaten.
- Keine Anwendung, RPC, Migration, DDL, DML oder dynamisches SQL.
- Keine URL, Host-/Projektkennung oder Credentials in Repository, Bericht oder
  Chat.
- Keine Freigabe von B2 oder B3.
- Kein Push, Ticket oder externer Write.
