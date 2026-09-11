# Supabase tooling za agente

Status: projektne skills kopije su dostupne; Live-MCP pristup bazi nije odobren

Ovaj dokument određuje kako agenti koriste službene Supabase skills i plugin
bez proširenja trenutnog governance ili database opsega.

## Razdvajanje odgovornosti

| Komponenta | Uloga | Trenutni status |
| --- | --- | --- |
| `supabase` skill | Aktuelne procedure za Supabase, auth, RLS, CLI, MCP i debugging. | Dozvoljeno za planiranje i review. |
| `supabase-postgres-best-practices` skill | Pravila za SQL, shemu, indekse, RLS, funkcije, konekcije i planove. | Dozvoljeno za planiranje i statički SQL review. |
| Supabase plugin/MCP | Live razvojni alati za projekt, bazu, advisors, migracije i druge Supabase funkcije. | Dokumentacija je dozvoljena; pristup projektu/bazi je blokiran do zasebnog gatea. |
| Runtime-Such-MCP | Budući kontrolisani CRM search ugovor. | Nije implementiran; plugin ga ne zamjenjuje. |
| Profilverwaltungs-MCP | Buduća odvojena administrativna granica iz ADR-0003. | Nije implementiran; plugin nije njegova sigurnosna granica. |

Više instaliranih distribucija službenog Supabase plugina mogu pokazivati na isti
Supabase app/MCP. One ne daju dodatna prava, redundanciju, projektno ograničenje
ili razdvojene identitete. Jedna aktivna distribucija je funkcionalno dovoljna.

## Obavezni redoslijed

1. Pročitati [stanje projekta](../project.md), relevantne ADR-ove i odgovarajući
   runbook.
2. Za svaki Supabase zadatak učitati `.agents/skills/supabase/SKILL.md`.
3. Prije SQL-a, sheme, migracije, RLS-a, funkcije, indeksa ili `EXPLAIN` plana
   učitati i `.agents/skills/supabase-postgres-best-practices/SKILL.md`, zatim
   samo relevantne reference.
4. Provjeriti aktuelni Supabase changelog i jednu mjerodavnu službenu stranicu
   prije implementacije ili promjene dugoročnog pravila.
5. Odvojiti preporuku iz skilla od potvrđene projektne činjenice. Fizička shema,
   tenant, role i RLS ostaju `DURCH DISCOVERY ZU PRÜFEN` do odobrenog audita.

## Live-MCP gate

Javni `search_docs` može se koristiti bez pristupa projektu. Svi pozivi koji
čitaju ili mijenjaju Supabase account, projekt, shemu, logove ili podatke čekaju
zasebno odobrenje.

Plugin/MCP put mora prije prvog database poziva dokazati:

- tačan lokalno attestiran `project_ref`, bez upisa identifikatora u Git ili chat;
- `read_only=true` i stvarni PostgreSQL identitet bez owner, migration,
  `BYPASSRLS`, superuser ili write prava;
- najviše feature grupe `database,debugging,docs`;
- app postavku `Always ask` dok discovery nije odobren, a nakon toga najmanje
  potvrdu prije svakog write ili osjetljivog read poziva;
- pregledanu SQL allowlistu, statement timeout, ograničenje rezultata i zabranu
  automatskog retryja;
- redakciju i siguran output izvan repozitorija, bez kontakata, CV teksta,
  tajni ili nepotrebnog PII-a.

`execute_sql` je opći SQL alat i ne smije se koristiti samo zato što je vidljiv.
`list_tables` i `get_advisors` također čekaju gate jer otkrivaju projektne
metapodatke. Mutirajući projekt-, branch-, migration-, Edge-Function- i Storage-
alati nisu dio read-only discovery opsega.

Trenutni [Gate B](../discovery/security-read-only-discovery-preflight-b.md)
ostaje vezan za svoj lokalni `psql` launcher. Plugin/MCP zahtijeva novu
gate verziju; odobrenje jednog puta ne prenosi se na drugi.

## Ažuriranje skillsa i plugina

Projektne skill direktorije tretirati kao vendorizirane cjeline. Ne mijenjati
njihov sadržaj ručno i ne kopirati samo `SKILL.md`; reference, assets i changelog
moraju ostati zajedno.

Pri ažuriranju:

1. pregledati službeni changelog plugina i oba skillsa;
2. provjeriti projektne instalacije sa `rtk proxy npx skills list`;
3. nakon pregleda izvora ažurirati samo ova dva projektna skilla:

   ```bash
   rtk proxy npx skills update supabase supabase-postgres-best-practices -p
   ```

4. ažurirati iz jednog odabranog službenog izvora, ne iz dvije distribucije;
5. pregledati puni Git diff pod `.agents/skills/` i potvrditi izvor;
6. provjeriti da su oba `SKILL.md`, changelogovi i sve referentne datoteke
   prisutni te da nema tajni ili lokalnih identifikatora;
7. pokrenuti dokumentacijske provjere iz
   [README-a](../../README.md#provjera-dokumentacije);
8. otvoriti novi Codex task kako bi se osvježio katalog skillsa.

U repozitoriju trenutno nema `skills-lock.json`; zato se porijeklo i svaka
buduća promjena moraju dokazati pregledom sadržaja i diffa, a ne pretpostaviti
iz naziva verzije u frontmatteru.

## Aktuelni vendor signali

Supabase changelog provjeren je 2026-09-11. Prije implementacije ponovo provjeriti
posebno ove promjenjive tačke:

- stari Management API `logs.all` endpoint uklanja se 2026-09-23; novi `logs`
  endpoint koristi ClickHouse SQL;
- eksplicitno pinanje verzije PostgreSQL ekstenzije se ignorira u korist
  zadane verzije;
- nove tabele se ne moraju automatski izložiti Data/GraphQL API-ju; Data API
  grantovi i RLS su odvojene kontrole.

Izvori: [AI Tools](https://supabase.com/docs/guides/ai-tools),
[Plugin](https://supabase.com/docs/guides/ai-tools/plugins),
[MCP](https://supabase.com/docs/guides/ai-tools/mcp),
[Agent Skills](https://supabase.com/docs/guides/ai-tools/ai-skills) i
[Changelog](https://supabase.com/changelog.md).
