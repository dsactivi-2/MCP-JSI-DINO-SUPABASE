<!-- markdownlint-disable MD013 -->
# Usporedba tri ispravna puta: autonomija uz ispravno izvršenje

Datum: 2026-09-12

Status: usporedba iz [nalaza](mcp-autowire-candidates.md); nije AUTO-02
odluka, nije instalacija, nije pristup bazi

## Zašto baš ove tri

Alati koji se sami spoje na cijelu CRM shemu nisu ispravni: LLM dobija SQL
ili CRUD, a `crm_api.search_candidates` već nudi e-mail i telefon. Od
kandidata koji **smiju** izvršavati pretragu ostaju samo uski, ručno
ograničeni putevi. Među njima su ova tri najautonomnija, a da i dalje
poštuju [ADR-0001](../decisions/0001-controlled-query-boundary.md):

| # | Opcija | Zašto je u finalu | Autonomija | Ispravnost |
| --- | --- | --- | --- | --- |
| 1 | MCP SDK v2 + Zod + PostgreSQL RPC | Već predloženi runtime u [SDK planu](../planning/sdk-integration-plan.md) | Srednja: shema alata validira JSON; SQL živi u jednoj funkciji | Najviša: nema table API-ja |
| 2 | Ista MCP granica + `supabase gen types` + samo `.rpc()` | Najbliže „baza se sama spoji u TypeScript“ uz službeni klijent | Viša: potpisi RPC-ja dolaze iz sheme | Visoka samo ako `.from()` ostane zabranjen |
| 3 | Ista MCP granica + `pgtyped` SQL allowlista | Najuža izvršna površina: postoje samo committani upiti | Visoka na SQL strani; MCP i dalje pišemo | Visoka: nema ORM CRUD-a |

Zajednički sloj za sva tri: LLM u klijentu prevodi jezik u JSON filter.
[Structured Outputs](https://platform.openai.com/docs/guides/structured-outputs)
mogu to učvrstiti. To nije četvrta opcija, nego pojačanje nivoa 0→1.

Google MCP Toolbox `postgres-sql` je srodnik opcije 3 s više host
autonomije i slabijim MCP-auth/Supabase fitom; vidi odjeljak ispod.

## Zajednički ugovor koji nijedna opcija ne smije dirati

- Tri alata: `search_candidates`, `get_candidate_profile`,
  `get_filter_options`.
- Ulaz je validiran JSON, ne SQL, ne ime tabele, ne expression.
- Postgres (ili ekvivalentni parametrizirani upit) filtrira, rangira,
  paginira; najviše 50 redova; Release 1 bez kontakata.
- MCP token ≠ DB credential.
- Runtime-Such-MCP je read-only; Profilverwaltungs-MCP ostaje odvojen.
- Stari `crm_api.search_candidates` se ne wrapa 1:1.

Taksonomija, Berufssuchprofil, Q7 i redakcija PII ostaju naš kod u sva
tri slučaja.

## Opcija 1 — MCP SDK v2 + Zod + PostgreSQL RPC

### 1. Tok spoja i izvršenja

```text
Klijent (ChatGPT/Claude/Codex)
  → MCP SDK v2 (registerTool + Zod)
  → poslovni validator (allowliste, identitet, cap)
  → jedan parametrizirani Postgres RPC
  → RLS + filter + rank + keyset
  → mala stranica + match evidence
```

SDK validira argumente alata prije handlera.
[MCP TS SDK v2](https://ts.sdk.modelcontextprotocol.io/v2) (2026-09-12).
Handler ne bira tabelu; zove jednu unaprijed napisanu funkciju.
PostgreSQL ostaje autoritativan, kako zahtijeva ADR-0001.

### 1. Šta je autonomno

- JSON ulaz se ne parsira ručno; Zod/JSON Schema odbija nepoznata polja.
- Klijentski LLM popunjava tool arguments iz prirodnog jezika.
- Jedan RPC može sadržavati cijelu filtersemantiku, pa MCP ostaje tanak.

### 1. Šta i dalje pišemo

- Tri `registerTool` definicije i izlaznu allowlistu.
- RPC potpis, RLS, projekciju bez kontakata, cursor, timeout.
- Auth adapter (MCP audience, downstream identitet).
- Taksonomiju i verziju Berufssuchprofila.

### 1. Veza s bazom

Direktni Postgres klijent ili uski adapter. Nema generisanog table
klijenta, pa nema slučajnog `.from('idk_kandidati')`. Token ugovor je
onaj iz SDK plana: ulazni MCP token se ne prosljeđuje Data API-ju.

### 1. Rizici

- Najmanje „gotovog“ koda; više ručnog SQL-a.
- Loš RPC (preširoka projekcija, SECURITY DEFINER) krši R1 jednako kao
  loš auto-MCP.
- Bez codegen-a tipovi RPC argumenata mogu odstupiti od stvarne funkcije.

### 1. Kad birati

Default ako želimo najmanju izvršnu površinu i isti put kao ADR + SDK
plan. Discovery i dalje mora dati kanonski model prije potpisa RPC-ja.

## Opcija 2 — MCP SDK v2 + `supabase gen types` + samo `.rpc()`

### 2. Tok spoja i izvršenja

```text
Klijent
  → isti MCP SDK v2 + Zod
  → supabase-js createClient<Database>()
  → samo .rpc('search_candidates_v1', args)
  → PostgREST / Postgres funkcija
  → RLS
```

`supabase gen types` radi TypeScript iz sheme, uključujući stored
procedures. [Generating types](https://supabase.com/docs/guides/api/rest/generating-types)
(2026-09-12). `--schema` sužava sheme, ne pojedinačne funkcije. Tipovi
sadrže i `Tables`. Ispravnost zavisi od discipline: handler smije zvati
samo imenovane RPC-je.

`@supabase/server` ostaje kandidat za JWT kontekst ako AUTH-01 to
dokazuje; nije zamjena za MCP.

### 2. Šta je autonomno

- Potpisi argumenata i rezultata RPC-ja prate bazu bez ručnog
  prepisivanja kolona.
- Službeni klijent rješava pooler, REST i (ako je odobreno) user JWT/RLS.
- Regeneracija tipova nakon migracije je jedna CLI komanda.

### 2. Šta i dalje pišemo

- Ista tri MCP alata i Zod filter kao u opciji 1.
- Iste Postgres funkcije; gen types ih ne stvara.
- Lint/CI zabranu `.from(`, `.schema(` i generic SQL u runtime paketu.
- Izdvajanje search sheme ako Data API inače vidi `crm` tabele.

### 2. Veza s bazom

Najprirodniji službeni spoj na Supabase. Downstream credential i dalje
mora biti odvojen od MCP tokena. `service_role` ostaje zabranjen kao
prečica. Produkcijski `gen types --project-id` na CRM s PII nije dio
ovog chata; lokalni/sintetički izvor tek nakon odobrenog puta.

### 2. Rizici

- Generisani `Database['public']['Tables']` vodi programera na CRUD.
  Jedan `.from('idk_kandidati').select('*')` ruši R1.
- Ako je izložena stara funkcija s telefonom, `.rpc()` je tipiziran i
  izgleda „ispravno“, a i dalje curi PII.
- `postgres-meta` iza CLI-ja nema vlastiti security sloj; ne smije biti
  runtime MCP. [postgres-meta](https://github.com/supabase/postgres-meta)

### 2. Kad birati

Kad opcija 1 treba tipizirani Supabase adapter. To je **ista arhitektura**
s boljim TS spojem, ne drugi proizvod. Preduslov: RPC allowlista u kodu
i testu, ne samo u recenziji.

## Opcija 3 — MCP SDK v2 + `pgtyped` SQL allowlista

### 3. Tok spoja i izvršenja

```text
Klijent
  → isti MCP SDK v2 + Zod
  → pgtyped PreparedQuery iz committanog .sql fajla
  → pg Client (parametri odvojeni od SQL teksta)
  → Postgres
```

`pgtyped` nije ORM. CLI čita **naše** annotated SQL fajlove, pita
Postgres za tipove, emitira `PreparedQuery`. Runtime šalje query i
parametre odvojeno. [PgTyped](https://pgtyped.dev/docs/) (2026-09-12).
Allowlista = Git. Čega nema u `.sql`, to se ne može pozvati.

### 3. Šta je autonomno

- Tipovi i izvršenje prate SQL koji smo već odobrili.
- Nema table klijenta; nema `.from()`.
- LLM i dalje vidi samo JSON alata; SQL string mu nije dostupan.
- Tri search upita mogu živjeti kao tri fajla, paralelno s MCP tool
  imenima.

### 3. Šta i dalje pišemo

- SQL za search/profile/options, uključujući cap 50, redakciju, keyset.
- Mapiranje Zod filtera na SQL parametre (nizovi zanimanja, raspon dobi).
- Isti MCP auth sloj kao u opciji 1.
- Migracije/indekse i dalje po ADR-0004; pgtyped ih ne uvodi.

### 3. Veza s bazom

`pg` Pool + `DATABASE_URL`. To je jedna DB rola, nije MCP JWT. RLS
vrijedi samo ako ta rola nije superuser/bypass i ako je RLS forsiran.
User-scoped identitet treba `SET ROLE` / `set_config` ili Postgres
funkciju koja čita `auth.uid()` — inače je ovo slabije od opcije 2 s
user JWT.

### 3. Rizici

- README: API se još može mijenjati.
- Složeni filteri (ANY/ALL, profil članovi, keyset) u čistom SQL-u brzo
  postaju teži za održavanje od jednog RPC-ja.
- Connection string u MCP procesu je credential; curenje procesa = DB
  pristup, ne samo tool katalog.
- Bez Postgres funkcije teže dijeliti isti ugovor s budućim HTTP klijentom.

### 3. Kad birati

Kad želimo najužu izvršnu listu **prije** kanonskog RPC-ja, npr. rani
vertikalni test na sintetičkoj bazi. Za produkcijski Runtime-Such-MCP
opcija 1/2 ostaje čistija granica (jedna funkcija, RLS, jedan potpis).

### Srodnik: Google MCP Toolbox `postgres-sql`

Custom tool je unaprijed napisan prepared statement; prebuilt
`execute_sql` je NO-GO.
[postgres-sql](https://googleapis.github.io/genai-toolbox/resources/tools/postgres/postgres-sql/)
(2026-09-12). Više autonomije hosta (YAML alati, spreman MCP), ali novi
runtime, IAM/source model i slabiji fit na MCP resource audience +
Supabase JWT. Koristiti samo ako namjerno želimo Toolbox kao MCP
proces, ne kao zamjenu za Zod filter.

## Matrica

| Dimenzija | 1 RPC | 2 gen types + `.rpc()` | 3 pgtyped |
| --- | --- | --- | --- |
| LLM vidi SQL? | Ne | Ne | Ne |
| Postoji table CRUD u runtime klijentu? | Ne | Da, u tipovima; zabraniti u kodu | Ne |
| Autonomija spoja na bazu | Ručni adapter | Najviša (službeni klijent + tipovi) | Visoka (SQL→TS) |
| Autonomija izvršenja | Jedan RPC | Isti RPC preko PostgREST | Samo Git SQL |
| MCP auth / dva tokena | Najlakše uskladiti sa SDK planom | Dobro, ako AUTH-01 dokaže JWT put | Slabije: pool rola |
| RLS po korisniku | U funkciji / `SET ROLE` | Data API + JWT, ako je odobreno | Samo ako pool to provede |
| Regeneracija nakon sheme | Ručno | `gen types` | `pgtyped` nad SQL fajlovima |
| Opasnost starog CRM RPC-ja | Wrap 1:1 | Wrap 1:1, još i tipiziran | Wrap 1:1 ako taj SQL commitujemo |
| Profilverwaltungs-MCP | Zaseban proces | Zaseban proces | Zaseban proces |
| Dodatni vendor | Ne | Supabase (već platforma) | pgtyped (mali) / Toolbox (veći) |
| Fit za Release 1 | Najčišći | Najbolji TS spoj uz disciplinu | Najbolji rani tracer, slabiji auth |
| Šta ostaje 100 % ručno | Filter, profili, Q7, redakcija | Isto | Isto, plus SQL umjesto RPC |

## Šta sve tri **ne** rade

- Ne razumiju B/H/S–DE–EN sinonime same od sebe.
- Ne grade Berufssuchprofil ni many-to-many članstvo.
- Ne kriju kontakte ako SQL/RPC ih selektuje.
- Ne zamjenjuju Gate B ni discovery.
- Ne smiju se spajati na produkcijski developer plugin.

## Preporuka za sljedeći korak

Ne birati treći proizvod. Birati **slojnicu**:

1. **Runtime ugovor = opcija 1.** Tri MCP alata, Zod, jedna search RPC.
   To ostaje ADR-kompatibilno i pokriva AUTO-02 evaluaciju.
2. **TS spoj = opcija 2 kao adapter unutar opcije 1**, čim postoji
   odobrena funkcija. `gen types` za `Functions`, CI zabranjuje
   `.from(` u runtime paketu.
3. **Opcija 3 samo kao lokalni tracer** ako RPC još ne postoji: tri
   pgtyped upita na sintetičkoj bazi, isti Zod ulaz. Ne promovirati to
   u produkcijski MCP dok auth/RLS nije isti kao u 1/2.

Ako se kasnije želi još autonomniji host, prvo izmjeriti Toolbox ili
Azure APIM **nad već postojećim tri operacije**, nikad nad PostgREST
dumpom.

## Izvori

- [ADR-0001](../decisions/0001-controlled-query-boundary.md)
- [SDK integracijski plan](../planning/sdk-integration-plan.md)
- [Nalaz auto-wire](mcp-autowire-candidates.md)
- [MCP TS SDK v2](https://ts.sdk.modelcontextprotocol.io/v2)
- [Supabase generating types](https://supabase.com/docs/guides/api/rest/generating-types)
- [PgTyped](https://pgtyped.dev/docs/)
- [Google postgres-sql](https://googleapis.github.io/genai-toolbox/resources/tools/postgres/postgres-sql/)
- [OpenAI Structured Outputs](https://platform.openai.com/docs/guides/structured-outputs)
