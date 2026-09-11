# Verifikation des CRM-MCP-Plans gegen aktuelle Best Practices

Datum: 2026-09-11

Status: `PASS_WITH_GAPS` als Architekturprüfung; Optimierungsvorschläge,
keine neue Architekturentscheidung und keine Freigabe für externe Änderungen.

## Urteil

Der akzeptierte Kern ist für den beschriebenen Use Case gut geeignet:
kleiner validierter Filter, kontrollierte PostgreSQL-Funktionen, drei fachliche
Suchwerkzeuge, höchstens 50 kontaktfreie Kandidaten pro Seite und getrennte
Profilverwaltung. Die geschätzten 200.000 Kandidaten begründen für sich allein
weder einen externen Suchdienst noch Cache oder Vektorspeicher.

**Optimalität, vollständige Suchqualität und Produktionsreife sind noch nicht
bewiesen.** Es fehlen bestätigte Schema-/Berechtigungsfakten, abgeschlossene
Fachsemantik, Auth-Interoperabilität und repräsentative Messungen. Den Kern neu
zu bauen wäre derzeit nicht begründet. Die beste Verbesserung ist ein präziserer
Verifikationsvertrag und weniger unnötige Abhängigkeiten zwischen Arbeitspaketen.

## Was beibehalten werden sollte

- **Eine kontrollierte Datengrenze:** SQL-Funktionen eignen sich für
  datenintensive Operationen. Funktionsrechte und der Ausführungskontext müssen
  ausdrücklich gestaltet werden; `security invoker` ist der bevorzugte
  Ausgangspunkt. Ein generischer SQL-/CRUD-MCP würde den akzeptierten Vertrag
  verbreitern. Die Such-RPC ist dabei nicht automatisch der Vertrag für die
  beiden anderen Fachtools. [Supabase Database Functions](https://supabase.com/docs/guides/database/functions)
- **Strukturierte IDs und kontrollierte Taxonomie zuerst:** FTS normalisiert
  Wörter sprachabhängig und unterstützt GIN-Indizes sowie sprachabhängige
  Konfigurationen. Das ist keine fachliche Übersetzung zwischen Berufskonzepten.
  B/H/S, DE und EN brauchen einzeln geprüfte Suchfälle und Konfigurationen;
  vorhandene Dictionary-Unterstützung bleibt Discovery-Evidenz.
  [PostgreSQL FTS](https://www.postgresql.org/docs/current/textsearch-tables.html)
- **Vektoren nur nach Qualitätsnachweis:** `pgvector` dokumentiert exakte Suche
  nach selektiven Filtern sowie Recall-Verluste bei ANN und nachgelagerter
  Filterung. Iterative Scans können mehr Treffer finden, enden aber an
  Ressourcengrenzen. Deshalb gehört ein exakter Referenzlauf in den späteren
  Vektortest. [pgvector: Filtering und Iterative Index Scans](https://github.com/pgvector/pgvector#filtering)
- **Vector Buckets bleiben optional:** Die aktuelle Dokumentation bezeichnet
  sie weiterhin als Alpha und nennt mögliche Breaking Changes. Ein zusätzlicher
  Speicherweg ist für diesen Bestand ohne Vergleich nicht begründet.
  [Supabase Vector Buckets](https://supabase.com/docs/guides/storage/vector/introduction)
- **Lokale synthetische Tests und CI:** Supabase dokumentiert automatisierte
  Datenbanktests in GitHub Actions. Das ermöglicht die akzeptierte Testkette ohne
  ein weiteres gehostetes Staging-Projekt. Beispiel-YAML mit `latest` ist keine
  reproduzierbare Projektvorlage; konkrete Tool-/Runtime-Versionen erst nach
  Auswahl festhalten. [Supabase CI-Tests](https://supabase.com/docs/guides/deployment/ci/testing)

## Vor der Implementierung zu präzisieren

### 1. Gates müssen Fehler tatsächlich blockieren

Die aktuelle CLI-Referenz beschreibt `db lint --fail-on none` als Default:
Der Prozess kann trotz Findings erfolgreich enden. Der spätere Wrapper muss
deshalb eine ausdrückliche Fehlerpolitik setzen und anhand eines absichtlich
fehlerhaften synthetischen Falls beweisen, dass CI blockiert.

`db push --dry-run` druckt die vorgesehenen Migrationen; es führt sie nicht
probeweise aus. `db diff` nennt unter anderem Views mit `security_invoker` als
bekannte Grenze. Eine leere Diff-Ausgabe ist daher kein ausreichender
RLS-/View-Nachweis. `db reset --local` baut den lokalen Zustand neu;
Remote-Reset-Flags können dagegen entfernte Objekte löschen.
[Supabase CLI Reference](https://supabase.com/docs/reference/cli/supabase-db-push)

Empfohlene Ergänzung von AUTO-03/04/06: geprüfte lokale Zielbindung,
explizite Lint-Fehlerschwelle, negativer Gate-Kontrollfall, katalogbasierte
Assertions für Rechte/View-Eigenschaften, saubere Neuinstallation **und**
Upgradeprobe vom vorherigen freigegebenen Schema mit synthetischem Altbestand.
Diese Aufgaben erhalten überprüfbare Ergebnisse; Lint ersetzt keine fachlichen
oder RLS-Laufzeittests. [Testing and linting](https://supabase.com/docs/guides/local-development/cli/testing-and-linting)

### 2. Dry-run, Rückschaltung und Restore sind drei Nachweise

Die lokale Upgradeprobe prüft die konkrete Migration. Rückschaltung prüft, ob
die vorherige Anwendung/RPC mit dem additiv erweiterten Schema weiterhin
funktioniert. Ein Backup-Restore prüft Datenwiederherstellung und Betriebsablauf.
Keiner dieser Nachweise ersetzt die anderen.

Auch ein erfolgreiches `EXPLAIN ANALYZE` ist kein ungefährlicher statischer
Check: Es führt die Anweisung aus, einschließlich ihrer Nebenwirkungen.
Ein `SELECT` kann Funktionen enthalten; die geprüfte erlaubte Query ist die
relevante Grenze. Messungen brauchen Budget, Timeout und minimierte Ausgaben.
[PostgreSQL EXPLAIN](https://www.postgresql.org/docs/current/sql-explain.html)

Ein universeller `BEGIN`/`ROLLBACK`-Wrapper ist zudem für Migrationen ungeeignet:
`CREATE INDEX CONCURRENTLY` darf nicht in einem Transaktionsblock laufen.
Transaktionale und nichttransaktionale Schritte benötigen deshalb eigene
Stop-/Wiederanlaufregeln. [PostgreSQL CREATE INDEX](https://www.postgresql.org/docs/current/sql-createindex.html)

Supabase-DB-Backups enthalten keine Storage-Objektdateien. Falls CVs später in
Storage nachgewiesen werden, muss der Wiederherstellungsumfang diese separat
abdecken. Das behauptet nicht, dass der aktuelle CRM-Bestand Storage verwendet.
[Supabase Database Backups](https://supabase.com/docs/guides/platform/backups)

### 3. Aktuelle Vendor-Änderungen in überprüfbare Kriterien übersetzen

- Seit 2026-08-05 ignoriert Supabase bei Extension-Erzeugung/-Update angeforderte
  Versionsangaben und verwendet die Default-Version; vorhandene Installationen
  ändern sich dadurch nicht automatisch. Lokale Images und CLI pinnen, zusätzlich
  tatsächliche DB-/Extension-Versionen und benötigte Fähigkeiten attestieren.
  Der Changelog gilt nicht gleichermaßen für Self-hosting.
  [Changelog vom 22.07.2026](https://supabase.com/changelog/extension-version-pinning-ignored)
- Das neue Data-API-Verhalten verlangt explizite Grants für neue Tabellen und
  soll am 2026-10-30 alle bestehenden Projekte erreichen. Bestehende Tabellen
  behalten laut Erläuterung ihre Grants. Discovery und Migrationstests müssen
  echte Rechte prüfen, statt automatische Exponierung anzunehmen.
  [Changelog vom 28.04.2026](https://supabase.com/changelog/45329-breaking-change-tables-not-exposed-to-data-and-graphql-api-automatically)
- Der Changelog kündigt die Entfernung von `logs.all` am 2026-09-23 an.
  Ein späteres Monitoring darf diesen alten Management-API-Pfad nicht als
  Ausgangspunkt übernehmen. Aktuelle Projektkonfiguration ist dadurch nicht
  bestätigt. [Supabase Changelog](https://supabase.com/changelog)

### 4. Auth und Protokoll früh als eigene Risiken testen

Die MCP-Spezifikation 2026-07-28 verlangt serverseitige Prüfung, dass ein Token
für den konkreten MCP-Server ausgestellt wurde. Supabase Auth kann Discovery,
Tokenverwaltung und Identitäten liefern; Autorisierungsendpunkt, Zustimmung,
Rollen-/Tenant-Zuordnung und Multi-Client-Tests bleiben Projektarbeit.
Keine pauschale Weiterreichung beliebiger Bearer-Tokens als Abkürzung.
[MCP Authorization](https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization),
[Supabase MCP Authentication](https://supabase.com/docs/guides/auth/oauth-server/mcp-authentication)

`outputSchema` und `structuredContent` sollen denselben freigegebenen
Ergebnisvertrag ausdrücken. Auch der Text-Fallback muss kontaktfrei und
inhaltsgleich sein. Schema-konforme Ausgabe ersetzt nicht die Prüfung von
Berechtigungen oder Fachsemantik. Zustände über Tool-Calls hinweg benötigen
explizite Handles; implizite Verbindungszustände sind keine stabile Grundlage.
[MCP Tools](https://modelcontextprotocol.io/specification/2026-07-28/server/tools)

Die bestehende Aussage über SDK v2 als stabile TypeScript-Linie ist aktuell
bestätigt. Das ist eine verfügbare Option, keine Auswahl des noch offenen
Projektstacks. [Offizielles TypeScript SDK](https://github.com/modelcontextprotocol/typescript-sdk)

## Zusätzliche Primärprüfung der Discovery-Gates

Der parallele Repository-Audit meldete folgende konkrete SQL-/Inventarstellen.
Ihre zugrunde liegende PostgreSQL-Semantik wurde zusätzlich verifiziert; gegen
eine Datenbank wurden sie nicht ausgeführt:

- `current_user` ist eine SQL-Spezialform ohne Klammern. Eine Referenz
  `pg_catalog.current_user` ist nicht die schemaqualifizierte Form dieser
  Spezialsyntax und darf nicht als gleichwertige Identitätsprüfung gelten.
  [PostgreSQL Session Information](https://www.postgresql.org/docs/current/functions-info.html)
- `DROP ROLE` scheitert, solange Privilegabhängigkeiten bestehen. Ein zuvor
  ausdrücklich erteilter `CONNECT`-Grant muss beim kontrollierten Cleanup
  berücksichtigt und vor dem Drop widerrufen werden. Breite `DROP OWNED`-
  Aktionen sind daraus nicht automatisch autorisiert.
  [PostgreSQL DROP ROLE](https://www.postgresql.org/docs/current/sql-droprole.html)
- `information_schema.table_privileges` und `routine_privileges` zeigen
  Berechtigungen, die an aktuell aktivierte Rollen oder durch solche Rollen
  vergeben wurden. Eine schwach privilegierte Discovery-Rolle erhält daraus
  kein vollständiges systemweites Grant-Inventar; leere Ergebnisse sind kein
  Beweis fehlender Grants. [table_privileges](https://www.postgresql.org/docs/current/infoschema-table-privileges.html),
  [routine_privileges](https://www.postgresql.org/docs/current/infoschema-routine-privileges.html)
- `pg_stats` beschränkt sichtbare Statistikzeilen auf lesbare Tabellen. Ein
  reiner Verbindungszugang belegt daher keinen umfassenden Statistik-/DQ-Zugriff.
  Berechtigungsgrenzen müssen im Ergebnis als Coverage-Gap ausgewiesen werden;
  zusätzliche Tabellenrechte sind keine stillschweigende Lösung.
  [PostgreSQL pg_stats](https://www.postgresql.org/docs/current/view-pg-stats.html)
- `pg_policy.polroles` verwendet die OID `0` für `PUBLIC`. Ein Join nur auf
  echte Rollen muss diesen Sonderfall ausdrücklich abbilden, sonst wird die
  öffentliche Policy-Geltung als fehlender Rollenname dargestellt.
  [PostgreSQL pg_policy](https://www.postgresql.org/docs/current/catalog-pg-policy.html)

Die lokalen Python-Umgebungen dieser Teilprüfung enthielten weder `pglast`
noch `pg_query`. Es wurde kein Parser installiert und keine neue Datenbank
gestartet. Syntax-/Lifecycle-Repros bleiben vor einer Gate-Ausführung nötig.

## Kürzerer Ablauf bei gleicher funktionaler Abdeckung

Die folgende Reihenfolge ist ein Vorschlag. Sie verändert weder offene
Interviewentscheidungen noch die erforderliche Freigabe für Umsetzung.

1. **Jetzt:** Dokumentwidersprüche bereinigen und die Sicherheitsfragen für
   den Discovery-Scope klären. Weitere Geschäftsentscheidungen folgen gemäß
   Q9 nach Discovery. Testfälle für bestätigte Regeln sammeln und
   die Zuordnung Anforderung → Vertrag → Test → Ticket vorbereiten.
2. **Nach nötiger Discovery-/Entscheidungsevidenz:** Vertrag finalisieren und
   Stack auswählen. Auth-/Client-POC und lokale Tooldiagnose als eigene kleine
   Arbeitspakete behandeln, statt sie in einem großen Sammelentscheid zu
   verstecken. Die aktuelle Interview-/Scaffold-Sperre bleibt bestehen.
3. **Nach Vertrags- und Scaffold-Freigabe:** Ein lokaler DB-/Migrationspfad
   entsteht mit pgTAP und Lint; daneben können MCP-Contract-Tests gegen einen
   Fake-Adapter und Auth-/Client-Tests vorbereitet werden. AUTO-05 braucht nicht
   für jeden Teil die vollständige Fertigstellung von AUTO-04.
4. **Integration:** Ein vertikaler Suchfall durch Validator, RPC, Rechte und
   Ergebnisvertrag wird vollständig getestet. Danach dieselbe Strecke um die
   übrigen bestätigten Filter, Profile und Filteroptionen erweitern. Dies sind
   Entwicklungsabschnitte; der Release umfasst weiterhin alle Must-haves.
5. **Vor Release:** vollständige positive/negative Suite, Upgrade- und
   Rückschaltprobe, Restore-Nachweis, repräsentative Last, Datenschutz und alle
   Zielclients prüfen. Monitoring und Alarme bereits als Releasevoraussetzung
   verifizieren; erst danach Produktionsfreigabe und kontrollierter Rollout.
6. **Betrieb:** native Signale beobachten. Zusätzliche Optimierer nur gegen
   belegte Diagnose-/Performanceprobleme bewerten. Die feste Wartezeit von vier
   bis acht Wochen in ADR-0004 kann durch einen belastbaren Workload-Trigger
   ersetzt werden, wenn der Nutzer die ADR-Änderung beschließt.

Das verkürzt unnötige Warteketten und doppelte Vertragsarbeit. Eine konkrete
Prozent- oder Zeiteinsparung ist nicht belegt. Pflichtprüfungen werden dadurch
nicht gestrichen. Isolation ist nötig, damit parallel arbeitende Tests nicht
dieselbe Datenbank zurücksetzen oder gemeinsam mutable Fixtures verändern.

## Automatisierung mit dem größten erwarteten Nutzen

- Ein kanonischer Schema-/Vertragssatz erzeugt Validatoren, Toolschemas,
  freigegebene Typen und Dokumentationsauszüge; fachliche Testorakel werden
  unabhängig geprüft und nicht allein aus der Implementierung erzeugt.
- Ein lokaler/CI-Einstieg erzeugt strukturierte Gate-Ergebnisse, verwendete
  Versionen und Artefakt-Hashes. Eine spätere Freigabe bezieht sich auf genau
  diesen Diff und das attestierte Ziel; geänderte Eingaben erfordern neue Checks.
- Dieselben synthetischen Fälle testen Sprachvarianten, Grenzwerte, fehlende
  Werte, Rechte, Kontaktfreiheit, Cursor-Manipulation und Fehlerausgaben.
  Fehler nur in einer Schicht zu testen genügt nicht.
- Dokument- und Ticketabgleich kann read-only fehlende IDs, ungeklärte
  Entscheidungen, Statusdrift und defekte Links melden. Externe Ticketänderungen
  bleiben eigenständig freizugebende Aktionen.
- Zusatztools erhalten Eintritts- und Ausstiegskriterien. Ohne messbaren Nutzen
  entstehen kein Cache, Sync-Dienst, Low-Code-UI oder externer Optimierer.

## Einordnung aller sieben bisherigen Researchdateien

<!-- markdownlint-disable MD013 -->

| Datei | Ergebnis dieser Prüfung |
| --- | --- |
| [Supabase-Werkzeuge](supabase-werkzeuge-fuer-crm-mcp.md) | Kern technisch passend; aktueller Berechtigungsmodus und vorgeschlagener Developer-MCP-Discoverypfad sind gegenüber neueren Projektregeln überholt. Branching ist keine aktive Umgebungsentscheidung. Changelog-Hinweise sind vorhanden, aber noch keine ausführbaren Gates. |
| [Berufssuchprofile Q8.4.2](berufssuchprofile-q8-4-2.md) | Bereits klar historisch eingeordnet. Mitgliedsrollen, Quellenwahl und Q8.5 bleiben Vorschläge/offen; normative Formulierungen im Haupttext beweisen keine Zustimmung. Der Verweis auf MCP 2025-11-25 ist historisch; neue Implementierung auf verifizierten Versionsvertrag festlegen. |
| [Readyset, Zero, Electric](supabase-partner-readyset-zero-electric.md) | Keine dieser Optionen ist zurzeit als notwendiger Release-Baustein belegt. Preise, konkrete Versionsstände und alle Partnerdetails wurden hier nicht erneut einzeln zertifiziert; bei Auswahl neu prüfen. |
| [Werkzeugempfehlung ohne Umbau](werkzeugempfehlung-verifikation-ohne-umbau.md) | Reduzierter Kern, synthetische Tests und Aufteilung der Testwerkzeuge bleiben sinnvoll; SDK-v2-Aussage bestätigt. Die pauschale Zusicherung „ohne Qualitätsverlust“ bleibt eine zu beweisende Hypothese. Lokale Tooldefekte sind historische Befunde, keine neue Diagnose. |
| [Semantisches Evaluations-Gate](semantic-search-evaluation-gate.md) | Baseline zuerst, harte Filter und Lifecycle-Nachweise sind richtig. Die zusätzliche Zahl 179 Tabellen bleibt unbestätigte historische Behauptung. Bei optionaler Evaluation Exact-vs-ANN-Recall unterscheiden und keinen vollständigen Vector-Bucket-POC erzwingen, wenn dokumentierte Ausschlusskriterien bereits greifen. |
| [Agent Skills erklärt](supabase-agent-skills-einfach-erklaert.md) | Anleitung/Tool/Produktgrenze sinnvoll. Die generische Formulierung „nach eigenem Gate“ muss den engeren Produktionsausschluss der aktuellen Projektregeln ausdrücklich mitdenken. Installation/Toolzustand wurden hier nicht neu geprüft. |
| [Optimaler SQL-/Automatisierungsweg](optimaler-sql-und-automatisierungsweg.md) | Native-first entspricht ADR-0004. „Schnellster“, „maximale Zeitersparnis“ und „größter Teil manueller Arbeit entfällt“ sind ohne Messung keine nachgewiesenen Resultate. Vier bis acht Wochen sind kein technischer Mindestzeitraum; die Vorgabe bleibt bis zur ADR-Änderung verbindlich. |

<!-- markdownlint-enable MD013 -->

Aktualisierung aus der frischen lokalen Hauptprüfung: `rtk proxy supabase
--version` scheiterte konkret an einem durch die Sandbox blockierten
Telemetry-Dateischreibzugriff. Das belegt eine Ausführungsgrenze, nicht allein
eine defekte Supabase-Installation. Promptfoo scheiterte erneut am dokumentierten
`better-sqlite3`-ABI-Konflikt. Keine Reparatur oder Umgehung wurde durchgeführt.

Wichtige Quellenkorrektur: Die **aktuelle** Supabase-MCP-Dokumentation erlaubt
mittlerweile eng begrenzten Produktionszugriff bei entsprechendem Evidenzbedarf
und empfiehlt Projektbindung, read-only sowie reduzierte Featuregruppen.
Das absolute Verbot dieses Projekts, den Developer-MCP mit seinem produktiven
Kandidatenbestand zu verbinden, ist deshalb als **eigene verbindliche
Projektgrenze** zu benennen. Es wird durch die Herstelleränderung nicht
aufgehoben. [Aktuelle Supabase-MCP-Empfehlungen](https://supabase.com/docs/guides/ai-tools/mcp#security-risks)

Auch Skill-Beispiele sind keine Garantien: Die lokale FTS-Referenz behauptet
pauschal, Wildcard-`LIKE` könne keinen Index verwenden; PostgreSQL dokumentiert
dafür jedoch Trigramm-Indizes. FTS ist kein semantisch identischer Ersatz jeder
Substring-Suche. Die pauschale O(1)-Aussage der Pagination-Referenz darf ebenfalls
nicht als SLO gelten; reale Kosten hängen von Index, Filter, Ranking und
Trefferverteilung ab. [PostgreSQL pg_trgm](https://www.postgresql.org/docs/current/pgtrgm.html)

## Prüfabdeckung und Grenzen

Alle sieben oben aufgeführten Researchdateien wurden vollständig gelesen.
Zusätzlich wurden Projektstatus, ADR-0004, Automatisierungsrunbook,
Automatisierungsticketplan, README sowie relevante Teile des Briefs gelesen.
Geladen wurden `research`, `supabase`, `supabase-postgres-best-practices` und
die Referenzen FTS, Pagination und Privilegien. Der übergreifende Audit prüft
die weiteren ADR-/Discovery-/Ticketdetails; dieser Bericht behauptet dafür
keine eigenständige Vollabdeckung.

Alle in diesem Bericht als aktuell verwendeten Webquellen wurden am
2026-09-11 über öffentliche offizielle Dokumentation oder Maintainer-Repositories
gelesen. Der Markdown-Changelog war über das Webwerkzeug nicht lesbar;
die HTML-Version und relevante Einzelmeldungen waren erreichbar. Die
unversionierten MCP-`latest`-URLs scheiterten, die konkrete Spezifikation
2026-07-28 und das offizielle SDK-Repository waren erreichbar.

Keine Datenbank-, Supabase-Plugin-, Produktions-, Installations- oder externen
Schreibaktionen wurden durchgeführt. Keine Laufzeit-, Last-, Wiederherstellungs-
oder Client-Kompatibilitätstests wurden durch diese Recherche ersetzt.
Das Ergebnis ist eine belegte Planungsempfehlung, kein Nachweis eines bereits
funktionierenden Systems.
