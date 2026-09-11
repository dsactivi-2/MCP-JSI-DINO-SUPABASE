# Optimaler SQL- und Automatisierungsweg für den CRM-MCP

Datum: 2026-09-11

Status: Primärquellenbasierte Entscheidungsgrundlage; keine Datenbankverbindung,
Installation, Migration oder externe Änderung

## Auftrag und feste Projektgrenzen

Gesucht wurde der Weg, der für den geplanten Supabase-PostgreSQL-CRM-MCP mit
geschätzt etwa 200.000 Kandidaten möglichst viel SQL-, Test-, Optimierungs- und
Betriebsarbeit automatisiert, ohne Qualitäts- oder Funktionsverlust und ohne
frühen großen Umbau.

Verbindlich bleiben der [Projektstatus](../project.md),
[ADR-0001](../decisions/0001-controlled-query-boundary.md) und
[ADR-0003](../decisions/0003-separated-profile-administration-mcp.md): Das
Runtime-LLM erzeugt nur einen streng validierten JSON-Filter und niemals frei
ausführbares SQL. PostgreSQL bleibt für Autorisierung, Filterung, Ranking und
Pagination verantwortlich. Der Such-MCP ruft nur eine vorab definierte RPC auf;
der Profilverwaltungs-MCP bleibt getrennt.

Die Übertragung von Kandidatendaten an externe Anbieter wurde auf Wunsch des
Nutzers **nicht als Ausschlusskriterium** bewertet. Berechtigungen,
Produktionssicherheit, Betriebsrisiko, Kosten und Herstellerbindung bleiben aber
relevante Auswahlkriterien.

## Ergebnis in einem Satz

**Der schnellste und am stärksten automatisierte Weg ist kein einzelnes
Partnerprodukt, sondern eine Supabase-native, versionierte Entwicklungskette mit
KI als SQL-Verfasser, automatischen lokalen und CI-Prüfungen sowie
workload-basiertem Monitoring; pganalyze wird erst nach einem gemessenen
Produktionsbedarf ergänzt.** InsightBase, pgMustard, Bytebase und n8n lösen
jeweils nur einen Teil und verkürzen den Release-1-Kern derzeit nicht stärker.

## Rangliste

### Platz 1: Supabase CLI, lokale Datenbank, pgTAP, Lint, CI und Advisors

Diese Kombination nimmt die meiste wiederkehrende Arbeit ab und verlangt keinen
neuen Datenpfad:

- Versionierte Migrationen und synthetische Seeds machen den Datenbankzustand
  reproduzierbar. `supabase db reset` baut die lokale Datenbank aus Migrationen
  und Seeds neu auf; `db diff` kann eine Migration erzeugen, muss aber laut
  Supabase anschließend geprüft werden
  ([Supabase Local Development Workflow](https://supabase.com/docs/guides/local-development/cli-workflows)).
- `supabase test db` führt pgTAP-Tests aus. Damit lassen sich Struktur,
  Constraints, Funktionen, Datenintegrität und besonders RLS automatisch testen
  ([Supabase Testing Overview](https://supabase.com/docs/guides/local-development/testing/overview)).
- `supabase db lint` verwendet `plpgsql_check` und erkennt unter anderem falsche
  Parametertypen, fehlende Returns, versteckte Casts und bestimmte Risiken in
  dynamischem SQL
  ([Supabase Testing and Linting](https://supabase.com/docs/guides/local-development/cli/testing-and-linting)).
- Supabase dokumentiert automatisierte Datenbanktests in CI und empfiehlt für
  Produktionsmigrationen eine CI/CD-Pipeline statt eines lokalen manuellen
  Deployments
  ([Automated Database Testing](https://supabase.com/docs/guides/deployment/ci/testing),
  [Managing Environments](https://supabase.com/docs/guides/deployment/managing-environments)).
- Security und Performance Advisors laufen automatisch und prüfen unter anderem
  fehlende oder doppelte Indizes, RLS-Konfiguration, Funktions-`search_path`,
  exponierte sensible Spalten und Tabellen-Bloat
  ([Supabase Advisors](https://supabase.com/docs/guides/observability/advisors)).
- `pg_stat_statements` sammelt normalisierte Laufzeit- und Aufrufstatistiken und
  zeigt dadurch, welche Queries tatsächlich langsam oder teuer sind
  ([Supabase pg_stat_statements](https://supabase.com/docs/guides/database/extensions/pg_stat_statements)).
- Der integrierte `index_advisor` simuliert passende Indizes, unterstützt
  Query-Parameter und vermeidet doppelte Vorschläge
  ([Supabase Index Advisor](https://supabase.com/docs/guides/database/extensions/index_advisor)).

Bewertung: **maximale unmittelbare Zeitersparnis, geringer Umbau, geringer
Vendor-Lock-in und Qualitätsgewinn**. Die SQL-Dateien bleiben normales
PostgreSQL und können auch außerhalb von Supabase verwendet werden.

### Platz 2: Supabase AI Assistant beziehungsweise lokaler Agent als SQL-Verfasser

Die KI soll Migrationen, RPC-Funktionen, RLS-Tests und Performance-Testfälle
entwerfen, aber niemals selbst ungeprüft in Produktion ausführen. Supabase
dokumentiert für seinen AI Assistant Schema- und Query-Erzeugung,
Fehlererklärung, RLS-Policy-, Funktions- und Trigger-Unterstützung sowie
natürlichsprachliche Datenabfragen. Das Produkt ist jedoch weiterhin als
**Public Alpha** gekennzeichnet
([Supabase AI Assistant](https://supabase.com/features/ai-assistant)). Supabase
stellt dieselben Arten von Arbeitsanweisungen auch als exportierbare Prompts für
lokale Coding-Agenten bereit
([Supabase AI Prompts](https://supabase.com/docs/guides/ai-tools/ai-prompts)).

Der große Gewinn liegt im Schreiben und Korrigieren von SQL. Die Qualität kommt
aber erst durch Platz 1: erzeugtes SQL wird als Diff behandelt, lokal neu
aufgebaut, gelintet, mit pgTAP und Contract-Tests geprüft und erst danach
freigegeben. Dadurch bleibt die akzeptierte Runtime-Grenze unverändert.

Bewertung: **sehr hohe Schreibersparnis bei sehr kleinem Umbau**, aber nur als
Vorschlagswerkzeug. Wegen Alpha-Status und möglicher Halluzinationen ist es kein
Qualitäts-Gate und kein autonomer Produktionsoperator.

### Platz 3: pganalyze nach vorhandenem echten Query-Workload

pganalyze automatisiert mehr laufende PostgreSQL-Optimierung als pgMustard: Ein
Collector sendet fortlaufend normalisierte Query-Statistiken und Schema-Daten;
Query-, Index- und VACUUM-Advisors, Plananalysen und Alerts bauen darauf auf
([pganalyze Overview](https://pganalyze.com/docs),
[Query Performance](https://pganalyze.com/docs/query-performance)). Der Indexing
Engine bewertet den gesamten Workload und modelliert Indexkombinationen, statt
nur eine einzelne Query zu betrachten
([pganalyze Indexing Engine](https://pganalyze.com/docs/indexing-engine)).

Das spart später viel DBA-Zeit, bringt jetzt aber noch wenig: Vor einer stabilen
`search_candidates_v1` und echten Last existiert kein repräsentativer Workload.
Der Dienst braucht einen zusätzlichen Collector und dauerhaften Zugriff auf
Statistiken. Der aktuelle Listenpreis liegt bei 149 USD pro Monat für eine
Produktionsdatenbank mit Index Advisor; Query Advisor und automatische
`auto_explain`-Pläne beginnen im Scale-Tarif bei 399 USD pro Monat
([pganalyze Pricing](https://pganalyze.com/pricing)). Empfehlungen bleiben
Schätzungen und sollen laut Hersteller vor Produktion getestet werden
([Testing Index Insights](https://pganalyze.com/docs/index-advisor/test-insights)).

Bewertung: **beste spätere externe Vollautomatisierung für Performance**, aber
nicht Teil des ersten Builds. Nach vier bis acht Wochen repräsentativem Betrieb
gegen den Nutzen des eingebauten Supabase-Monitorings testen.

## Vergleich der weiteren Kandidaten

<!-- markdownlint-disable MD013 -->

| Kandidat | Automatisiert | Zeitgewinn | Integration / Umbau | Qualitäts- und Betriebsrisiko | Entscheidung |
| --- | --- | --- | --- | --- | --- |
| Supabase Query Performance, Advisors, `pg_stat_statements`, `index_advisor` | Query-Findung, feste Sicherheits-/Performancechecks, Indexvorschläge | Hoch | Niedrig | Vorschläge sind keine Messung; Indizes nicht automatisch anwenden | **Jetzt einplanen** |
| Supabase AI Assistant / lokale Agent-Prompts | SQL-, RLS-, Funktions- und Testentwürfe, Fehlererklärung | Sehr hoch | Sehr niedrig | Alpha; kann fachlich falsches SQL erzeugen | **Jetzt als Autor, nie als Freigeber** |
| pganalyze | Kontinuierliche Query-, Plan-, Index-, VACUUM-Analyse und Alerts | Später sehr hoch | Mittel: Collector und Konto | Zusätzlicher Dienst, Kosten, Statistikzugriff; Empfehlungen testen | **Nach echtem Workload pilotieren** |
| pgMustard | Einzelne JSON-`EXPLAIN`-Pläne erklären und bewerten; API verfügbar | Mittel | Niedrig, aber Plan muss erzeugt/hochgeladen werden | Kein Dauer-Monitoring; kein On-Prem-Angebot | **Günstige manuelle Hilfe, nicht Kern** |
| Bytebase | SQL-Review, GitOps, Schema-Diff, Freigaben, Drift und Deployment | Hoch bei vielen DB-Änderungen oder Teams | Mittel bis hoch: neuer Kontroll- und Deploypfad | Doppelung mit Supabase CLI/CI; neue Betriebsfläche | **Erst bei wachsendem Team/Migrationsvolumen** |
| InsightBase | Natürliche Sprache zu BI-Abfragen, Tabellen und Charts | Hoch für Ad-hoc-Analysen | Mittel: direkter PostgreSQL-Zugang und semantische Einrichtung | Dupliziert nicht den kontrollierten MCP-Vertrag; Produktstatus/Preis aktuell nicht belastbar verifiziert | **Separates BI-POC, nicht Release-1-Suche** |
| n8n | Zeitpläne, Benachrichtigungen, Exporte und Integrationen | Hoch für Nebenprozesse | Mittel: Workflow-Runtime, Credentials und Betrieb | Postgres-Node kann Query, Insert, Update und Delete; zu breit für Runtime-Suche | **Nur außerhalb des Suchpfads** |
| Supabase Cron | Wiederkehrende SQL-Funktionen oder HTTP-Aufrufe mit Run-Historie | Mittel bis hoch für DB-nahe Jobs | Niedrig | Jobs laufen in der Datenbank; Fehler- und Lastgrenzen beachten | **Vor n8n für einfache DB-interne Jobs** |
| Readyset, Zero, Electric | Query-Cache beziehungsweise Client-/HTTP-Synchronisation | Gering für diesen Release | Hoch | Zusätzlicher Proxy/Replica/Authpfad | **Nur bei später bewiesenem Spezialbedarf** |

<!-- markdownlint-enable MD013 -->

### pgMustard

pgMustard ist ein im Supabase-Partnerkatalog aufgeführter Plananalysator. Die
Integration lässt einen JSON-Plan aus `EXPLAIN ANALYZE` einfügen und liefert
Visualisierung und Hinweise
([Supabase Partnerseite](https://supabase.com/partners/integrations/pgmustard)).
Ein Einzelplatz kostet aktuell 95 EUR pro Jahr und enthält unbegrenzte manuelle
Planreviews sowie 1.000 API-Credits
([pgMustard Pricing](https://www.pgmustard.com/pricing)). Das ist preiswert,
aber weiterhin ein manueller Einzelfall-Workflow. PostgreSQL weist zudem darauf
hin, dass `EXPLAIN ANALYZE` die Anweisung wirklich ausführt
([PostgreSQL EXPLAIN](https://www.postgresql.org/docs/current/sql-explain.html)).
Für Produktionsprüfungen dürfen deshalb nur kontrollierte `SELECT`-Fälle mit
Timeout und Ergebnisverwerfung genutzt werden.

### Bytebase

Bytebase bietet eine umfassende Database-CI/CD-Schicht: Git-basierte
Schema-Versionierung, deklarative Migrationen, mehr als 200 SQL-Review-Regeln,
Rollout-Policies und Changelog sind laut aktueller Preisseite bereits in der
kostenlosen, selbst gehosteten Community Edition enthalten; Pro kostet 20 USD
pro Nutzer und Monat
([Bytebase Pricing](https://www.bytebase.com/pricing/)). Das ist attraktiv,
wenn mehrere Personen, Datenbanken und regelmäßige Produktionsänderungen
koordiniert werden. Im jetzigen Ein-Personen-/Discovery-Stand würde es aber den
bereits vorgesehenen Supabase-CLI- und CI-Prozess verdoppeln. Es ist daher ein
späteres Skalierungswerkzeug und kein jetziger Beschleuniger.

### InsightBase

Die einzige belastbar erreichbare Primärquelle war die Supabase-Partnerseite.
Sie beschreibt einen direkten PostgreSQL-Zugang und natürlichsprachliche
Antworten, Tabellen und Charts
([InsightBase bei Supabase](https://supabase.com/partners/integrations/insightbase)).
Die Herstellerdomain `insightbase.ai` lieferte bei der Prüfung am 2026-09-11
einen HTTP-Fehler. Aktuelle Preise, Wartungsstatus, Query-Grenzen,
Berechtigungsmodell und SQL-Prüfung konnten daher nicht primär verifiziert
werden. Unabhängig vom Datenschutz ist das für eine Produktionsabhängigkeit ein
Reife- und Betriebsrisiko. InsightBase kann später als getrennte BI-Oberfläche
getestet werden, ersetzt aber weder JSON-Validierung noch die feste Such-RPC.

### Workflow-Automation: Supabase Cron vor n8n im Datenbankkern

Supabase Cron kann SQL-Snippets, Datenbankfunktionen oder HTTP-Aufrufe planen,
führt eine Run-Historie und arbeitet für DB-Funktionen ohne Netzwerk-Latenz. Die
Dokumentation empfiehlt höchstens acht gleichzeitige Jobs und maximal zehn
Minuten Laufzeit pro Job
([Supabase Cron](https://supabase.com/docs/guides/cron)). Für kleine interne
Aufgaben wie das Aktualisieren erlaubter Suchstatistiken oder feste
Gesundheitschecks ist es einfacher als eine neue Workflow-Plattform.

n8n besitzt sowohl Supabase- als auch PostgreSQL-Nodes. Der PostgreSQL-Node kann
beliebiges SQL sowie Insert, Update und Delete ausführen; der Supabase-Node bietet
ebenfalls schreibende Row-Operationen
([n8n PostgreSQL Node](https://docs.n8n.io/integrations/builtin/app-nodes/n8n-nodes-base.postgres/),
[n8n Supabase Node](https://docs.n8n.io/integrations/builtin/app-nodes/n8n-nodes-base.supabase/)).
Deshalb soll n8n nicht den Suchpfad oder Migrationen steuern. Es ist später gut
für Benachrichtigungen, genehmigte Exporte oder externe Folgeprozesse, jeweils
mit einem technisch auf genau die erlaubte RPC begrenzten Credential.

### Caching und Sync

Der vorhandene
[Vergleich von Readyset, Zero und Electric](supabase-partner-readyset-zero-electric.md)
bleibt gültig: Keines der Produkte reduziert die SQL-, Vertrags- oder
Testarbeit von Release 1. Readyset ist nur bei später gemessener hoher
Wiederholungsrate ein Cache-Kandidat; Zero und Electric gehören zu einer
späteren eigenen Live-Web-Oberfläche, nicht in den MCP-Suchpfad.

## Minimaler stufenweiser Zielprozess

### Stufe 0: jetzt, ohne Stack- oder Datenbankumbau

1. Read-only Discovery nach bestehendem Gate abschließen.
2. Genau einen kanonischen JSON-Filter, Ergebnisvertrag und die feste
   `search_candidates_v1`-Signatur freigeben.
3. KI nur auf lokale, versionierte Projektinformationen und den redigierten
   Schema-Befund anwenden; sie erzeugt SQL-, Migration- und Testentwürfe, keine
   Live-Ausführung.

### Stufe 1: mit dem ersten lokalen Scaffold

1. Supabase CLI und lokale, synthetische Datenbank reproduzierbar herstellen.
2. Jede fachliche DB-Änderung als kleine additive Migration versionieren.
3. Pro Migration automatisch `db reset`, `db lint`, pgTAP-RLS-/RPC-/Grant-Tests,
   Typgenerierung und MCP-Contract-Tests ausführen.
4. KI-Änderungen nur als prüfbaren Diff akzeptieren. Kein Agent erhält einen
   automatischen Produktions-Apply.

### Stufe 2: vor jedem freigegebenen Produktions-Release

1. Migration und Rollback-Plan automatisch prüfen; einen Dry-run erzeugen.
2. Kontrollierte `EXPLAIN`-Tests gegen repräsentative Datenverteilung ausführen;
   `EXPLAIN ANALYZE` nur für sichere `SELECT`-Abfragen.
3. Performance/Security Advisors und `index_advisor` auswerten.
4. Erst nach bestandenem Gate und ausdrücklicher Freigabe deployen.

### Stufe 3: nach dem Start

1. `pg_stat_statements`, Supabase Reports, Advisors und Metrics API automatisch
   in einem read-only Stunden-/Tageslauf auswerten. Supabase dokumentiert solche
   Health-, Security-, Performance- und Capacity-Agenten ausdrücklich
   ([Supabase Observability](https://supabase.com/docs/guides/observability)).
2. Nur bei einer relevanten Abweichung melden; niemals Empfehlungen automatisch
   anwenden.
3. Nach vier bis acht Wochen echten Workloads pganalyze testweise zuschalten.
   Nur behalten, wenn es gegenüber der nativen Kette messbar mehr Probleme früher
   erkennt oder Optimierungszeit spart.
4. pgMustard für seltene schwierige Einzelpläne verwenden. Bytebase erst bei
   wachsendem Team oder hohem Migrationsvolumen; n8n erst für externe
   Folgeprozesse.

## Konkrete Stop-Regeln

- Kein Text-to-SQL-Werkzeug wird Teil des Runtime-MCP oder erhält eine Funktion
  zum Ausführen frei generierter SQL-Strukturen.
- Kein Advisor, Agent oder Partner legt automatisch Produktionsindizes an oder
  führt Migrationen ohne separates Apply-Gate aus.
- Keine Optimierung wird allein aufgrund geschätzter Planner-Kosten akzeptiert;
  sie braucht einen reproduzierbaren Vorher-/Nachher-Test.
- n8n, InsightBase und generische Postgres-MCPs dürfen die feste RPC-Allowlist
  nicht umgehen.
- Caches, Replicas, Suchmaschinen und neue Workflow-Runtimes werden erst nach
  einem gemessenen Engpass eingeführt.

## Kosten-, Lock-in- und Betriebsurteil

- **Niedrigste Kosten und geringster Lock-in:** Supabase CLI, PostgreSQL,
  pgTAP, `plpgsql_check`, `pg_stat_statements`, `EXPLAIN` und versionierte SQL-
  Migrationen. Der Kern bleibt Standard-PostgreSQL.
- **Höchster sofortiger Schreibgewinn:** Supabase AI Assistant oder ein lokaler
  Agent mit offiziellen Supabase-Prompts, abgesichert durch die native
  Testkette.
- **Höchster späterer Betriebsgewinn:** pganalyze, wenn der reale Workload die
  monatlichen Kosten und den Collector rechtfertigt.
- **Preiswerte Einzelfallhilfe:** pgMustard.
- **Zu früh:** Bytebase, InsightBase, n8n im Datenbankkern sowie Readyset, Zero
  und Electric.

## Verbleibende Lücken

- Ohne abgeschlossenes Schema- und Index-Discovery kann keine konkrete Query,
  RPC oder Indexkombination bewertet werden.
- Die geschätzten 200.000 Kandidaten und die reale Query-Verteilung sind nicht
  auditiert.
- Es gibt derzeit keinen freigegebenen Anwendungsstack, kein repräsentatives
  Lastprofil und keine festgelegten SLOs.
- Der vorhandene lokale Bericht
  [Werkzeugempfehlung ohne Umbau](werkzeugempfehlung-verifikation-ohne-umbau.md)
  dokumentiert eine nicht einsatzbereite Supabase-CLI-Installation und weitere
  lokale Toollücken. Diese technische Störung wurde in dieser reinen
  Webrecherche nicht erneut diagnostiziert.
- InsightBase-Preise und aktueller Hersteller-Support konnten nicht aus einer
  erreichbaren Herstellerquelle verifiziert werden.

## Schlussentscheidung

Für diesen Use Case ist **mehr Automatisierung durch eine geschlossene
Qualitätskette** besser als die frühe Einführung vieler Einzelprodukte. Platz 1
und 2 werden zusammen aufgebaut: Die KI schreibt den ersten Entwurf, die lokale
Supabase-/PostgreSQL-Kette beweist ihn automatisch. Platz 3 beobachtet später den
echten Workload. Dadurch entfällt der größte Teil der manuellen SQL-, Test- und
Diagnosearbeit, während Runtime-Vertrag, Suchqualität und Produktionsfreigabe
unverändert kontrolliert bleiben.
