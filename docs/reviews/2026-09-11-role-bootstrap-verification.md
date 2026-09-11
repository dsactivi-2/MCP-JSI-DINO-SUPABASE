# Provjera pripreme discovery role

Datum: 2026-09-11. Status: **PASS_WITH_GAPS / PRODUKCIJA NO-GO**.

## Odluke i obuhvat

Korisnik je odobrio ograničeni izuzetak od prethodnog restore testa isključivo
za izradu discovery role (ADR-0002 Q10.2d) i privremeni sintetički PostgreSQL
testcontainer (Q10.2e). Restore ostaje obavezan prije promjena tabela ili podataka.
U produkciji nije uspostavljena konekcija, kreirana rola niti promijenjen grant.

## Rezultat izvršenih provjera

<!-- markdownlint-disable MD013 -->

| Provjera | Stvarni rezultat |
| --- | --- |
| PostgreSQL 17.11, V1 | 12 provjera; uspješan superuser setup/rollback i atomarno odbijanje nepodržanog non-superuser puta. |
| PostgreSQL 17.11, zaseban V2 nacrt | 16 provjera; uspješan non-superuser setup/rollback i odbijanje SET/INHERIT, drugog administratora i izlaznog članstva. |
| Negativne provjere privilegija | PUBLIC TEMP, INSERT, UPDATE, UPDATE kolone i istoimeni aplikacijski `pg_settings` odbijeni bez djelimične role. |
| Rollback s neočekivanom zavisnošću | Rola i prethodni grantovi ostaju sačuvani nakon atomarnog odbijanja. |
| Izolacija | Fiksni postojeći image; bez mreže, host portova, host datoteka i stvarnih podataka; samo tmpfs. Vlastiti containeri uklonjeni. |
| Lokalni owner preflight | Zaustavljen prije `Popen`: nedostaje nezavisna potvrda pooler identiteta i DB-role. Nema bazne konekcije. |
| Lokalni standardni provjerni tok | Postojeći Python/Fake/Bash i Markdownlint koraci prošli. Ukupni exit 2 zbog ranije tuđe whitespace izmjene u skill referenci. |
| Novi Python alati | Sintaksa provjerena bez generisanih datoteka. |

<!-- markdownlint-enable MD013 -->

## Ispravke i ograničenja

Stvarni runtime test je dokazao da V1 pogrešno klasificira standardni UPDATE nad
`pg_catalog.pg_settings` kao podatkovni write. Ispravka izuzima samo UPDATE te
tačno identificirane sistemske view; ownership i druge privilegije ostaju pod
provjerom. Aplikacijska view istog naziva nije izuzeta.

Non-superuser administrator ne može izvršiti postojeći `SET ROLE` i ne može sam
ukloniti automatski ADMIN-only grant koji mu PostgreSQL dodijeli. Zasebni V2
nacrt eksplicitno provjerava novu rolu i dopušta samo početni ADMIN-only grant
kreatoru, bez SET/INHERIT opcija. Administrator s ADMIN opcijom kasnije može
mijenjati članstvo; to nije nepromjenjiva sigurnosna barijera. V1 politika nije
tiho zamijenjena, a V2 nije produkcijski odobren niti primijenjen.

Prijava u testu koristi lokalni trust. Nije dokazana lozinkom autentificirana
prijava, prava u Supabase projektu, stvarna verzija servera ili produkcijska
kompatibilnost. Produkcijski mutacijski launcher i završni post-check ostaju
neizvedeni. Za daljnji rad potreban je nezavisan projektni identitet; hash
transportnog korisnika ne smije potvrđivati samog sebe iz neprovjerene datoteke.

Postojeća nepovezana whitespace izmjena u
`.agents/skills/supabase-postgres-best-practices/references/_contributing.md:30`
ostavljena je neizmijenjena. Zbog toga se cijeli lokalni gate ne označava PASS.

## Review i reprodukcija

Dva nezavisna reviewa pregledala su izolaciju, cleanup, izuzetke prava i
read-only owner preflight. Ispravljeni su čišćenje pri neizvjesnom container
startu, prekid psql procesa, odvojena pooler/DB identifikacija i negativni
membership/UPDATE testovi. Neizvjestan cleanup se izričito prijavljuje.

Komande i SQL hashovi su u
[paketu role](../discovery/least-privilege-discovery-role-v1.md).
Lokalni izvještaji ovog prolaza nalaze se izvan Git-a u
`/private/tmp/crm-role-exception-20260911/` i ne sadrže ciljne URL-ove,
credentiale ili podatke kandidata.

Korišteni skills: domain-modeling za odluke, Supabase i Postgres best practices
za SQL/rechte, TDD za runtime provjere, diagnosing-bugs za reproducirani
`pg_settings` nalaz i code-review za nezavisnu kontrolu. Tehničke primarne
reference povezane su u paketu role.
