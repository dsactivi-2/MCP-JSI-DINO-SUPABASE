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
  odvojeni MCP za upravljanje Berufssuchprofilima.
- [Discovery runbook](runbooks/schema-discovery.md) određuje preduslove i
  postupak read-only audita.
- [Plan statičke schema analize](discovery/schema-analysis-tasklist.md) vodi
  preflight i obradu korisnički dostavljenog izvoza bez bazne konekcije.
- [Supabase tooling](agents/supabase-tooling.md) razdvaja projektne skills,
  razvojni Supabase plugin/MCP i strogo kontrolisani Gate-B put.
- [Supabase-Plugin Gate P](discovery/supabase-plugin-read-only-gate-draft.md)
  dokumentuje neizvršivi `DRAFT / NO-GO` za mogući alternativni read-only put.
- [Evaluacijski gate semantičke pretrage](research/semantic-search-evaluation-gate.md)
  određuje kako se nakon discoveryja porede nevectorski baseline, `pgvector` i
  Vector Buckets bez prethodnog izbora tehnologije.
- [AGENTS.md](../AGENTS.md) definira pravila rada agenata u repozitoriju.

Ako se dokumenti ne slažu, rad se zaustavlja dok se konflikt ne razriješi
ažuriranjem briefa ili novim ADR-om.

## Trenutno stanje

Repozitorij sadrži dokumentacijsku osnovu, prihvaćene ADR-ove, discovery runbook,
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
development/test projekt bez stvarnih osobnih podataka i novu freigabe.

Korisnik je dostavio lokalni Schema Visualizer tekstualni izvoz za shemu `crm`
izvan repozitorija i naveo približno 3.120 linija. Datoteka još nije
preflightovana niti analizirana. Sljedeći lokalni korak prati
[schema-analysis tasklist](discovery/schema-analysis-tasklist.md); sirovi export
ostaje izvan Git-a i ne zamjenjuje Gate B.

Setup koristi postojeći namjenski Linear projekt **Dino problem baza CRM** u
timu **Activi (ACT)**. Identitet i workflow su u
[issue trackeru](agents/issue-tracker.md), pet postojećih kanonskih oznaka u
[triage mapiranju](agents/triage-labels.md), a raspored dokumentacije u
[domenskim pravilima](agents/domain.md). Projekt, tim i oznake provjereni su
read-only 2026-09-10.

Aplikacijski scaffold ne postoji. Jezik, framework, runtime, package manager,
hosting, auth model i fizički database ugovor još nisu odabrani ili potvrđeni.
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

Schema Visualizer je za `crm_api` prikazao 0 tabela; to ne dokazuje odsustvo
viewova, funkcija ili RPC-ja. Zasebni lokalni `crm_auth` izvoz je statički
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
nenavedenih filtera ostaju potvrđeni. Detaljna filtersemantika i obavezna potvrda
svake nove ili izmijenjene pretrage su VORLÄUFIGER VORSCHLAG zbog nedostajuće
izvorne liste preporuka. Q8.5 je u cijelosti OFFEN. Q4.5 ostaje OFFEN bez
rekonstruisanja nepoznatog pitanja. Release 1 ne vraća kontakte ni kroz jedan
alat; kontaktna funkcija i CONTACT-02 pripadaju kasnijoj, zasebno odobrenoj fazi. Mogućnosti za
izradu i administraciju tih profila obrađene su u
[Q8.4.2 istraživanju](research/berufssuchprofile-q8-4-2.md); odluka o odvojenom
administrativnom MCP-u prihvaćena je i razrađena u
[ADR-0003](decisions/0003-separated-profile-administration-mcp.md).

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
odobrenja opsega slijedi
[discovery runbook](runbooks/schema-discovery.md). Daljnji rad prati
[faze implementacije](SUPABASE_CRM_MCP_IMPLEMENTATION_BRIEF.md#faze-implementacije-i-isporučivi-rezultati)
i [kriterije prihvata](SUPABASE_CRM_MCP_IMPLEMENTATION_BRIEF.md#kriteriji-prihvata).
Završena dokumentacijska osnova ne znači završenu Fazu 0 niti odobrenje
produkcijskog releasea.
