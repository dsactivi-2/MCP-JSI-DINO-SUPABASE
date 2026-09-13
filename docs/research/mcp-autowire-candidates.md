<!-- markdownlint-disable MD013 -->
# Istraživanje: gotovi MCP i TypeScript slojevi za CRM pretragu

Datum: 2026-09-12

Status: nalaz iz javnih primarnih izvora; nije stack odluka, nije pristup
bazi, nije izmjena ADR-ova

Brief: [mcp-autowire-research-brief.md](mcp-autowire-research-brief.md)

## Kratka ocjena

Nijedan pregledani proizvod nije siguran **runtime Search-MCP** za ovaj
use case. Alati koji "odmah razumiju bazu" ili "sami grade MCP" defaultno
daju LLM-u SQL, PostgREST CRUD ili CMS/admin površinu nad svim tabelama.
To krši [ADR-0001](../decisions/0001-controlled-query-boundary.md) i
Release-1 zabranu kontakata. Postojeći
`crm_api.search_candidates` s e-mailom i telefonom bio bi upravo takav
1:1 wrap.

Korisni su samo **codegen i server okvir**:

1. `supabase gen types` za tipove; `pgtyped` ako SQL ostane u
   committanim fajlovima. Drizzle/Prisma/Kysely samo kao interni codegen,
   ne kao MCP surface.
2. Službeni MCP TypeScript SDK v2 `registerTool` + Zod/JSON Schema za
   tri alata. To već predlaže
   [SDK plan](../planning/sdk-integration-plan.md).
3. OpenAI Structured Outputs kao opcija da klijentski LLM drži JSON
   filter; SQL i dalje piše Postgres RPC, ne model.

Sve ostalo (taksonomija, Berufssuchprofil, match evidence, cap 50,
redakcija PII, Q7 potvrda) ostaje naš ugovor. FTS/`pg_trgm` i vanjski
search enginei su kasniji backend iza istog JSON-a, ne zamjena MCP-a.

## Tabela kandidata

| Kandidat | Klasa | Default surface | Ocjena |
| --- | --- | --- | --- |
| `supabase gen types` | A | samo TypeScript tipovi iz sheme | **GO-codegen-only** |
| `drizzle-kit pull` | A | `schema.ts` iz DDL introspekcije | **GO-codegen-only** |
| `prisma db pull` + Prisma Client | A | modeli pa puni Client CRUD | **GO-codegen-only**; Client nije MCP |
| `kysely-codegen` | A | `.d.ts` iz introspekcije | **GO-codegen-only** |
| `pgtyped` | A | samo committani SQL fajlovi | **GO-codegen-only** (najuža allowlista) |
| Zapatos | A | tipovi **i** CRUD + proizvoljni SQL | **GO-codegen-only** za tipove; runtime **NO-GO** |
| `@supabase/postgres-meta` | A | `POST /query` + DDL | **NO-GO** runtime |
| MCP TypeScript SDK v2 | C | ručno `registerTool` + Zod | **GO** kao okvir, ne auto-wire |
| OpenAI Structured Outputs | C | JSON Schema / Zod parse | **GO** za nivo 0→1, ne za bazu |
| PostgREST shema + `/rpc` | E | sve funkcije i tabele izloženog schema | **LATER** samo uz usku search shemu; default **NO-GO** |
| Postgres FTS / `pg_trgm` | D | SQL backend | **LATER** nakon discoveryja |
| Typesense / Meilisearch | D | vlastiti index + API | **LATER**; Typesense NL search **NO-GO** |
| Google MCP Toolbox custom `postgres-sql` | B | ručno parametrizirani SQL alati | **GO-codegen-only**; prebuilt **NO-GO** |
| Azure APIM REST→MCP | B | odabrane REST operacije | **GO-codegen-only** nad našim 3 op |
| Neon MCP / Cloud SQL MCP | B | `run_sql` / `execute_sql` | **NO-GO** |
| Cloudflare `openApiMcpServer` | B | `search` + `execute` | **NO-GO** |
| Službeni Postgres MCP (arhiviran) | B | `query(sql)` + shema svake tabele | **NO-GO** |
| Službeni Supabase MCP | B | project/SQL/migracije/grane | **NO-GO** runtime (već odlučeno) |
| `@supabase/mcp-server-postgrest` | B | `postgrestRequest` + `sqlToRest` | **NO-GO** |
| Crystal DBA Postgres MCP Pro | B | schema-aware SQL + execution | **NO-GO** runtime |
| Directus MCP | E | CMS sadržaj i kolekcije | **NO-GO** |
| OpenAPI→MCP generatori | B | MCP za svaki OpenAPI path | **NO-GO** nad PostgREST dumpom |
| Hasura v2 | E | instant GraphQL CRUD | **NO-GO** |

## Klasa A — TypeScript iz sheme

### `supabase gen types` — GO-codegen-only

Službena dokumentacija: APIs se generišu iz baze, pa introspekcija daje
TypeScript definicije. CLI:
`npx supabase gen types typescript --project-id … --schema public` ili
`--local` / `--db-url`. Izlaz je `Database` interfejs s `Tables`,
`Insert`, `Update` i funkcijama, za klijentske biblioteke, ne MCP
server. [Generating TypeScript Types](https://supabase.com/docs/guides/api/rest/generating-types)
(čitanje 2026-09-12).

Za nas: tipizirati uski adapter oko odobrenih RPC-ja. Ne smije se
spajati `--project-id` na produkcijski CRM iz ovog chata; lokalni ili
sintetički izvor tek nakon odobrenog puta. `--schema` sužava izvoz, ali
i uska shema s PII tabelama i dalje nije MCP ugovor.

### `drizzle-kit pull` — GO-codegen-only

Zvanično: povlači DDL postojeće baze i generiše `schema.ts` za
database-first tok. [drizzle-kit pull](https://orm.drizzle.team/docs/drizzle-kit-pull)
(2026-09-12). To je Drizzle schema, zatim ORM pristup tabelama. Korisno
za interni kod uz allowlistu; nije MCP.

### `prisma db pull` — GO-codegen-only

Zvanično: spaja se na bazu i upisuje Prisma modele koji odražavaju
trenutnu shemu; introspekcija mapira tabele, kolone i indekse. Cilj je
Prisma Client. Komanda prepisuje `schema.prisma`.
[prisma db pull](https://www.prisma.io/docs/cli/db/pull.md),
[What is introspection?](https://www.prisma.io/docs/orm/prisma-schema/introspection.md)
(2026-09-12). Client bi po defaultu vidio i kontakt/CV tabele. Nije
runtime MCP.

### Kysely / `kysely-codegen` — GO-codegen-only

Službeni Kysely docs: tipove sheme treba dati konstruktoru; automatsko
generisanje je **treća strana**. Navodi
[kysely-codegen](https://github.com/RobinBlomberg/kysely-codegen),
prisma-kysely i kanel-kysely.
[Generating types](https://kysely.dev/docs/generating-types) (2026-09-12).
`kysely-codegen` README: iz `DATABASE_URL` piše `.d.ts`, "that's it"
(2026-09-12). Query builder i dalje može dirati svaku tabelu ako joj damo
te tipove; MCP ih ne smije izložiti.

### Zapatos — tipovi da, runtime ne

Zvanično radi pet stvari: CLI piše TS shemu za **svaku tabelu**, tagged
SQL, everyday CRUD, nested JOIN JSON, transakcije.
[Zapatos](https://jawj.github.io/zapatos/) (2026-09-12). Tipovi su
codegen. CRUD i arbitrary SQL kao MCP surface su **NO-GO**.

### `pgtyped` — GO-codegen-only, najuža SQL allowlista

Nije ORM. CLI čita naše annotated SQL/TS queryje, tipove uzima s
Postgresa, emitira `PreparedQuery`. Allowlista su fajlovi u Gitu, ne
cijela shema. [PgTyped](https://pgtyped.dev/docs/) (2026-09-12). LLM te
SQL fajlove ne smije pisati; postojeći `crm_api.search_candidates` i
dalje nije dozvoljen wrap.

### `@supabase/postgres-meta` — NO-GO runtime

Generator iza `gen types`, ali i REST `POST /query` i DDL. README:
nema security sloja. [postgres-meta](https://github.com/supabase/postgres-meta)
(2026-09-12). Lokalni/CI generator da; produkcijski MCP ne.

## Klasa B — auto-MCP nad bazom

### Arhivirani službeni Postgres MCP — NO-GO

README: read-only pristup; alat **`query`** prima `sql: string` u
READ ONLY transakciji; resource za shemu **svake** tabele.
[servers-archived postgres](https://github.com/modelcontextprotocol/servers-archived/blob/main/src/postgres/README.md)
(2026-09-12). To je tačno ADR-0001 zabrana: LLM piše SQL. Arhiva nije
produkcijski runtime.

### Službeni Supabase MCP — NO-GO runtime

Docs: LLM "interact with and query your Supabase projects"; caution o
riziku. Hosted `https://mcp.supabase.com/mcp`, lokalno
`http://localhost:54321/mcp`. Query parametri: `project_ref`,
`read_only=true`, `features=database,docs`. Production vodič uči LLM
da zove `create_branch`, `apply_migration`, `list_migrations`.
[Supabase MCP Server](https://supabase.com/docs/guides/ai-tools/mcp),
[From development to production](https://github.com/supabase/mcp/blob/main/docs/production.md)
(2026-09-12). To je developer MCP, već zabranjen na produkcijskom CRM s
PII. `read_only` ne daje tri typed search alata ni redakciju kontakata.

### `@supabase/mcp-server-postgrest` — NO-GO

Zvanično: "allows LLMs to perform CRUD operations on your app via REST
API". Alati: `postgrestRequest(method, path, body)` i `sqlToRest(sql)`.
Konfig: `apiUrl`, `apiKey`, `schema`.
[mcp-server-postgrest README](https://github.com/supabase/mcp/blob/main/packages/mcp-server-postgrest/README.md)
(2026-09-12). LLM bira GET/POST/PATCH/DELETE i path. Na `crm` shemi to
je masovni CRUD i stari RPC s telefonima. Čak i `sqlToRest` ostavlja
SQL u modelu.

### Crystal DBA Postgres MCP Pro — NO-GO runtime

README: "Schema Intelligence — context-aware SQL generation" i "Safe SQL
Execution" uz read-only opciju, plus index tuning i EXPLAIN.
[postgres-mcp](https://github.com/crystaldba/postgres-mcp/blob/main/README.md)
(2026-09-12). Namjena je DBA/dev, ne recruiter search ugovor. SQL od
agenta ostaje. Eventualno kasnije na sintetičkoj bazi kao advisor, ne
kao Runtime-Such-MCP.

### Google MCP Toolbox — prebuilt NO-GO, custom GO-codegen-only

Prebuilt Postgres daje `list_tables` / `execute_sql`; docs: za
build-time, not for runtime. Custom `postgres-sql` izvršava unaprijed
napisan prepared statement. Može hostati tri alata nakon što SQL
napišemo.
[postgres-sql](https://googleapis.github.io/genai-toolbox/resources/tools/postgres/postgres-sql/)
(2026-09-12).

### Azure APIM REST→MCP — GO-codegen-only nad našim API-jem

Odabrane REST operacije postaju MCP alati. Radi samo ako backend već
jeste naš ugovor bez kontakata. Ne čita Postgres shemu.
[Export REST as MCP](https://learn.microsoft.com/en-us/azure/api-management/export-rest-mcp-server)
(2026-09-12).

### Cloudflare OpenAPI MCP, Neon, Cloud SQL — NO-GO

Cloudflare default: `search` + `execute` nad cijelim spec. Neon:
`run_sql`, not recommended in production. Cloud SQL: any valid SQL.
(2026-09-12).

### OpenAPI→MCP generatori — NO-GO nad dumpom

Pretraga nalazi treće strane (npr. openapi-mcp-generator) koje pretvaraju
OpenAPI u MCP alate. PostgREST OpenAPI je katalog svih tabela i RPC-ja.
Generator bi objavio baš to. Korisno tek ako **mi** objavimo OpenAPI od
tri search alata, što je naš kod, ne auto-wire baze.

## Klasa C — NL → JSON, ne NL → SQL

### MCP TypeScript SDK v2 — GO kao okvir

Stabilna grana uz spec 2026-07-28; paket `@modelcontextprotocol/server`.
Primjer: `registerTool` s `inputSchema: z.object({...})`; SDK validira
poziv prije handlera.
[v2 docs](https://ts.sdk.modelcontextprotocol.io/v2),
[README](https://github.com/modelcontextprotocol/typescript-sdk/blob/main/README.md)
(2026-09-12). Pokriva nivo 1 (JSON ugovor) i transport. Ne introspektira
Postgres i ne nudi search. To je planirani ručni server, ne gotov CRM
MCP.

### OpenAI Structured Outputs — GO za nivo 0→1

Model mora vratiti JSON prema zadanoj JSON Schema / Zod; nema izmišljenih
enum vrijednosti ni ispuštenih required polja.
[Structured model outputs](https://platform.openai.com/docs/guides/structured-outputs)
(2026-09-12). Korisno u MCP klijentu da namjera postane filter. Ne izvršava
SQL i ne vidi tabele. Server i dalje mora validirati, autorizirati i zvati
RPC.

## Klasa D — search backend iza JSON ugovora

### Postgres FTS i `pg_trgm` — LATER

Službeno poglavlje 12: FTS je u PostgreSQL jezgru.
[Chapter 12. Full Text Search](https://www.postgresql.org/docs/current/textsearch.html)
(2026-09-12). Gate B2 već vidi trigram indekse po imenu; to nije MCP.
Ostaje evaluacija nakon discoveryja, iza istog JSON filtera, kako već
traži [semantic-search-evaluation-gate.md](semantic-search-evaluation-gate.md).

### Typesense / Meilisearch — LATER; Typesense NL NO-GO

Typesense: gurati postojeće podatke u engine; ne crawl, instant search.
[What is Typesense?](https://typesense.org/docs/overview/what-is-typesense.html)
(2026-09-12). Meilisearch: index dokumenata i embeddinga, full-text i
semantička pretraga, zaseban API.
[Welcome to Meilisearch](https://www.meilisearch.com/docs/learn/getting_started/what_is_meilisearch)
(2026-09-12). Typesense Natural Language Search LLM-om pravi
`filter_by` i krši pravilo da nenavedene kategorije ostanu neaktivne.
[NL search](https://typesense.org/docs/30.2/api/natural-language-search.html)
(2026-09-12). Oba zahtijevaju kopiju podataka. Nisu Release 1.

## Klasa E — admin/API iz sheme

### PostgREST sheme i RPC — default NO-GO, uski adapter LATER

Izlaže tabele, viewove i funkcije shema iz `db-schemas`. Role mora imati
USAGE. `pg_catalog` / `information_schema` su zabranjeni u
`db-schemas`. Svaka funkcija izložene sheme dostupna je pod `/rpc`.
[Schemas](https://postgrest.org/en/stable/references/api/schemas.html),
[Functions as RPC](https://postgrest.org/en/stable/references/api/functions.html)
(2026-09-12). Ako bismo izložili `crm`, LLM/MCP vidi PII i stare RPC-je.
Ako kasnije napravimo **posebnu** shemu samo s
`search_candidates`, `get_candidate_profile`, `get_filter_options`
bez kontakata, PostgREST može biti HTTP adapter ispod našeg MCP-a. To
nije auto-wire postojeće baze.
 Službeno: ne izlagati tabele, nego viewove ili funkcije
 ([schema isolation](https://docs.postgrest.org/en/stable/explanations/schema_isolation.html),
 2026-09-12).

### Directus MCP — NO-GO

Docs (v11.12+): AI alati "manage your content"; alati za kolekcije,
sadržaj, fajlove, data modele.
[Directus MCP](https://directus.io/docs/guides/ai/mcp) (2026-09-12).
CMS/admin granica, ne recruiter search s cap 50 i bez kontakata.

### Hasura v2 — NO-GO

Default je instant GraphQL CRUD na tracked tabelama. Custom function
mora vraćati SETOF već tracked tabele.
[custom functions](https://hasura.io/docs/2.0/schema/postgres/custom-functions/)
(2026-09-12).

## Šta bismo i dalje morali napisati

Čak i uz najbolji codegen:

- JSON Schema/Zod filter (nivoi 1–6) i server validaciju;
- tri MCP alata, ne tabelarni CRUD;
- PostgreSQL RPC s RLS, keyset pagination, cap 50, match evidence;
- taksonomiju i verzije Berufssuchprofila (ADR-0003);
- redakciju kontakata/CV/bilješki, uključujući stare RPC signatura;
- Q7 tok pri nula pogodaka;
- auth audience odvojen od DB credentiala.

Nijedan pregledani auto-MCP to ne isporučuje iz legacy CRM sheme.

## Šta nije provjereno

- Živi pozivi, instalacije i runtime testovi.
- Živi codegen protiv ovog CRM-a (namjerno).
- PG 17 certifikati za Drizzle/Kysely/pgtyped.
- Da li se Directus auto-REST da potpuno ugasi.
- Stock PG 17 FTS rječnici za B/H/S.
- `supabase gen types --schema` na Gate-B katalogu bez PII tabela
  zahtijeva odobreni read-only put.

## Izvori

- [prisma db pull](https://www.prisma.io/docs/cli/db/pull.md) (2026-09-12)
- [Prisma introspection](https://www.prisma.io/docs/orm/prisma-schema/introspection.md) (2026-09-12)
- [drizzle-kit pull](https://orm.drizzle.team/docs/drizzle-kit-pull) (2026-09-12)
- [Supabase generating types](https://supabase.com/docs/guides/api/rest/generating-types) (2026-09-12)
- [Kysely generating types](https://kysely.dev/docs/generating-types) (2026-09-12)
- [kysely-codegen](https://github.com/RobinBlomberg/kysely-codegen) (2026-09-12)
- [Zapatos](https://jawj.github.io/zapatos/) (2026-09-12)
- [MCP postgres archived](https://github.com/modelcontextprotocol/servers-archived/blob/main/src/postgres/README.md) (2026-09-12)
- [Supabase MCP docs](https://supabase.com/docs/guides/ai-tools/mcp) (2026-09-12)
- [Supabase MCP production.md](https://github.com/supabase/mcp/blob/main/docs/production.md) (2026-09-12)
- [mcp-server-postgrest](https://github.com/supabase/mcp/blob/main/packages/mcp-server-postgrest/README.md) (2026-09-12)
- [postgres-mcp README](https://github.com/crystaldba/postgres-mcp/blob/main/README.md) (2026-09-12)
- [MCP TS SDK v2](https://ts.sdk.modelcontextprotocol.io/v2) (2026-09-12)
- [MCP TS SDK README](https://github.com/modelcontextprotocol/typescript-sdk/blob/main/README.md) (2026-09-12)
- [OpenAI Structured Outputs](https://platform.openai.com/docs/guides/structured-outputs) (2026-09-12)
- [PostgreSQL FTS](https://www.postgresql.org/docs/current/textsearch.html) (2026-09-12)
- [PostgREST schemas](https://postgrest.org/en/stable/references/api/schemas.html) (2026-09-12)
- [PostgREST RPC](https://postgrest.org/en/stable/references/api/functions.html) (2026-09-12)
- [Typesense overview](https://typesense.org/docs/overview/what-is-typesense.html) (2026-09-12)
- [Meilisearch welcome](https://www.meilisearch.com/docs/learn/getting_started/what_is_meilisearch) (2026-09-12)
- [Directus MCP](https://directus.io/docs/guides/ai/mcp) (2026-09-12)
- [PgTyped](https://pgtyped.dev/docs/) (2026-09-12)
- [postgres-meta](https://github.com/supabase/postgres-meta) (2026-09-12)
- [Google postgres-sql](https://googleapis.github.io/genai-toolbox/resources/tools/postgres/postgres-sql/) (2026-09-12)
- [Azure APIM MCP](https://learn.microsoft.com/en-us/azure/api-management/export-rest-mcp-server) (2026-09-12)
- [Hasura custom functions](https://hasura.io/docs/2.0/schema/postgres/custom-functions/) (2026-09-12)
- [Typesense NL search](https://typesense.org/docs/30.2/api/natural-language-search.html) (2026-09-12)
- [PostgREST schema isolation](https://docs.postgrest.org/en/stable/explanations/schema_isolation.html) (2026-09-12)

Sirovi search/extract JSON: `/tmp/ts-schema-codegen.json`,
`/tmp/db-to-mcp.json`, `/tmp/nl-json-search-admin.json`,
`/tmp/autowire-more.json`, `/tmp/autowire-extract.json`,
`/tmp/autowire-extract2.json`.
