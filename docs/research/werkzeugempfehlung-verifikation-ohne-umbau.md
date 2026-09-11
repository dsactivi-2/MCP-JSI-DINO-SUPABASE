# Verifikation der Werkzeugempfehlung ohne großen Sofortumbau

Datum: 2026-09-11

Status: Recherchegrundlage; keine Stack-, Auth-, Hosting- oder
Produktionsfreigabe

## Auftrag und Grenzen

Geprüft wurde, ob die zuletzt empfohlene Kombination aus Supabase-RPC und
PostgREST, offiziellem MCP-TypeScript-SDK, Zod/Hono, Supabase Auth, Supabase
CLI, pgTAP, `db lint`, Typgenerierung, MCP Inspector, Promptfoo, k6,
OpenRefine, Langfuse und einer optionalen Low-Code-Oberfläche dieses Projekt
tatsächlich beschleunigt, ohne Qualität oder Funktionen zu verlieren und ohne
jetzt einen großen Umbau auszulösen.

Die Prüfung basiert auf dem [Projektstatus](../project.md), dem
[Implementierungsbrief](../SUPABASE_CRM_MCP_IMPLEMENTATION_BRIEF.md),
[ADR-0001](../decisions/0001-controlled-query-boundary.md),
[ADR-0002](../decisions/0002-search-design-interview.md),
[ADR-0003](../decisions/0003-separated-profile-administration-mcp.md) und
der bestehenden
[Supabase-Werkzeugrecherche](supabase-werkzeuge-fuer-crm-mcp.md). Extern wurden
nur offizielle Dokumentation, Spezifikationen und Projekt-Repositories
verwendet. Es gab keinen Zugriff auf ein Supabase-Projekt, eine Datenbank oder
Kandidatendaten und keine Installation oder Reparatur lokaler Werkzeuge.

## Kurzurteil

**Ja, aber nur als gestufter Minimalstack.** Die Kombination verkürzt die
spätere Umsetzung voraussichtlich deutlich und erhält die geplanten
Qualitäts- und Funktionsgrenzen, wenn sie auf diese Kernteile reduziert wird:

1. nach Discovery eine einzige versionierte PostgreSQL-RPC als fachliche
   Datengrenze;
2. nach Vertrags- und Stackentscheidung das offizielle MCP-SDK mit genau einer
   Schema-Bibliothek und genau einem Supabase-Client;
3. lokale, synthetische Migrationstests mit Supabase CLI, pgTAP und `db lint`;
4. MCP Inspector für Protokoll- und Contract-Smoke-Tests;
5. Promptfoo erst für die stabile natürlichsprachliche Filterübersetzung und
   nur mit synthetischen Daten und kontrolliertem Datenfluss;
6. k6 erst beim SLO- und Lasttest.

Das ist kein Sofortumbau: Die bestehenden importierten Tabellen bleiben gemäß
Q10.3 unverändert. RPC, Views, Rechte und Tests werden später additiv als erste
kompatible Bausteine des Zielmodells ergänzt. Der aktuelle Engpass ist weiterhin
der genehmigte read-only Discovery, nicht fehlender Anwendungscode.

Die frühere Empfehlung war an vier Stellen zu pauschal:

- „RPC + PostgREST“ darf nur die feste RPC über die bestehende Data API meinen,
  nicht den generischen PostgREST-MCP oder Tabellen-CRUD.
- Supabase Auth spart nicht die gesamte Auth-Arbeit: Ein eigener
  Autorisierungs-/Consent-Endpunkt, Rollen-/Tenant-Mapping und Client-POC bleiben
  erforderlich.
- Zod ist beim MCP-SDK v2 eine mögliche Standard-Schema-Implementierung, aber
  nicht zwingend; Hono ist nur bei passendem Hosting nötig.
- Langfuse und Low-Code-UI sparen in Release 1 keine Nettozeit, weil sie neue
  Betriebs-, Berechtigungs- und Datenschutzflächen eröffnen.

## Entscheidungsmatrix

<!-- markdownlint-disable MD013 -->

| Baustein | Einstufung | Zeitwirkung | Qualitäts-/Funktionswirkung | Versteckter Aufwand |
| --- | --- | --- | --- | --- |
| Feste PostgreSQL-RPC über PostgREST/Data API | **Übernehmen nach Discovery und Vertragsfreigabe** | Sehr hoch: keine eigene Daten-API und zentrale Suchlogik | Erhält Filterung, Ranking, RLS, Pagination und 50er-Limit in PostgreSQL | RPC-, Return-Type-, Grant-, RLS-, Timeout- und Schema-Cache-Design |
| Generischer PostgREST-MCP oder Tabellen-CRUD | **Ablehnen** | Scheint schnell, erzeugt später Sicherheitsumbau | Verletzt SQL-/Allowlist-Grenze und getrennten Admin-MCP | Breite GET/POST/PATCH/DELETE-Fläche und schwer kontrollierbare Toolsemantik |
| MCP TypeScript SDK v2 | **Nach Stackentscheidung übernehmen** | Hoch: Transport, Protokoll und Toolserver nicht selbst bauen | Offizielle stabile Linie; Client-Kompatibilität bleibt zu testen | SDK ist frisch stabil; Version pinnen und Compatibility-Matrix pflegen |
| Zod | **Mit TypeScript wahrscheinlich übernehmen** | Mittel: Filter- und Toolschemas werden ausführbar | Verringert ungültige Eingaben; ersetzt keine fachliche Validierung | Doppelte Schemaquellen vermeiden; JSON-Schema/Contract als maßgeblich festlegen |
| Hono | **Nur bei Edge-/Fetch-Hosting übernehmen** | Mittel im passenden Runtime-Modell | Keine Funktionsminderung | Bei Node/Fastify sonst unnötige zweite Webschicht |
| Fastify oder anderer Node-Adapter | **Nur als Alternative, nicht zusätzlich** | Mittel bei Node-Hosting | Keine Funktionsminderung bei sauberer Adaptergrenze | Hostingentscheidung und Auth-Middleware bleiben |
| `supabase-js` und generierte Typen | **Nach Schema-Mapping und TypeScript-Wahl** | Hoch: typisierte RPC-Aufrufe | Senkt Contract-Drift | Nur freigegebene API-Schemas typisieren; keine breite PII-Oberfläche generieren |
| Supabase Auth OAuth 2.1 | **Späterer Auth-POC, dann entscheiden** | Potenziell hoch | Kann bestehende Identitäten und RLS-Kontext erhalten | Eigener Authorization Endpoint, Consent, Scopes, Redirect-URI-Schutz, Rollen-/Tenant-Mapping und Tests aller Zielclients |
| Supabase CLI und lokaler Stack | **Nach Discovery/Scaffold übernehmen, vorher Tool reparieren** | Hoch für reproduzierbare Migrationen | Stärkt Dry-run, lokale Tests und Typgenerierung | Container, Migrationsbaseline und synthetische Seeds; lokaler Stack ist nicht produktionsgehärtet |
| pgTAP und `supabase db lint` | **Mit erster DB-Migration übernehmen** | Hoch durch wiederholbare RLS-/RPC-Regressionstests | Qualitätsgewinn, keine Funktionsminderung | Tests müssen geschrieben und gepflegt werden; Lint ersetzt keine Laufzeit-, RLS- oder Performance-Tests |
| MCP Inspector | **Mit erstem MCP-Endpunkt übernehmen** | Hoch für frühes Protokollfeedback | Ergänzt Contract-/Interoperabilitätstests | Kein Ersatz für automatische Security-, Auth- oder Fachtests |
| Promptfoo | **Später, nach stabilem Filtervertrag** | Hoch für Sprach-, Injection- und Leak-Regressionen | Qualitätsgewinn bei kuratierten erwarteten Ergebnissen | Lokale Installation ist derzeit defekt; manche wichtige Red-Team-Plugins sind remote-only und können Daten extern verarbeiten |
| k6 | **Später in Benchmark-/SLO-Phase** | Mittel | Macht Last- und Latenzgrenzen messbar | Noch nicht installiert; repräsentative synthetische Verteilung und konkrete SLOs fehlen |
| OpenRefine | **Optional nach Data-Quality-Audit** | Mittel bei Schreibvarianten und Taxonomieentwürfen | Hilft syntaktisch; semantische Zuordnung bleibt menschlich geprüft | Nicht installiert; manueller Workflow, sichere minimierte Exporte und Wiedereinspielung nötig |
| Langfuse | **Für Release 1 nicht einführen** | Kurzfristig negativ | Später eventuell nützlich für LLM-Evals und Betrieb | Cloud-Datenfluss oder Self-host-Betrieb mit Web, Worker, Postgres, ClickHouse, Redis und Blob Store; Maskierung und Retention müssen aktiv gestaltet werden |
| Appsmith/ToolJet | **Jetzt nicht auswählen; späterer Admin-UI-POC** | Erst nach stabilem Admin-Vertrag positiv | Darf ADR-0003 nicht ersetzen | Zusätzliche App, Auth/RBAC, Deployment, Backup, Upgrades und sichere API-Integration |

<!-- markdownlint-enable MD013 -->

## Begründung der Kernentscheidungen

### 1. RPC verkürzt ohne Umbau, wenn sie wirklich die einzige Datengrenze ist

ADR-0001 verlangt bereits einen kleinen validierten JSON-Filter und eine
vordefinierte PostgreSQL-RPC. PostgREST stellt Funktionen eines exponierten
Schemas unter `/rpc` bereit und akzeptiert JSON-Argumente. Es warnt zugleich,
dass jede für die aktive Rolle erreichbare Funktion ausführbar ist und dass
Funktionsänderungen einen Schema-Cache-Reload benötigen. Strikte Return-Typen
sind empfohlen. Das bestätigt den Zeitgewinn, aber ebenso die Notwendigkeit
eines engen exponierten Schemas, expliziter `EXECUTE`-Rechte und einer festen
Return-Struktur
([PostgREST: Functions as RPC](https://postgrest.org/en/stable/references/api/functions.html)).

Die minimale Umsetzung ist daher nicht „PostgREST als neue Plattform“, sondern
eine versionierte `search_candidates_v1`-Funktion hinter dem ohnehin
vorhandenen Supabase-Data-API-Pfad. Importtabellen werden nicht umgebaut. Eine
zusätzliche eigene CRUD-/REST-Schicht entfällt, die Sicherheitskontrolle bleibt
in Datenbank und MCP.

### 2. MCP SDK v2 ist geeignet; Zod und Hono sind keine Paketpflicht

Das offizielle TypeScript-SDK bezeichnet v2 inzwischen als stabile Release-
Linie zur MCP-Spezifikation vom 2026-07-28. Es trennt Server- und Clientpakete
und akzeptiert Standard-Schema-kompatible Bibliotheken wie Zod v4, Valibot oder
ArkType. V1 erhält übergangsweise Fehler- und Sicherheitskorrekturen
([offizielles TypeScript-SDK](https://github.com/modelcontextprotocol/typescript-sdk)).

Damit ist die frühere Aussage „SDK v2 + Zod“ technisch tragfähig, aber erst nach
der offenen Stackentscheidung. Zod sollte nur gewählt werden, wenn TypeScript
gewählt wird und der kanonische Vertrag ohne doppelte, auseinanderlaufende
Definitionen daraus abgeleitet werden kann. Hono ist ein Hostingadapter, keine
fachliche Voraussetzung. Ein gleichzeitiger Hono-/Fastify-Aufbau würde Arbeit
erzeugen statt sparen.

### 3. Supabase Auth ist ein Beschleuniger, keine fertige Auth-Lösung

Supabase dokumentiert OAuth 2.1 mit PKCE, Discovery, optionaler dynamischer
Clientregistrierung, JWTs und RLS-Kontext für eigene MCP-Server. Die gleiche
Dokumentation nennt aber als Voraussetzung ausdrücklich einen selbst zu
bauenden Authorization Endpoint und verlangt bei dynamischer Registrierung
Benutzerzustimmung, Monitoring und Redirect-URI-Prüfung
([Supabase MCP Authentication](https://supabase.com/docs/guides/auth/oauth-server/mcp-authentication)).

Im Projekt sind Auth- und Tenant-Modell noch offen; der statische `crm_auth`-
Export beweist keine wirksame RLS- oder Tenant-Isolation. Supabase Auth kann
daher später Arbeit sparen, sobald Discovery und Rollen-Mapping zeigen, dass es
passt. Eine frühzeitige Aktivierung würde eher Nacharbeit und
Interoperabilitätsrisiko erzeugen. Der POC muss ChatGPT, Claude, Codex, Grok und
den Referenzclient mit echten Redirect-, Refresh-, Revocation- und
Negativfällen abdecken, jedoch nur mit synthetischen Testidentitäten.

### 4. CLI, pgTAP, Lint und Typen amortisieren sich ab der ersten Migration

Die Supabase CLI unterstützt lokale Migrationen, lokale Typgenerierung,
`supabase test db` mit pgTAP und `supabase db lint` mit `plpgsql_check`.
`db lint` findet unter anderem Typfehler, fehlende Returns, tote Pfade,
unerwünschte Casts und bestimmte dynamische SQL-Risiken
([Testing and linting](https://supabase.com/docs/guides/local-development/cli/testing-and-linting)).
Die lokale Entwicklungsumgebung ist ausdrücklich nicht produktionsgehärtet;
Remote-Link, Push und insbesondere `db reset --linked` haben eigene Risiken
([Local development workflow](https://supabase.com/docs/guides/local-development/cli-workflows)).

Die Werkzeuge sollen deshalb erst mit der additiven Migrationsbaseline
eingeführt werden. Das respektiert die Nutzerentscheidung gegen ein separates
gehostetes Development-/Staging-Projekt: Eine lokale, nicht exponierte Instanz
mit synthetischen Seeds ist kein neues Produktivprojekt. Sie darf jedoch weder
den abgelehnten Restore-Preflight der lokalen Rohartefakte umgehen noch
Produktionsdaten kopieren. Typen werden erst aus dem freigegebenen API-Schema
generiert und sind bei einem Python-Stack kein Auswahlgrund.

### 5. Inspector, Promptfoo und k6 gehören an unterschiedliche Gates

Der MCP Inspector kann Tools auflisten und aufrufen und besitzt CLI-Ausgaben,
die sich automatisieren lassen. Er ist deshalb ab dem ersten lauffähigen
MCP-Endpunkt ein schneller Smoke- und Contract-Test, aber keine vollständige
Qualitätssicherung
([offizielles MCP Inspector Repository](https://github.com/modelcontextprotocol/inspector)).

Promptfoo ist erst sinnvoll, wenn Eingaben, erwartete Filter und sichere Fehler
stabil genug sind. Seine offizielle Datenschutzdokumentation bestätigt, dass
Prompts, Antworten und Kriterien je nach Generation, Grading und Cloud-Funktion
extern verarbeitet werden. Mehrere für dieses Projekt interessante
Security-Plugins, darunter BOLA und indirekte Prompt Injection, sind remote-only.
„Local generation“ und deaktivierte Telemetrie sind zudem keine vollständige
Netzwerkisolation. Vollständig air-gapped wird als Enterprise-On-Prem-Funktion
beschrieben
([Promptfoo Data Handling](https://www.promptfoo.dev/docs/red-team/troubleshooting/data-handling/)).
Folglich dürfen nur synthetische Fälle eingesetzt werden; PII-, BOLA- und
Injection-Gates brauchen zusätzlich deterministische Tests auf MCP-, RPC- und
RLS-Ebene.

k6 kann SLOs als Thresholds ausdrücken und bei Verletzung mit einem
Nicht-null-Exitcode enden. Das ist für Phase 6 des Implementierungsbriefs
passend, spart davor aber keine Arbeit, solange numerische SLOs und ein
repräsentativer synthetischer Datenbestand fehlen
([k6 Thresholds](https://grafana.com/docs/k6/latest/using-k6/thresholds/)).

### 6. OpenRefine, Langfuse und Low-Code sind bewusste Spätoptionen

OpenRefine arbeitet lokal und kann syntaktische Varianten gruppieren. Das
Projekt weist selbst darauf hin, dass Clustering keine semantisch verlässliche
Reconciliation ist
([OpenRefine Clustering](https://openrefine.org/docs/technical-reference/clustering-in-depth)).
Es eignet sich nach dem Data-Quality-Audit für überprüfbare Aliasvorschläge,
nicht für automatische Veröffentlichungen oder die offene Semantik von Q8.5.

Langfuse würde Release 1 operativ vergrößern. Die offizielle Self-host-
Architektur umfasst zwei Anwendungskomponenten sowie Postgres, ClickHouse,
Redis/Valkey und S3-kompatiblen Blob-Speicher
([Langfuse Self-hosting](https://langfuse.com/self-hosting)). Clientseitige
Maskierung ist verfügbar, muss aber von der Anwendung korrekt implementiert
werden; zentrale serverseitige Maskierung ist eine Enterprise-Funktion und ist
standardmäßig nicht fail-closed
([Langfuse Data Masking](https://langfuse.com/self-hosting/security/data-masking)).
Für Release 1 sind minimierte strukturierte Metriken und Logs ausreichend.

Eine Low-Code-Oberfläche kann später Formulare und Rollenverwaltung sparen,
aber erst nachdem der getrennte Profilverwaltungsvertrag aus ADR-0003 steht.
ToolJet dokumentiert eigenes RBAC, zugleich aber auch einen zusätzlichen
Deployment-Stack mit eigener PostgreSQL-Datenbank für Appdefinitionen,
Credentials und Benutzerdaten
([ToolJet RBAC](https://docs.tooljet.ai/docs/user-management/role-based-access/user-roles/),
[ToolJet Docker Compose](https://docs.tooljet.ai/docs/setup/docker/)). Ein
direkter Datenbankzugriff aus Appsmith oder ToolJet würde die getrennte
Vertrauensgrenze umgehen. Deshalb wird jetzt weder ein Produkt ausgewählt noch
eine Admin-Oberfläche gebaut.

## Lokaler Read-only-Befund

Die lokale Bestandsprüfung hat keine Installation verändert:

<!-- markdownlint-disable MD013 -->

| Werkzeug | Befund |
| --- | --- |
| Node.js | vorhanden unter `/Users/activi/.local/bin/node`, Version 22.22.3 |
| pnpm | vorhanden, Version 11.25.0 |
| Deno | vorhanden, Version 2.9.4 |
| Docker | vorhanden, Version 29.4.0 |
| Supabase CLI | Symlink auf `/opt/homebrew/Cellar/supabase/2.115.0/bin/supabase`; `rtk supabase --version` endete mit Exitcode 1 und internem JS-/Effect-Dump |
| Promptfoo | vorhanden unter `/opt/homebrew/bin/promptfoo`; Versionsprüfung scheiterte mit Exitcode 1 wegen `better-sqlite3`-ABI-Konflikt (`NODE_MODULE_VERSION` 141 statt benötigter 147) |
| k6 | nicht vorhanden |
| OpenRefine | nicht vorhanden |

<!-- markdownlint-enable MD013 -->

Damit sind Supabase CLI und Promptfoo **installiert, aber nicht einsatzbereit**.
Ihre Reparatur ist eine getrennte Diagnoseaufgabe und keine Voraussetzung für
den aktuellen Discovery-Schritt. k6 und OpenRefine sollen nicht vorsorglich
installiert werden.

## Minimaler Weg ohne großen Umbau

1. Gate B1/B2 und den eng begrenzten read-only Discovery abschließen; keine
   Runtime-, Auth- oder Hostingentscheidung vorziehen.
2. Aus dem Discovery genau einen kanonischen JSON-Filter, Ergebnisvertrag und
   die Signatur von `search_candidates_v1` entwerfen und freigeben.
3. Stackentscheid als kleines POC treffen: TypeScript-SDK v2 mit genau einer
   Schema-Bibliothek gegen einen in-memory/fake RPC-Adapter; noch keine
   Produktionsverbindung.
4. Eine additive lokale Migrationsbaseline mit synthetischen Seeds einrichten;
   zuvor die Supabase-CLI-Störung diagnostizieren. Mit der ersten RPC zugleich
   pgTAP-, RLS-, Grant-, Pagination- und `db lint`-Tests hinzufügen.
5. Den MCP-Adapter nur auf diese RPC beschränken und mit MCP Inspector sowie
   automatischen Contract-Tests prüfen.
6. Supabase Auth separat gegen das bestätigte `crm_auth`-/Tenant-Modell und alle
   Zielclients testen; erst nach bestandenem POC als Auth-Lösung festlegen.
7. Nach stabilem Sprachvertrag Promptfoo reparieren und ausschließlich mit
   synthetischen mehrsprachigen, Injection- und Leak-Fällen einsetzen.
8. Nach festgelegten SLOs k6 ergänzen. OpenRefine nur bei belegtem
   Taxonomie-Cleanup-Bedarf; Langfuse und Low-Code-UI frühestens nach Release-1-
   Kern und getrenntem Admin-Vertrag neu bewerten.

Dieser Ablauf reduziert Eigenentwicklung an Protokoll, Data API, Migrationen
und Tests, ohne die akzeptierte JSON→Validator→RPC→PostgreSQL-Grenze, den
50-Kandidaten-Cap, die Kontakt-Sperre oder die getrennte Profilverwaltung
abzuschwächen. Er vermeidet zugleich einen frühen Framework-, Auth-,
Observability- oder UI-Umbau.

## Verbleibende Unsicherheiten

- Der reale Zeitgewinn der RPC lässt sich erst nach Schema-, Index- und
  Datenqualitäts-Discovery quantifizieren.
- Ob TypeScript/Node, Deno/Edge oder ein anderer Runtime-Stack am wenigsten
  Betriebsarbeit verursacht, ist noch nicht entschieden.
- Supabase Auth ist nur dann die kürzeste Lösung, wenn das bestätigte Rollen-
  und Tenant-Modell sauber auf JWT/RLS abbildbar ist und alle Zielclients den
  Flow interoperabel umsetzen.
- Synthetische Daten müssen die reale Verteilung ausreichend abbilden, ohne
  Kandidatendaten zu kopieren; dafür fehlen noch Auditbefunde.
- Promptfoo deckt wegen seiner Datenflüsse und remote-only Plugins nicht allein
  die benötigten Security-Gates ab.
- Für Appsmith wurde in dieser Prüfung keine Produktauswahl getroffen; beide
  Low-Code-Kandidaten bleiben austauschbare Spätoptionen hinter derselben
  Admin-API-Grenze.

## Fazit

Die Empfehlung verkürzt das Projekt **ohne Qualitäts- oder Funktionsverlust**,
wenn nur RPC, offizielles MCP-SDK, eine Schema-Bibliothek, ein Supabase-Client
und die gestufte Testkette zum Kern werden. Sie verkürzt es **nicht**, wenn
Supabase Auth, Hono/Fastify, Langfuse, OpenRefine und eine Low-Code-Oberfläche
gleichzeitig als Sofortstack eingeführt werden.

Für den aktuellen Stand lautet die richtige Aktion daher: Discovery fortsetzen,
keinen Anwendungssaffold vorziehen und keine weiteren Tools installieren. Nach
dem Contract-Gate kann der Kern additiv aufgebaut werden; die bestehenden
Importtabellen müssen dafür nicht sofort umgebaut werden.
