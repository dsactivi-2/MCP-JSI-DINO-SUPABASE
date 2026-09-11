# Provjera konkretnog plana prava

Datum: 2026-09-11. **PASS_WITH_GAPS za pripremu; NO-GO za produkciju.**

## Read-only dokaz Q10.2i

Jedna uspješna produkcijska konekcija preko postojećeg pregledanog psql puta,
uz read-only transakciju i potvrđeni lokalni identitetski binding. Pročitani su
samo odobreni kataloški podaci. Nema poziva aplikacijskih funkcija/viewova,
kandidata, large-object sadržaja, tajni u izvještaju ili promjene baze.

Potvrđeno: PostgreSQL 17, 33 role, discovery rola ne postoji, nema dodatnih
PUBLIC definera izvan ciljanog skupa i nema PUBLIC MAINTAIN. Dvije ranije
funkcije odgovaraju Q10.2h source hashovima. Za obje i database TEMP postoje
potrebne ovlasti; za osam LO helpera nema SET-owner ni grant option ovlasti.
[Plan](../discovery/public-rights-change-proposal.md) sadrži 351 predloženi
nedostajući direktni grant i 11 ciljnih PUBLIC opoziva.

Minimizovani inventar i vezani ACL diff ostaju izvan Git-a u lokalnom direktoriju
`/private/tmp/crm-rights-plan-20260911/`. Ne predstavljaju backup baze.
Generator je na neizmijenjenom live snapshotu provjeren: odbija generisanje
zbog nedostajućih ovlasti. Nije izdat izvršivi produkcijski SQL paket.

## Sintetička verifikacija

Novi privremeni PostgreSQL 17.11 kontejner iz ranije odobrenog lokalnog imagea,
bez mreže, host mountova ili stvarnih podataka: svih **25 lifecycle provjera**
prošlo je; vlastiti kontejner je uklonjen. Četiri lokalna unit testa plana
prošla su. Relevantni testovi obuhvataju:

- očuvanje ciljnih prava postojećih rola, grantora i grant option lanca;
- odbijanje novog logina za LO create, direktni i PUBLIC-view poziv definera
  te TEMP, uz očuvan indirektni pristup postojećeg testnog logina;
- kanonski ACL rollback i potpuni rollback greške usred promjene;
- odbijanje ponovne primjene, promijenjene liste rola, ACL-a, dodatnog PUBLIC
  definera i naknadnog MAINTAIN prava.

Spec review je našao izostalu ponovnu provjeru dodatnih PUBLIC rizika i izostali
ON_ERROR_STOP u SQL tekstu. Red testovi su potvrdili greške; oba su ispravljena,
novi Green ciklus prolazi. Naknadni spec review nema preostalih nalaza u tom
opsegu. Zasebni standards/privacy review prihvatio je read-only inventar;
nijedan review nije odobrenje produkcijske mutacije.

Ponovljiv lokalni test, uz ranije odobrenje izoliranog kontejnera:

```sh
rtk proxy python3 -B tests/discovery/rights_plan_test.py
rtk proxy python3 -B tests/discovery/role_lifecycle_integration.py \
  --allow-new-isolated-container --owner-compatible-draft
rtk proxy /bin/bash scripts/check-local.sh
```

## Hash veza

SHA-256 u trenutku završnog funkcionalnog testa:

```text
rights_plan.py
2a10cc79cb9de8963575de20a81cce988d67168ebb6d2e8831c73e9cccaeeb1b
rights_plan_test.py
92a76e1efce3bd4aa07ffcc882b75b3997fed55f599acf49aefde4e8954cdb9c
role_lifecycle_integration.py
9e2be9603812446aac41563bc96d19187e136314e55940b07328c9654343d6b8
inventory.json
e59ae3017a2f74ebdb06dbd20b0e2abf80db288e987498f470c36cde7de426c4
bound-acl-plan.json
b6bcab35a27d8825ad17c1695ee3610a67be10debac34859fb5e52a62ce19412
synthetic.json
b4916055a890deb14812bc70bfd3ede5bd36ae33f6074077e202e01a06e047f5
```

## Lokalna provjera dokumentacije

Svi lokalni unit/fake-process/launcher testovi prolaze. Provjera 453 relativna
Markdown linka i lint 40 aktivnih Markdown dokumenata prolaze bez nalaza.
`git diff --check -- docs scripts tests` prolazi. Puni `check-local.sh` ipak
završava kodom 2 zbog ranijeg, nepovezanog trailing whitespacea u
`.agents/skills/supabase-postgres-best-practices/references/_contributing.md:30`.
Ta postojeća izmjena je sačuvana; puni gate nije označen zelenim.

## Ograničenja

Nedostaju ovlasti za osam sistemskih funkcija, produkcijski compatibility test,
password-auth dokaz, koordinisan administratorski prozor i odobrenje promjene.
SQL guardovi nisu globalni catalog lock. Nije dokazana potpuna zabrana svih
PUBLIC/invoker efekata. Očuvanje ACL-a nije dokaz poslovne potrebe svih prava.
Dnevni backup je korisnička izjava; restore iznimka za novu rolu se ne proširuje.

## Dodatak: Q10.2j dozvola i ponovna provjera

Korisnik je izričito odobrio opisani plan. Nakon toga je izvedena jedna nova
read-only konekcija bez retryja ili mutacije. Minimizovani rezultat je
`approved-recheck.json` u istom lokalnom direktoriju; njegov SHA-256 jednak je
ranijem `inventory.json` hashu. Inventar je nepromijenjen: 33 role, osam ciljeva
bez SET-owner i grant option, discovery rola ne postoji. Raniji nedostatak
korisničke dozvole je riješen; tehničke ovlasti nisu. Čeka se naziv konkretnog
ovlaštenog pristupa, ne nova opća dozvola. Ranije navedeni ostali preduslovi
nisu ovim pozivom dokazani.
