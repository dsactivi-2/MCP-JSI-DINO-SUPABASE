# Runbook: Automatizirani razvoj, test i optimizacija baze

## Svrha

<!-- markdownlint-disable-next-line MD013 -->
Ovaj runbook provodi [ADR-0004](../decisions/0004-automated-database-development.md)
nakon odobrenog discoveryja i ugovora. On opisuje redoslijed i stop kriterije;
tačne izvršne komande dodaju se tek kada postoji odabrani stack i reproducibilan
scaffold.

## Preduslovi

- read-only discovery je završen ili je konkretna nepoznanica formalno
  prihvaćena;
- odobreni su kanonski model, JSON Schema i RPC potpis;
- odabrani su runtime, package manager i lokalni Supabase način rada;
- postoji sintetički dataset reprezentativne strukture i distribucije;
- produkcijski credentiali nisu dio lokalnog ili CI okruženja;
- dokumentovane lokalne blokade Supabase CLI-ja (sandbox/telemetrija) i
  Promptfooa (native ABI) su odvojeno dijagnosticirane i ponovo provjerene prije
  nego postanu obavezni gateovi.

## Obavezni artefakti

- male, verzionirane i aditivne SQL migracije;
- sintetički seedovi bez zavisnosti od produkcijskog dumpa;
- pgTAP testovi strukture, grantova, RLS-a, RPC-a i rollback kompatibilnosti;
- MCP contract, injection, jezični i pagination testovi;
- kontrolisani performance slučajevi i prije/poslije planovi;
- mašinski čitljiv rezultat svakog gatea bez tajni.

## Tok promjene

1. Agent ili čovjek priprema mali SQL i testni diff.
2. Lokalna baza se gradi od nule iz verzioniranih migracija i seedova.
3. SQL lint, pgTAP i contract testovi moraju proći.
4. Relevantni upit prolazi kontrolisani `EXPLAIN`; `EXPLAIN ANALYZE` se koristi
   samo za tačno pregledane slučajeve, uključujući sve pozvane funkcije,
   unutar odobrenog opterećenja. Sam `SELECT` ne dokazuje odsustvo nuspojava.
5. Advisor i index prijedlozi se pregledaju, ali se ne primjenjuju automatski.
6. CI ponavlja isti tok u čistom okruženju i proizvodi sažetak `PASS`, `WARN`,
   `FAIL` ili `PASS_WITH_GAPS`.
7. Za produkciju se izrađuju dry-run, rollback plan i tačan plan promjene.
8. Nakon zasebne freigabe izvršava se apply, zatim health, RLS, contract,
   integritet i performance provjera.

## Pravila za AI-generirani SQL

- AI dobija odobreni ugovor i redigirani schema kontekst, ne nagađa fizičke
  objekte.
- Svaki AI izlaz je prijedlog u diffu sa testovima.
- Nema slobodne runtime SQL putanje niti generičkog table CRUD MCP-a.
- Dinamički SQL zahtijeva zasebno obrazloženje; gdje nije nužan, odbija se.
- Neuspjeli test ili neobjašnjiv plan zaustavlja promociju promjene.

## Monitoring prije rollouta i tokom rada

Prije rollouta AUTO-07 mora dokazati dashboarde, minimalne alarme i
incident/on-call/rollback postupak; kasnija dorada nije zamjena tog gatea.

1. Ugrađeni Supabase izvještaji, Advisors i `pg_stat_statements` predstavljaju
   početni izvor signala.
2. Provjera se raspoređuje kao read-only periodični posao koji ostaje tih bez
   značajne promjene i alarmira samo na prag ili regresiju.
3. Preporuka se pretvara u ticket sa dokazom; nikad u automatsku migraciju.
4. pganalyze POC je dozvoljen nakon četiri do osam sedmica reprezentativnog
   workload-a i zahtijeva mjerljivo poređenje s nativnim putem.

## Stop kriteriji

Za promjene MCP SDK-a, auth/DB adaptera ili middlewarea primijeniti i
[SDK-01–08](../planning/sdk-integration-plan.md#provjerljivi-gateovi-i-radni-paketi)
u postojećim AUTO/AUTH/OPS/CLIENT paketima. Dependency upgrade zahtijeva
fiksiran skup verzija, contract/auth/transport regresiju i provjeren povratak.
Protokolski testovi prate odabranu verziju; starije sesije nisu univerzalni
zahtjev novog transporta. Zelen Fake-MCP ili Inspector ne zamjenjuje stvarni
sintetički DB privilege/RLS/RPC test.

Neprovjeren MCP audience/downstream credential put, korisnički kontekst
podijeljen između zahtjeva, alpha komponenta bez odluke ili middleware koji
blokira streaming zaustavljaju promociju jednako kao neuspjeli DB gate.

- migracija mijenja importovanu tabelu u aditivnoj A fazi;
- lokalni ili CI tok zavisi od produkcijskog credentiala ili ručnog skrivenog
  koraka;
- RLS, privilege, contract, rollback ili performance provjera ne prolazi;
- Advisor ili AI prijedlog nema reproduktivan dokaz koristi;
- plan prekoračuje odobreni timeout, resource budget ili zaključava kritičan
  produkcijski put;
- alat pokušava automatski primijeniti produkcijsku promjenu.

## Izlazni kriterij

Promjena je spremna za produkcijsku freigabe tek kada su svi primjenjivi gateovi
zeleni, gapovi dokumentovani, rollback provjeren i tačan apply plan pregledan.

## Jedan lokalni i CI ugovor rezultata

AUTO-04/05 uspostavljaju isti ulazni tok u lokalnom radu i CI-u. Manifest
bilježi verzije alata, stvarne DB/extension verzije i potrebne sposobnosti,
ciljni alias, hash migracija/ugovora, svaki korak i izlazni kod bez tajni.
CLI/image pin nije dokaz stvarne verzije server extensiona.

Obavezna politika: svaki neuspjeh vraća nonzero; nedostajuća obavezna provjera
ili neodobren gap takođe blokira promociju. `WARN`/`PASS_WITH_GAPS` ne postaje
release PASS samo zato što je proces završio kodom 0. SQL lint mora eksplicitno
postaviti prag greške, bez oslanjanja na default `--fail-on none`. Tačan podržan
flag i verzija potvrđuju se kroz CLI help pri scaffold-u. Namjerno neispravan
sintetički SQL/RLS/ugovor mora zaustaviti cijeli tok i CI. Pipeline/tee ne smije
sakriti exitcode. Nema automatskog retryja neizvjesnog writea.

Katalogassertions provjeravaju stvarne grants, PUBLIC/default prava, funkcijske
postavke i view security. Prazan schema diff ili zelen lint nisu sami dokaz
RLS-a.
Fachliche test-orakle vlasnik odobrava nezavisno od generatora/implementacije.
DB i Fake-MCP testovi smiju paralelno koristiti samo izolirane mutable resurse.

## Različiti obavezni dokazi

- **Frischaufbau:** čista lokalna sintetička baza iz cijele migracijske
  historije.
- **Upgrade:** prethodni odobreni schema ugovor i sintetički stari podaci, zatim
  samo novi rez; ID/mengen/lineage/constraint/RLS/RPC poređenje nakon promjene.
- **Dry-run:** pregled planiranih migracija i ciljne veze. `db push --dry-run`
  ne izvršava migracije i ne dokazuje lockove, integritet, RLS ili restore.
- **Rückschaltung:** prethodna aplikacija/RPC ostaje funkcionalna uz aditivni
  schema rez; test kompatibilnosti i vratiti saobraćaj, ne nekontrolisani DROP.
- **Restore:** stvarna obnova prema zasebno odobrenom putu, integritet i
  RTO/RPO.
  DB backup ne obuhvata Storage datoteke; ako ih discovery dokaže, zasebno
  obuhvatiti njihov restore. Odbijeni lokalni backup-preflight ostaje isključen.

Transakcionalne i netransakcionalne migracije imaju različite stop/restart
postupke. `CREATE INDEX CONCURRENTLY` ne stavlja se u univerzalni transakcijski
wrapper; za svaki odobren netransakcionalni korak definirati prekid, djelimično
stanje, provjeru i posebno odobren nastavak. Produkcijski apply nije dio CI-a.

Ove specifikacije konkretiziraju A09 i postojeći ADR-0004. Tehnička evidencija:
[Primärprüfung](../research/2026-09-11-plan-best-practice-verification.md).
Komande za DB gate još nisu etablirane; trenutni lokalni dokument-/Fake-gate
u README-u nije dokaz DB, aplikacijske, load ili restore spremnosti.
