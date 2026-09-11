# Registar verzija discovery pristupa

Ažurirano: 2026-09-11. **Nijedna nova discovery rola nije primijenjena.**

Verzija SQL nacrta, verzija discovery gatea i odobrenje čitanja su odvojene
stvari. Oznaka V3 zato sama ne znači da postoji odobren SQL za izvođenje.

| Paket | Status | Značenje |
| --- | --- | --- |
| Rola V1 | NACRT / NO-GO | Strogi gate; nula članstava. |
| Rola V2 | NACRT / NO-GO | Samo automatski admin-only grant kreatoru u PG17. |
| Rola V3 pokušaj | POVUČENO | TEMP/schema-USAGE izuzeće je odbačeno. |
| Gate B1 V3 | PLANIRANO | Zasebni budući paket provjere nove role. |
| Q10.2g | IZVRŠENO, UZ OGRANIČENJA | Uži PUBLIC EXECUTE/schema-USAGE audit. |
| Q10.2h | IZVRŠENO, UZ OGRANIČENJA | Funkcije, zavisnosti i helper ACL-ovi. |
| Q10.2i | PRIPREMA TESTIRANA / NO-GO | Za osam LO ciljeva nedostaju ovlasti. |
| Q10.2j | KORISNIČKI ODOBRENO / TEHNIČKI NO-GO | Ovlašteni put nije imenovan. |

## Rola V1 i V2

[V1 SQL](sql/01-create-least-privilege-discovery-role-v1.sql) i
[V2 SQL](sql/02-create-least-privilege-discovery-role-v2-draft.sql) ostaju
nepromijenjeni. Njihovi testovi pokazuju konkretno provjerene grantove i
rollback ponašanje. Ne dokazuju potpunu read-only granicu za sve PUBLIC
funkcije. Produkcijski PUBLIC TEMP, funkcijska prava i dodatne granice moraju
biti riješeni prije primjene.

V2 prihvata samo PostgreSQL-ov admin-only grant kreatoru: ADMIN da, SET i
INHERIT ne. Takav administrator kasnije može mijenjati članstvo. To nije
nepromjenjiva sigurnosna izolacija.

## Povučeni V3 pokušaj

Predloženo je dozvoliti TEMP u vlastitoj sesiji i izuzeti SECURITY-DEFINER
funkcije bez schema USAGE. Prijedlog je povučen nakon stvarnih sintetičkih
kontraprimjera:

- već definirani PUBLIC SELECT view može posredno pozvati funkciju u
  nedostupnoj schemi i izmijeniti trajnu test-tabelu;
- isključivanje read-only zadane postavke i PUBLIC invoker funkcija mogu
  omogućiti trajni large object.

V3 SQL i njegov CLI izbor su uklonjeni. Ne postoji odobrenje za njegovu
primjenu. Korisnički zahtjev da se dokumentuje „v“ bilježi ovaj verzijski
status; ne pretvara povučenu ideju u prihvaćenu odluku.

## Važeće odobrenje

[ADR-0002 Q10.2h](../decisions/0002-search-design-interview.md) dokumentuje
izričito korisničko „ja“ za dodatni isključivo read-only scope. Za taj isti
scope ne traži se nova potvrda. Mutacije, promjene PUBLIC prava, stvarno
izvršavanje funkcija/viewova i čitanje kandidata nisu obuhvaćeni.

Detalji nalaza i odobrenog scopea su u
[PUBLIC auditu](../reviews/2026-09-11-public-definer-audit.md).
Poredak pristupa određuje
[konsolidovani plan](access-plan-consolidated.md).
Stvarni rezultat Q10.2h je u
[završnom izvještaju](../reviews/2026-09-11-public-paths-audit.md).

Q10.2i odobrava pripremu [konkretnog plana prava](public-rights-change-proposal.md),
ne njegovu primjenu. [Rezultat](../reviews/2026-09-11-rights-plan-verification.md)
bilježi 25 sintetičkih provjera i stvarni blokator ovlasti.

Q10.2j naknadno odobrava opisanu ciljanu promjenu. Novi read-only poziv
potvrđuje da sadašnji pristup i dalje nema ovlasti za osam LO funkcija.
Nije bilo primjene; korisnička dozvola i tehnička izvršivost su odvojene.
