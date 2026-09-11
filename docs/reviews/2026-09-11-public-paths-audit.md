# Q10.2h: prošireni read-only pregled

Datum: 2026-09-11. Status: **IZVRŠENO / PASS_WITH_GAPS / ROLE SETUP NO-GO**.

Korisnik je izričito odobrio dodatni scope u
[ADR-0002 Q10.2h](../decisions/0002-search-design-interview.md).
Istovremeno je zatražio dokumentaciju verzije i usklađivanje dokumenata.
[Registar verzija](../discovery/role-version-register.md) bilježi povučeni
V3 pokušaj odvojeno od budućeg Gate-B1-V3 paketa. Nijedna nova rola nije
kreirana i nema novog odobrenja za mutacije.

## Pripremljena obrada

[Launcher](../../scripts/discovery/audit-public-paths.py) koristi postojeću
nezavisnu projektnu vezu i ograničeni psql collector. Jedna read-only,
repeatable-read transakcija pokriva:

- dvije PUBLIC-EXECUTE-SECURITY-DEFINER rutine bez schema-USAGE filtera;
- ulazne katalogske zavisnosti routine/view, najviše četiri nivoa i 256
  različitih izlaznih objekata; bez njihovih definicija ili izvršavanja;
- grantove devet imenovanih helper porodica iz prethodnog odobrenog izvještaja.

Definicije početnih rutina ostaju u ograničenoj lokalnoj memoriji. Izlaz
sadrži kontrolisane oznake, hashove, brojeve i dozvoljena helper imena.
Nema sirovih definicija, literala, projektnih URL-ova, view upita, kandidata
ili large-object sadržaja u izvještaju.

Broj dvije rutine nije dokaz kontinuiteta njihovog identiteta kroz različite
snimke. Izlaz prikazuje zavisne objekte i minimalnu dubinu, ne kompletne grane
poziva niti pripadnost pojedinom početnom objektu. Dinamički SQL, mnogi
string-body pozivi i druge vrste zavisnosti ostaju izvan potpunog dokaza.
Nulti rezultat stoga nikad ne daje opću read-only garanciju.

## Stvarni produkcijski nalazi

Završni ograničeni read-only poziv uspješno je obradio dvije definicije samo
u lokalnoj memoriji. Sirovi izvori nisu sačuvani. Redigirani nalaz:

| Nalaz | F001 | F002 |
| --- | --- | --- |
| Jezik / vrsta | PL/pgSQL funkcija | PL/pgSQL funkcija |
| PUBLIC EXECUTE | Da | Da |
| Direktni ostali granteeji | 1 | 1 |
| Owner BYPASSRLS i CREATEROLE | Da | Da |
| Owner superuser | Ne | Ne |
| Lokalni search_path postavljen | Da | Da |
| Leksički EXECUTE indikator | Da | Ne |
| Leksički direktni write/DDL indikatori | Nisu nađeni | Nisu nađeni |
| Dokaz read-only ponašanja | Ne postoji | Ne postoji |

Nisu pronađeni ulazni routine/view čvorovi u pregledanom katalogskom presjeku,
frontier na četvrtom nivou ni druge direktne root zavisnosti. To ne isključuje
pozive skrivene u string-body definicijama, dinamičkom SQL-u ili aplikacijama.
Posebno je F001 dinamički slučaj; izostanak leksičkih write riječi nije dokaz
sigurnog ponašanja. Nije procijenjena sigurnost konkretne search_path vrijednosti.

Pronađeno je svih devet helper porodica, ukupno deset overloadova:

- PUBLIC može izvršavati lo_create, lo_creat, lo_from_bytea, lo_put,
  lowrite, lo_unlink, lo_truncate i lo_truncate64: osam funkcija.
- Oba lo_import overloada nemaju PUBLIC EXECUTE.
- Sve imaju PUBLIC schema USAGE i nisu SECURITY DEFINER.

Ovo je dokaz grantova, ne produkcijskog izvršavanja. Raniji sintetički test je
pokazao da odgovarajuća PUBLIC invoker funkcija može kreirati trajni large
object. U produkciji nije izvršena nijedna pregledana funkcija ili view,
nisu čitani kandidati niti large-object sadržaji i nije bilo DB mutacije.

## Verifikacija i otklonjena smetnja

Nakon korisničke potvrde da je OrbStack otvoren, Docker je ponovo dostupan.
Read-only popis vlastitih markiranih test-containera bio je prazan; prethodni
cleanup gap je time zatvoren. Novi izolirani PostgreSQL-17.11 ciklus završio
je s 23 uspješne provjere i uklonjenim vlastitim containerom.

Prošireni SQL test stvarno je obradio dvije funkcije, indirektni lanac viewova
na drugom nivou, helper prava i nepromijenjenu test-tabelu. Povećanje početnog
broja rutina na tri završilo je odbijanjem rezultata. Lokalni trust ostaje
ograničenje: password autentikacija nove produkcijske role nije dokazana.

Tri ranija pokretanja live launchera nisu proizvela validan izvještaj.
Ručno usmjereni dijagnostički pozivi uslijedili su nakon dopune fiksnih
sigurnih error klasa; launcher ne sadrži automatski retry. Ukupno su bila
četiri pokretanja, od kojih je završno uspješno; broj stvarno uspostavljenih
veza u prekinutim pokušajima nije zasebno potvrđen.

Reprodukovana je lokalna greška: pri većem queryju neblokirajući pipe može
vratiti BlockingIOError iako je selector ranije prijavio mogućnost pisanja.
Collector sada nastavlja unutar iste fiksne vremenske granice. Pri ranom
zatvaranju stdin-a također obradi ograničeni stderr. Stderr je ograničen na
8192 bajta u memoriji i daje samo dozvoljene fiksne klase, nikad sirovu poruku.
Nisu povećani postojeći query timeouti ni grantovi.

Osam process testova, pet osnovnih privacy testova i dva proširena privacy
testa prolaze. Oba nezavisna reviewa su završena; naknadno je posebno pregledan
ispravljeni pipe/cleanup put. Opseg promjene prolazi whitespace provjeru;
raniji nepovezani skill whitespace ostaje zaseban globalni check gap.

## Daljnji korak

Q10.2h je iskorišten za odobreno čitanje i ne traži novu potvrdu istog opsega.
Njegov rezultat nije odobrenje za promjenu PUBLIC prava ili kreiranje role
uz slabije gateove. Konkretni poznati ciljevi i zaštita postojećih korisnika
opisani su u [nacrtu prava](../discovery/public-rights-change-proposal.md).
Rola još nije kreirana. Gate B1/B2/B3 i opći schema audit nisu ovim zamijenjeni.
