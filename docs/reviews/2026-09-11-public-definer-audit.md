# PUBLIC funkcije: ograničeni audit i sigurnosni kontraprimjeri

Datum: 2026-09-11. Status: **PASS_WITH_GAPS za čitanje; ROLE SETUP NO-GO**.

## Odobrenje i stvarno izvršen opseg

Q10.2g u [ADR-0002](../decisions/0002-search-design-interview.md) odobrava
ograničeni pregled funkcija u potvrđenom projektu „JSI Base“. Pripremljena
abfrage bira SECURITY-DEFINER rutine sa PUBLIC EXECUTE i PUBLIC schema USAGE.
Koristi pregledanu lokalnu psql vezu i nezavisnu projektnu hash-vezu.
Nije korišten Supabase developer plugin.

Prvi uspješni live poziv vratio je **0** rutina u tom uskom presjeku.
Zbog neslaganja s ranijim preflightom izvršen je zaseban katalogski brojčani
abgleich, bez definicija. Njegov rezultat je:

| Katalogski obim | Broj različitih rutina |
| --- | ---: |
| SECURITY DEFINER sa PUBLIC EXECUTE | 2 |
| Od njih sa PUBLIC schema USAGE | 0 |
| Od njih sa dostupnim owner/language katalogskim vezama | 0 |

Oba poziva završila su uspješno, po jednom vezom bez retryja. Nema čitanja
kandidata, izvršavanja pregledanih rutina ili DB mutacije. Zbog praznog
rezultata **nijedna produkcijska definicija nije pročitana**. Spremljeni su samo
redigirani izvještaji izvan Git-a; sirovi sadržaji nisu zapisani.

Raniji nalaz `public_definer_execute_with_schema_usage=1` nije potvrđen ovim
novim snimcima. Uzrok razlike nije utvrđen; historijski dokaz nije prepravljen.
Zadnja provjera PUBLIC TEMP i dalje je raniji nalaz `1`. Produkcijski MAINTAIN
i dalje nije provjeren. Ovi pozivi nisu zamjena za B1/B2/B3.

## Važna korekcija tumačenja

PUBLIC schema USAGE je provjera direktnog pronalaženja imena. Njegovo
odsustvo **nije dokaz da funkcija nema indirektan put izvršavanja**.
Termin „neizvršiva funkcija“ zato nije opravdan rezultatom 0 u ovoj abfrage.

Nezavisni review je predložio dva kontraprimjera, zatim stvarno reprodukovana
u odobrenom izoliranom PostgreSQL-17.11 containeru s umjetnim podacima:

1. Direktan poziv funkcije u skrivenoj schemi je odbijen, ali PUBLIC SELECT
   view koji već referencira tu SECURITY-DEFINER funkciju poziva je uspješno.
   Funkcija je upisala red u sintetičku trajnu tabelu.
2. Obična login rola isključuje svoju read-only zadanu postavku i preko
   `pg_catalog.lo_create(0)` kreira trajni large object.

To su dokazi PostgreSQL ponašanja u testu, **ne nalazi o stvarnim viewovima,
definicijama ili large-object pravima produkcije**. Privremeni V3 prijedlog
za izuzeće TEMP i funkcija bez schema USAGE zato je povučen; njegov SQL nije
ostavljen kao kandidat za primjenu. Stroži V1/V2 gateovi nisu ublaženi.
Ni oni sami ne dokazuju potpuno read-only ponašanje svih PUBLIC invoker
funkcija. `default_transaction_read_only` je zadana postavka, ne nepromjenjiva
autorizacijska granica.

## Konkretan sljedeći pregled i odluka o pravima

Dodatni read-only opseg je **odobren u Q10.2h i naknadno izvršen**:

Priprema, verifikacija i završni nalazi vode se u
[Q10.2h izvještaju](2026-09-11-public-paths-audit.md).

- iste dvije rutine sa PUBLIC EXECUTE, uključujući njihov identitet, ACL,
  vlasnika i definicije iako nemaju PUBLIC schema USAGE;
- katalogske zavisnosti i relevantni grantovi viewova/rutina koji mogu
  posredno dosegnuti te dvije rutine; bez pozivanja viewova ili funkcija;
- efektivni PUBLIC grantovi za uski skup invoker large-object funkcija
  `lo_create`, `lo_creat`, `lo_from_bytea`, `lo_put`, `lo_import`, `lo_unlink`,
  `lowrite`, `lo_truncate`, `lo_truncate64`; bez njihova izvršavanja,
  čitanja large-object sadržaja ili sadržaja datoteka.

Odobrenje od 2026-09-11 obuhvata sljedeću obradu i ne traži ponovnu potvrdu
istog scopea. Nova obrada treba pregledan, ograničen lokalni handler. Definicije,
identiteti i literali ostaju izvan modela, chata i Git-a. Nerazriješene pozivne
putanje ostaju gap, nikad dokaz sigurnosti. Ovaj opseg nije opći schema audit.

Tek rezultat može odrediti konkretan diff PUBLIC/grant prava uz očuvanje
potrebnih postojećih korisnika. Iz postojećih ACL-ova se ne izmišlja poslovna
potreba. Ne predlaže se globalni REVOKE bez te procjene. Promjene PUBLIC TEMP,
funkcijskih grantova, sigurnosne granice i produkcijska primjena trebaju
zasebnu konkretno vezanu odluku. Rola još nije kreirana.

## Lokalna verifikacija i izvori

- Devet lokalnih privacy/process testova: canary redakcija, nepouzdan JSON,
  nepotpuni sadržaj, limiti, timeout i gašenje procesa, uključujući grešku
  inicijalizacije selectora.
- Izolirani PostgreSQL-17.11: prazni i neprazni audit, SQL-standard i window
  funkcije, oba ACL/scope isključenja, brojčani abgleich, bez izvršavanja
  auditiranog writera; dva gore navedena kontraprimjera su namjerni dokazi
  ograničenja. V2 ciklus ima 22 uspješne provjere, uključujući grant/rollback
  regresije; ukupni status ostaje PASS_WITH_GAPS.
- Vlastiti container je uklonjen. Nema host mountova, mreže ili stvarnih
  podataka. Test koristi lokalni trust i ne dokazuje password autentikaciju.
- Dva nezavisna reviewa otkrila su i ispratila korekcije procesa, tipa OID,
  window scopea i razlikovanja SQL-standard CREATE wrappera od bodyja.
- Zajedničke lokalne provjere i aktivni Markdownlint prolaze do završne
  globalne whitespace provjere. Ona vraća exit 2 zbog ranijeg, nepovezanog
  trailing whitespacea u skill referenci `_contributing.md:30`. Scope
  `docs scripts tests` prolazi `git diff --check`; tuđa izmjena je sačuvana.

Prüfer: [audit launcher](../../scripts/discovery/check-public-definers.py),
[privacy handler](../../scripts/discovery/definer_audit.py),
[synthetic lifecycle](../../tests/discovery/role_lifecycle_integration.py).
`prosrc` i `prosqlbody` razlikuju se prema službenom
[PostgreSQL-17 katalogu pg_proc](https://www.postgresql.org/docs/17/catalog-pg-proc.html).

SQL-standard CREATE wrapperi mogu dati leksički CREATE indikator. Nijedan
leksički nalaz nije semantički dokaz, a odsustvo write riječi nije dokaz
read-only ponašanja.
