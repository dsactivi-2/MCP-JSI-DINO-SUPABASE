# Ograničeni produkcijski preflight za discovery rolu

Datum: 2026-09-11. Rezultat: **READ_ONLY_EVIDENCE / ROLE SETUP NO-GO**.

## Identitet i način pristupa

Nakon korisničke korekcije vidljivog projekta, „JSI Base“ je nezavisno upoređen
sa spremljenim pooler korisnikom. Poređenje koristi hash cijelog transportnog
korisnika, uključujući projektni dodatak. Posebna lokalna identity datoteka ima
`0600`; postojeći B1 attesti, service i password datoteka nisu izmijenjeni.
Sadržaj password datoteke nije pročitan niti prikazan; libpq ju je koristio.

Izvršene su dvije različite read-only provjere, svaka kroz jednu vremenski
ograničenu lokalnu psql konekciju bez retryja. Nije korišten Supabase developer
plugin. Izlaz sadrži isključivo brojeve i logičke oznake; bez projektnih URL-ova,
imena kandidata, naziva funkcija ili njihovih definicija. TLS postavka `require`
nije dokaz kriptografske provjere imena servera.

## Stvarni nalazi

| Provjera | Rezultat |
| --- | --- |
| Konfigurirani cilj i serverska DB-rola odgovaraju očekivanim | DA |
| Glavna verzija PostgreSQL-a | 17 |
| Izvršitelj je superuser | NE |
| Izvršitelj ima CREATEROLE i ownership baze | DA |
| `dino_crm_discovery_ro_v1` već postoji | NE |
| PUBLIC ima database TEMP | DA |
| PUBLIC ima database CREATE ili schema CREATE | NE |
| PUBLIC relation/column/sequence write u prvom opsegu | NE |
| PUBLIC može izvršavati SECURITY-DEFINER funkcije | DA |
| Najmanje jedna takva funkcija je i u PUBLIC-accessible schemi | DA |

Relation/column write izuzima isključivo UPDATE ugrađene
`pg_catalog.pg_settings`, kako je dokumentovano i sintetički testirano.
SECURITY DEFINER sam po sebi ne dokazuje write ponašanje. Definicije i efekti
funkcija nisu analizirani; nijedna aplikacijska funkcija nije izvršena.
Naknadni review je otkrio da prvi live filter nije uključivao PostgreSQL-17
privilegiju `MAINTAIN`. Njeno stvarno produkcijsko stanje ostaje neprovjereno.
Filter i oba lokalna SQL nacrta su ispravljeni nakon sintetičkog reprodukovanja
greške; prethodni live nalaz nije retroaktivno proširen. Dva već dokazana
blockera su dovoljna za NO-GO, bez dodatne produkcijske konekcije.

## Posljedica i sljedeća granica

Nova rola bi automatski dobila PUBLIC privilegije. PostgreSQL nema pojedinačni
DENY koji bi samo toj roli oduzeo postojeća PUBLIC prava. Oba trenutna
setup nacrta zato moraju zaustaviti primjenu. Nije kreirana rola niti izmijenjen
ijedan grant, tabela ili zapis kandidata.

Potreban je zasebno ograničen plan za provjeru postojećih javno izvršivih
funkcija, njihovih potrebnih korisnika i efekata te odluka o PUBLIC TEMP.
Ovaj nalaz ne autorizira globalni REVOKE, izmjenu funkcija ili automatsko
ublažavanje sigurnosnog gatea. B1/B2/B3 nisu ovim zamijenjeni.

## Verifikacija

Prije drugog live preflighta, nova PUBLIC-abfrage provjerena je u odobrenom
izoliranom PostgreSQL-17.11 containeru: prazni baseline, eksplicitni PUBLIC
INSERT i bezopasna sintetička SECURITY-DEFINER funkcija daju očekivane oznake.
Naknadno je dodat negativni `MAINTAIN` test; V2 sada sadrži 18 provjera i
završava `PASS_WITH_GAPS`; password login i
produkcijska kompatibilnost ostaju neprovjereni. Vlastiti container je uklonjen.

<!-- markdownlint-disable-next-line MD013 -->
Prüfer: [check-role-bootstrap.py](../../scripts/discovery/check-role-bootstrap.py),
<!-- markdownlint-disable-next-line MD013 -->
[role_lifecycle_integration.py](../../tests/discovery/role_lifecycle_integration.py).

## Dodatni pregled: odobren i izvršen u ograničenom opsegu

Q10.2g je naknadno odobren. Stvarni rezultati i korekcija tumačenja schema
USAGE nalaze se u [novom izvještaju](2026-09-11-public-definer-audit.md).
Sljedeći pasusi čuvaju opis prvobitno predloženog užeg opsega; nisu odobrenje
proširenog pregleda indirektnih poziva ili drugih funkcija.

Predmet su isključivo SECURITY-DEFINER funkcije koje su u potvrđenom projektu
javno izvršive i imaju odgovarajući javni schema pristup. Priprema pregleda
obuhvatila bi identitet/signaturu, vlasnika, ACL, jezik i definiciju funkcije,
da se procijene efekti i postojeći potrebni korisnici. Nijedna funkcija se ne
izvršava i nema čitanja kandidata, izmjena grantova ili globalnih REVOKE-a.

Definicije mogu sadržavati osjetljive literale. Prije takvog čitanja mora biti
pregledan ograničeni lokalni izlazni handler: bez slanja sirovih definicija,
literala ili credentiala u model, chat ili Git; nepotpuna redakcija znači STOP.
Korisniku se predaje redigiran nalaz i konkretan prijedlog potrebnih prava.
Odobrenje pripreme ovog dodatnog pregleda nije odobrenje kasnijih mutacija.
