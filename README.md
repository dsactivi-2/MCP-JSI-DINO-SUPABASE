# Supabase CRM MCP

Sigurno višejezično pretraživanje približno 200.000 CRM kandidata kroz MCP
klijente. Repozitorij trenutno sadrži dokumentacijsku osnovu; aplikacijski
scaffold i pristup bazi još nisu uspostavljeni. Navedeni obim je projektna
procjena (DURCH DISCOVERY ZU PRÜFEN), ne potvrđen broj zapisa.

## Početak

Prvo [stanje projekta](docs/project.md). Pojmove u [CONTEXT.md](CONTEXT.md).
Zahtjeve u [briefu](docs/SUPABASE_CRM_MCP_IMPLEMENTATION_BRIEF.md) samo kad
treba ugovor ili kriterij prihvata, ne na početku svake sesije.

## Mapa dokumentacije

| Dokument | Namjena |
| --- | --- |
| [AGENTS.md](AGENTS.md) | Pravila rada agenata. |
| [CONTEXT.md](CONTEXT.md) | Domenski rječnik. |
| [docs/project.md](docs/project.md) | Faza, blocker, sljedeći korak. |
| [Implementacijski brief](docs/SUPABASE_CRM_MCP_IMPLEMENTATION_BRIEF.md) | Zahtjevi, faze, prihvat. |
| [docs/decisions/](docs/decisions/) | ADR-ovi, uključujući aktivni intervju ADR-0002. |
| [Inventar CRM-Scan](docs/discovery/crm-work-inventory.md) | PHP-scan landkarte. |
| [docs/agents/](docs/agents/) | Linear, tooling, routing. |
| [docs/runbooks/](docs/runbooks/) | Discovery, wiring, automatizacija. |
| [docs/discovery/](docs/discovery/) | Codebefund, gate, filter-nacrt. |
| [docs/research/](docs/research/), [reviews](docs/reviews/), [worklogs](docs/worklogs/), [handoffs](docs/handoffs/) | Dokaz; historijski se ne prepisuje. |
| [Plan statičke schema analize](docs/discovery/schema-analysis-tasklist.md) | Lokalni schema izvoz bez bazne konekcije. |
| [Supabase-Plugin Gate P](docs/discovery/supabase-plugin-read-only-gate-draft.md) | NO-GO nacrt; plugin nije odobren. |

## Konsolidovani plan

[Registar zahtjeva](docs/planning/release-1-requirements.md),
[radni paketi](docs/planning/release-1-automation-tickets.md),
[A01–A12 matrica](docs/planning/audit-correction-matrix.md) i
[pristupni plan](docs/discovery/access-plan-consolidated.md) vode lokalnu
<!-- markdownlint-disable-next-line MD013 -->
korekturu. [Prüfbericht](docs/reviews/2026-09-11-local-correction-verification.md)
navodi stvarne rezultate i otvorene granice.

## Provjera dokumentacije

Iz korijena repozitorija, uz već dostupan `markdownlint-cli2`:

```bash
rtk proxy markdownlint-cli2 '*.md' 'docs/**/*.md'
rtk proxy python3 tests/docs/relative_markdown_links_test.py
rtk git diff --check
rtk git status --short
```

Repozitorij trenutno nema opći `.markdownlint.json`; zato je puna lint provjera
dijagnostička i može prijaviti postojeći dug. Uska konfiguracija
`tests/docs/markdownlint-gate-b.json` vrijedi samo za Gate-B testne artefakte i
ne treba je primjenjivati kao opće pravilo. Uz lint provjeriti ciljne datoteke,
direktorije i fragmente svih Markdown referenci te dostupnost javnih vanjskih
referenci. Lint sam ne potvrđuje sve linkove. Ako alat ili referenca nisu
dostupni, zabilježiti nedostatak.

Link/fragment checker zadano čita Working Tree, uključujući nove root/docs
Markdown datoteke. `--source index` eksplicitno bira staged snapshot.
Parser pokriva lokalne inline linkove i ATX headings izvan fenced code blokova;
ne predstavlja puni CommonMark renderer niti provjerava javni web.

Aplikacijske build/test/typecheck komande bit će definirane nakon izbora
stacka i scaffolda. Lokalni dokumentacijski i Fake-psql testovi već postoje.
Njihov obavezni redoslijed i gateovi već su određeni u
<!-- markdownlint-disable-next-line MD013 -->
[runbooku automatizacije baze](docs/runbooks/database-development-automation.md).

## Lokalna provjera plana schema izvoza

Provjera ne čita izvornu produkcijsku datoteku i ne uspostavlja konekciju:

```bash
rtk proxy /opt/homebrew/bin/python3 tests/docs/schema_analysis_tasklist_static_test.py
```

## Lokalna provjera Gate-B1-V2 launchera

Ove provjere koriste isključivo sintetički Fake-\`psql\` u privremenim
direktorijima. Ne uspostavljaju mrežnu ili baznu vezu i ne predstavljaju
odobrenje Gatea B1 V2.

```bash
rtk proxy /bin/bash tests/discovery/gate_b1_launcher_test.sh
rtk proxy /opt/homebrew/bin/python3 tests/discovery/gate_b1_static_test.py
rtk proxy /opt/homebrew/bin/python3 tests/discovery/gate_b2_scope_static_test.py
rtk proxy /bin/bash -n scripts/discovery/run-gate-b1.sh
rtk proxy /bin/bash -n tests/discovery/gate_b1_launcher_test.sh
```

## Zajednički lokalni dokumentacijski i Fake-gate

```bash
rtk proxy /bin/bash scripts/check-local.sh
```

Isti ulaz može koristiti CI kada bude odobren. Izvršava postojeće lokalne
Python/Fake testove, pojedinačne Bash syntax provjere, aktivni Markdownlint,
Working-Tree linkove i `git diff --check`; svaki neuspjeh vraća nonzero.
Ne pokreće produkcijski launcher, SQL, DB scaffold ili backup.

Puni Markdownlint svih root/docs datoteka ostaje dijagnostička provjera iznad.
Historijski auditi, worklogovi i izvorni statički nalazi ne prepravljaju se radi
novog zelenog rezultata. Spisak takvih arhivskih izuzetaka je eksplicitan u
skripti; sve ostale datoteke uključujući nove aktivne dokumente se provjeravaju.
Duge usporedne tabele imaju samo lokalnu MD013 iznimku; ostala lint pravila
ostaju aktivna. Redigirani izlaz ne sadrži stvarni projektni endpoint.
