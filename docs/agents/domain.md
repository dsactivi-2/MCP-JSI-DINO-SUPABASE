# Domenska dokumentacija

Repozitorij ima jedan domenski kontekst. Njegov rječnik je u korijenskom
[CONTEXT.md](../../CONTEXT.md), a **docs/decisions/** je jedini ADR direktorij.

## Čitanje prije rada

1. Pročitati [stanje projekta](../project.md), [CONTEXT.md](../../CONTEXT.md)
   i [inventar CRM-Scan](../discovery/crm-work-inventory.md) za već mapirane
   PHP-nalaze.
2. Pročitati važeće ADR-ove iz [decisions/README.md](../decisions/README.md).
3. Za zahtjeve koristiti
   [implementacijski brief](../SUPABASE_CRM_MCP_IMPLEMENTATION_BRIEF.md), a za
   discovery [runbook](../runbooks/schema-discovery.md).
4. Za SQL razvoj, testiranje, optimizaciju i release provjere koristiti
   [ADR-0004](../decisions/0004-automated-database-development.md) i
   [runbook automatizacije](../runbooks/database-development-automation.md).
5. Za MCP SDK, auth middleware ili Supabase runtime adapter koristiti
   [SDK plan](../planning/sdk-integration-plan.md) i njegovu primarnu provjeru.
   Preporuka, potvrđena odluka i izvršeni integration test imaju odvojene statuse.
   Za službene MCP design-skills koristiti
   [MCP server-dev tooling](mcp-server-dev-tooling.md). Za Linear, Serena,
   Git, plugin-e i wizards koristiti [tool routing](tool-routing.md).

## Održavanje

- U issueima, specifikacijama i kodu koristiti pojmove iz domenskog rječnika.
- Novi razriješeni domenski pojam dodati u `CONTEXT.md`; trenutni status i
  otvorene uslove održavati u `docs/project.md`.
- Dugoročne arhitekturne odluke zapisivati isključivo u `docs/decisions/`.
  Predlošci vještina koriste ovu putanju pri čitanju i pisanju ADR-ova.
- Konflikt s prihvaćenim ADR-om izričito navesti prije promjene. Zamjenu odluke
  dokumentirati novim ADR-om i eksplicitno označiti zamijenjenu odluku.
- Važeći ADR je red u [decisions/README.md](../decisions/README.md), ne svaka
  datoteka u tom direktoriju.
- [reviews](../reviews/), [worklogs](../worklogs/), [handoffs](../handoffs/) i
  [research](../research/) se ne prepisuju. Nova dated datoteka da; izmjena
  stare pada u `scripts/check-local.sh`.
- Kontekst, README i konfiguracija vještina upućuju na zahtjeve i odluke;
  ne prepisuju njihov sadržaj.
- Lokalni `AUTO-01`–`AUTO-08` ostaju privremeni ključevi pod `docs/planning/`.
  Wayfinder mapa ACT-100–109 već postoji; drugi map za isti cilj se ne kreira.
  Nova Linear issuea samo uz izričitu freigabe.
