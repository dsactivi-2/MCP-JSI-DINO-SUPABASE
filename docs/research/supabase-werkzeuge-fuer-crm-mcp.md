# Recherche: Supabase-Werkzeuge für den CRM-MCP

Datum: 2026-09-11

Status: Recherchegrundlage; Skills und Supabase-Plugin installiert und lokal
abgeglichen; keine Freigabe für Datenbankzugriff, Migration oder Deployment

## Aktuelle Einordnung nach dem Audit

Korrekturstand 2026-09-11: `Always ask` wurde vom Nutzer bestätigt. Der
Developer-MCP bleibt für das Produktionsprojekt mit realen Kandidatendaten
verboten. Das ist die strengere **Projektentscheidung**, keine pauschale
Behauptung über aktuelle Herstellerverbote. Ein späterer Plugin-Test erfordert
separate Nicht-Produktion ohne reale Personendaten; ein solches Projekt ist
nicht geplant. Historische Installations-/Toolbefunde unten sind
Zeitpunktnachweise und wurden in dieser Korrekturrunde nicht erneut geprüft.
Aktuelle Priorität: [Zugangsplan](../discovery/access-plan-consolidated.md) und
[Primärprüfung](2026-09-11-plan-best-practice-verification.md).

## Fragestellung und Projektgrenzen

Geprüft wurde, welche offiziellen Supabase-Empfehlungen, SDKs, MCP- und
AI-Hilfsmittel das Vorhaben konkret erleichtern können. Grundlage waren der
Nutzeranhang, der [Projektstatus](../project.md), der
[Implementierungsbrief](../SUPABASE_CRM_MCP_IMPLEMENTATION_BRIEF.md),
[ADR-0001](../decisions/0001-controlled-query-boundary.md),
[ADR-0002](../decisions/0002-search-design-interview.md),
[ADR-0003](../decisions/0003-separated-profile-administration-mcp.md) und das
[Discovery-Runbook](../runbooks/schema-discovery.md).

Die Bewertung respektiert insbesondere diese Grenzen:

- Das LLM strukturiert nur einen eng validierten JSON-Filter und erzeugt oder
  führt keinen beliebigen SQL-Code aus.
- PostgreSQL bleibt für Filterung, Ranking, Autorisierung und Pagination
  maßgeblich; pro Seite werden höchstens 50 Kandidaten ausgegeben.
- Kandidaten-, CV- und Kontaktdaten werden nicht massenhaft oder ungefiltert an
  ein LLM gesendet. Release 1 gibt keinerlei Kontaktdaten aus.
- Der Runtime-Such-MCP und der spätere Profilverwaltungs-MCP bleiben getrennte
  Vertrauens- und Berechtigungsgrenzen.
- Physische Tabellen, Spalten, RLS- und Tenant-Fakten sind erst durch den
  genehmigten read-only Discovery zu bestätigen.

## Kurzurteil

Mehrere offizielle Supabase-Bausteine helfen deutlich, aber nicht alle erfüllen
dieselbe Aufgabe:

1. **Jetzt sinnvoll:** die beiden installierten offiziellen Agent Skills als
   aktuelle Arbeitsanleitung sowie `search_docs` für öffentliche Dokumentation,
   ohne Projekt- oder Datenbankzugriff.
2. **Installiert, für das produktive CRM ausgeschlossen:** der offizielle
   Supabase-MCP. Nur eine separat freigegebene Nicht-Produktions-Evaluation
   ohne echte Personendaten wäre möglich; aktuell ist sie nicht geplant.
3. **Nach Discovery und Stack-Entscheidung sinnvoll:** Supabase CLI, pgTAP,
   `db lint`, generierte Typen und genau ein zum Runtime-Stack passendes SDK,
   das ausschließlich kontrollierte RPCs aufruft.
4. **Technisch passend, aber noch zu prüfen:** PostgreSQL Full Text Search,
   ein eigener MCP auf Edge Functions. Branching ist keine gewählte
   Umgebung; ein separates gehostetes Staging-Projekt wurde abgelehnt.
5. **Für den Produktiv-Runtime nicht empfehlen:** der offizielle
   Entwickler-MCP, der generische PostgREST-MCP, ein unauthentifizierter
   Edge-Function-MCP oder ein Backend-Client mit Supabase-Secret-Key als Ersatz
   für die geplante RLS-/Tenant-Grenze.

## Verifizierter Installationsstand

Die projektlokalen Verzeichnisse `.agents/skills/supabase/` und
`.agents/skills/supabase-postgres-best-practices/` enthalten die vollständigen
Skills einschließlich Referenzen, Assets und Changelogs. Ihr Inhalt stimmt mit
der vorhandenen Supabase-Community-Distribution überein.

Zwei installierte Plugin-Distributionen zeigen auf denselben offiziellen
Supabase app/MCP. Sie liefern keine zwei Verbindungen, Identitäten oder
Sicherheitsgrenzen. Der aktive Connector konnte mehrere Account-Projekte
auflisten; damit ist die Verbindung nicht auf das CRM-Projekt begrenzt. Eine
read-only Attestation liegt nicht vor. Es wurden bei dieser Prüfung keine
Tabellen, Kandidaten-, Kontakt- oder CV-Daten gelesen und keine Änderung
ausgeführt.

Der frühere Stand war „Allow low-risk actions“; inzwischen hat der Nutzer
„Always ask“ bestätigt. Dies ist allein keine Datenbank-Sicherheitskontrolle;
zusätzlich bleiben ein
wirklicher read-only Datenbankkontext, Projektbindung und minimale Feature-
Gruppen erforderlich.

## Bewertungsübersicht

### Jetzt nutzen

- **`supabase` Agent Skill:** aktuelle Verfahrenshinweise zu Auth, RLS, CLI,
  Logs und Edge Functions. Projektbezogen einsetzen; Projektregeln und
  Freigaben bleiben maßgeblich.
- **`supabase-postgres-best-practices` Agent Skill:** Review-Hilfe für
  Discovery-SQL, Funktionen, Indizes, RLS und Performance. Tatsächliche
  Schemafakten weiterhin durch Discovery belegen.
- **`search_docs`:** aktuelle öffentliche Supabase-Dokumentation lesen. Dieser
  Aufruf greift nicht auf das CRM-Projekt oder seine Daten zu.

### Nach Discovery oder Stack-Entscheidung prüfen

- **Offizieller Supabase-MCP:** nur für eine separat freigegebene isolierte
  Nicht-Produktion ohne echte Personendaten; kein CRM-Produktionszugriff.
- **Advisors:** nach Discovery-Freigabe als deterministische Zusatzbefunde;
  Findings sind keine verifizierte Ursache und kein automatischer Fix.
- **CLI, lokale Instanz und Migrationen:** nach Discovery und Scaffold für
  reproduzierbare Entwicklung und Dry-runs. Keine Remote-Resets, Daten-Dumps
  oder Pushes ohne gesonderte Freigabe.
- **pgTAP und `supabase db lint`:** nach Scaffold für RLS-, RPC- und
  Contract-Tests sowie PL/pgSQL-Prüfungen in einer isolierten Umgebung.
- **`supabase gen types`:** nach Schema-Mapping für exponierte Tabellen, Views
  und RPCs; unerwünschte PII-Flächen nicht als Anwendungs-API typisieren.
- **`@supabase/supabase-js` oder `supabase-py`:** nach Stack-Entscheidung genau
  ein SDK für Auth-Kontext und kontrollierte RPC-Aufrufe wählen.
- **Database Functions/RPC:** nach Discovery als Kern der Query-Grenze nutzen.
  `security invoker` und explizite Function-Rechte bevorzugen.
- **Full Text Search:** nach Discovery auf B/H/S, DE und EN benchmarken, nur
  nach deterministischen Filtern und nicht als Ersatz für kontrollierte IDs.
- **Branching:** nach Schema-Baseline als isolierte, standardmäßig datenlose
  Testumgebung prüfen. Kopierte Produktionsdaten wie Produktion schützen.
- **Edge-Function-MCP:** nach Discovery nur als POC. Der offizielle Guide ist
  unauthentifiziert; interoperable Auth und RLS müssen vor Produktion bewiesen
  sein.
- **`@supabase/server` (Public Beta):** nach Stack-Entscheidung für
  Edge-Function-Auth prüfen. Benutzer-JWT kann RLS erhalten; Secret-Modus
  liefert
  privilegierten Zugriff. Den Beta-Status vor einer Produktionsentscheidung neu
  bewerten.

### Nicht empfehlen

- **Installierten Live-MCP vor dem Gate verwenden:** Die Installation und ein
  sichtbares Tool sind keine Freigabe. Account-weite Projekt-, Schema-, SQL-,
  Advisor-, Log- oder Datenaufrufe bleiben blockiert.
- **Beide Plugin-Distributionen als Schutzschichten behandeln:** Sie verwenden
  denselben app/MCP und schaffen weder least privilege noch Trust-Trennung.
- **Self-hosted `@supabase/mcp-server-supabase` als Produkt-MCP:** Es fügt
  keine CRM-Fachtools hinzu und bleibt eine breite Entwicklerschnittstelle.
- **`@supabase/mcp-server-postgrest`:** Generisches CRUD und SQL-zu-REST
  widersprechen Tool-Allowlist, SQL-Sperre und kontrollierter RPC-Passage.
- **`mcp-lite` als Default:** Edge-kompatibel, aber keine Sicherheitslösung.
  Für dieses Projekt zuerst das offizielle MCP-SDK evaluieren.
- **Reflex:** Löst weder MCP-Auth, Query-Grenze noch Discovery; der UI-Stack ist
  offen.
- **Vektorsuche jetzt:** Weder `pgvector` noch Vector Buckets vorziehen. Erst
  erwägen, wenn strukturierte Filter, Taxonomie, FTS und Trigramme einen
  gemessenen Qualitätsbedarf nicht erfüllen.

<!-- markdownlint-disable-next-line MD013 -->
## 1. Offizieller Supabase-MCP: gutes internes Discovery-Werkzeug, falscher Runtime

Der Anhang liegt mit seiner Kernaussage richtig: Der offizielle MCP lässt sich
über Projektbindung, read-only Modus und Feature-Gruppen einschränken, aber
nicht
in einen eigenen CRM-MCP mit eigenen Werkzeugnamen umbauen. Das offizielle
Repository bestätigt außerdem, dass `readOnly` mutierende Werkzeuge aus den
statischen Tool-Schemas entfernt. Self-hosting stellt dieselben
Supabase-Plattformwerkzeuge über einen eigenen HTTP-Endpunkt bereit; es macht
daraus keine fachliche Kandidatensuche
([Supabase MCP Docs](https://supabase.com/docs/guides/ai-tools/mcp),
[offizielles MCP-Repository](https://github.com/supabase/mcp)).

Für dieses Projekt ist die wichtigere Präzisierung: Supabase bezeichnet diesen
MCP ausdrücklich als internes Entwicklerwerkzeug und warnt davor, ihn Kunden
oder Endnutzern zu geben. Die Werkzeuge laufen im Kontext von
Entwicklerberechtigungen; Prompt Injection bleibt trotz Schutztexten in
Tool-Ergebnissen möglich. Supabase empfiehlt manuelle Freigabe jedes Tool-Calls
sowie Projektbindung, read-only und minimale Feature-Gruppen
<!-- markdownlint-disable-next-line MD013 -->
([Supabase MCP: Sicherheitsrisiken und Empfehlungen](https://supabase.com/docs/guides/ai-tools/mcp#security-risks)).

Die folgende generische technische Checkliste gilt nur für einen zulässigen
Nicht-Produktions-Engineering-Pfad; sie öffnet keinen produktiven CRM-Zugriff:

- erst nach Erfüllung der Voraussetzungen des Discovery-Runbooks;
- nur für genau das bestätigte Projekt;
- mit `read_only=true` und ausschließlich benötigten Gruppen;
- mit vorher geprüfter SQL-Allowlist und kleinstmöglichen Ergebnissen;
- ohne Roh-CVs, Kontakte, Geheimnisse oder breite Kandidatenresultate;
- mit manueller Prüfung der erzeugten Tool-Calls und Ausgaben.

Der vorhandene Gate B ist technisch an genau einen lokalen `psql`-Prozess,
streambare Query-Grenzen, feste SQL-Hashes, keine Retries und einen externen
Restricted-Raw-Pfad gebunden. Der installierte MCP erfüllt diese nachgewiesenen
Launcher-Eigenschaften nicht automatisch. Er beschleunigt daher das aktuelle
Gate-B-Verfahren nicht; ein alternativer MCP-Pfad benötigt eine neue Gate-
Version und eigene Tests.

Der produktive Runtime-Such-MCP bleibt dagegen der eigene Drei-Tool-Vertrag aus
dem Brief. Auch der spätere Profilverwaltungs-MCP bleibt separat.

## 2. Offizielle Agent Skills: der unmittelbar nutzbare Gewinn

Supabase veröffentlicht zwei Agent Skills. `supabase` deckt Produkte,
Authentifizierung, RLS, CLI, MCP, Logs und Debugging ab.
`supabase-postgres-best-practices` ist ausdrücklich für Schema, Migrationen,
RLS, Indizes, Funktionen, Performance und `EXPLAIN` gedacht. Skills benötigen
keine Live-Verbindung zum Projekt und können projektbezogen installiert werden
([Supabase Agent Skills](https://supabase.com/docs/guides/ai-tools/ai-skills)).

Das ist für die aktuelle Governance-/Discovery-Vorbereitung die risikoärmste
Erleichterung: Die Skills können beim Review der bereits entworfenen
Discovery-Abfragen und späterer DB-Entwürfe helfen, ohne Zugangsdaten oder
Produktionsdaten an ein Tool zu binden.

Der offizielle Supabase Plugin bündelt beide Skills mit dem Live-MCP. Diese
Bequemlichkeit ist erst sinnvoll, wenn Projektbindung, read-only Modus,
Feature-Gruppen und Zugriffsfreigabe beschlossen sind. Da der Plugin inzwischen
installiert ist, bleiben seine Live-Werkzeuge bis dahin unbenutzt; die Skills
werden weiterhin separat und projektlokal geladen
<!-- markdownlint-disable-next-line MD013 -->
([Supabase Plugin für AI Coding Agents](https://supabase.com/docs/guides/ai-tools/plugins)).

## 3. CLI, Advisors, pgTAP und generierte Typen

Nach Discovery und Einrichtung einer isolierten Entwicklungsumgebung kann die
Supabase CLI vier wiederkehrende Aufgaben vereinfachen:

- lokale Supabase-Instanz und reproduzierbare Migrationen;
- `supabase db push --dry-run` vor einem gesondert genehmigten Apply;
- `supabase test db` für pgTAP-Tests und `supabase db lint` für
  PL/pgSQL-Prüfungen;
- `supabase gen types` für typisierte Tabellen, Views und gespeicherte
  Funktionen.

Die offizielle Workflow-Dokumentation verlangt Review erzeugter Migrationen und
weist darauf hin, dass lokale Resets destruktiv sind; ein verknüpfter
Remote-Reset
löscht die Remote-Schemaobjekte und ist nur für Development/Staging gedacht
<!-- markdownlint-disable-next-line MD013 -->
([Local Development Workflow](https://supabase.com/docs/guides/local-development/cli-workflows),
<!-- markdownlint-disable-next-line MD013 -->
[Testing and Linting](https://supabase.com/docs/guides/local-development/cli/testing-and-linting),
[Generating Types](https://supabase.com/docs/guides/api/rest/generating-types)).

Advisors sind bereits während des genehmigten Audits nützlich. Sie liefern
deterministische Checks unter anderem für fehlende Foreign-Key-Indizes,
deaktiviertes oder unvollständiges RLS, `security definer` Views, veränderbaren
Function-`search_path`, exponierte sensible Spalten und ausführbare
privilegierte
Funktionen. Supabase stellt dieselben Checks in Studio, über MCP
`get_advisors`, CLI `supabase db advisors` und Management API bereit. Die Docs
betonen jedoch, dass ein Finding kein Fix ist und gegen aktuelle Evidenz geprüft
werden muss
([Supabase Advisors](https://supabase.com/docs/guides/observability/advisors)).

## 4. RPC, SDK und RLS: passende Runtime-Bausteine

Supabase empfiehlt Database Functions für datenintensive Operationen und zeigt,
wie Anwendungen sie über RPC aufrufen. Das passt direkt zu ADR-0001: Der MCP
validiert einen kleinen Filter, danach führt eine einzige versionierte
`search_candidates_v1`-Funktion Filterung, Ranking und Pagination aus. Die
Supabase-Dokumentation empfiehlt `security invoker` als Standard. Funktionen
sind standardmäßig breit ausführbar; deshalb müssen Ausführungsrechte für
`public`, `anon` und `authenticated` entzogen und nur der vorgesehenen Rolle
explizit erteilt werden. Falls `security definer` unvermeidbar ist, muss der
`search_path` festgesetzt und jedes Objekt schemaqualifiziert werden
<!-- markdownlint-disable-next-line MD013 -->
([Supabase Database Functions](https://supabase.com/docs/guides/database/functions)).

Für den Service kann später entweder das offizielle
[`@supabase/supabase-js`](https://github.com/supabase/supabase-js) oder
[`supabase-py`](https://github.com/supabase/supabase-py) genutzt werden. Die
Wahl hängt vom noch offenen Runtime-Stack ab; beide bieten RPC-Aufrufe
([JavaScript RPC](https://supabase.com/docs/reference/javascript/rpc),
[Python RPC](https://supabase.com/docs/reference/python/rpc)). Der SDK-Einsatz
sollte auf den kontrollierten RPC- und Auth-Pfad begrenzt werden, nicht auf
generische Tabellenabfragen, die aus LLM-Ausgaben zusammengesetzt werden.

RLS bleibt Defense-in-Depth. Supabase weist darauf hin, dass Grants zuerst und
RLS-Policies danach geprüft werden und dass Views RLS standardmäßig umgehen
können. Deshalb müssen Tabellen, Views, Funktionen, Grants und Policies
gemeinsam auditiert und negativ getestet werden
<!-- markdownlint-disable-next-line MD013 -->
([Supabase Row Level Security](https://supabase.com/docs/guides/database/postgres/row-level-security)).

Ein Supabase-Secret-Key beziehungsweise der Legacy-`service_role` umgeht RLS.
Er ist daher kein geeigneter Default für den Runtime-Suchpfad. Bevorzugt wird
ein
Benutzer-JWT, der in der Datenbank auf Rolle und Tenant abgebildet wird, oder
ein
eigener minimal privilegierter Server-/DB-Pfad mit vollständiger eigener
Autorisierung. Schlüssel dürfen nie in Prompt, URL, Quellcode oder Log landen
([Supabase API Keys](https://supabase.com/docs/guides/getting-started/api-keys),
[Securing your data](https://supabase.com/docs/guides/database/secure-data)).

## 5. Suche: FTS zuerst messen, Vektoren nicht vorziehen

Supabase dokumentiert PostgreSQL Full Text Search mit `tsvector`,
`websearch_to_tsquery`, Präfixsuche, Negation, Ranking und gewichteten Spalten.
Ranking und Suche lassen sich in einer Database Function kapseln und per RPC
aufrufen. Damit ist FTS ein passender Kandidat für den lexical-search Anteil,
nachdem strukturierte Filter und Autorisierung den Suchraum begrenzt haben
<!-- markdownlint-disable-next-line MD013 -->
([Supabase Full Text Search](https://supabase.com/docs/guides/database/full-text-search)).

Die Dokumentation löst jedoch nicht automatisch die projektspezifische
Mehrsprachigkeit. B/H/S, Deutsch und Englisch, Diakritik, Flexionen und
fachlich erlaubte Synonyme müssen gegen echte Datenverteilungen und eine
kontrollierte Taxonomie getestet werden. FTS darf keine stillen
LLM-Synonymerweiterungen einführen. `pg_trgm` und jeder Vektorpfad bleiben
nachgelagerte Benchmark-Entscheidungen, wie bereits im Brief vorgesehen.

Supabase Vector Buckets können Embeddings in einem S3-basierten Vector Store
halten und über den S3 Vector Wrapper als Foreign Table aus PostgreSQL abgefragt
werden. Damit ist ein SQL-Join zwischen Similarity-Ergebnis und autoritativen
CRM-Zeilen technisch möglich. Das ersetzt weder die Erzeugung des Query-
Embeddings noch den Nachweis, dass selektive CRM-Filter vor dem endgültigen
`top_k` korrekt wirken. Vector Buckets sind derzeit Public Alpha, der Wrapper
unterstützt nur den dokumentierten `<===>`-Distanzoperator, und Supabase ordnet
sie eher großen backendorientierten Workloads zu. Für den geschätzten CRM-Umfang
ist deshalb kein Vorteil gegenüber `pgvector` oder dem nichtvektoriellen
<!-- markdownlint-disable-next-line MD013 -->
Baseline belegt ([Vector Buckets](https://supabase.com/docs/guides/storage/vector/introduction),
<!-- markdownlint-disable-next-line MD013 -->
[Querying Vectors](https://supabase.com/docs/guides/storage/vector/querying-vectors)).

Der verbindliche Prüfweg steht im
[Evaluations-Gate für semantische Suche](semantic-search-evaluation-gate.md).
Er trennt explizite Kandidatensuche, Ähnlichkeitssuche, Dublettenprüfung und die
außerhalb dieses Projekts liegende Call-Memory-Verknüpfung.

## 6. Branching und eigener Edge-MCP

Supabase Branches schaffen getrennte Instanzen mit eigenen Credentials.
Preview-Branches starten standardmäßig ohne Produktionsdaten, was für sichere
Schema-, RLS- und RPC-Tests attraktiv ist. Branches mit der Option „Include
data“ enthalten dagegen eine Produktionskopie und müssen genauso geschützt
werden. Kosten, Planverfügbarkeit und die Eignung für einen repräsentativen,
anonymisierten Testdatensatz sind vor Auswahl zu prüfen
([Supabase Branching](https://supabase.com/docs/guides/deployment/branching)).

Der offizielle BYO-MCP-Guide zeigt einen eigenen MCP auf Edge Functions mit dem
offiziellen TypeScript-SDK, Hono, Zod, Streamable HTTP und MCP Inspector. Das
ist
ein sinnvoller später POC-Kandidat für den eigenen Runtime-Such-MCP. Der Guide
stellt aber klar, dass sein Beispiel keine Authentifizierung verlangt und
verwendet `--no-verify-jwt`; Auth-Unterstützung für MCP auf Edge Functions wird
als noch kommend bezeichnet. Das Beispiel darf daher nicht als
Produktionsvorlage für Kandidatendaten übernommen werden
([Deploy MCP servers](https://supabase.com/docs/guides/ai-tools/byo-mcp)).

Supabase Edge Functions können reguläre Benutzer-JWTs validieren und einen auf
den Benutzer/RLS-Kontext beschränkten Client bereitstellen. Der dokumentierte
Secret-Modus liefert dagegen einen privilegierten Client, der RLS umgeht. Ob
die Benutzer-Authentifizierung mit allen vorgesehenen MCP-Clients und deren
OAuth-/Transportverhalten interoperabel ist, muss ein eigener Auth-POC beweisen
([Securing Edge Functions](https://supabase.com/docs/guides/functions/auth)).

## 7. Nicht geeignete Abkürzungen

### Generischer PostgREST-MCP

Das offizielle Paket `@supabase/mcp-server-postgrest` bietet ein generisches
`postgrestRequest` für GET, POST, PATCH und DELETE sowie `sqlToRest`, das
LLM-generierten SQL-ähnlichen Input in REST-Requests übersetzt. Genau diese
breite CRUD-/Übersetzungsfläche widerspricht dem akzeptierten Drei-Tool-Vertrag,
der SQL-Sperre und der getrennten Admin-Grenze. Es sollte für dieses Projekt
nicht eingesetzt werden
<!-- markdownlint-disable-next-line MD013 -->
([offizielles PostgREST-MCP-README](https://github.com/supabase/mcp/tree/main/packages/mcp-server-postgrest)).

### Self-hosted Supabase-MCP

`createSupabaseMcpHandler()` ist nützlich, wenn die vorhandenen
Supabase-Entwicklertools unter eigener Infrastruktur bereitgestellt werden
sollen. Es erweitert den Server aber nicht um kontrollierte CRM-Fachwerkzeuge.
Ein Self-host würde daher zusätzliche Betriebs- und Auth-Komplexität schaffen,
ohne die Runtime-Architektur zu ersetzen
<!-- markdownlint-disable-next-line MD013 -->
([Self-hosting im Supabase-MCP-Repository](https://github.com/supabase/mcp#self-hosting-the-mcp-endpoint)).

### `mcp-lite`, Reflex und ungefilterte Secret-Key-Zugriffe

Supabase nennt `mcp-lite` als Edge-kompatible Alternative. Für diese sensible,
mehrclientfähige Anwendung gibt es derzeit keinen belegten Vorteil gegenüber
dem offiziellen MCP-SDK; Auth, Rate Limits, Fehlerverträge und Tests bleiben in
beiden Fällen Projektverantwortung. Reflex ist lediglich ein möglicher
UI-Framework-Entscheid und hilft weder bei Discovery noch bei MCP-Sicherheit.
Ein Supabase-Secret-Key vereinfacht zwar Backendzugriff, umgeht aber RLS und ist
deshalb als allgemeiner Kandidatenzugang abzulehnen.

## Bewertung des Nutzeranhangs

- **Offiziellen Supabase-MCP konfigurieren, nicht umbauen:** richtig.
  Self-hosting ändert daran nichts.
- **Offiziellen und eigenen MCP nebeneinander nutzen:** richtig mit wichtiger
  Trennung. Der offizielle MCP bleibt internes Discovery-/Entwicklerwerkzeug;
  Endnutzer erhalten nur den kontrollierten Fach-MCP.
- **Eigenen MCP mit offiziellem SDK auf Edge Functions bauen:** technisch
  richtig, produktiv derzeit unvollständig. Der Guide ist unauthentifiziert;
  Auth- und Client-Interoperabilität müssen zuerst bewiesen werden.
- **`mcp-lite` als besonders einfacher Weg:** möglich, aber kein belegter
  Sicherheits- oder Projektvorteil.
- **Logs über `query_logs` nutzen:** später nützlich, aber nur minimiert und
  zweckgebunden. Logs dürfen kein PII enthalten und ersetzen keinen Audit.
- **Reflex für ein Mitarbeiter-UI:** derzeit nicht relevant; UI-Stack und
  eigenes Frontend sind offen.
- **Wichtige Lücken im Anhang:** Agent Skills, Advisors, CLI/pgTAP/`db lint`,
  Typgenerierung, Branching, der RLS-Bypass von Secret-Keys und die Ablehnung
  des generischen PostgREST-MCP.

## Empfohlene Reihenfolge

1. Die offiziellen Skills `supabase` und
   `supabase-postgres-best-practices` projektbezogen prüfen und getrennt vom
   Live-MCP einsetzen.
2. Die bestehende Gate-B-Freigabe und den kleinsten read-only Discovery-Scope
   abschließen. Noch keinen Live-MCP, CLI-Link oder Branch mit Produktionsdaten
   einrichten.
3. Nur den separat freigegebenen lokalen Discovery-Zugang verwenden. Der
   Developer-MCP ist kein alternativer Produktionspfad; Advisors benötigen
   ebenfalls einen eigenen erlaubten Scope.
4. Nach Discovery den kanonischen Datenvertrag und die einzige
   `search_candidates_v1`-RPC festlegen; RLS, Grants, Views und Function-Rechte
   gemeinsam designen.
5. Erst danach Runtime, SDK und Hosting wählen. Edge Functions nur dann wählen,
   wenn der Auth-POC für alle Zielclients bestanden ist.
6. Lokale Supabase-Umgebung, Migrationen, pgTAP, `db lint`, Typgenerierung und
   MCP Inspector in die reproduzierbare Testkette aufnehmen.
7. FTS, `pg_trgm` und später eventuell `pgvector` oder Vector Bucket/S3 Wrapper
   ausschließlich nach dem dokumentierten Evaluations-Gate anhand
   anonymisierter Tests, Query-Pläne, Qualitätsmessungen, Lifecycle und Kosten
   entscheiden. Branching bleibt eine getrennte Umgebungsentscheidung.

## Offene Prüfungen

- Ob der bestehende Supabase-Plan Branching, benötigte Advisor-Funktionen,
  Log-Retention und geeignete Connection-Limits umfasst.
- Ob ein dataloser Branch plus synthetischer/anonymisierter Seed die reale
  Kandidatenverteilung ausreichend repräsentiert.
- Ob Supabase Auth die benötigte interne Recruiter-, Rollen- und
  Tenant-Abbildung
  vollständig trägt oder ein vorgeschalteter Identity Provider nötig ist.
- Ob Edge Functions die geforderten End-to-End-Timeouts,
  Connection-Pool-Grenzen,
  Backpressure und MCP-Auth-Interoperabilität erfüllen.
- Welche PostgreSQL-Textsuchkonfigurationen und Indizes die realen B/H/S-,
  deutschen und englischen Daten benötigen.
- Ob ein Vektorpfad nach dem nichtvektoriellen Baseline überhaupt Mehrwert
  liefert und, falls ja, ob `pgvector` oder Vector Bucket/S3 Wrapper
  Filterkorrektheit, SLO, Privacy, Lifecycle und Kosten besser erfüllt.
- Welches SDK nach der noch offenen Stack-Entscheidung tatsächlich gewählt wird.

## Quellenstand

Alle externen Quellen sind offizielle Supabase-Dokumentation oder offizielle
Supabase-Repositories und wurden am 2026-09-11 geprüft. Volatile Angaben wie
Toolgruppen, Auth-Support, Branching, API-Key-Empfehlungen und SDK-Support
müssen
vor Implementierung erneut gegen die aktuelle Dokumentation verifiziert werden.

Der Supabase-Changelog wurde zusätzlich am 2026-09-11 geprüft. Für spätere
Planung relevant sind die Entfernung des Management-API-Endpunkts `logs.all` am
2026-09-23 zugunsten des neuen `logs`-Endpunkts mit ClickHouse SQL, das
Ignorieren
explizit gepinnter Extension-Versionen und die geänderte automatische
Exponierung
neuer Tabellen gegenüber Data/GraphQL APIs. Diese Punkte sind volatile
Vendor-Signale, keine bestätigten Fakten über das CRM-Projekt
([Supabase Changelog](https://supabase.com/changelog.md)).

Die verbindliche Agentenroute steht in
[Supabase tooling za agente](../agents/supabase-tooling.md).
