# Tool routing za agente

Status: inventar 2026-09-13; dostupnost alata nije odobrenje

Ovaj dokument veže instalirane skills, plugin-e i MCP-ove na prihvaćene CRM
granice. Globalni MCP redoslijed ostaje u dijeljenom routing fajlu; ovdje
vrijedi samo ovaj repozitorij.

## Instalirano i dozvoljeno

<!-- markdownlint-disable MD013 -->

| Komponenta | Gdje | Uloga ovdje |
| --- | --- | --- |
| Linear plugin | native Codex Linear | Jedini issue tracker. Projekt **Dino problem baza CRM**, tim `ACT`. |
| Git MCP | globalni stdio `git` | Svaki poziv s `repo_path` na ovaj repozitorij; inače `rtk git`. |
| Serena | `.serena/` | Simboli i memories. Ako MCP nije spojen: lokalni files. |
| `supabase` skill | `.agents/skills/supabase/` | Planiranje, auth/RLS/CLI review. Nije dokaz sheme. |
| `supabase-postgres-best-practices` | `.agents/skills/supabase-postgres-best-practices/` | SQL/indeks/RLS review. Nije produkcijski apply. |
| Supabase plugin/MCP | native Codex | `search_docs` smije. Projekt, shema, SQL i podaci su blokirani. Gate P je `NO-GO`. |
| `mcp-server-dev` | plugin skills `build-mcp-server` / `build-mcp-app` / `build-mcpb` | Samo dizajn. Vidi [MCP server-dev tooling](mcp-server-dev-tooling.md). |
| `example-server` | Codex MCP | Protokolni primjer. Nije CRM ni Postgres sloj. |
| `start-matt-wizard` | `.agents/skills/start-matt-wizard/` | Samo na izričit zahtjev. Ovaj repo je već postavljen. |
| CRM wizards | `scripts/wizards/` | PHP-Verdrahtung. Wizard 01 bez limita 200 linija; broj je `wc -l` cijele datoteke. |
| `scripts/check-local.sh` | `scripts/` | Jedini lokalni dokazni ulaz. |

<!-- markdownlint-enable MD013 -->

Vendorizirane Supabase skill direktorije ne mijenjati ručno. Postupak
ažuriranja je u [Supabase tooling](supabase-tooling.md). Skill procedure
vrijede; skill MCP/CLI prečice (`execute_sql`, `get_advisors`, OAuth na
produkcijski projekt) ovdje ne vrijede. Vidi
[skill pravila](supabase-tooling.md#skill-pravila-u-ovom-projektu).

## Linear

Identitet projekta i tok rada: [issue tracker](issue-tracker.md).

Wayfinder mapa **ACT-100**–**ACT-109** postoji od 2026-09-12. Naslovi još
govore Jobstep/OrbStack. Izričite odgovore daju [ADR-0002](../decisions/0002-search-design-interview.md)
Q17 i Q20–Q22. Ta pitanja se ne otvaraju ponovo iz Linear naslova.

`AUTO-01`–`AUTO-08` ostaju lokalni ključevi u
[planu automatizacije](../planning/release-1-automation-tickets.md). Nisu
Linear ID-ovi. Drugi wayfinder map za isti cilj se ne kreira.

## Zabranjeni spojevi

- Generic Postgres MCP protiv ovog projekta.
- Developer plugin/MCP na produkcijski CRM projekt ili restore klon.
- Auto-SQL MCP kao Runtime-Such-MCP.
- Scaffold Runtime-Such-MCP dok korisnik to izričito ne zatraži.

## Fallback

Ako Serena, Context7 ili drugi MCP nisu spojeni u sesiji, raditi dalje
lokalnim čitanjem. Ne instalirati ni prekonfigurisati MCP zbog ove mape.
