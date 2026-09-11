# Evaluacijski gate za semantičku pretragu

Datum: 2026-09-11

Status: planirani evaluacijski gate; bez izbora tehnologije, pristupa bazi,
kreiranja Vector Bucketa ili promjene produkcije

## Svrha

Ovaj gate određuje kako se nakon read-only discoveryja provjerava treba li CRM
semantičku pretragu i, ako treba, koji je tehnički put opravdan. Kandidati za
poređenje su postojeća strukturirana pretraga uz taksonomiju i FTS, `pgvector`
te Supabase Vector Buckets preko S3 Vector Wrappera.

Gate ne pretpostavlja da je vektorska komponenta potrebna. Približno 200.000
kandidata i 179 tabela ostaju projektne tvrdnje koje prvo treba potvrditi kroz
discovery. Supabase Vector Buckets su na datum ovog dokumenta Public Alpha i ne
smiju postati produkcijska zavisnost bez ponovne provjere aktuelnog statusa.

## Opseg mogućih slučajeva upotrebe

<!-- markdownlint-disable MD013 -->

| ID | Slučaj upotrebe | Status u ovom projektu |
| --- | --- | --- |
| SEM-UC-01 | Eksplicitna semantička pretraga kandidata uz obavezne CRM filtere. | Kandidat za evaluaciju nakon discoveryja. |
| SEM-UC-02 | Eksplicitno traženje kandidata sličnih odabranom profilu. | Otvorena product odluka; ne smije biti automatski fallback za nula rezultata. |
| DQ-UC-01 | Prepoznavanje vjerovatnih duplikata u kontrolisanom back-office postupku. | Dio šireg data-quality cilja; zaseban batch ugovor i ljudski review. |
| CALL-UC-01 | Spajanje embeddinga razgovora s kandidatskim zapisima. | Izvan opsega ovog CRM releasea; zahtijeva zaseban purpose, privacy i trust-boundary ADR. |

<!-- markdownlint-enable MD013 -->

Release 1 ne vraća kontaktne podatke ni kroz jedan od ovih puteva. Rezultat
semantičke pretrage ne smije samostalno promijeniti status kandidata, objaviti
profilno mapiranje, spojiti duplikate ili donijeti odluku o zapošljavanju.

## Nepromjenjive granice

- LLM proizvodi samo strogo validiran strukturirani zahtjev i ne generira SQL.
- PostgreSQL ostaje autoritativan za identitet, tenant/RLS opseg, tvrde filtere,
  rangiranje i paginaciju.
- Aktivni tvrdi filteri moraju važiti za svaki vraćeni rezultat prije primjene
  konačnog limita; naknadno filtriranje već skraćenog globalnog `top_k` skupa
  nije prihvatljivo.
- Search vraća najviše 50 kandidata po stranici i ne vraća kontakte u Releaseu 1.
- Generiranje embeddinga upita je poseban korak; SQL join ne uklanja potrebu za
  modelom embeddinga, njegovom verzijom, troškom i kontrolom podataka.
- Embedding i pripadajući identifikator su izvedeni lični podaci, ne anonimni
  tehnički brojevi. Primjenjuju se purpose limitation, retention, pristup,
  brisanje, ispravka, audit i data-lineage pravila.
- Ispravke i brisanja kandidata moraju se propagirati u embeddinge unutar
  odobrenog SLA-a. Zastarjeli ili orphan embedding ne smije vratiti kandidata.
- Semantička pretraga ne smije tiho zamijeniti tačnu pretragu. Q7 i dalje traži
  izričitu saglasnost prije izvršenja olabavljene pretrage.

## Redoslijed provjere

1. **Discovery dokazi:** potvrditi relevantne izvore teksta, stabilne ID-ove,
   tenant/RLS model, statuse, jezike, zanimanja, kvalitet, svježinu, brisanje,
   stvarni volumen i postojeće indekse/funkcije.
2. **Product opseg:** odlučiti koji su slučajevi upotrebe dozvoljeni, da li je
   semantički način eksplicitan i kako se razlikuje od tačne pretrage i Q7
   filter-relaxation toka.
3. **Referentni skup:** pripremiti odobrene, anonimizirane ili sintetičke upite
   s ljudski označenim relevantnim kandidatima i negativnim primjerima.
4. **Baseline:** prvo izmjeriti kontrolisane ID filtere, taksonomiju, FTS i po
   potrebi `pg_trgm`. Bez mjerljive kvalitetne praznine vektorski prototip staje.
5. **Izolirani prototipi:** nad istim referentnim skupom porediti `pgvector` i
   Vector Bucket/S3 Wrapper. Nema produkcijskih podataka, bucket mutacije ili
   wrapper instalacije bez posebnog odobrenja.
6. **Odluka:** prije izbora tehnologije uporediti kvalitet, ispravnost filtera,
   performanse, sigurnost, lifecycle, operativni rizik i trošak. Odluku zapisati
   u ADR; odbijena vektorska opcija također dobija obrazloženje i kriterij ponovne
   procjene.

Numerički pragovi se usvajaju prije benchmarka. Ne prilagođavaju se naknadno da
bi favorizirali određeni backend.

## Kandidati za poređenje

<!-- markdownlint-disable MD013 -->

| Kandidat | Šta dokazuje | Posebna pitanja |
| --- | --- | --- |
| Strukturirani filteri + taksonomija + FTS/`pg_trgm` | Da li jednostavniji PostgreSQL put već daje potreban kvalitet. | Višejezičnost, dijakritika, sinonimi, održavanje GIN/trigram indeksa. |
| `pgvector` u PostgreSQL-u | Da li transakcijski blizak vektorski rank daje kvalitet uz jednostavniji auth i lifecycle. | Veličina indeksa, write trošak, planovi poslije selektivnih filtera, konkurentnost. |
| Vector Bucket + S3 Vector Wrapper | Da li odvojeno skalabilno spremište i SQL join opravdavaju dodatnu zavisnost. | Alpha rizik, jedini podržani operator, FDW pushdown, hladna/topla latencija, RLS/grant granica, cijena i brisanje. |

<!-- markdownlint-enable MD013 -->

## Obavezni dokazi i stop-kriteriji

<!-- markdownlint-disable MD013 -->

| Područje | Dokaz prije prolaza | Stop-kriterij |
| --- | --- | --- |
| Ispravnost filtera | Negativni testovi za tenant, status, zanimanje, jezik, dostupnost i isključenja; svaki rezultat zadovoljava aktivne filtere. | Filter se primjenjuje tek nakon ograničenog globalnog `top_k` ili se kandidat izvan opsega može vratiti. |
| Kvalitet | Unaprijed definisani Precision@k, Recall@k ili nDCG na višejezičnom referentnom skupu, uz pregled false-positive/false-negative rezultata. | Nema značajne koristi nad baselineom ili kvalitet zavisi od neodobrenih sinonima/atributa. |
| Plan i performanse | `EXPLAIN (ANALYZE, BUFFERS)` gdje je primjenjivo, p50/p95/p99, broj obrađenih/vraćenih redova, cold/warm mjerenje i concurrency test. | Prekoračen resursni/SLO prag, nestabilan plan ili nedokazan FDW filter pushdown. |
| Sigurnost | Minimalne privilegije, RLS/tenant negativni testovi, column allowlista i najviše 50 rezultata. | Wrapper, funkcija ili servis zaobilazi RLS ili zahtijeva široki secret/owner pristup. |
| Privatnost i fairness | Dokumentovan embedding sadržaj, model/provider, pravna svrha, bias pregled i zabrana kontakata. | Nejasna svrha, nedopušten prijenos podataka ili nedokaziva diskriminatorna obilježja u ranku. |
| Lifecycle | Test insert/update/delete/re-embed, model i source verzija, freshness SLO, orphan kontrola i rollback. | Izbrisani/ispravljeni kandidat ostaje pretraživ ili dvije verzije daju neobjašnjiv rezultat. |
| Operacije i trošak | Izračun storagea, embeddinga, DB/FDW poziva, egressa, observabilityja i incident postupka. | Trošak ili Alpha/vendor rizik nema odobren limit i vlasnika. |

<!-- markdownlint-enable MD013 -->

Posebno za SQL join mora test dokazati semantiku: selektivni CRM filteri ne
smiju samo ukloniti rezultate iz već ograničenog globalnog nearest-neighbor
skupa. Query plan, vraćeni skup i granični primjer s relevantnim kandidatom odmah
iza početnog `top_k` moraju biti dio testa.

## Mjesto u faznom planu

<!-- markdownlint-disable MD013 -->

| Faza | Dopušteni rad vezan za semantičku pretragu |
| --- | --- |
| 0 – Governance | Održavati ovaj gate i javne izvore. Ne kreirati bucket, wrapper, embedding pipeline ili produkcijsku konfiguraciju. |
| 1 – Discovery | Prikupiti samo odobrene činjenice potrebne za opseg i referentni skup. |
| 2 – Ugovor i model | Donijeti product odluke za SEM-UC-01/02 i DQ-UC-01; definirati strogi semantic input, evidence i error ugovor ako je opseg odobren. |
| 3 – Sigurni DB prototip | Izvesti baseline i izolirano poređenje backenda; pregledati planove, grantove, lifecycle i rollback. |
| 4 – MCP servis | Implementirati samo odabrani, verzionirani RPC/adapter iza postojeće validacijske granice. |
| 5 – Višeklijentska validacija | Dokazati identičan ugovor, autorizaciju i prikaz match evidencea u svim klijentima. |
| 6 – Benchmark i SLO | Potvrditi numeričke ciljeve na reprezentativnom volumenu i troškovnom budžetu. |
| 7 – Rollout | Poseban feature flag, shadow/pilot, monitoring svježine i dokumentovan rollback. |

<!-- markdownlint-enable MD013 -->

Semantička funkcija nije uslov za minimalni Release 1. Ako baseline zadovolji
dogovorene ciljeve, evaluacija završava odlukom da se vektorska komponenta ne
uvodi.

## Izlazni artefakti

- odobren popis slučajeva upotrebe i zabranjenih automatizacija;
- verzioniran, anonimiziran ili sintetički referentni skup i scoring postupak;
- reprodukcijski benchmark izvještaj za baseline i odobrene prototipe;
- sigurnosni, privacy, fairness, lifecycle i cost pregled;
- ADR s izborom `bez vektora`, `pgvector`, `Vector Bucket` ili drugom posebno
  evaluiranom opcijom;
- ažurirani MCP/RPC ugovor, test matrica, SLO i rollback samo ako je semantički
  opseg odobren.

## Službeni izvori

- [Supabase Vector Buckets](https://supabase.com/docs/guides/storage/vector/introduction)
- [Supabase Querying Vectors](https://supabase.com/docs/guides/storage/vector/querying-vectors)
- [Supabase S3 Vector Wrapper](https://supabase.com/docs/guides/database/extensions/wrappers/s3_vectors)
- [Supabase Full Text Search](https://supabase.com/docs/guides/database/full-text-search)
- [Supabase Changelog](https://supabase.com/changelog.md)

Izvori i status Alpha moraju se ponovo provjeriti neposredno prije prototipa ili
dugoročne odluke.
