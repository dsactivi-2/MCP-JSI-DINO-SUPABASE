<!-- markdownlint-disable MD013 -->
# Istraživački brief: gotovi MCP i TypeScript slojevi za CRM pretragu

Datum: 2026-09-12

Status: brief za istraživačke agente; nije nalaz, nije stack odluka i ne
zamjenjuje discovery ni ADR

## Svrha

Ovaj dokument daje agentu dovoljno konteksta da istraži postoje li gotovi
alati koji bolje pokrivaju naš use case od ručno građenog Runtime-Such-MCP-a.
Traže se TypeScript slojevi koji iz sheme izvode tipove i veze, te alati koji
iz PostgreSQL/Supabase baze automatski grade ili konfiguriraju MCP.

Dokument nije dump sheme. Ne sadrži vrijednosti, SQL, credentiale niti
pun inventar kolona. Fizički nazivi su samo orijentacija iz statičkog
izvoza i ostaju `DURCH DISCOVERY ZU PRÜFEN`.

## Istraživačko pitanje

Postoji li 2026. spreman, primarno dokumentovan proizvod ili biblioteka koji:

1. iz postojeće PostgreSQL/Supabase sheme izvodi TypeScript tipove, klijente
   ili MCP alate bez ručnog mapiranja svake tabele;
2. ili automatski gradi MCP server nad bazom;
3. i pritom može poštovati našu granicu: LLM ne piše SQL, baza ostaje
   autoritativna, rezultat je mala stranica kandidata bez kontakata.

Ako takav proizvod postoji, treba reći šta tačno radi, šta i dalje moramo
sami graditi, i da li krši prihvaćene ADR-ove. Ako ne postoji, treba reći
koji dijelovi su ipak korisni kao generatori tipova ili razvojni pomoćnici.

## Šta ovaj brief nije

- Nije nalog za povezivanje na produkcijsku bazu.
- Nije nalog za izmjenu ADR-0001, ADR-0003 ili Release-1 ugovora.
- Nije ponovna evaluacija već istraženih Readyset/Zero/Electric partnera.
- Nije dozvola da se cijela baza, CV ili kontakti šalju LLM-u.

## Cilj proizvoda

Interni recruiteri trebaju na B/H/S, njemačkom i engleskom prirodnim jezikom
pronaći relevantne kandidate u CRM-u. Upit opisuje poslovne kriterije:
zanimanje, iskustvo, lokaciju, jezik, vještine, dob i dostupnost. Sistem
vraća malu, objašnjivu stranicu stvarnih zapisa za ljudsku procjenu.

Prvi korisnici su mala interna grupa. Ciljni klijenti su ChatGPT, Claude,
Codex, Grok i drugi MCP klijenti. Release 1 ne donosi odluku o zapošljavanju
i ne izlaže kontakte, ni u pojedinačnom profilu.

Obim je projektna procjena: približno 200.000 kandidata i, po korisničkoj
izjavi, 179 tabela. Oba broja su `DURCH DISCOVERY ZU PRÜFEN`.

## Arhitektonske granice koje alat mora poštovati

| Granica | Pravilo |
| --- | --- |
| ADR-0001 | LLM smije proizvesti samo mali, strogo validiran JSON filter. Runtime LLM ne generiše niti izvršava proizvoljni SQL. |
| PostgreSQL | Baza autoritativno filtrira, rangira, autorizira i paginira. Najviše 50 kandidata po stranici. |
| Release 1 | Nijedan izlaz nema telefon, e-mail ili druge kontakte. CV, bilješke, ugovori i identifikacioni brojevi ostaju skriveni. |
| ADR-0003 | Runtime-Such-MCP je read-only. Profilverwaltungs-MCP je kasnija, odvojena trust granica za Berufssuchprofile. |
| Auth | Prijava klijenta nije dovoljna. Svaki poziv nosi identitet i opseg. Tenant/RLS činjenice još nisu auditirane. |
| Semantička pretraga | Nije default Release 1. Tek nakon dokaza da strukturirani filteri, taksonomija, FTS i po potrebi `pg_trgm` nisu dovoljni. |
| Produktivni plugin | Službeni Supabase developer MCP/plugin ne smije se spajati na produkcijski CRM s pravim kandidatima. |

Alat koji nudi `query(sql)`, generic PostgREST CRUD nad svim tabelama ili
slanje sheme/redova u model pada na ovom testu, osim ako se dokaže uski,
allowlistani način rada koji te staze isključuje.

## Baza: karakter, ne svaka kolona

Podaci dolaze iz ugašenog operativnog CRM-a, dumpovani i učitani u
Supabase/PostgreSQL 17. Baza nije namjenski modelirana za ovaj search MCP.
Q10 pretpostavlja kratkoročno aditivni Release-1 sloj iznad postojećih
tabela, zatim male, provjerene rezove ka kanonskom modelu. Importovane
tabele se u A fazi ne mijenjaju niti brišu.

Statički Schema Visualizer izvoz, bez konekcije na bazu, daje samo ovo:

| Površina | Šta je beleg | Šta nije dokazano |
| --- | --- | --- |
| Shema `crm` | 100 potpunih table blokova, 1.104 kolone, svaka prikazana tabela ima PK | FK, unique, indeksi, viewovi, RPC, row count, RLS enable/force, tenant |
| RLS nazivi u istom izvozu | 188 objektnih naziva, 374 policy reda | 88 naziva nema table/column blok; izvoz je nepotpun |
| Shema `crm_api` | 0 tabela u izvozu | Ne dokazuje odsustvo viewova, funkcija ili RPC-ja |
| Shema `crm_auth` | 6 tabela / 28 kolona za user-employee map, role, permission, scope | Efektivna RLS zaštita, veza na `auth.users`, tenant izolacija |

Katalogbefund Gate B2 V3, samo imena i procjene, bez čitanja redova. To
sužava sliku, ali ne zamjenjuje ugovor ni data-quality audit:

| Objekat | Katalogska procjena | Značenje za auto-wire |
| --- | --- | --- |
| `idk_kandidati` | ~122.004 `reltuples` | Manje od projektnih 200.000; i dalje `DURCH DISCOVERY ZU PRÜFEN`, nije prebrojani broj redova. |
| `occupation` / `occupation_alias` / `job_occupation_map` | ~702 / ~1.241 / ~87.844 | Taksonomija zanimanja postoji kao objekti, ne samo kao policy nazivi. Mapiranje je veliko. |
| `search_candidates_by_occupation`, `search_candidates_filtered` | RPC postoje | Stari CRM search put. Runtime-MCP ih ne smije automatski preuzeti. |
| `crm_api.search_candidates` | Signatura uključuje e-mail i telefon | Auto-MCP koji ovu funkciju izloži 1:1 krši Q4 / Release 1. |
| `candidate_documents`, `candidate_document_text`, `candidate_document_embeddings` | `vector(1536)`, veličina < 1 MiB, `reltuples` -1 | Embedding skelet, prazan ili skoro prazan. Nije R1 standard pretrage. |
| Trigram indeksi na freetextu | postoje po imenu | Korisni za kasniji FTS/`pg_trgm` baseline, ne za generic SQL MCP. |

Auto-wire alat koji introspektira bazu vjerovatno vidi i ove RPC-je i
PII kolone. Default "objavi sve funkcije" je zato NO-GO test, ne prednost.

Grupisanje tabela je `ARBEITSANNAHME`:

| Sloj | Primjeri fizičkih naziva | Uloga za search |
| --- | --- | --- |
| Kandidatski korijen | `idk_kandidati` kao centralni kandidat; uz to legacy/alternativni skupovi `idk_dak_kandidati`, `idk_nd_kandidata` | Identitet, status, dob, lokacijska polja, partner, grubo iskustvo u struci. Autoritativnost među skupovima je `OFFEN`. |
| 1:n profilne strukture | `idk_kandidat_edukacija`, `idk_kandidat_radno_iskustvo`, `idk_kandidat_jezici`, `idk_kandidat_vjestine` | Obrazovanje, iskustvo, jezici, vještine. ID-kolone nisu dokazani FK. |
| Kontrolisani katalozi | `idk_kandidat_pozicija` (višejezični nazivi, bez kandidat-ID), `idk_kandidati_grupe`, `idk_kandidat_status*` | Mogući lookup; članstvo kandidata u grupi nije prikazano. |
| Policy-only u statičkom izvozu | `idk_struke`, `idk_profil_kriterij`, `idk_skole`, `idk_pp_city`, `idk_pp_regions` | Statički izvoz nije imao kolone. Gate B2 kasnije nalazi `occupation*` kao katalogske objekte, vidi tabelu iznad. |
| Lokacije | Nema potpunog table bloka u izvozu | Grad/regija/država trenutno izgledaju kao polja na kandidatu i freetext na iskustvu/edukaciji. |
| Auth/scope | `user_employee_map`, `roles`, `permissions`, `role_permissions`, `user_roles`, `user_scopes` | `ARBEITSANNAHME` za kasnije mapiranje MCP identiteta; nije dokaz tenant modela. |
| Operativa izvan searcha | dokumenti, ugovori, financije, partneri, ticketi, poruke, nostrifikacija, cron, skladište | Release 1 ih ne izlaže. Auto-MCP koji objavi sve tabele je štetan. |

Karakter podataka, koliko se vidi iz imena kolona a ne iz vrijednosti:

- Miješani operativni CRM, ne čist search index.
- Višejezični freetext: 37 kolona u 14 tabela ima sufikse `_de`, `_en`,
  `_rs`, `_it`, `_ba`. Iskustvo i pozicije imaju original plus prijevod.
- 151 kolona u 75 tabela ima status/source/type/group imena; da li su to
  kontrolisani ID-ovi ostaje `DURCH DISCOVERY ZU PRÜFEN`.
- Osjetljive površine postoje po imenu: ime, JMBG, pasoš, datum rođenja,
  adresa, e-mail, telefon, lozinka/token, CV, slika, bilješke, dokumenti.
- `idk_kandidat_radno_iskustvo` čuva intervale i freetext poziciju/poslodavca;
  Q8.5 (ukupno ili relevantno iskustvo) je u cijelosti `OFFEN`.
- `idk_kandidati.kandidat_iskustvo_u_struci` i
  `kandidat_iskustvo_u_struci_trajanje` su dodatni, nepotvrđeni signali.
- Lokacije kao normalizirane tabele nisu u potpunom statičkom izvozu;
  Gate B2 ih nije potvrdio kao search katalog.

Zato alat koji "odmah razumije bazu" vidi operativni legacy model s PII,
duplim kandidatskim skupovima i nepotpunim relacijama. To nije kanonski
search model iz briefa.

Kanonski pojmovi na koje se stvarna shema tek treba mapirati:
identitet, dob, Ausbildungsberuf, Erfahrungsberuf, Tätigkeitsart,
Berufssuchprofil, lokacija, jezik, vještina, dostupnost, svježina.

## Filteri u više nivoa

To je srž use casea. Gotov alat mora objasniti koji nivo pokriva, a koji
ostaje ručni ugovor.

| Nivo | Šta radi | Ko odlučuje |
| --- | --- | --- |
| 0. Prirodni jezik | Recruiter kaže npr. "električar, 5 godina, Njemačka, njemački B2". Jezici upita: B/H/S, DE, EN. | LLM u MCP klijentu. |
| 1. Namjera → JSON | Mali filter objekt. Nepoznata polja, SQL fragmenti, nazivi tabela/kolona i arbitrary expression su zabranjeni. | MCP validator + JSON Schema + allowliste. |
| 2. Taksonomija | "Elektriker" / "električar" / "electrician" smiju pogoditi isti kanonski ID samo nakon odobrenog sinonima. Slobodni LLM sinonimi ne šire filter. | Verzionirana taksonomija. |
| 3. Berufssuchprofil | Imenovana, verzionirana grupa Ausbildungsberufe + Erfahrungsberufe + Tätigkeitsarten. Članstvo je neekskluzivno many-to-many. Isti beruf ostaje direktno pretraživ. | Profilverwaltungs-MCP objavljuje; Runtime-Such-MCP samo čita aktivnu verziju. |
| 4. Kategorije filtera | Aktivna je samo izričito navedena kategorija. Nenavedena ne ograničava rezultat. "Elektriker mit fünf Jahren" ne uključuje Ausbildung ako Ausbildung nije navedena. | Potvrđeno u ADR-0002. |
| 5. Operatori | Različite kategorije: predloženo `AND`. Više zanimanja/lokacija/dostupnosti: predloženo `ANY`. Jezici/vještine: izričito ANY/ALL. Raspon dobi: obje granice. `NOT` samo ako je izričito zatražen. Detalji operatora su `VORLÄUFIGER VORSCHLAG` zbog rekonstrukcijske praznine. | Validator, zatim PostgreSQL. |
| 6. Pregled i potvrda | Q7: pri nula pogodaka predložiti labavljenje, izvršiti tek nakon saglasnosti. Opća potvrda svake nove pretrage je `VORLÄUFIGER VORSCHLAG`. | MCP tok, ne baza. |
| 7. RPC | Jedna parametrizirana PostgreSQL funkcija. Filter, rank, keyset pagination, RLS, timeout, cap 50. Match evidence po retku. | PostgreSQL. |
| 8. Profil | `get_candidate_profile(id)` vraća dozvoljena polja bez kontakata. | Isti ugovor, uža projekcija. |
| 9. Opcije | `get_filter_options(field, query)` autocomplete kanonskih pojmova i profila, bez kandidatskih redova. | Katalog/taksonomija, ne search tabela. |

Runtime MCP izlaže samo ta tri alata: `search_candidates`,
`get_candidate_profile`, `get_filter_options`.

Primjer koji alat mora preživjeti: "električar s pet godina iskustva, 25–40
godina, Bayern ili Baden-Württemberg, njemački najmanje B1, dostupni u 4
sedmice". Sistem ne smije izmisliti školu, telefon ili drugi kandidatski
skup. Ako nema tačnih pogodaka, ostaje nula dok recruiter ne potvrdi
labavljenje.

## Šta je već istraženo, ne ponavljati kao novi nalaz

| Dokument | Zaključak koji brief pretpostavlja |
| --- | --- |
| [Supabase alati](supabase-werkzeuge-fuer-crm-mcp.md) | Službeni developer MCP nije runtime search MCP. Za produkcijski CRM s PII je zabranjen. Skills i `search_docs` su razvojni vodič. |
| [MCP/Supabase SDK](mcp-supabase-sdk-integration.md) | Službeni MCP TypeScript SDK v2 i Supabase server/middleware rješavaju različite zadatke. Prednost ima mali MCP server plus uski adapter; to nije gotov CRM search. |
| [Readyset/Zero/Electric](supabase-partner-readyset-zero-electric.md) | Nijedan ne pojednostavljuje Release 1 search ugovor. |
| [SQL automatizacija](optimaler-sql-und-automatisierungsweg.md) | Native-first: CLI, migracije, lint, pgTAP, Advisors. AI piše diff, ne apply. |
| [SDK plan](../planning/sdk-integration-plan.md) | Evaluacijski pravac, ne instaliran stack. |

Nova pretraga treba ići izvan tog kruga: generatori MCP-a iz sheme,
Postgres/PostgREST/OpenAPI→MCP, schema-aware TypeScript, NL→structured
query (ne NL→SQL), search enginei samo ako mogu sjediti iza JSON ugovora.

## Tražene klase rješenja

Agent treba pokriti svaku klasu primarnim izvorom (repo README, spec,
službena docs), ne blogom.

1. **Schema-aware TypeScript** koji iz Postgres/Supabase izvoza ili live
   introspection gradi tipove i query buildere. Pitati: da li emitira samo
   tipove, ili i runtime pristup svim tabelama? Da li se da stegnuti na
   allowlistu RPC-ja?
2. **Auto-MCP nad bazom**: Postgres MCP, Supabase MCP, PostgREST MCP,
   OpenAPI→MCP, "database to MCP" generatori. Pitati: default surface je
   `query(sql)` / CRUD na svakoj tabeli, ili se može objaviti samo tri
   typed alata?
3. **NL → structured filter**, ne NL → SQL. Pitati: postoji li proizvod
   koji iz JSON Schema ili Zod ugovora radi tool calling, autocomplete i
   validaciju, a SQL ostavlja backendu?
4. **Search platforme** (FTS, Typesense, Meilisearch, Elasticsearch,
   pgvector) samo kao kasniji execution backend iza istog JSON ugovora.
   Ne kao zamjena za MCP granicu.
5. **Admin/CMS koji iz sheme crta API** (Directus, Hasura, PostgREST UI).
   Pitati: mogu li se sakriti PII tabele i izložiti samo RPC, ili je to
   generic data browser?

Za svakog kandidata odgovoriti:

- Šta službeno obećava, s URL-om primarnog izvora i datumom čitanja.
- Koji nivo filtera (0–9) pokriva, a koji ostaje naš kod.
- Da li default put krši ADR-0001 (SQL od LLM-a, bulk rows u model).
- Da li radi sa legacy shemom bez pouzdanih FK i s PII tabelama.
- Auth model: RLS passthrough, service_role, vlastiti OAuth, MCP resource
  audience. MCP token se ne smije slijepo proslijediti kao DB credential.
- Licence, hosting, vendor lock-in, zrelost (GA / alpha).
- Šta bismo i dalje morali napisati: taksonomija, Berufssuchprofil,
  match evidence, cap 50, redakcija kontakata, preview/confirm tok.
- Ocjena: `GO kao runtime`, `GO samo kao codegen/dev`, `LATER`,
  `NO-GO`.

## Obavezan izlaz istraživanja

Jedan Markdown nalaz u `docs/research/`, s citatima. Struktura:

1. Kratka ocjena u 5–10 rečenica.
2. Tabela kandidata s ocjenom i nivoima koje pokrivaju.
3. Za najboljeg kandidata po klasi: kako bi se uklopio, šta ostaje ručno,
   koji ADR bi se morao mijenjati.
4. Eksplicitna izjava ako nijedan alat ne smije biti runtime search MCP.
5. Popis izvora. Svaka tehnička tvrdnja ima primarni URL.
6. Šta nije provjereno.

Zabranjeno:

- spajanje na produkcijski Supabase projekt ili čitanje kandidatskih redova;
- izvršavanje SQL-a, dumpova, backup ZIP-ova ili OrbStack kontejnera;
- ispis credentiala, connection stringova, pravih imena, telefona, CV teksta;
- predstavljanje fizičkih tabela kao kanonskog ugovora;
- preporuka `service_role` kao prečice za RLS.

## Copy-paste prompt za drugog agenta

```text
Research whether ready-made 2026 tools can replace or shrink a custom
Supabase/PostgreSQL MCP for recruiter candidate search. Use primary sources
only (official docs, specs, first-party READMEs). Do not connect to any
database. Do not read or quote personal data.

Product: internal recruiters query ~200k CRM candidates in Bosnian/Croatian/
Serbian, German and English via ChatGPT/Claude/Codex/Grok MCP clients.
The LLM may translate natural language into a tiny validated JSON filter.
It must never generate or run SQL. PostgreSQL must filter, rank, authorize
and paginate. Max 50 candidates per page. Release 1 returns no contact
data, CVs, notes, contracts or IDs such as passport/JMBG. Zero exact hits
stay zero until the user confirms a relaxation. Unmentioned filter
categories stay inactive.

The database is a dumped operational CRM on Supabase Postgres 17, not a
search-optimized schema. Static export (no live DB): schema crm has 100
complete tables / 1104 columns; user also stated 179 tables; 88 extra
names appear only as RLS policies. crm_api export showed 0 tables.
crm_auth has 6 role/permission/scope tables. Likely candidate hub:
idk_kandidati plus 1:n education, work experience (multilingual freetext
plus date intervals), languages, skills. Location lookup tables were
missing from the complete export. Duplicate/legacy candidate tables exist.
Foreign keys, indexes, RLS effectiveness, row counts and tenant isolation
are unproven. Many tables are finance, tickets, documents, partners —
those must not become MCP tools.

Catalog-only Gate B2 V3 estimates, no row reads: idk_kandidati ~122004
reltuples; occupation ~702, occupation_alias ~1241, job_occupation_map
~87844. Existing RPCs search_candidates_by_occupation and
search_candidates_filtered must not be auto-exposed. crm_api.search_candidates
already lists email and phone in its signature: wrapping that 1:1 is a
Release-1 violation. candidate_document_embeddings is a near-empty
vector(1536) skeleton, not the R1 search path. Trigram indexes exist on
freetext. Default "publish every table and RPC" is a fail.

Needed filter layers:
0 NL intent
1 JSON schema filter (no SQL, no table/column names)
2 approved multilingual taxonomy
3 versioned occupation-search profiles (many-to-many, non-exclusive;
  runtime MCP read-only; separate admin MCP later)
4 category AND, within-category ANY for occupations/locations;
  explicit ANY/ALL for languages/skills; age range is mandatory
5 parameterized Postgres RPC + RLS + keyset pagination + match evidence
Runtime MCP tools only: search_candidates, get_candidate_profile,
get_filter_options.

Search these classes:
A) TypeScript that infers types/clients from Postgres/Supabase schema
B) tools that auto-build MCP from Postgres, PostgREST, OpenAPI or Supabase
C) NL → structured JSON/Zod tools that do not emit SQL
D) search engines only as optional backends behind the same JSON contract
E) schema-generated admin/API layers (Hasura, Directus, PostgREST)

Do not re-litigate: official Supabase developer MCP as production runtime
(forbidden on this PII project), Readyset/Zero/Electric for Release 1,
or sending the table dump to an LLM.

For each candidate: primary URL + date, which layers it covers, whether
its default path is arbitrary SQL or full-table CRUD, auth model, license,
maturity, what we would still build, verdict GO-runtime / GO-codegen-only /
LATER / NO-GO.

Write one cited Markdown report. If nothing is a safe runtime MCP, say so
plainly and list what is still useful as codegen.
```

## Izvori u ovom repozitoriju

- [CONTEXT.md](../../CONTEXT.md)
- [Stanje projekta](../project.md)
- [Implementacijski brief](../SUPABASE_CRM_MCP_IMPLEMENTATION_BRIEF.md)
- [ADR-0001](../decisions/0001-controlled-query-boundary.md)
- [ADR-0002](../decisions/0002-search-design-interview.md)
- [ADR-0003](../decisions/0003-separated-profile-administration-mcp.md)
- [Statička `crm` analiza](../discovery/crm-schema-static-analysis.md)
- [Statička `crm_auth` analiza](../discovery/crm-auth-schema-static-analysis.md)
