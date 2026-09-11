# Pregled projekta: Supabase CRM MCP

Status: dokumentacijska osnova kompletirana; governance i priprema discoveryja

Ažurirano: 2026-09-11

Primarni jezik dokumentacije: B/H/S latinica

## Svrha

Projekt gradi siguran MCP sloj za prirodno pretraživanje približno 200.000 CRM
zapisa kandidata na B/H/S, njemačkom i engleskom. Obim je projektna procjena,
DURCH DISCOVERY ZU PRÜFEN.

Ciljni klijenti uključuju ChatGPT, Claude, Codex, Grok i druge
MCP-kompatibilne klijente.

## Autoritativni dokumenti

- [README.md](../README.md) daje ulaznu mapu i dokumentacijske provjere.
- [CONTEXT.md](../CONTEXT.md) sadrži poslovni kontekst i domenski rječnik.
- [Implementacijski brief](SUPABASE_CRM_MCP_IMPLEMENTATION_BRIEF.md) sadrži
  zahtjeve, faze, test-matricu i otvorena pitanja.
- [docs/decisions/](decisions/) je jedini direktorij dugoročnih arhitekturnih
  odluka; [ADR-0001](decisions/0001-controlled-query-boundary.md) definira
  prihvaćenu granicu pretrage, a
  [ADR-0002](decisions/0002-search-design-interview.md) čuva status pitanja i
  odgovora aktivnog design intervjua. Prihvaćeni
  [ADR-0003](decisions/0003-separated-profile-administration-mcp.md) zahtijeva
  odvojeni MCP za upravljanje Berufssuchprofilima. Prihvaćeni
  [ADR-0004](decisions/0004-automated-database-development.md) definira
  native-first automatizaciju razvoja, testiranja i optimizacije baze.
- [Discovery runbook](runbooks/schema-discovery.md) određuje preduslove i
  postupak read-only audita.
- [Runbook automatizacije baze](runbooks/database-development-automation.md)
  određuje razvojne, CI, performance i release gateove nakon discoveryja.
- [Plan automatizacijskih ticketa](planning/release-1-automation-tickets.md)
  daje blockers-first redoslijed prije zasebne Linear freigabe.
- [SDK integracijski plan](planning/sdk-integration-plan.md) razrađuje MCP,
  Supabase adapter, token granice i provjere; dokumentovani prijedlog nije
  instalacija niti potvrđen stack.
- [Plan statičke schema analize](discovery/schema-analysis-tasklist.md) vodi
  preflight i obradu korisnički dostavljenog izvoza bez bazne konekcije.
- [Supabase tooling](agents/supabase-tooling.md) razdvaja projektne skills,
  razvojni Supabase plugin/MCP i strogo kontrolisani Gate-B put.
- [Supabase-Plugin Gate P](discovery/supabase-plugin-read-only-gate-draft.md)
  dokumentuje neizvršivi `DRAFT / NO-GO` za mogući alternativni read-only put.
<!-- markdownlint-disable-next-line MD013 -->
- [Evaluacijski gate semantičke pretrage](research/semantic-search-evaluation-gate.md)
  određuje kako se nakon discoveryja porede nevectorski baseline, `pgvector` i
  Vector Buckets bez prethodnog izbora tehnologije.
- [AGENTS.md](../AGENTS.md) definira pravila rada agenata u repozitoriju.

Ako se dokumenti ne slažu, rad se zaustavlja dok se konflikt ne razriješi
ažuriranjem briefa ili novim ADR-om.

## Trenutno stanje

Raniji [ograničeni Q10.2g audit](reviews/2026-09-11-public-definer-audit.md)
nalazi dvije SECURITY-DEFINER rutine sa PUBLIC EXECUTE, bez PUBLIC schema
USAGE; u tom ranijem pozivu definicije nisu pročitane. Sintetički kontraprimjeri
pokazuju da schema USAGE i promjenjivi read-only default ne dokazuju potpunu
zabranu trajnih upisa. Predložena V3 iznimka je povučena. Rola još nije
kreirana. Korisnik je dodatni uski read-only scope izričito odobrio u Q10.2h;
Q10.2h je sada izvršen. Dvije definicije ostaju NOT_PROVEN_READ_ONLY, a osam
pregledanih LO helper funkcija ima PUBLIC EXECUTE. Detalji i 23 sintetičke
provjere su u [izvještaju](reviews/2026-09-11-public-paths-audit.md).
Q10.2i je zatim omogućio [konkretan plan prava](discovery/public-rights-change-proposal.md):
33 postojeće role, 351 predloženi grant i 11 PUBLIC opoziva. Novi ciklus ima
25 sintetičkih provjera. Sadašnji pristup nema ovlast za osam LO funkcija;
produkcijski paket ostaje tehnički NO-GO. Q10.2j daje korisničku dozvolu za
opisanu promjenu, ali naknadna read-only provjera potvrđuje nepromijenjene
ovlasti. Korisnik trenutno ne treba praviti novog administratora. Poseban
pristup za čitanje ostaje naručen po Q10.2b; prepreka je sadašnji nacrt njegovih
sigurnosnih granica. Slijedi provjera podržanog koncepta pristupa, prema
[pojašnjenju](discovery/access-plan-consolidated.md#klarstellung-welche-benutzer-sind-erforderlich).
Detalji su u
[provjeri plana](reviews/2026-09-11-rights-plan-verification.md). [Registar verzija](discovery/role-version-register.md)
razlikuje
povučeni pokušaj role V3 od još planiranog Gate-B1-V3 paketa.

Repozitorij sadrži dokumentacijsku osnovu, prihvaćene ADR-ove, discovery
runbook,
lokalni Matt Pocock setup i Serena projektnu konfiguraciju.

Projektne kopije službenih skillsa `supabase` i
`supabase-postgres-best-practices` postoje pod `.agents/skills/` i mogu se odmah
koristiti za planiranje i review bez pristupa bazi. Instalirani Supabase plugin
povezan je s istim službenim Supabase app/MCP slojem kroz više distribucija;
duplikat ne daje dodatnu izolaciju ni novi trust boundary. Read-only i
projektno ograničenje aktivne veze nisu dokazani, pa plugin nije odobren za
project, schema, data ili SQL pozive. Trenutni Gate B i dalje koristi isključivo
pregledani lokalni `psql` put iz svog preflight dokumenta.

Korisnik je 2026-09-11 potvrdio postavku `Always ask`. Statički Tool-Katalog
ipak još sadrži account i write alate, pa
[Plugin Gate P](discovery/supabase-plugin-read-only-gate-draft.md) ostaje
`NO-GO`. Nije izveden nijedan projektni ili bazni Plugin poziv.

Korisnik je također potvrdio da je ciljni Supabase projekt produkcijski i da
sadrži stvarne podatke kandidata. Službeni razvojni Plugin/MCP ne smije se
direktno povezati s tim projektom. Eventualni Live-Plugin test zahtijeva zaseban
development/test projekt bez stvarnih osobnih podataka i novo odobrenje.
Pošto takav projekt nije planiran, Plugin Gate P ostaje blokiran; to ne daje
pravo da se developer plugin spoji na produkciju.

Korisnik je dostavio lokalni Schema Visualizer tekstualni izvoz za shemu `crm`
izvan repozitorija. Datoteka je prošla lokalni preflight bez ispisa vrijednosti
i statičku analizu prema
[schema-analysis tasklisti](discovery/schema-analysis-tasklist.md). Sirovi
export ostaje izvan Git-a, a redigirani rezultat ne zamjenjuje Gate B.

Setup koristi postojeći namjenski Linear projekt **Dino problem baza CRM** u
timu **Activi (ACT)**. Identitet i workflow su u
[issue trackeru](agents/issue-tracker.md), pet postojećih kanonskih oznaka u
[triage mapiranju](agents/triage-labels.md), a raspored dokumentacije u
[domenskim pravilima](agents/domain.md). Projekt, tim i oznake provjereni su
read-only 2026-09-10.

Aplikacijski scaffold ne postoji. Jezik, framework, runtime, package manager,
hosting, auth model i fizički database ugovor još nisu odabrani ili potvrđeni.
Q11 potvrđuje lokalnu SDK konsolidaciju i paralelnu provjeru. Ažurirani
[plan](planning/sdk-integration-plan.md) preferira evaluaciju TypeScript
MCP SDK-a v2 i uskog Supabase adaptera; `@supabase/server` je uslovljen auth
ugovorom, a `@supabase/middleware` dodatnom potrebom i alpha odlukom.
[Primarna provjera](research/mcp-supabase-sdk-integration.md) koriguje raniji
v1 paketni primjer i odvaja MCP tokene od downstream DB credentiala.
SDK-01–08 su planirane provjere u postojećim radnim paketima, ne izvršeni
testovi. SDK odabir ne uklanja Q9, Discovery, AUTO-02 ili release gateove.
[Provjera SDK dokumentacije](reviews/2026-09-11-sdk-documentation-verification.md)
odvaja lokalni rezultat i preostale gapove.

Dokumentacijske provjere opisane su u
[README.md](../README.md#provjera-dokumentacije); aplikacijske provjere još
nisu uspostavljene. Povezani audit baze nije proveden. Lokalni, schema-only
Schema Visualizer izvoz za korisnički scope `crm` statički je analiziran bez
bazne konekcije. Redigirani
[izvještaj](discovery/crm-schema-static-analysis.md) dokazuje 100 potpunih
table blokova, 1.104 kolone i primary key u svakom prikazanom bloku. Ne
prikazuje foreign-key, unique ni identity constraints. RLS sekcija navodi 188
objektnih naziva, od kojih 88 nema table/column blok; zato je rezultat
`PASS_WITH_GAPS` i nije zamjena za Gate-B discovery.

Prihvaćen je automatizacijski pravac iz
[ADR-0004](decisions/0004-automated-database-development.md): nakon discoveryja
i ugovora Supabase CLI, lokalna sintetička baza, verzionirane migracije,
`db lint`, pgTAP, contract testovi, Advisors i CI čine osnovni razvojni put.
AI smije pripremati samo pregledive SQL i testne diffove. pganalyze se evaluira
tek nakon reprezentativnog workload-a. Odluka ne bira otvoreni aplikacijski
stack i ne aktivira još nepostojeće komande.

Schema Visualizer je za `crm_api` prikazao 0 tabela; to ne dokazuje odsustvo
viewova, funkcija ili RPC-ja. Zasebni lokalni `crm_auth` izvoz je statički
<!-- markdownlint-disable-next-line MD013 -->
analiziran u [redigiranom izvještaju](discovery/crm-auth-schema-static-analysis.md):
šest tabela modelira korisnik-zaposlenik mapiranje, uloge, dozvole, role-
permission veze, user-role veze i scopeove. Prikazani policies i ID-kolone ne
dokazuju efektivnu RLS zaštitu, tenant izolaciju ili foreign keys.

Semantička pretraga je planirana samo kao evaluacijska grana nakon discoveryja,
ne kao komponenta Releasea 1 po zadanim postavkama. Nisu kreirani Vector Bucket,
S3 Vector Wrapper, embedding pipeline ni produkcijska konfiguracija. Gate prvo
traži dokaz kvalitetne praznine nakon strukturiranih filtera, taksonomije, FTS-a
i po potrebi `pg_trgm`, zatim izolirano poređenje s `pgvector`-om i Vector
Bucketom. Call-memory integracija ostaje izvan opsega ovog projekta.

Design intervju o toku pretrage, filterima, potvrdi, historiji i izvozu je u
toku. Njegove potvrđene, djelimične i otvorene odluke vode se u
[ADR-0002](decisions/0002-search-design-interview.md). Entwurf nije produkcijsko
odobrenje niti zamjena za završnu specifikaciju.

Q8.4 potvrđuje osnovni koncept kontrolisanih, ponovo upotrebljivih
Berufssuchprofila. Neekskluzivnost, direktna pretraga zanimanja i neaktivnost
nenavedenih filtera ostaju potvrđeni. Detaljna filtersemantika i obavezna
potvrda
svake nove ili izmijenjene pretrage su VORLÄUFIGER VORSCHLAG zbog nedostajuće
izvorne liste preporuka. Q8.5 je u cijelosti OFFEN. Q4.5 ostaje OFFEN bez
rekonstruisanja nepoznatog pitanja. Release 1 ne vraća kontakte ni kroz jedan
alat; kontaktna funkcija i CONTACT-02 pripadaju kasnijoj, zasebno odobrenoj
fazi. Mogućnosti za
izradu i administraciju tih profila obrađene su u
[Q8.4.2 istraživanju](research/berufssuchprofile-q8-4-2.md); odluka o odvojenom
administrativnom MCP-u prihvaćena je i razrađena u
[ADR-0003](decisions/0003-separated-profile-administration-mcp.md).

Q10 potvrđuje da je Supabase dump iz ugašenog CRM-a privremena radna osnova za
discovery i planiranje. Lokalni SQL dump, OrbStack kontejner i ZIP backup ostaju
neprovjereni i ne predstavljaju dokaz restorea. Korisnik ne želi zaseban
Supabase development/staging projekt. Potvrđen je prijelaz: kratkoročno se
postojeće importovane tabele čuvaju neizmijenjene i potrebni Release-1 sloj se
gradi aditivno kao opcija A; zatim se isti kompatibilni elementi proširuju u
kanonski cilj opcije D kroz male, provjerene migracijske rezove. Odluka ne
odobrava bazni pristup, migraciju ili produkcijski apply.

Korisnik je preuzeo product, data, security, privacy/legal, operations i
discovery odgovornost trenutno, bez obavezne nezavisne provjere druge osobe.
RACI, on-call postupak i konkretni procesi provjere ostaju OFFEN. Rizik te
kombinacije ostaje evidentiran. Faza 0 nije završena dok nije odobren opseg
read-only audita.

## Prvi isporučivi cilj

Prvi cilj je reproducibilan i pregledan discovery paket koji sadrži:

- inventar relevantnih shema, tabela, kolona, relacija, funkcija i indeksa;
- pregled RLS pravila, grantova, rola i tenant granica;
- anonimizirani data-quality baseline;
- mapiranje stvarne sheme na kanonski model kandidata;
- pregledive prijedloge JSON, MCP i RPC ugovora;
- evidentirane rizike, nepoznanice i potrebne vlasničke odluke.

Ovaj cilj ne uključuje produkcijske mutacije, deploy ili aktiviranje
credentiala.

## Put do implementacije

Prema Q9 prvo se razjašnjavaju sigurnosni preduslovi i odobrenje audita,
zatim slijedi read-only discovery, a tek potom nastavak intervjua. Korisnikova
navedena brojka od 179 tabela je DURCH DISCOVERY ZU PRÜFEN.

Prije bazne konekcije dozvoljena je statička, lokalna analiza korisnički
dostavljenog schema izvoza nakon sigurnosnog preflighta. Ona može suziti popis
relevantnih objekata, ali ne potvrđuje podatke, RLS, prava, tenant granice,
indekse ili runtime ponašanje.

Prije povezivanja prioritetan je ljudski review oba statička izvještaja. Nakon
njega je pripremljen minimalni B2 scope samo za `crm`, `crm_api` i `crm_auth`;
sve ostale sheme ostaju izvan prvog metadata inventara. B1 V2 ostaje neodobren
postojeći paket, ne automatski sljedeći korak.
Korisnik je potvrdio da nema namjenske discovery role i naložio njenu izradu
(Q10.2b). Izabran je bootstrap nove role; ona još nije kreirana. Prije izvedbe
treba ispuniti sigurnosne preduslove prema
[konsolidovanom pristupnom planu](discovery/access-plan-consolidated.md).
Q10.2d izuzima isključivo ovu izradu role od prethodnog restore testa. Test
ostaje obavezan prije promjena tabela ili podataka; dnevni backup je potvrđen
kao korisnička izjava, bez tehničke provjere.
Q10.2e je omogućio privremene sintetičke testove: prvi V1 je imao 12 provjera,
zasebni V2 nacrt 16, uz ograničenja password/prava produkcije. Owner preflight je
zaustavljen lokalno zbog nepotpune potvrde pooler/projekt identiteta.
<!-- markdownlint-disable-next-line MD013 -->
Detalji: [provjera role](reviews/2026-09-11-role-bootstrap-verification.md).
Naknadno je korisnik odabrao odgovarajući projekt „JSI Base“ i nezavisni hash
abgleich je prošao (Q10.2f). Dvije ograničene read-only provjere potvrdile su
PostgreSQL 17, CREATEROLE/DB-owner pristup bez superusera i nepostojanje nove role.
Tadašnji nalazi PUBLIC TEMP i SECURITY-DEFINER prava blokirali su izradu role.
Najnoviji audit gore precizira razliku između EXECUTE prava i schema USAGE;
sigurnost indirektnih poziva ostaje otvorena. Posljednji V2 sintetički ciklus
ima 25 provjera, uključujući kontraprimjere, Q10.2h audit i Q10.2i plan prava.
Nije bilo produkcijske mutacije ili čitanja kandidata. Opći schema audit i
dalje nije izvršen.
Za novu rolu potreban je vlastiti B1 V3 paket, koji još ne postoji. B2/B3
launcher, streammarker i coverage gateovi još nisu implementirani; B2 ostaje
blokiran do pregledanog B1 PASS i vlastite freigabe.
Raniji read-only lokalni preflight je potvrdio da target attest,
connection-service i
credential datoteka postoje kao regularne, symlink-free datoteke vlasnika
trenutnog korisnika s modom `0600`; njihov sadržaj nije čitan. Obavezni approval
attest tada nije postojao; ova korektura ne provjerava njegov današnji sadržaj
ili postojanje i ne daje dozvolu za launcher.
Nakon odobrenja opsega slijedi
[discovery runbook](runbooks/schema-discovery.md). Daljnji rad prati
<!-- markdownlint-disable-next-line MD013 -->
[faze implementacije](SUPABASE_CRM_MCP_IMPLEMENTATION_BRIEF.md#faze-implementacije-i-isporučivi-rezultati)
<!-- markdownlint-disable-next-line MD013 -->
i [kriterije prihvata](SUPABASE_CRM_MCP_IMPLEMENTATION_BRIEF.md#kriteriji-prihvata).
Nakon discoveryja i odobrenja ugovora slijedi minimalni aditivni Release-1 sloj
opcije A. Svaka njegova struktura mora biti kompatibilan prvi dio ciljnog modela
opcije D. Kasniji D prijelaz radi se po domenama uz lineage, količinski i
funkcionalno poređenje, RLS/contract testove, rollback i zasebno odobrenje
svakog
produkcijskog reza. Importovane tabele se ne mijenjaju niti uklanjaju u A fazi.
Prije prve implementacijske migracije uspostavlja se automatizacijski scaffold
prema [runbooku](runbooks/database-development-automation.md). Svaki SQL
prijedlog, uključujući AI-generirani, mora proći lokalni reset, lint,
DB/contract testove, kontrolisani plan upita i CI prije produkcijskog dry-runa.
Monitoring počinje ugrađenim Supabase/PostgreSQL signalima; dodatni servisi
ulaze samo nakon mjerljivog triggera.
Završena dokumentacijska osnova ne znači završenu Fazu 0 niti odobrenje
produkcijskog releasea.

## Lokalna konsolidacija plana

[Registar zahtjeva](planning/release-1-requirements.md) mapira sve R1 funkcije,
profile, sigurnost i operativne obaveze na
[lokalne radne pakete](planning/release-1-automation-tickets.md).
[A01–A12 matrica](planning/audit-correction-matrix.md) i
[prijedlozi odluka](planning/decision-drafts.md) odvajaju lokalno popravljene
nalaze od discoveryja i novih freigabe. SQL nacrti nisu izvršeni.

R1 plan uključuje zajednički ugovor, odvojene nezavisne pripreme, rani
vertikalni search test, isti lokalni/CI gate, Frischaufbau i upgrade,
Rückschaltung i restore te monitoring prije rollouta. Formalno skraćenje
intervjua i pganalyze čekanja ostaje ENTWURF; postojeći ADR-gateovi važe.
