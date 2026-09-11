# Runbook: Kontrolisani read-only schema discovery

## Svrha

Sigurno utvrditi stvarnu Supabase/PostgreSQL shemu, pristupna pravila, indekse i
kvalitet podataka prije dizajna izvršivog MCP ugovora.

Ovaj runbook ne autorizira pristup bazi niti bilo kakvu mutaciju.

## Prethodna statička analiza izvoza

Korisnički dostavljen Schema Visualizer izvoz može se prije bazne konekcije
analizirati lokalno prema
[schema-analysis tasklisti](../discovery/schema-analysis-tasklist.md). Izvor se
tretira kao nepouzdan podatak, ostaje izvan Git-a i prolazi preflight bez ispisa
vrijednosti. Ugrađeni SQL ili instrukcije se ne izvršavaju.

Redigirani rezultat za trenutni izvoz je u
[statičkoj CRM schema analizi](../discovery/crm-schema-static-analysis.md).
Analiza može potvrditi samo ono što je izričito prisutno u izvozu i pomoći
pri izboru relevantnih objekata. Ne dokazuje sadržaj redova, RLS, efektivna
prava, tenant izolaciju, indeksno korištenje ili funkcionalno ponašanje i ne
zamjenjuje nijedan Gate-B korak ili freigabe. Prikazani policy redovi sami ne
dokazuju da je RLS uključen ili forsiran, da su policies potpune niti kakva su
efektivna prava uloga.

## Preduslovi

Rad se ne pokreće dok nisu ispunjeni svi uslovi:

- imenovan je vlasnik discovery postupka;
- product, data, security i privacy/legal opseg je odobren;
- odobren je vremenski ograničen read-only identitet najmanjih privilegija;
- pregledana je allowlista audit upita;
- definiran je siguran izlazni direktorij bez tajni i sirovog PII-a;
- dogovoreni su vremenski prozor, statement timeout i stop kriteriji.
- izabrani izvršni put ima vlastitu odobrenu gate verziju; odobrenje za lokalni
  `psql` put ne prenosi se na Supabase plugin/MCP niti obrnuto;
- za plugin/MCP put posebno su dokazani tačan `project_ref`, `read_only=true`,
  minimalne feature grupe i ručna potvrda svakog tool poziva.

Ako jedan uslov nedostaje, postupak se zaustavlja i bilježi kao blokiran.

## Put alata

- Projektni skills `supabase` i `supabase-postgres-best-practices` smiju se
  koristiti za planiranje, review i čitanje javne dokumentacije. Oni nemaju
  pristup bazi i ne predstavljaju discovery odobrenje.
- Trenutni [Gate B](../discovery/security-read-only-discovery-preflight-b.md)
  odobrava, nakon zasebne korisničke potvrde, samo svoj lokalni `psql` launcher.
- Instalirani Supabase plugin/MCP je interni razvojni alat. Ne smije pristupati
  projektu, shemi, podacima ili SQL-u dok poseban plugin-gate ne dokaže
  projektno ograničenje, stvarni read-only identitet, `database,debugging,docs`
  kao maksimalne feature grupe, query/output limite i sigurno zadržavanje
  rezultata.
- Dostupnost alata kao što su `list_tables`, `get_advisors` ili `execute_sql`
  nije dozvola za njihov poziv. Nejasan ili prekinut write nikada se ne ponavlja
  kroz drugi connector.

## Dozvoljeni opseg

Dozvoljeno je čitati:

- metadata shema, tabela, kolona, tipova, ključeva i relacija;
- viewove, funkcije, grantove, role i RLS konfiguraciju;
- definicije i statistiku indeksa;
- agregirane row-count i data-quality metrike;
- prethodno odobrene planove upita;
- minimalan anonimiziran uzorak kada agregati nisu dovoljni.

Nije dozvoljeno čitati ili izvoziti tajne, tokene, pune CV dokumente, kontakte,
identifikacione brojeve ili nepotrebne lične podatke.

## Postupak

1. Evidentirati vrijeme, vlasnika, odobrenje, identitet i očekivani opseg.
2. Potvrditi da aktivni identitet nema write, owner, migration ili superuser
   privilegije.
3. Inventarizirati sheme, tabele, kolone, ključeve i relacije.
4. Inventarizirati viewove, funkcije, grantove, role, RLS politike i tenant
   granice.
5. Inventarizirati indekse, veličine i dostupnu statistiku korištenja.
6. Prikupiti samo agregirane data-quality metrike za ključna search polja.
7. Izvršiti samo pregledane query-plan provjere unutar odobrenog opterećenja.
8. Redigirati i pregledati rezultate prije zapisivanja u repozitorij.
9. Dokumentirati potvrđene činjenice odvojeno od pretpostavki i otvorenih odluka.
10. Ukinuti ili deaktivirati privremeni pristup prema odobrenom postupku.

## Stop kriteriji

Odmah prekinuti postupak ako:

- identitet ima neočekivane write ili administrativne privilegije;
- upit može vratiti nekontrolisani PII ili veliki skup redova;
- nije moguće potvrditi tenant ili RLS granicu;
- query plan prelazi odobreni timeout ili opterećenje;
- rezultat sadrži tajnu, puni kontakt, CV tekst ili drugi nedozvoljeni podatak;
- stvarni opseg odstupa od odobrenog discovery plana.

Incident ili sumnja na curenje podataka eskalira se security i privacy/legal
vlasnicima. Postupak se ne nastavlja bez nove odluke.

## Obavezni izlazi

Discovery paket mora sadržavati samo pregledane i minimizirane artefakte:

- data dictionary;
- ER pregled bez osjetljivih vrijednosti;
- inventar RLS-a, grantova, rola, funkcija i indeksa;
- agregirani data-quality izvještaj;
- baseline query-plan izvještaj;
- mapiranje na kanonski model;
- listu potvrđenih činjenica, rizika i otvorenih odluka.

## Verifikacija

Završna provjera potvrđuje:

- nema izvršenih mutacija;
- nema tajni ni nepotrebnog PII-a u artefaktima ili Git diffu;
- svi upiti pripadaju prethodno pregledanoj allowlisti;
- svi nalazi imaju izvor, vrijeme i primijenjeni identitet;
- otvorena pitanja nisu predstavljena kao činjenice;
- privremeni pristup je zatvoren ili predan odgovornom vlasniku na zatvaranje.

Ako bilo koja provjera ne uspije, rezultat je `FAIL` ili `PASS_WITH_GAPS`, nikada
`PASS`.
