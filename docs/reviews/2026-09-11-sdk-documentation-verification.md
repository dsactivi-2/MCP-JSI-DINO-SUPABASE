# Provjera SDK dokumentacijske konsolidacije

Datum: 2026-09-11. Opseg: lokalna dokumentacija i javni primarni izvori.

## Rezultat i granice

**PASS_WITH_GAPS:** SDK plan, brief, registar i postojeći radni paketi
usklađeni su kao neimplementirani prijedlog. Dokumentacijska provjera ne
dokazuje funkcionalan MCP server, OAuth tok ili bazna prava.

`ask-matt` je usmjerio rad na postojeći `grill-with-docs`/domenski kontekst,
`writing-for-agents` za održavanje dokumenata i `research` za nezavisnu
paralelnu provjeru izvora. Postojeći Matt setup i Linear pravila su zadržani;
nema novog setupa, implementacije ili vanjske objave specifikacije.

## Šta je korigovano

- [SDK primarna provjera](../research/mcp-supabase-sdk-integration.md) odvaja
  aktuelni MCP v2 od ranijeg v1 primjera i prati verziju HTTP protokola.
- [Integracijski plan](../planning/sdk-integration-plan.md) definira jedan
  MCP auth sloj, uslovni Supabase adapter, zaseban downstream token ugovor i
  opcionalnu alpha middleware. SDK-01–08 imaju postojeće vlasnike i pakete.
- [Brief](../SUPABASE_CRM_MCP_IMPLEMENTATION_BRIEF.md) sada opisuje server-side
  autentikaciju i strogu RPC granicu; SDK se ne predstavlja kao gotov CRM.
- [Registar](../planning/release-1-requirements.md) i
  [radni plan](../planning/release-1-automation-tickets.md) čuvaju postojeće
  blockere i dodaju provjerljivu SDK kompatibilnost umjesto nove platforme.
- Q11 bilježi stvarni dokumentacijski nalog, bez konačnog izbora stacka.
  README, projektni status, AGENTS i runbook vode do iste tehničke razrade;
  CONTEXT ostaje poslovni rječnik.
- Ispravljena je tvrdnja da nema `skills-lock.json`. Skill lock nije
  aplikacijski dependency lockfile i ne dokazuje instalaciju SDK-a.

Prihvaćeni ADR-0001/0003/0004 nisu zamijenjeni. Q8.5, Q4.5, opća potvrda
pretrage, fizički model i produkcijski gateovi nisu proglašeni riješenim.

Paralelni review usporedio je SDK izmjene s lokalnim snapshotom prije rada.
Ispravljena su oba nalaza: zabrana MCP token passthrougha sada je bez
uslovljavajuće formulacije, a istraživačka tabela razlikuje limite search,
profile i options alata. Ostale provjerene SDK promjene čuvaju postojeće
blockere i granice između prijedloga, odluke i implementacije.

## Reproducibilna verifikacija

Iz korijena repozitorija:

```bash
rtk proxy markdownlint-cli2 README.md AGENTS.md CONTEXT.md \
  docs/project.md docs/agents/domain.md docs/agents/supabase-tooling.md \
  docs/decisions/0002-search-design-interview.md \
  docs/SUPABASE_CRM_MCP_IMPLEMENTATION_BRIEF.md \
  docs/planning/sdk-integration-plan.md \
  docs/planning/release-1-requirements.md \
  docs/planning/release-1-automation-tickets.md \
  docs/research/mcp-supabase-sdk-integration.md \
  docs/runbooks/database-development-automation.md \
  docs/reviews/2026-09-11-sdk-documentation-verification.md
rtk proxy python3 tests/docs/relative_markdown_links_test.py
rtk proxy git diff --check -- README.md AGENTS.md CONTEXT.md docs
rtk proxy git diff --check
rtk git status --short
```

Markdownlint promijenjenih dokumenata, lokalni linkovi/fragmenti i scoped
`git diff --check` su PASS. Novi dokumenti dodatno prolaze Markdownlint jer
Git diff ne obuhvata untracked sadržaj. Konačni Bash izlazi provjeravaju se
nakon završnog reviewa.

## Preostali gapovi

- Globalni `git diff --check` nalazi trailing whitespace u ranije promijenjenoj
  vendoriziranoj `.agents/skills/supabase-postgres-best-practices/references/`
  `_contributing.md`, red 30. Ta datoteka nije mijenjana u ovoj SDK dopuni;
  globalni rezultat nije PASS.
- Traženi pomoćni skill `markdownlint` nije pronađen u lokalnom katalogu ni
  plugin cacheu; dostupan `markdownlint-cli2` izvršen je direktno prema README-u.
- Izvorni Supabase Markdown changelog nije dohvaćen; službeni HTML changelog
  i konkretne obavijesti pročitani su prema istraživačkom izvještaju.
- Nema aplikacijskog scaffolda, pinovanih SDK patch verzija ili izvršenih
  SDK-01–08. Build/typecheck, OAuth/client testovi, RLS/RPC, streaming,
  performance i rollout ostaju buduća evidencija nakon odgovarajućih gateova.

Zatečene promjene discovery dokumentacije, skripti, testova i vendoriziranih
skillsa nisu resetovane niti uključene kao rezultat ovog SDK rada. Nije bilo
pristupa produkciji, čitanja kandidata, instalacije, migracije, deploya,
commita ili Linear upisa.
