# Pregled projekta: Supabase CRM MCP

Status: dokumentacijska osnova + PHP-Verdrahtung;
JSON-Filter Entwurf; Bericht-Audit 2026-09-13 abgeschlossen

Ažurirano: 2026-09-13

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
- [Briefing-Intro](planning/briefing-intro.md) je kratki njemački uvod u
  Sachlage: Import, veličina banke, ciljni MCP i trenutni korak.
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
- [Runbook CRM-Suchverdrahtung](runbooks/crm-source-wiring-capture.md)
  vodi mapiranje maske na RPC iz CRM izvornog koda; OrbStack samo kao fallback.
- [Plan CRM-Verdrahtung](runbooks/crm-wiring-human-plan.md) je ljudska
  download-uputa: svaki korak, mjesto, naredba i unos u predložak.
- [Wizards CRM-Verdrahtung](runbooks/crm-wiring-wizards.md) određuje koji
  wizard kada: 01 sken, zatim Codex ili 02, pa 03 abnahme.
- [Predložak CRM-Verdrahtung](discovery/crm-app-wiring.template.md) je prazan
  obrazac.
- [Inventar CRM-Scan 2026-09-13](discovery/crm-work-inventory.md)
  Landkarte: was gemappt ist, wo es liegt, was offen ist.
- [Handoff Scan-to-MCP 2026-09-13](handoffs/2026-09-13-scan-to-mcp.md)
  Historische Session-Übergabe. Nächster Schritt darin veraltet: Entwurf ist geprüft.
- [Aktueller Session-Prompt](handoffs/2026-09-13-aktueller-session-prompt.md)
  Nutzer liest Verdict. Nicht Tool-Namen, nicht MCP.
- [Bericht-Audit Prompt](handoffs/2026-09-13-verify-verifier-report.md)
  Ablauf 2026-09-13 ausgeführt; Vorbericht-PASS nicht haltbar.
- [Codebefund PHP-Filter](discovery/crm-app-wiring.md) je lesart
  `kandidati.php` nakon Wizard 01; Q17 izjednačuje Heft i staru UI.
- [Codebefund Filter-SQL](discovery/crm-filter-sql-codebefund.md) kako
  `lista_kandidata` stvarno filtrira.
- [Codebefund Status/Klick/Cron](discovery/crm-status-codebefund.md) B7
  i Automatik.
- [Codebefund C 4–9 Nachrichten](discovery/crm-notify-codebefund.md)
  Kanal und Auslöser je Wechsel; Produkt default aus.
- [PHP-Suchzettel](discovery/crm-php-hits/) su sirovi rg-ispisi Wizard 01/04.
- [Plan automatizacijskih ticketa](planning/release-1-automation-tickets.md)
  daje blockers-first redoslijed prije zasebne Linear freigabe.
- [SDK integracijski plan](planning/sdk-integration-plan.md) razrađuje MCP,
  Supabase adapter, token granice i provjere; dokumentovani prijedlog nije
  instalacija niti potvrđen stack.
- [Plan statičke schema analize](discovery/schema-analysis-tasklist.md) vodi
  preflight i obradu korisnički dostavljenog izvoza bez bazne konekcije.
- [Supabase tooling](agents/supabase-tooling.md) razdvaja projektne skills,
  razvojni Supabase plugin/MCP i strogo kontrolisani Gate-B put.
- [MCP server-dev tooling](agents/mcp-server-dev-tooling.md) veže službene
  `build-mcp-server` skillove na ADR-0001 i SDK plan; nije scaffold niti
  produkcijski spoj.
- [Tool routing](agents/tool-routing.md) veže Linear, Serena, Git, plugin-e,
  wizards i skills na granice projekta.
- [Issue tracker](agents/issue-tracker.md) čuva Linear identitet i live mapu
  ACT-100–109.
- [Supabase-Plugin Gate P](discovery/supabase-plugin-read-only-gate-draft.md)
  dokumentuje neizvršivi `DRAFT / NO-GO` za mogući alternativni read-only put.
<!-- markdownlint-disable-next-line MD013 -->
- [Evaluacijski gate semantičke pretrage](research/semantic-search-evaluation-gate.md)
  određuje kako se nakon discoveryja porede nevectorski baseline, `pgvector` i
  Vector Buckets bez prethodnog izbora tehnologije.
- [Brief za MCP/TypeScript auto-wire istraživanje](research/mcp-autowire-research-brief.md)
  opisuje bazu, filtere u više nivoa i prompt za pretragu gotovih alata; nije
  nalaz niti stack odluka.
- [Nalaz MCP/TypeScript auto-wire](research/mcp-autowire-candidates.md)
  ocjenjuje gotove MCP/ORM/search alate; nijedan nije siguran runtime Search-MCP.
- [Usporedba tri ispravna puta](research/mcp-autowire-top3-vergleich.md)
  poredi RPC, `gen types`+`.rpc()` i pgtyped bez auto-SQL MCP-a.
- [Verifikacija jezika-do-RPC 2026-09-13](research/2026-09-13-nl-to-rpc-wiring-verification.md)
  potvrđuje JSON-Filter + RPC; ne mijenja naredni korak (Audit-Verdict).
- [Agent-Prompt Suche/Tabellen/Fehler](research/mcp-search-agent-prompt.md)
  copy-paste opis tabela, suchlesarten i grešaka Ausbildung/Beruf/Freitext.
- [Runbook Option 1 Setup](runbooks/option-1-mcp-sdk-rpc-setup.md)
  lokalni eval MCP SDK v2 + Zod + sinteticki Postgres RPC; nije produkcija.
- [End-to-end Runtime-Such-MCP](runbooks/runtime-search-mcp-end-to-end.md)
  povezuje katalog, Jobstep-maske, ugovor, sinteticki MCP i produkcijski
  pilot; nije freigabe niti stack odluka.
- [AGENTS.md](../AGENTS.md) definira pravila rada agenata u repozitoriju.

Ako se dokumenti ne slažu, rad se zaustavlja dok se konflikt ne razriješi
ažuriranjem briefa ili novim ADR-om.

## Trenutno stanje

Raniji [ograničeni Q10.2g audit](reviews/2026-09-11-public-definer-audit.md)
nalazi dvije SECURITY-DEFINER rutine sa PUBLIC EXECUTE, bez PUBLIC schema
USAGE; u tom ranijem pozivu definicije nisu pročitane. Sintetički kontraprimjeri
pokazuju da schema USAGE i promjenjivi read-only default ne dokazuju potpunu
zabranu trajnih upisa. Predložena V3 iznimka je povučena. U tom trenutku
rola još nije bila kreirana. Korisnik je dodatni uski read-only scope
izričito odobrio u Q10.2h;
Q10.2h je sada izvršen. Dvije definicije ostaju NOT_PROVEN_READ_ONLY, a osam
pregledanih LO helper funkcija ima PUBLIC EXECUTE. Detalji i 23 sintetičke
provjere su u [izvještaju](reviews/2026-09-11-public-paths-audit.md).
Q10.2i je zatim omogućio [konkretan plan prava](discovery/public-rights-change-proposal.md):
33 postojeće role, 351 predloženi grant i 11 PUBLIC opoziva. Novi ciklus ima
25 sintetičkih provjera. Sadašnji pristup nema ovlast za osam LO funkcija;
produkcijski paket ostaje tehnički NO-GO. Q10.2j daje korisničku dozvolu za
opisanu promjenu, ali naknadna read-only provjera potvrđuje nepromijenjene
ovlasti. Korisnik trenutno ne treba praviti novog administratora. Q10.2k
potvrđuje: discovery rola se ipak postavlja bez osam LO PUBLIC opoziva; kasnije
učvršćivanje tih osam ciljeva je zaseban put. PostgreSQL PUBLIC EXECUTE na tim
funkcijama ostaje naslijeđeno residualno pravo, ne dokaz da ih nova rola ne
smije izvršiti. Q10.2l potvrđuje: prije kreiranja role prvo se PUBLIC skida
s `TEMPORARY` i dvije Definer funkcije, uz Direktgrants postojećim rolama.
Q10.2m daje Apply-Freigabe za baš ovaj ACL rez. Q10.2c1 prihvaća restore u novo
projekt kao restore-dokaz; in-place produkcijski restore nije zasebno tražen.
Q10.2n je izvršen: Dry-run pa apply za TEMP i dvije Definer funkcije.
PUBLIC TEMP i ta dva EXECUTE više nisu na PUBLIC. Osam LO-EXECUTE ostaje.
Rola `dino_crm_discovery_ro_v1` je kreirana, login radi. Gate B1/B2/B3 V3
kao ta rola su PASS. Sirovi B2/B3 izlaz je izvan Git-a.
Vidi
[pojašnjenje korisnika](discovery/access-plan-consolidated.md#klarstellung-welche-benutzer-sind-erforderlich).
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
Gate B2 V3 pokazuje aditivne embedding tabele ispod 1 MiB bez HNSW/IVFFlat
indeksa, uz naseljenu occupation taksonomiju. To nije izbor vektorskog backenda
niti R1 default; v. [evaluacijski gate](research/semantic-search-evaluation-gate.md)
i Q14 u [ADR-0002](decisions/0002-search-design-interview.md).

Q12/Q13 u ADR-0002 bilježe korisničku namjeru za privilegovani pregled/export i
kasnije generisanje životopisa. Q4 je 2026-09-12 `ERSETZT`: interni Vermittler
vidi cijeli pool i kontakte; Kunde vidi kontakte samo u Einstellungsfreigabe.
Pojmovi User/Superuser nisu razriješeni.

Design intervju o toku pretrage, filterima, potvrdi, historiji i izvozu je u
toku. Njegove potvrđene, djelimične i otvorene odluke vode se u
[ADR-0002](decisions/0002-search-design-interview.md). Entwurf nije produkcijsko
odobrenje niti zamjena za završnu specifikaciju.

Q8.4 potvrđuje osnovni koncept kontrolisanih, ponovo upotrebljivih
Berufssuchprofila. Neekskluzivnost, direktna pretraga zanimanja i neaktivnost
nenavedenih filtera ostaju potvrđeni. Detaljna filtersemantika i obavezna
potvrda
svake nove ili izmijenjene pretrage su VORLÄUFIGER VORSCHLAG zbog nedostajuće
izvorne liste preporuka. Q8.5 je u cijelosti OFFEN. Q4.5 je ukinuta kao prazan
broj, bez rekonstruisanja nepoznatog pitanja. Interni alati vraćaju i
kontakte. CONTACT-02 je Einstellungsfreigabe
kontakata Kupcu nakon zasuge, ne kasnija interna faza. Mogućnosti za
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
navedena brojka od 179 tabela je DURCH DISCOVERY ZU PRÜFEN. Gate B2 V3 vidi 199
relacija u `crm`/`crm_api`/`crm_auth`. Prva mapa imena na domene:
[katalog-domain mapping](discovery/catalog-domain-mapping.md) (Q16).

Lokalni PHP-CRM (`src/crm`) je Wizard-01-skeniran. Formular
`kandidati.php?page=list_ajax` je codebefund Hauptsuche. Filter-SQL
`lista_kandidata` je pročitan:
[crm-filter-sql-codebefund.md](discovery/crm-filter-sql-codebefund.md).
Status-Klicks B7:
[crm-status-codebefund.md](discovery/crm-status-codebefund.md).
Landkarte: [crm-work-inventory.md](discovery/crm-work-inventory.md).
Q17: Heft i stara UI su ravnopravni. Wizard-03-Alltag je potvrđen
(R1 = stara Hauptsuche). Struke/Smjer = Ausbildungsberuf. „5 Jahre“
nije R1-polje. INNER JOIN se ne kopira: bez grupe/obrade ostaju vidljivi.
C 4–9 je pročitan:
[crm-notify-codebefund.md](discovery/crm-notify-codebefund.md).
JSON-Filter Entwurf:
[crm-json-filter-draft.md](discovery/crm-json-filter-draft.md).
Provjeren 2026-09-13 (PHP + Heft). Struke/Smjer = Ausbildungsberuf.
„5 Jahre“ nije R1-polje. INNER JOIN: sichtbar ohne Gruppe/Bearbeitung.
Bericht-Audit: Punkte 1–3 bestätigt. Archiv-Satz bleibt.
Nije korak za imena alata i nije MCP-bau.

Wizard 01 je 2026-09-13 ponovo skenirao **bez** limita 200 linija (RPC 21,
tabele 1732, UI 2487). `*.sql` i `Info/` isključeni zbog dumpa. Ne vraćati
200-kapač.

Q20 (2026-09-13): R1-Suche scanniert Filter, alle Status-Ebenen und
Statuswechsel (Cron und Klicks in `do.php`/`ajax.php`, B7 sehr wichtig).
Benachrichtigungen 4–9 (C) sind als Codebefund gelesen, sehr wichtig,
im Produkt default aus.
Module 11–16 für späteren zweiten MCP; tiefe Scan-Freigabe
dafür steht aus. Punkt 10 DIPL-Erinnerung ist spätere Option, nicht Jetzt-Scan.

Q21 (2026-09-13): PHP scannen für den Funktionskatalog. Umsetzen modern
(JSON-Filter, ADR-0001), nicht 1:1 PHP-SQL nach Supabase. Parität der
Fähigkeiten, nicht der alten Implementierung.

Q22 (2026-09-13): Jetziger Scan = altes Frontend + Businesslogik/Trigger.
occupation / Akten-Jahre / Stadt-Skills-als-Filter sind jetzt nicht Scan-Ziel.

Filter-SQL der Hauptsuche: [crm-filter-sql-codebefund.md](discovery/crm-filter-sql-codebefund.md).

Prije bazne konekcije dozvoljena je statička, lokalna analiza korisnički
dostavljenog schema izvoza nakon sigurnosnog preflighta. Ona može suziti popis
relevantnih objekata, ali ne potvrđuje podatke, RLS, prava, tenant granice,
indekse ili runtime ponašanje.

Prije povezivanja prioritetan je ljudski review oba statička izvještaja. Nakon
njega je pripremljen minimalni B2 scope samo za `crm`, `crm_api` i `crm_auth`;
sve ostale sheme ostaju izvan prvog metadata inventara. B1 V2 ostaje neodobren
postojeći paket, ne automatski sljedeći korak.
Korisnik je potvrdio da nema namjenske discovery role i naložio njenu izradu
(Q10.2b). Izabran je bootstrap nove role; kasnije je kreirana
`dino_crm_discovery_ro_v1` (Gate B1/B2/B3 V3 PASS). Prije izvedbe
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
Gate B1 V3 kao discovery rola je izvršen i PASS. B2/B3
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
