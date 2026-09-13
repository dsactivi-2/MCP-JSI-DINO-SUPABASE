# Supabase CRM MCP

Sigurno višejezično pretraživanje približno 200.000 CRM kandidata kroz MCP
klijente. Repozitorij trenutno sadrži dokumentacijsku osnovu; aplikacijski
scaffold i pristup bazi još nisu uspostavljeni. Navedeni obim je projektna
procjena (DURCH DISCOVERY ZU PRÜFEN), ne potvrđen broj zapisa.

## Početak

Pročitati [stanje projekta](docs/project.md), zatim
[domenski kontekst](CONTEXT.md) i
[implementacijski brief](docs/SUPABASE_CRM_MCP_IMPLEMENTATION_BRIEF.md).

## Mapa dokumentacije

<!-- markdownlint-disable MD013 -->

| Dokument | Namjena |
| --- | --- |
| [AGENTS.md](AGENTS.md) | Pravila rada u repozitoriju. |
| [CONTEXT.md](CONTEXT.md) | Poslovni kontekst i domenski rječnik. |
| [docs/project.md](docs/project.md) | Trenutna faza, nedostaci i sljedeći cilj. |
| [Briefing-Intro](docs/planning/briefing-intro.md) | Kratki njemački uvod: Import, veličina banke, ciljni MCP, trenutni korak. |
| [Implementacijski brief](docs/SUPABASE_CRM_MCP_IMPLEMENTATION_BRIEF.md) | Zahtjevi, faze i kriteriji prihvata. |
| [ADR-0001](docs/decisions/0001-controlled-query-boundary.md) | Prihvaćena arhitekturna granica; ADR-ovi žive u [docs/decisions/](docs/decisions/). |
| [ADR-0002](docs/decisions/0002-search-design-interview.md) | Entwurf s pitanjima, odgovorima i otvorenim odlukama aktivnog design intervjua. |
| [ADR-0003](docs/decisions/0003-separated-profile-administration-mcp.md) | Prihvaćena granica i obaveze odvojenog Profilverwaltungs-MCP-a. |
| [ADR-0004](docs/decisions/0004-automated-database-development.md) | Prihvaćena automatizacija SQL razvoja, testiranja, optimizacije i release gateova. |
| [Runbook automatizacije baze](docs/runbooks/database-development-automation.md) | Redoslijed lokalnih, CI, performance i produkcijskih provjera nakon scaffolda. |
| [Plan automatizacijskih ticketa](docs/planning/release-1-automation-tickets.md) | Blockers-first nacrt ticketa prije zasebne Linear freigabe. |
| [SDK integracijski plan](docs/planning/sdk-integration-plan.md) | Ažurirani prijedlog MCP/Supabase sklopa, token granice i SDK-01–08 gateovi; nije implementacija. |
| [SDK primarna provjera](docs/research/mcp-supabase-sdk-integration.md) | Verzijske korekcije, auth/transport rizici i optimizacije iz službenih izvora. |
| [Provjera SDK dokumentacije](docs/reviews/2026-09-11-sdk-documentation-verification.md) | Lokalna verifikacija dopune i granice preostalog integracijskog dokaza. |
| [Q8.4.2 istraživanje](docs/research/berufssuchprofile-q8-4-2.md) | Primarne reference i evaluacija kontrolisanih Berufssuchprofila. |
| [Audit i matrica korekcija](docs/reviews/decision-reconstruction-corrections.md) | Odobrene dokumentacijske korekcije, evidencija i otvorene odluke; izvorni audit ostaje historijski nalaz. |
| [Discovery runbook](docs/runbooks/schema-discovery.md) | Preduslovi i postupak odobrenog read-only audita. |
| [Runbook CRM-Suchverdrahtung](docs/runbooks/crm-source-wiring-capture.md) | Quellcode zuerst: Maske → RPC, Output-Vorlage, OrbStack nur als Fallback. |
| [Plan CRM-Verdrahtung Schritt für Schritt](docs/runbooks/crm-wiring-human-plan.md) | Download-Anleitung: wo, welcher Befehl, was in die Vorlage. |
| [Wizards CRM-Verdrahtung](docs/runbooks/crm-wiring-wizards.md) | Welcher Wizard wann; 01 scannen, dann Codex oder 02, danach 03. |
| [Vorlage CRM-Verdrahtung](docs/discovery/crm-app-wiring.template.md) | Leeres Output-Dokument zum Ausfüllen außerhalb Git. |
| [Inventar CRM-Scan](docs/discovery/crm-work-inventory.md) | Landkarte: gemappte Daten, Dateien, Lücken, nächster Schritt. |
| [Codebefund PHP-Filter](docs/discovery/crm-app-wiring.md) | Lesart der alten `kandidati.php`-Filter-UI nach Wizard 01. |
| [Codebefund Filter-SQL](docs/discovery/crm-filter-sql-codebefund.md) | Wie `lista_kandidata` wirklich filtert. |
| [PHP-Suchzettel](docs/discovery/crm-php-hits/) | Wizard-01/04-`rg`-Output; nicht abschreiben. |
| [Codebefund Status/Klick/Cron](docs/discovery/crm-status-codebefund.md) | B7-Klicks, Ebenen, Cron. |
| [Codebefund C 4–9 Nachrichten](docs/discovery/crm-notify-codebefund.md) | Kanal und Auslöser je Statuswechsel; Produkt default aus. |
| [JSON-Filter Entwurf R1](docs/discovery/crm-json-filter-draft.md) | Entwurf geprüft, kein Vertrag. Struke/Smjer = Ausbildungsberuf; 5 Jahre nicht in R1. Offen: INNER JOIN, Archiv-Satz. |
| [Bericht-Audit Prompt](docs/handoffs/2026-09-13-verify-verifier-report.md) | Ablauf 2026-09-13 ausgeführt; Vorbericht-PASS nicht haltbar. |
| [Aktueller Session-Prompt](docs/handoffs/2026-09-13-aktueller-session-prompt.md) | Nutzer liest Verdict. Nicht Tool-Namen, nicht MCP. |
| [Handoff Scan-to-MCP](docs/handoffs/2026-09-13-scan-to-mcp.md) | Historische Session-Übergabe (Dump/Q4/step1-2). |
| [Statička CRM schema analiza](docs/discovery/crm-schema-static-analysis.md) | Redigirani inventar lokalnog Schema Visualizer izvoza bez bazne konekcije. |
| [Statička `crm_auth` analiza](docs/discovery/crm-auth-schema-static-analysis.md) | Redigirani pregled lokalnog auth/role/scope schema izvoza. |
| [Plan statičke schema analize](docs/discovery/schema-analysis-tasklist.md) | Siguran tok i checklist za lokalni Schema Visualizer export bez bazne konekcije. |
| [Supabase-Plugin Gate P](docs/discovery/supabase-plugin-read-only-gate-draft.md) | Neizvršivi NO-GO nacrt za eventualni projektno ograničen read-only Plugin pristup. |
| [Supabase tooling](docs/agents/supabase-tooling.md) | Obavezno usmjeravanje za instalirane Supabase skills i blokirani Live-MCP pristup. |
| [MCP server-dev tooling](docs/agents/mcp-server-dev-tooling.md) | Službeni MCP design-skills; remote HTTP i JSON-filter granica, bez produkcijskog spoja. |
| [Tool routing](docs/agents/tool-routing.md) | Instalirani Linear, Serena, Git, plugin-i, wizards i skills; dostupnost nije odobrenje. |
| [Istraživanje Supabase alata](docs/research/supabase-werkzeuge-fuer-crm-mcp.md) | Procjena plugina, MCP-a, skillsa, CLI-ja i kasnijih razvojnih alata. |
| [Brief za MCP/TypeScript auto-wire istraživanje](docs/research/mcp-autowire-research-brief.md) | Agent-prompt: obim baze, filteri u više nivoa i klase gotovih alata. |
| [Nalaz MCP/TypeScript auto-wire](docs/research/mcp-autowire-candidates.md) | Primarni izvori: nijedan auto-MCP nije siguran runtime; codegen i SDK v2 jesu. |
| [Usporedba tri ispravna puta](docs/research/mcp-autowire-top3-vergleich.md) | RPC, `gen types`+`.rpc()` i pgtyped: autonomija uz ADR-0001. |
| [Agent-Prompt Suche/Tabellen/Fehler](docs/research/mcp-search-agent-prompt.md) | Copy-paste: Tabellen, Suchlesarten, Ausbildung/Beruf/Freitext. |
| [Runbook Option 1 Setup](docs/runbooks/option-1-mcp-sdk-rpc-setup.md) | Lokales Eval: MCP SDK v2, Zod, synthetische Postgres-RPC. |
| [Optimalni SQL i automatizacijski put](docs/research/optimaler-sql-und-automatisierungsweg.md) | Primarne reference, rangiranje alata i prihvaćeni native-first cilj. |
| [Gate semantičke pretrage](docs/research/semantic-search-evaluation-gate.md) | Kriteriji, faze i stop-uslovi za poređenje FTS-a, `pgvector`-a i Vector Bucketa. |
| [Objašnjenje Supabase skillsa](docs/research/supabase-agent-skills-einfach-erklaert.md) | Sadržaj, granice i postupak ažuriranja projektnih kopija skillsa. |
| [Pristupni plan](docs/discovery/access-plan-consolidated.md) | Bootstrap, restore uslov, verzije gateova i naredna freigabe. |
| [Registar verzija pristupa](docs/discovery/role-version-register.md) | Status rola V1-V3, Gate-B1-V3 i odobrenja Q10.2g-Q10.2m. |
| [Plan PUBLIC prava](docs/discovery/public-rights-change-proposal.md) | Ciljni ACL rez Q10.2l A i residualnih osam LO privilegija. |
| [Karta odluka](docs/discovery/project-decision-map.md) | Fakti, odluke, prijedlozi, annahme, gateovi i kritični put. |
| [Gate B preflight](docs/discovery/security-read-only-discovery-preflight-b.md) | Aktivni read-only discovery gate i njegove granice. |
| [docs/reviews/](docs/reviews/) i [docs/worklogs/](docs/worklogs/) | Datirani dokazi; historijski nalazi se ne prepravljaju. |
| [Issue tracker](docs/agents/issue-tracker.md), [triage oznake](docs/agents/triage-labels.md), [domenska pravila](docs/agents/domain.md) | Linear ACT-100 mapa, triage i domenski unos. |

<!-- markdownlint-enable MD013 -->

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
