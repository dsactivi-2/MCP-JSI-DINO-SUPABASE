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

| Dokument | Namjena |
| --- | --- |
| [AGENTS.md](AGENTS.md) | Pravila rada u repozitoriju. |
| [CONTEXT.md](CONTEXT.md) | Poslovni kontekst i domenski rječnik. |
| [docs/project.md](docs/project.md) | Trenutna faza, nedostaci i sljedeći cilj. |
| [Implementacijski brief](docs/SUPABASE_CRM_MCP_IMPLEMENTATION_BRIEF.md) | Zahtjevi, faze i kriteriji prihvata. |
| [ADR-0001](docs/decisions/0001-controlled-query-boundary.md) | Prihvaćena arhitekturna granica; ADR-ovi žive u [docs/decisions/](docs/decisions/). |
| [ADR-0002](docs/decisions/0002-search-design-interview.md) | Entwurf s pitanjima, odgovorima i otvorenim odlukama aktivnog design intervjua. |
| [ADR-0003](docs/decisions/0003-separated-profile-administration-mcp.md) | Prihvaćena granica i obaveze odvojenog Profilverwaltungs-MCP-a. |
| [Q8.4.2 istraživanje](docs/research/berufssuchprofile-q8-4-2.md) | Primarne reference i evaluacija kontrolisanih Berufssuchprofila. |
| [Audit i matrica korekcija](docs/reviews/decision-reconstruction-corrections.md) | Odobrene dokumentacijske korekcije, evidencija i otvorene odluke; izvorni audit ostaje historijski nalaz. |
| [Discovery runbook](docs/runbooks/schema-discovery.md) | Preduslovi i postupak odobrenog read-only audita. |
| [Supabase-Plugin Gate P](docs/discovery/supabase-plugin-read-only-gate-draft.md) | Neizvršivi NO-GO nacrt za eventualni projektno ograničen read-only Plugin pristup. |
| [Supabase tooling](docs/agents/supabase-tooling.md) | Obavezno usmjeravanje za instalirane Supabase skills i blokirani Live-MCP pristup. |
| [Istraživanje Supabase alata](docs/research/supabase-werkzeuge-fuer-crm-mcp.md) | Procjena plugina, MCP-a, skillsa, CLI-ja i kasnijih razvojnih alata. |
| [Objašnjenje Supabase skillsa](docs/research/supabase-agent-skills-einfach-erklaert.md) | Sadržaj, granice i postupak ažuriranja projektnih kopija skillsa. |
| [Issue tracker](docs/agents/issue-tracker.md), [triage oznake](docs/agents/triage-labels.md), [domenska pravila](docs/agents/domain.md) | Lokalni Matt Pocock setup. |

## Provjera dokumentacije

Iz korijena repozitorija, uz već dostupan `markdownlint-cli2`:

```bash
rtk proxy markdownlint-cli2 '*.md' 'docs/**/*.md'
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

Build, test i typecheck komande bit će definirane nakon izbora stacka i scaffolda.

## Lokalna provjera Gate-B1-V2 launchera

Ove provjere koriste isključivo sintetički Fake-\`psql\` u privremenim
direktorijima. Ne uspostavljaju mrežnu ili baznu vezu i ne predstavljaju
odobrenje Gatea B1 V2.

```bash
rtk proxy /bin/bash tests/discovery/gate_b1_launcher_test.sh
rtk proxy /opt/homebrew/bin/python3 tests/discovery/gate_b1_static_test.py
rtk proxy /bin/bash -n scripts/discovery/run-gate-b1.sh tests/discovery/gate_b1_launcher_test.sh
```
