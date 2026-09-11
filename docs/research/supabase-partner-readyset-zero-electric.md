# Recherche: Readyset, Rocicorp Zero und Electric mit Supabase

Datum: 2026-09-11

Status: Entscheidungsgrundlage aus aktuellen Primärquellen; keine
Datenbankverbindung, Installation, Migration oder externe Änderung

## Fragestellung und Projektgrenzen

Geprüft wurden drei Einträge aus dem Supabase-Partnerkatalog: Readyset,
Rocicorp Replicache beziehungsweise dessen Nachfolger Zero und Electric. Die
Bewertung fragt nicht nur, ob die Produkte technisch mit Supabase funktionieren,
sondern ob sie den geplanten Release 1 des CRM-Such-MCPs vereinfachen oder nach
einem gemessenen Engpass sinnvoll optimieren können.

Maßgeblich bleiben der [Projektstatus](../project.md), der
[Implementierungsbrief](../SUPABASE_CRM_MCP_IMPLEMENTATION_BRIEF.md),
[ADR-0001](../decisions/0001-controlled-query-boundary.md) und
[ADR-0003](../decisions/0003-separated-profile-administration-mcp.md): Das LLM
erzeugt keinen beliebigen SQL-Code, PostgreSQL entscheidet über Filterung,
Ranking, Autorisierung und Keyset-Pagination, pro Seite werden höchstens 50
Kandidaten ausgegeben, Release 1 liefert keine Kontaktdaten und der spätere
Profilverwaltungs-MCP bleibt eine getrennte Vertrauensgrenze. Schema-, RLS- und
Tenant-Fakten sind weiterhin `DURCH DISCOVERY ZU PRÜFEN`.

## Kurzurteil

**Keines der drei Produkte vereinfacht den geplanten Release 1.** Alle ergänzen
einen bestehenden, bereits autorisierten Datenpfad; keines ersetzt den
validierten JSON-Filter, die kontrollierte PostgreSQL-Funktion, RLS/Tenant-
Prüfungen oder die mehrsprachige Suchlogik. Für den aktuellen Governance- und
Discovery-Stand würde jedes Produkt zusätzliche Infrastruktur, Datenkopien,
Berechtigungen und Betriebsrisiken einführen, bevor ein passender Engpass
nachgewiesen ist.

<!-- markdownlint-disable MD013 -->

| Produkt | Was es tatsächlich optimiert | Urteil für Release 1 |
| --- | --- | --- |
| Readyset | Wiederholte identische oder ähnlich parametrisierte SQL-Leseabfragen | **Nicht jetzt.** Ein späterer Benchmark-Kandidat, vorzugsweise zunächst als shallow Cache, falls `pg_stat_statements` eine hohe Wiederholungsrate und relevante DB-Last belegt. |
| Zero | Sofortige, reaktive Browser-UX mit lokaler Datenhaltung und optimistischen Writes | **Nein.** Passt zu einer späteren eigenen Web-App, nicht zu ChatGPT/Claude/Codex als MCP-Clients. |
| Electric | Live-Verteilung autorisierter Tabellen-Ausschnitte über HTTP/CDN in lokale Apps und Services | **Nein.** Kann später Live-Dashboards oder Katalogansichten bedienen, vereinfacht aber keine dynamische, gerankte Kandidatensuche. |

<!-- markdownlint-enable MD013 -->

Die drei Produkte lösen auch nicht die fachliche Mehrsprachigkeit. Taxonomie,
B/H/S-, DE- und EN-Normalisierung, FTS/Trigramm-Eignung und Ranking bleiben
PostgreSQL- beziehungsweise Anwendungsentscheidungen, die nach Discovery mit
echten, kontrollierten Suchfällen gemessen werden müssen.

## Der Partnerkatalog ist kein aktueller technischer Vertrag

Supabase erklärt selbst, dass Partnerkatalog-Einträge Drittanbieter-
Integrationen sind und die zugehörigen Integrationen und Dokumentationen von den
Partnern verwaltet werden. Der Katalog nennt eine PostgreSQL-Verbindung nur als
eine mögliche Integrationsfläche
([Supabase Partner Catalog](https://supabase.com/docs/guides/integrations/partner-catalog)).

Zwei Abweichungen sind für diese Entscheidung wesentlich:

- Die [Readyset-Katalogseite](https://supabase.com/partners/integrations/readyset)
  verlangt ein Support-Ticket für `prep_readyset()`, IPv4, eine direkte
  Verbindung ohne Pooler und zwei besondere Start-Flags. Die aktuelle
  [Readyset-Supabase-Anleitung](https://readyset.io/docs/cache/connect/cloud-databases/supabase)
  beschreibt dagegen RDST und erlaubt je nach Modus Transaction Pooler, Session
  Pooler oder Direct Connection; nur die direkte Verbindung benötigt wegen
  Readysets unvollständiger IPv6-Unterstützung das IPv4-Add-on. `prep_readyset()`
  erscheint dort nicht. Daher darf die Kataloganleitung nicht ungeprüft als
  heutiger Standard in den Projektplan übernommen werden.
- Der Supabase-Katalog beschreibt weiterhin
  [Replicache](https://supabase.com/partners/integrations/replicache). Die
  aktuelle Zero-Dokumentation bezeichnet Replicache als Vorgänger von Zero
  ([Zero: What is Sync?](https://zero.rocicorp.dev/docs/sync)); das öffentliche
  [Replicache-Repository](https://github.com/rocicorp/replicache) wurde am
  10. Juni 2026 archiviert. Für eine neue Architektur ist deshalb Zero und nicht
  Replicache zu bewerten.

## 1. Readyset

### Readyset-Funktion

Readyset ist ein PostgreSQL-/MySQL-wire-kompatibler SQL-Proxy. Nicht gecachte
Abfragen werden zur Ursprungsdatenbank weitergereicht. Aktuell existieren zwei
Cachearten
([Caching Queries](https://readyset.io/docs/cache/cache)):

- **Deep Cache:** erstellt einen inkrementell gepflegten Datenfluss aus einem
  initialen Snapshot und dem Logical-Replication-Stream.
- **Shallow Cache:** hält das Ergebnis einer parametrisierten Abfrage bis zum
  TTL-Ablauf im Speicher; dafür sind weder Snapshot noch Logical Replication
  nötig und mehr SQL-Strukturen werden unterstützt.

Die Anwendung muss ihren SQL-Verkehr durch Readyset leiten und die gewünschten
Queries explizit cachen oder einen automatischen Modus aktivieren. Damit bleibt
die fachliche Abfrage unverändert, aber es entsteht ein zusätzlicher Proxy-
Hop samt Cache- und Benutzerverwaltung
([Readyset Cache](https://readyset.io/docs/cache)).

### Readyset-Voraussetzungen und Grenzen

- Die aktuelle Supabase-Anleitung ist ausdrücklich für lokale oder
  Test-Deployments mit Docker gedacht. Sie unterstützt Pooler-Verbindungen; eine
  Direct Connection setzt wegen Readysets IPv6-Grenze das Supabase-IPv4-Add-on
  voraus
  ([Readyset mit Supabase](https://readyset.io/docs/cache/connect/cloud-databases/supabase)).
- Deep Caching verlangt PostgreSQL 13+, Logical Replication und nach der
  aktuellen Installationsdokumentation einen Superuser. Die Supabase-
  Unterstützung wird dort als **Alpha** geführt. Shallow Caching benötigt nur
  normalen Lesezugriff
  ([Readyset-Installation](https://readyset.io/docs/cache/install-rs)).
- Deep Caching unterstützt RLS-geschützte Tabellen nicht. Shallow Caching kann
  eine enge, auf Supabase/PostgREST zugeschnittene Teilmenge von RLS-Policies
  analysieren und relevante Sessionwerte in den Cache-Key aufnehmen; nicht
  sicher analysierbare Policies oder `SECURITY DEFINER`-Funktionen werden nicht
  gecacht. Policyänderungen werden standardmäßig nur alle 60 Sekunden erkannt
  und ein anhaltend fehlschlagender Poll lässt den letzten Katalogstand bestehen
  ([Readyset RLS](https://readyset.io/docs/concepts/shallow-caching/row-level-security)).
- Shallow Cache Authorization prüft Tabellen-Grants separat, aber Änderungen an
  Grants können standardmäßig bis zu fünf Minuten verzögert wirksam werden.
  Außerdem zeigt `SHOW CACHES` die Query-Texte auch Nutzern, die die zugrunde
  liegenden Tabellen nicht lesen dürfen
  ([Cache Authorization](https://readyset.io/docs/reference/cache-authorization)).
- Der Deep-Cache-SQL-Umfang ist eingeschränkt: unter anderem keine
  `UNION`/`INTERSECT`/`EXCEPT`, nur begrenzte Join- und Parameterformen und laut
  aktueller Seite keine PostgreSQL-Schema-Namespaces. Das ist für die bereits
  bekannten logischen Projektbereiche `crm`, `crm_api` und `crm_auth` ein
  besonders relevantes Kompatibilitätsrisiko
  ([Supported Queries](https://readyset.io/docs/concepts/deep-caching/queries)).

Ob die spätere kontrollierte `search_candidates_v1`-Funktion überhaupt gecacht
werden kann, ist deshalb **nicht belegt**. Vor jeder Entscheidung müsste die
konkrete, nach Discovery entwickelte Query mit `EXPLAIN CREATE CACHE` beziehungsweise
`EXPLAIN CACHE SUPPORT` geprüft werden. Ein Cache-Treffer ist zudem nur dann
wahrscheinlich, wenn dieselben Filterparameter häufig wiederkehren; eine große
Zahl individueller Suchkombinationen und benutzerbezogener RLS-Keys fragmentiert
den Cache.

### Readyset-Nutzen für den CRM-MCP

Readyset ist der einzige der drei Kandidaten mit einem plausiblen späteren
Performance-Pfad: wiederkehrende Standardlisten, populäre Suchprofile oder
Dashboards könnten nachweisbar Datenbanklast erzeugen. Es vereinfacht den
Release jedoch nicht, weil es Auth-Kontext, Query-Kompatibilität, TTL/Policy-
Staleness, Cache-Metriken, Failover und eine weitere Kopie sensibler Ergebnisse
beherrschbar machen muss.

Empfehlung: erst den direkten PostgreSQL-/RPC-Baseline-Pfad bauen, passende
Indizes und Keyset-Pagination messen und `pg_stat_statements` auswerten. Nur wenn
ein reproduzierbarer Lasttest einen Cache-Bedarf zeigt, Readyset in einer
isolierten Umgebung gegen exakt den kontrollierten RPC-Pfad benchmarken. Wegen
RLS und Least Privilege zunächst shallow statt deep prüfen; Deep Cache ist für
den derzeitigen Sicherheitsentwurf kein Default.

### Readyset-Reife und Kosten

Readyset Community ist selbst gehostet und kostenlos, aber unter BSL 1.1
source-available; der Code wechselt nach vier Jahren zu Apache 2.0. Readyset
Cloud beginnt laut aktueller Preisseite bei 199 USD pro Monat und bis zu zehn
Queries. Private/BYOC ist individuell bepreist
([Readyset Pricing](https://readyset.io/pricing),
[Readyset Repository](https://github.com/readysettech/readyset)). Die Alpha-
Kennzeichnung der Supabase-Unterstützung ist für Produktionsdaten wichtiger als
die allgemeine PostgreSQL-GA-Angabe.

## 2. Rocicorp Zero und Replicache

### Zero-Funktion

Zero ist ein Sync-System für Web-Anwendungen. `zero-cache` hält eine SQLite-
Replica, beantwortet reaktive ZQL-Queries und synchronisiert ausgewählte Daten
in lokale Browser-Speicher. Mutationen verändern den lokalen Zustand sofort und
werden anschließend über einen anwendungseigenen `/mutate`-Endpoint nach
PostgreSQL geschrieben; ein `/query`-Endpoint transformiert und autorisiert
Leseabfragen
([Zero Installation](https://zero.rocicorp.dev/docs/install),
[Self-Hosting Zero](https://zero.rocicorp.dev/docs/self-host)).

Replicache war der allgemeinere Client-Sync-Vorgänger. Für Neuentwicklung ist
Zero die aktive Linie; der archivierte Replicache-Pfad sollte nicht als neue
Abhängigkeit eingeführt werden.

### Zero-Voraussetzungen und Grenzen

- Zero benötigt PostgreSQL 15+ und Logical Replication. `ZERO_UPSTREAM_DB` muss
  bei Supabase eine Direct Connection sein. Für `ZERO_CVR_DB` und
  `ZERO_CHANGE_DB` empfiehlt Rocicorp den Session Pooler; der Transaction Pooler
  kann benannte Prepared Statements brechen
  ([Connecting to Postgres](https://zero.rocicorp.dev/docs/connecting-to-postgres)).
- Auf Supabase ist bei IPv4-only Hosting das kostenpflichtige IPv4-Add-on nötig.
  Supabase-HA-Failover wird derzeit nicht unterstützt; nach einer Promotion muss
  Zero vollständig neu synchronisieren. Publikationsänderungen brauchen wegen
  fehlender DDL-Events einen expliziten Schema-Change-Hook
  ([Zero: Supabase notes](https://zero.rocicorp.dev/docs/connecting-to-postgres#supabase)).
- Standardmäßig publiziert Zero alle Tabellen im `public`-Schema an
  `zero-cache`. Eine eigene Publication kann Tabellen und Spalten begrenzen.
  Client-Permissions begrenzen derzeit Tabellen und Zeilen, aber noch nicht
  einzelne Spalten; dafür muss die Publication Kontaktdaten bereits ausschließen
  ([Supported Postgres Features](https://zero.rocicorp.dev/docs/postgres-support#limiting-replication)).
- Zero übernimmt Supabase-RLS nicht als Endnutzer-Autorisierung. Die aktuelle
  Dokumentation sagt ausdrücklich, dass Zero kein First-Class-RLS-System nutzt;
  Authentifizierung und Berechtigungsfilter werden in den eigenen Query- und
  Mutate-Endpunkten mit einem `Context` implementiert
  ([Zero Authentication](https://zero.rocicorp.dev/docs/auth#permission-patterns)).
- Standardmäßig verbleiben synchronisierte Daten nach Logout auf dem Gerät und
  können auf gemeinsam genutzten Rechnern von anderen lokalen Benutzern gelesen
  werden. In-Memory Storage verhindert Persistenz, verliert aber den wesentlichen
  Offline-/Warmstart-Vorteil
  ([Zero Authentication](https://zero.rocicorp.dev/docs/auth#set-userid-on-client)).

Logical Replication ist außerdem keine per-App-User-RLS-Grenze: Berechtigungen
werden am Publisher beim Start der Replikationsverbindung geprüft, nicht für
jeden späteren Change Record oder Browsernutzer. Publications müssen daher
explizit eingeschränkt und der Zugriff hinter Zero erneut autorisiert werden
([PostgreSQL Logical Replication Security](https://www.postgresql.org/docs/current/logical-replication-security.html)).

### Zero-Nutzen für den CRM-MCP

Zero optimiert eine eigene interaktive Browser-App, nicht einen serverseitigen
MCP-Tool-Call. ChatGPT, Claude, Codex und Grok können die lokale Zero-Replica
nicht als gemeinsamen transparenten Cache nutzen. Der geplante MCP besitzt
bereits einen kontrollierten Query-Endpunkt; Zero würde zusätzlich
`zero-cache`, Replica, CVR-/Change-Storage, Query-/Mutate-API, eine zweite
Berechtigungsimplementierung und Client-Datenlöschung einführen.

Empfehlung: für Release 1 nicht einsetzen. Zero kann später separat evaluiert
werden, falls ein eigenes Recruiting-Web-Frontend mit kollaborativer, sofortiger
UI und optimistischen Änderungen beschlossen wird. Dann muss es einen eigenen
Privacy-/Security-Gate erhalten; insbesondere dürfen Kontaktspalten nie in der
Publication landen und lokale Datenretention muss verbindlich geregelt sein.

### Zero-Reife und Kosten

Zero Client und Server sind Apache-2.0-lizenziert und selbst hostbar
([Zero Open Source](https://zero.rocicorp.dev/docs/open-source)). Die aktuellen
Self-Hosting-Beispiele verwenden Version 1.9.0. Cloud Zero kostet laut aktueller
Seite 30 USD/Monat für Hobby, 300 USD/Monat für Professional oder ab 1.000
USD/Monat plus AWS für BYOC
([Zero Pricing](https://zero.rocicorp.dev/#pricing)). Der offene Code ändert
nichts am erheblichen zusätzlichen Betriebsumfang.

## 3. Electric

### Electric-Funktion

Electric ist in der aktuellen Generation primär **Read-Path-Sync**. Ein Dienst
liest PostgreSQL über Logical Replication und stellt `Shapes` per HTTP bereit.
Eine Shape ist derzeit eine unveränderliche Teilmenge einer einzelnen Tabelle,
definiert durch optionale `where`-, `columns`- und `queryable_columns`-Angaben;
Subqueries können Beziehungen für die Auswahl berücksichtigen
([Electric Shapes](https://electric.ax/docs/sync/guides/shapes)).

Electric implementiert keinen eingebauten Write-Path. Writes laufen weiterhin
über die bestehende API oder einen anderen anwendungsspezifischen Mechanismus
und erscheinen anschließend über den Replikationsstrom
([Electric Writes](https://electric.ax/docs/sync/guides/writes)). Das bestätigt
die Grundbeschreibung des Nutzers, bedeutet aber auch: Electric ersetzt keine
Supabase-RPC-, Edge-Function- oder MCP-Autorisierung.

### Electric-Voraussetzungen und Grenzen

- Electric benötigt die Supabase-Direct-Connection, weil Pooler Logical
  Replication nicht unterstützen. Der Dienst muss IPv6-fähig laufen; alternativ
  ist auf Pro/Team das Supabase-IPv4-Add-on nötig
  ([Electric mit Supabase](https://electric.ax/docs/sync/integrations/supabase)).
- Für strenge Umgebungen existiert ein manueller Modus: eine dedizierte Rolle
  erhält `REPLICATION` und `SELECT` nur auf expliziten Tabellen, während ein DBA
  Publication und `REPLICA IDENTITY FULL` vorkonfiguriert. Der automatische
  Modus benötigt zusätzlich `CREATE` und Tabelleneigentum
  ([Electric PostgreSQL Permissions](https://electric.ax/docs/sync/guides/postgres-permissions)).
- Electrics HTTP-API ist standardmäßig öffentlich und stellt alle Daten bereit,
  die der Datenbankbenutzer lesen kann. Produktion muss sie per API-Token,
  Netzwerkgrenzen und vor allem einem autorisierenden Proxy absichern
  ([Electric Security](https://electric.ax/docs/sync/guides/security)).
- Die empfohlene Autorisierung liegt vor Electric: Proxy oder Gatekeeper prüft
  Credentials und setzt Tabellen-, Spalten- und parametrisierte `where`-
  Beschränkungen serverseitig. PostgreSQL-RLS wird damit nicht automatisch zum
  Shape-Zugriffsvertrag
  ([Electric Auth](https://electric.ax/docs/sync/guides/auth)).

Die lokale oder serverseitige Shape-Replica ist eine zusätzliche Kopie der
publizierten Kandidatendaten. `REPLICA IDENTITY FULL` kann zudem alle Spaltenwerte
für Updates in den WAL-Stream aufnehmen. Für echte Kandidatendaten sind daher
Publication-Allowlist, Spaltenminimierung, Verschlüsselung, Retention,
Löschung und Processor-/DPA-Prüfung vor jedem POC zwingend.

### Electric-Nutzen für den CRM-MCP

Electric passt gut zu vielen Lesern derselben Live-Liste oder desselben
Katalogausschnitts: HTTP ermöglicht CDN-Caching und Request Collapsing. Die
geplante Kandidatensuche ist jedoch eine dynamische, autorisierte, mehrtabellige
Filter-/Ranking-Funktion mit maximal 50 Ergebnissen und Keyset-Cursor. Eine
einzelne unveränderliche Tabellen-Shape ist dafür kein Ersatz. Ein
autorisierender Proxy müsste die kontrollierte Query-Grenze praktisch erneut
implementieren; dadurch wird Release 1 komplexer statt einfacher.

Empfehlung: für Release 1 nicht einsetzen. Später nur für eine klar getrennte
Live-Ansicht prüfen, wenn viele gleichzeitige Nutzer tatsächlich dieselben,
bereits minimierten und autorisierten Ausschnitte lesen. Keine Shape darf
Kontakt- oder CV-Inhalte allein deshalb replizieren, weil sie in einer
Quelltabelle vorhanden sind.

### Electric-Reife und Kosten

Electric ist Apache-2.0-lizenziert. Die aktuelle Release-Seite zeigt den
TypeScript-Client 1.5.x; ein behobenes SQL-Injection-Advisory verlangt bei
Self-Hosting mindestens Electric 1.5.0
([Electric Releases](https://github.com/electric-sql/electric/releases),
[GHSA-h5rg-pxx7-r2hj](https://github.com/electric-sql/electric/security/advisories/GHSA-h5rg-pxx7-r2hj)).
Electric Cloud berechnet im PAYG-Tarif 1 USD pro Million Writes und 0,10 USD pro
GB-Monat Retention; Postgres Sync kostet zusätzlich 2 USD pro Million
ausgegebenen Shape-Log-Writes. Pro beginnt bei 249 USD/Monat, Scale bei 1.999
USD/Monat
([Electric Pricing](https://electric.ax/pricing)).

## Sicherheitsvergleich

<!-- markdownlint-disable MD013 -->

| Thema | Readyset | Zero | Electric |
| --- | --- | --- | --- |
| Zusätzliche Datenkopie | Shallow: gecachte Resultate; Deep: Tabellen-Snapshot und inkrementelle Datenstruktur | Vollständige serverseitige Replica der Publication plus ausgewählte Daten auf Clients | Publication/Shape-Daten im Sync-Dienst und typischerweise in lokalen Clients oder Services |
| Verhältnis zu Supabase RLS | Shallow unterstützt nur eine enge Policy-Grammatik mit Polling; Deep unterstützt RLS-Tabellen nicht | Eigene Query-/Mutate-Autorisierung; Supabase-RLS ist kein Client-Vertrag | Eigener Auth-Proxy/Gatekeeper; HTTP-API ist sonst öffentlich |
| Kontaktfreiheit Release 1 | Ergebnisprojektion und Cache-Key müssen geprüft werden | Spalten bereits in der Publication ausschließen | Spalten in Shape und Publication minimieren |
| Hauptbetriebsrisiko | Cache-/Policy-Staleness, SQL-Kompatibilität, Proxy und Alpha-Supabase-Support | HA-Resync, doppelte Autorisierung, Client-Retention, mehrere State-Stores | Öffentliche Default-API, Publication/Replica, Proxy-Auth und Shape-Lifecycle |

<!-- markdownlint-enable MD013 -->

Bei allen drei Varianten wird ein Drittprodukt zu einem neuen Speicher- und
Verarbeitungssystem für sensible personenbezogene Daten. Eine Partnerlistung ist
keine Datenschutz-, Security- oder Produktionsfreigabe. Vor einem späteren POC
sind mindestens Datenfluss, Hostingregion, Verschlüsselung, Backups, Retention,
Löschung, Incident Response, DPA/Subprozessoren, Least-Privilege-Rolle,
Publication-Allowlist und negative Tenant-/Kontakt-Tests separat zu genehmigen.

## Empfohlene Entscheidung

1. **Release 1 unverändert lassen:** validierter JSON-Filter, eine kontrollierte
   PostgreSQL-Funktion/RPC, RLS/Grants, Keyset-Pagination und maximal 50
   kontaktfreie Treffer.
2. **Keine der drei Integrationen in die aktuelle Discovery-Phase aufnehmen.**
   Sie beantwortet zunächst Schema, Rechte, RLS, Tenant-Grenzen, Indizes und
   reale Queryformen.
3. **Readyset nur als späteren Performance-Gate-Kandidaten vormerken.** Trigger:
   ein reproduzierbarer Baseline-Lasttest zeigt trotz korrekter Indizes eine
   relevante, wiederholte Leselast. Dann shallow und deep getrennt bewerten;
   deep bleibt wegen Superuser/RLS/Supabase-Alpha besonders kritisch.
4. **Zero nur für ein späteres eigenes Web-Frontend prüfen.** Es ist keine
   Optimierung für generische MCP-Clients und Replicache sollte nicht neu
   eingeführt werden.
5. **Electric nur für einen getrennten Live-Listen-/Dashboard-Use-Case prüfen.**
   Trigger: viele Leser konsumieren denselben stabilen, minimierten Shape und
   CDN-Fan-out ist nachweislich der Engpass.

Damit bleibt die Architektur heute kleiner und sicherer, ohne spätere
Optimierungsmöglichkeiten auszuschließen. Jede spätere Evaluation braucht eine
isolierte Testumgebung ohne reale Kandidatendaten sowie einen eigenen, ausdrücklich
genehmigten Gate; eine Verbindung mit dem bestätigten Produktionsprojekt ist
nicht Bestandteil dieser Recherche.
