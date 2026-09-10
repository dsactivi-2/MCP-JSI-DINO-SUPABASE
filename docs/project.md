# Projektübersicht: Supabase CRM MCP

Status: Projektgrundlage und kontrollierte Discovery-Vorbereitung

Primarni jezik dokumentacije: B/H/S latinica

## Svrha

Projekt gradi siguran MCP sloj za prirodno pretraživanje približno 200.000 CRM
zapisa kandidata na B/H/S, njemačkom i engleskom.

Ciljni klijenti uključuju ChatGPT, Claude, Codex, Grok i druge
MCP-kompatibilne klijente.

## Autoritativni dokumenti

- `SUPABASE_CRM_MCP_IMPLEMENTATION_BRIEF.md` sadrži puni implementacijski brief,
  zahtjeve, faze, test-matricu i otvorena pitanja.
- `decisions/` sadrži prihvaćene dugoročne arhitekturne odluke.
- `runbooks/` sadrži sigurne i ponovljive operativne postupke.
- Root `AGENTS.md` definira pravila rada agenata u repozitoriju.

Ako se dokumenti ne slažu, rad se zaustavlja dok se konflikt ne razriješi
ažuriranjem briefa ili novim ADR-om.

## Potvrđene granice

- Baza ostaje autoritativni izvor rezultata.
- LLM proizvodi mali strukturirani filter, ne SQL.
- Cijela baza se nikada ne šalje modelu.
- Produkcijski pristup mora provoditi autentikaciju, autorizaciju, RLS i tenant
  izolaciju.
- Search rezultat ima najviše 50 kandidata po stranici.
- Kontaktni i osjetljivi podaci nisu dio osnovnog search rezultata.
- Nepoznate činjenice o shemi moraju se utvrditi kontrolisanim read-only auditom.
- Odluke koje utiču na kandidate ostaju pod ljudskim pregledom.

## Trenutno stanje

Repozitorij trenutno sadrži dokumentacijski brief i Serena projektnu
konfiguraciju. Aplikacijski jezik, framework, runtime, package manager, hosting,
auth model i fizički database ugovor još nisu odabrani ili potvrđeni.

Faza 0 nije završena dok nisu imenovani product, data, security, privacy/legal i
operativni vlasnici te odobren opseg read-only audita.

## Prvi isporučivi cilj

Prvi cilj je reproducibilan i pregledan discovery paket koji sadrži:

- inventar relevantnih shema, tabela, kolona, relacija, funkcija i indeksa;
- pregled RLS pravila, grantova, rola i tenant granica;
- anonimizirani data-quality baseline;
- mapiranje stvarne sheme na kanonski model kandidata;
- pregledive prijedloge JSON, MCP i RPC ugovora;
- evidentirane rizike, nepoznanice i potrebne vlasničke odluke.

Ovaj cilj ne uključuje produkcijske mutacije, deploy ili aktiviranje
credentiala.

## Minimalni proizvod

Minimalni produkcijski MCP izlaže:

1. `search_candidates`
2. `get_candidate_profile`
3. `get_filter_options`

Release nije spreman bez contract, multilingual, injection, RLS, pagination,
privacy, performance, rollback i interoperability dokaza definiranih u
implementacijskom briefu.
