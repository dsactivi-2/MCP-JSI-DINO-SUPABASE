# MCP server-dev tooling

Status: službeni design-skills su instalirani; runtime Search-MCP nije
scaffoldiran i nije spojen na produkciju

Ovaj dokument veže službeni plugin **mcp-server-dev** na prihvaćene CRM
granice. Plugin je vođeni workflow za dizajn MCP alata, ne gotov Recruiting
server i ne odobrenje baze.

## Šta je instalirano

<!-- markdownlint-disable MD013 -->

| Komponenta | Gdje | Uloga ovdje |
| --- | --- | --- |
| `build-mcp-server` | Codex plugin `mcp-server-dev@mcpmarket`; Claude plugin `mcp-server-dev@claude-plugins-official` | Ulaz: use case, deployment, tool-design, auth. |
| `build-mcp-app` | isti plugin | Kasniji UI widgeti (npr. candidate picker); nije R1 default. |
| `build-mcpb` | isti plugin | Lokalni bundled server; nije izbor za Cloud-Postgres/Supabase. |
| Službeni MCP example server | već postojeći Codex MCP `example-server` | Samo protokolni primjer; nije CRM niti Postgres sloj. |
| Postgres reference server | nije registriran | Samo obrazac DB-sloja iz službenih [example servers](https://modelcontextprotocol.io/examples); bez live DSN. |

<!-- markdownlint-enable MD013 -->

Marketplace za Claude je `anthropics/claude-plugins-official`. Codex nema
isti Claude marketplace format, pa je plugin lokalno zapakovan u
`~/plugins/mcp-server-dev` uz Apache-2.0 LICENSE i NOTICE.

Novi Codex task treba učitati skillove. Ova sesija ih još ne vidi.

## Šta nije urađeno

- Nije scaffoldiran Runtime-Such-MCP niti Profilverwaltungs-MCP.
- Nije dodan generic Postgres MCP, `execute_sql` alat ili LLM-SQL put.
- Supabase developer plugin/MCP i dalje se ne smije spojiti na produkcijski
  CRM projekt. Gate P ostaje `NO-GO`; Gate B ostaje lokalni `psql` launcher.
- `set_status` i `trigger_notification` nisu dodani kao runtime search
  alati. PHP ih katalogizira kao CRM sposobnosti (Q21); C 4–9 ima produktni
  default isključen. Write/notify MCP čeka zaseban ugovor i odobrenje.

## Obavezni redoslijed

1. Pročitati [stanje projekta](../project.md),
   [ADR-0001](../decisions/0001-controlled-query-boundary.md) i
   [SDK plan](../planning/sdk-integration-plan.md).
2. Za dizajn servera učitati skill `build-mcp-server`, zatim samo potrebne
   reference (`tool-design.md`, `remote-http-scaffold.md`, `auth.md`).
3. Primijeniti donju CRM matricu umjesto generic primjera iz skilla.
4. Scaffold raditi samo u sintetičkom/neprodukcijskom okruženju, npr.
   [Option 1 Setup](../runbooks/option-1-mcp-sdk-rpc-setup.md).
5. Scaffold samo na izričit zahtjev. Bericht-Audit 2026-09-13 je izvršen.
   JSON ostaje nacrt. Nema produkcijskog MCP-a.

Skillovi daju obrasce. Oni ne dokazuju shemu, ne biraju stack i ne
mijenjaju ADR-ove.

## CRM matrica za `build-mcp-server`

<!-- markdownlint-disable MD013 -->

| Pitanje skilla | Projektni odgovor | Izvor |
| --- | --- | --- |
| Šta se povezuje? | Cloud Postgres/Supabase preko kontrolisane RPC, ne preko slobodnog SQL-a. | ADR-0001 |
| Ko koristi? | Interni Vermittler vidi cijeli pool i kontakte; Kunde vidi predložene kandidate bez kontakata dok CONTACT-02. | ADR-0002 Q4 |
| Koliko akcija? | Mala površina, Pattern A (jedan alat po akciji), ispod ~15. | SDK plan |
| Deployment | Remote streamable HTTP. MCPB/local stdio nisu default. | ovaj dokument; skill default za cloud API |
| Auth | MCP audience odvojen od downstream DB identiteta. Nema admin/service-role klijenta. | SDK plan |
| UI widgeti | Nisu R1. `build-mcp-app` tek ako elicitation ne pokrije picker. | ADR-0001; skill Phase 2 |
| Developer plugin | Nikad na produkcijski projekt s pravim podacima kandidata. | [Supabase tooling](supabase-tooling.md) |

<!-- markdownlint-enable MD013 -->

Postgres reference server smije inspirisati DB adapter (parametrizirani
pristup, pagination, timeout). Ne smije postati runtime alat. LLM emituje
samo validirani JSON filter; PostgreSQL filtrira, rangira i paginira.
Search cap ostaje 50.

## Ugovor alata

Runtime-Such-MCP objavljuje samo:

- `search_candidates`
- `get_candidate_profile`
- `get_filter_options`

Nazivi su ugovor alata, ne fizički SQL. Profilverwaltungs-MCP ostaje
odvojena granica po [ADR-0003](../decisions/0003-separated-profile-administration-mcp.md).

Kandidati iz brifinga kao `set_status` ili `trigger_notification` idu u
kasniji, odvojeni write/workflow MCP, ne u read-only search ugovor.

Gotov auto-SQL MCP nije siguran runtime. Vidi
[nalaz auto-wire](../research/mcp-autowire-candidates.md).

## Invokacija

- Codex, novi task: zatražiti skill `build-mcp-server` ili plugin
  `mcp-server-dev`.
- Claude Code: `/mcp-server-dev:build-mcp-server`.
- Ne pokretati scaffold dok discovery/audit faza to ne dopusti i dok nije
  dato odobrenje za neprodukcijsko okruženje.

Inventar ostalih instaliranih alata je u [tool routing](tool-routing.md).
