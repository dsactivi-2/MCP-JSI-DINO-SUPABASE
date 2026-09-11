# Konkretan plan promjene PUBLIC prava

Datum: 2026-09-11. Status: **LOKALNO TESTIRANO / PRODUKCIJA NO-GO**.

Q10.2i je odobrio pripremu i ograničeno čitanje. Naknadni Q10.2j daje
korisničku dozvolu za opisanu ciljanu promjenu prava; tehničke ovlasti i dalje
nedostaju. Ne traži se ponovo ista opća dozvola.
[Provjera plana](../reviews/2026-09-11-rights-plan-verification.md) veže nalaz,
generator i sintetičke testove. Rola još nije kreirana; V1/V2 gate ostaje
strog, a povučeni V3 se ne vraća.

## Tačan opseg predloženih promjena

Read-only inventar je potvrdio 33 postojeće role, dvije ranije identificirane
SECURITY-DEFINER funkcije, osam poznatih LO funkcija i database TEMP za PUBLIC.
Hash definicije oba ranija nalaza odgovara Q10.2h dokazu. Nema dodatnih
PUBLIC-EXECUTE definera izvan ovog skupa; PUBLIC MAINTAIN nije pronađen.

| Cilj | Novi direktni grantovi | PUBLIC opozivi | Ovlast sadašnjeg pristupa |
| --- | ---: | ---: | --- |
| F001 i F002: EXECUTE | 64 | 2 | Potvrđena za ovaj nacrt. |
| Osam LO funkcija: EXECUTE | 256 | 8 | Nedostaje za svih osam. |
| Trenutna baza: TEMPORARY | 31 | 1 | Potvrđena za ovaj nacrt. |
| Ukupno | 351 | 11 | Cijeli paket ostaje NO-GO. |

LO ciljevi su lo_create, lo_creat, lo_from_bytea, lo_put, lowrite,
lo_unlink, lo_truncate i lo_truncate64. Dva lo_import overloada nemaju PUBLIC
EXECUTE prema Q10.2h i nisu dio promjene.

Za svaku od 33 postojeće role prvo se dodaje nedostajući direktni EXECUTE ili
TEMPORARY grant, zatim se uklanja odgovarajući PUBLIC grant. Postojeći grantori,
grant option, direktni grantovi i ostala database prava ostaju sačuvani.
Postojeći PUBLIC CONNECT nije cilj promjene. Sve je jedna transakcija.

Ovo je izbor očuvanja sadašnjih efektivnih ACL prava, a ne dokaz poslovne
potrebe ili minimalnog skupa primalaca. Uključuje postojeće sistemske i NOLOGIN
role. Buduće role ta prava više ne bi dobivale preko PUBLIC; mogu ih dobiti
izričitim grantom ili članstvom u postojećoj privilegovanoj roli. Novi direktni
grantovi mogu ostati i nakon kasnijeg uklanjanja članstva. Zato ova promjena
zahtijeva operativnu odluku, ne samo tehnički prolaz testa.

## Dokaz i zaštite

[Generator](../../scripts/discovery/rights_plan.py) priprema deterministički
SQL i njegovu inverziju samo ako inventar potvrđuje ovlast za sve ciljeve.
Vezani ACL plan s tačnim OID-ovima, primaocima, grantorima i before/after ACL-om
ostaje lokalno izvan Git-a kao `bound-acl-plan.json`; hash je u izvještaju.
Ne sadrži nazive privatnih objekata, kontakte, vrijednosti kandidata ili tajne.

SQL predviđa ON_ERROR_STOP, provjeru baze/izvršitelja/verzije, identiteta i
ACL-a svakog cilja, cjelokupnog skupa rola i članstava. Prije i poslije promjene
provjerava dodatne PUBLIC definere i MAINTAIN. Poslije provjerava očuvana
ciljna prava svake postojeće role. Promjena relevantnog stanja prekida paket.
Nema automatskog retryja ni djelimične primjene.

Rollback vraća kanonizovane ACL stavke, uključujući grantor i grant option;
ne obećava identičan NULL-versus-default zapis u katalogu. Zahtijeva očekivani
ACL, isti skup rola i odsustvo nove discovery role. Ako se ona kasnije kreira,
prvo se mora zasebno ukloniti vlastitim provjerenim rollbackom.

Ove provjere nisu globalno zaključavanje kataloga. Prije moguće primjene treba
osigurati koordinisan prozor bez paralelnih administratorskih promjena,
osvježiti inventar i ponovo vezati SQL. Sadašnji paket nije dokaz potpune
read-only izolacije svih funkcija niti produkcijskog rada aplikacija.

## Stvarni blokator i sljedeći korak

Sadašnji pristup nema ni SET ovlast na vlasničku rolu ni EXECUTE WITH GRANT
OPTION za osam LO funkcija. Generator zato odbija neizmijenjeni produkcijski
snapshot. Puni 11-ciljni paket i dalje nije izvršiv. Q10.2l A odvaja tri
cilja koja sadašnji pristup smije mijenjati; to još nije produkcijski SQL.
Osam LO ciljeva ostaje residualno. Superuser za discovery rolu nije odobren.

## Q10.2l A: izvršivi podskup

Korisnik je 2026-09-11 potvrdio Option A: prije discovery role skinuti s
PUBLIC-a samo ono što sadašnji pristup smije mijenjati (`TEMPORARY` i dvije
Definer funkcije), uz Direktgrants postojećim rolama. Osam LO PUBLIC EXECUTE
ostaje residualno i nije dio ovog reza.

Q10.2j i dalje ne vrijedi automatski za ovaj manji paket. Generator smije
lokalno pripremiti SQL samo sa `scope=q10_2l_a`. Produkcijski apply, B1 i
kreiranje role nisu ovim odobreni. Q10.2d pokriva samo kasniju izradu role,
ne ovu ACL promjenu.
Ranija restore iznimka važi samo za kreiranje nove role; ne obuhvata PUBLIC
prava. Q10.2i nije odobrenje za njihovu primjenu.

## Ponovna provjera nakon dozvole Q10.2j

Jedan novi read-only poziv potvrđuje nepromijenjen inventar: 33 role i osam
ciljeva bez obje potrebne ovlasti. Rola nije kreirana i nema mutacije.
Korisnik potvrđuje da smatra ovlašteni put mogućim; tehnički dokaz drugog
podržanog puta ne postoji. Raniji zahtjev da korisnik napravi ili imenuje novog
administratora bio je pogrešan sljedeći korak: novi nalog ne dobiva automatski
nedostajuće ovlasti. Prvo treba provjeriti podržan koncept pristupa.
[Pojašnjenje uloga](access-plan-consolidated.md#klarstellung-welche-benutzer-sind-erforderlich)
razdvaja postojeći pristup, naručenog budućeg čitaoca i nepotrebno traženog
novog administratora.
