# Registar zahtjeva Releasea 1

Datum: 2026-09-11. Status: lokalna specifikacija rada, bez implementacije.

## Izvori i odgovornost

Oznake Q upućuju na [ADR-0002](../decisions/0002-search-design-interview.md).
<!-- markdownlint-disable-next-line MD013 -->
MH znači Must-have odjeljak [briefa](../SUPABASE_CRM_MCP_IMPLEMENTATION_BRIEF.md).
<!-- markdownlint-disable-next-line MD013 -->
Arhitekturni izvori su [ADR-0001](../decisions/0001-controlled-query-boundary.md),
[ADR-0003](../decisions/0003-separated-profile-administration-mcp.md) i
[ADR-0004](../decisions/0004-automated-database-development.md).
A oznake upućuju na [korekcijsku matricu](audit-correction-matrix.md).

Korisnik trenutno nosi sve navedene odgovorne uloge prema Q3; konkretni RACI i
operativni procesi ostaju otvoreni. Agent je izvršilac lokalne pripreme, ne
vlasnik poslovnog odobrenja. Radni paketi, artefakti i blokatori su u
[planu](release-1-automation-tickets.md). Svi R1 redovi su NEIMPLEMENTIRANI;
„obavezno” označava release kriterij, a ne završenu ili fizički dokazanu
funkciju.

REQ-*su zahtjevi; AUTO-*/DISC-*/ostali ključevi su lokalni paketi, bez Linear
ID-ova. TEST-AUTO-* i postojeći ID-ovi u briefu su test-scenariji. Kriteriji bez
starog test-ID-a imaju stabilnu REQ-ID kao identitet acceptance slučaja.
Fachliche Sollwerte nastaju iz potvrđenih pravila i ručno pregledanih primjera,
nezavisno od generiranih validatora i implementacije.

## SDK razrada postojećih kriterija

[SDK integracijski plan](sdk-integration-plan.md) povezuje provjerene SDK
mogućnosti s postojećim auth, contract, transport i runtime granicama.
SDK-01–08 su planirani testovi, ne izvršena evidencija. Izbor konkretne
biblioteke ostaje OFFEN u AUTO-02; sigurnosni kriteriji vrijede i za alternativni
adapter. Dodatni middleware nije obavezan proizvod.

## Jedinstveni release status i provjerljiva abnahme

Dugi redovi su namjerno tabelarni radi potpunog mappinga.

<!-- markdownlint-disable MD013 -->

| ID | Release / obaveza | Izvor | Odgovorna uloga | Radni paket | Zavisnosti | Provjerljiv kriterij / evidencija |
| --- | --- | --- | --- | --- | --- | --- |
| REQ-GOV-01 | R1 preduslov | Q3, Q5, Q6, Q9 | Product/Security/Privacy | GOV-01 | nema | Vlasnik potvrđuje samo discovery-svrhu, pristupni/privacy scope, izvršioca i rizik jedne osobe; bez novih poslovnih odluka prije discoveryja. Release-pravni osnov, dob i RACI slijede DEC-01/PRIV-01. |
| REQ-DISC-01 | R1 preduslov | Q9, Q10.2a; A01 | Operations/Security | DISC-01 | GOV-01 | Bootstrap evidencija, odgovorni akter i zaseban restore put su pregledani; bez toga NO-GO. |
| REQ-DISC-02 | R1 preduslov | Q10.2a; A02 | Operations/Security | DISC-02 | DISC-01 | Sintetički setup: tačna rola/CONNECT; pogrešno ciljanje i PUBLIC prava prekidaju cijelu transakciju; rollback uklanja samo vlastiti grant/rolu, nepoznata zavisnost ostavlja stanje neizmijenjeno. |
| REQ-DISC-03 | R1 preduslov | Q9; A05 | Security/Discovery | DISC-03 | DISC-01; DISC-02 samo za novu rolu | B1 verzija odgovara identitetu; target/hash/time/retention provjereni, jedan pokušaj; fake negativni slučajevi i stvarni pregledani B1 PASS. |
| REQ-DISC-04 | R1 preduslov | Q9; A03, A06 | Discovery/Security | DISC-04 | DISC-03 | B2 inventar sa per-query coverage, markerima, manifestom i zasebnom freigabe; 5001 red ili nepotpuna vidljivost ne daje potpun PASS. |
| REQ-DISC-05 | R1 preduslov | Q9; A06 | Discovery/Security | DISC-05 | DISC-04 | Objektno odobrene definicije: PUBLIC policies, view security, routine body/config; zaseban output/launcher gate; bez tajni u redigiranom nalazu. |
| REQ-DISC-06 | R1 preduslov | Brief MH1; Q9 | Data/Discovery | DISC-06 | DISC-04, DISC-05 | Agregati missing/format/duplikat/stale/konflikt/izvedeno i planski baseline imaju tačan scope, redakciju, budžet i vlastita odobrenja; procjene odvojene od tačnog broja. |
| REQ-MODEL-01 | R1 obavezno | Brief MH2; Q10.3 | Data | DATA-01 | AUTO-02 | Odobren data dictionary, izvor-cilj mapping, ID kontinuitet, lineage, svježina i unknown; svaka A struktura je D-kompatibilna, import se ne mijenja. |
| REQ-TAX-01 | R1 obavezno | Brief MH2; Q8.4 | Data/Product | TAX-01 | DATA-01 | B/H/S-DE-EN ID/naziv/sinonim/odobrenje/vlasnik/verzija; samo odobreni sinonimi ekvivalentni; dvosmislenost traži pojašnjenje (LANG-02, TYPO-01, AMB-01). |
| REQ-PROF-01 | R1 obavezno | ADR-0003; Q8.4.2 | Data/Product | TAX-01 | DATA-01 | Verzionirani neekskluzivni profili odvajaju tri kategorije; isti pojam pripada dvama profilima i ostaje direktno pretraživ; brisanje članstva ne mijenja druge profile. |
| REQ-CONTRACT-01 | R1 obavezno | ADR-0001/0004; Brief MH4 | Product/Security | AUTO-02, AUTO-05 | DEC-01 | Jedan odobren input/output/error/cursor ugovor izvodi sheme, validatore i tipove; drift blokira CI; unknown field/type/range/ID se odbija (SCHEMA-01, RANGE-01, CON-01). |
| REQ-SDK-01 | R1 integracija; biblioteke OFFEN | Q11; SDK plan; ADR-0001/0004 | Security/Operations | AUTO-02, AUTO-03, AUTH-01, AUTO-05, OPS-01, CLIENT-01, REL-01 | DEC-01; odobren stack i scaffold | SDK-01/05/08: usklađene SDK/protokol/runtime verzije, lockfile i alpha odluka; stvarni HTTP/proxy test, upgrade/povratak i podržani klijenti. V1/v2 importi i legacy/novi transport ne miješaju se. |
| REQ-FILTER-01 | R1 obavezno; detalji OFFEN | Q5, Q8, Q8.5; Brief MH2.1 | Product/Privacy | SEARCH-02 | SEARCH-01, DEC-01 | Dob/ref-datum, iskustvo, zanimanja, aktivnosti, lokacija, jezici, vještine, dostupnost, svježina i text prema odobrenom ugovoru; uključene/isključene granične vrijednosti nezavisno provjerene. Q8.5 se ne pretpostavlja. |
| REQ-FILTER-02 | R1 obavezno | Q8 potvrđeni dio | Product | SEARCH-02 | SEARCH-01 | Izostavljeno ostaje neaktivno; iskustvo ne aktivira Ausbildung; L-OMIT-01 nikad ne dodaje dob ili jezik. |
| REQ-FILTER-03 | R1 obavezno | Q7; ADR-0001 | Product | SEARCH-02 | SEARCH-01 | ZERO-01: tačno nula i prijedlog; bez nove pretrage dok korisnik ne potvrdi konkretnu promjenu. Opća potvrda ostaje prijedlog. |
| REQ-LANG-01 | R1 obavezno | Brief MH9; A04 | Product/Data | SEARCH-02 | TAX-01, AUTO-05 | L-BS/DE/EN-01 imaju isti nezavisni poslovni oracle; dijakritika, padeži, složenice, skraćenice i greške daju odobren rezultat/pojašnjenje. |
| REQ-SEARCH-01 | R1 obavezno | ADR-0001; Brief MH3/5 | Data/Security | SEARCH-01 | DATA-01, AUTH-01, AUTO-04, AUTO-05 | Prvi vertikalni slučaj ide validator → autorizacija → RPC → DB filter/rank → MCP izlaz. Nema proizvoljnog SQL-a ni masovnog učitavanja; SQLI-01 ostaje vrijednost. |
| REQ-SEARCH-02 | R1 obavezno | Brief MH5/7 | Data/Product | SEARCH-02 | SEARCH-01 | Svaki vraćeni ID postoji; matched_fields i match_type su tačni, nedostajuće je null/unknown; hard cap 50 i bajtni limit (RANGE-01, ZERO-01). |
| REQ-RANK-01 | R1 obavezno | ADR-0001; Brief acceptance | Product/Data | SEARCH-02 | DEC-01, SEARCH-01 | Odobrena DB ranking formula i jedinstveni tie-breaker daju očekivani poredak i pri jednakom scoreu; nema runtime LLM prerangiranja. |
| REQ-PAGE-01 | R1 obavezno | Brief acceptance | Data/Security | SEARCH-02 | SEARCH-01 | PAGE-01/CURSOR-02: duboke stranice bez velikog OFFSET-a, potpis/version/filter/sort/tenant veze; manipulacija i promjena konteksta odbijeni; snapshot garancija dokumentovana. |
| REQ-TOOL-02 | R1 obavezno | Brief MH3 | Security/Product | TOOL-02 | DATA-01, AUTH-01, AUTO-05 | get_candidate_profile vraća jedan dozvoljeni profil, sigurno tretira nepostojeći/tuđi ID i nema kontakata ni u tekstualnom fallbacku (RLS-01, CONTACT-R1). |
| REQ-TOOL-03 | R1 obavezno | Brief MH3 | Data/Product | TOOL-03 | TAX-01, AUTH-01, AUTO-05 | get_filter_options ograničeno razrješava dozvoljeno polje, query, pojmove i profile; bez kandidatskih podataka, SQL identifikatora i neograničenih lista. |
| REQ-AUTH-01 | R1 obavezno; model OFFEN | ADR-0001; Brief MH6 | Security | AUTH-01 | AUTO-02, AUTO-03 | SDK-02/03: svaki poziv validira identitet, issuer, MCP audience i svrhu; tuđi/istekli token i nedozvoljeni scope odbijeni. Downstream credential je zasebno odobren, bez MCP token passthrougha. Tenant/rola dolaze iz potvrđenog modela, a paralelni zahtjevi ne dijele korisnički kontekst. |
| REQ-AUTH-02 | R1 obavezno | ADR-0001/0003; Brief MH6 | Security | AUTH-02 | AUTH-01, DATA-01, AUTO-04 | Negativni DB testovi rola/tenant/kolona/routine/view i PUBLIC prava; bez owner/superuser/BYPASSRLS/migration prava u runtimeu (RLS-01, ROLE-01). |
| REQ-CONTACT-01 | R1 obavezno | Q4; Brief acceptance | Privacy/Security | AUTH-02, CLIENT-01 | AUTH-01 | CONTACT-R1 na svim alatima, strukturiranom/tekst izlazu, greškama, logovima i promptima: nijedna rola ne dobija kontakte. |
| REQ-LIMIT-01 | R1 obavezno | Brief MH6/9 | Operations/Security | OPS-01 | AUTO-03, AUTO-05 | Per-user/tenant/client rate, globalni backpressure, concurrency, request/response size, timeout i cancel negativni testovi; jedan kvar ne ostavlja DB upit aktivnim (PERF-02, LOAD-01). |
| REQ-TRANSPORT-01 | R1 obavezno | Brief MH6 | Security/Operations | AUTH-01, OPS-01, OPS-02 | AUTO-02, AUTO-03 | TLS za svaki mrežni put; nevažeći certifikat i plaintext pristup odbijeni. Tajne samo u odobrenom secret sistemu, nikad u klijentu/promptu/logu/repozitoriju; sintetički secret-canary ne procuri. |
| REQ-ACCESS-REV-01 | R1 obavezno | Brief MH6 | Security/Operations | AUTH-02, AUTO-07 | AUTH-01, OPS-02 | Prije rollouta definiran period, vlasnik i dokaz redovne revizije grantova, RLS testova, ključeva i pristupnih logova; kontrolni drift izaziva pregled. Rotacija/ukidanje pristupa imaju poseban odobren postupak, bez automatske mutacije. |
| REQ-INJECT-01 | R1 obavezno | ADR-0001; Brief MH7 | Security | AUTO-05, AUTH-02 | AUTO-02 | SQLI-01 i PI-01 kroz korisnički input, cursor i spremljeni tekst/CV; encoding i citirani podaci ne mijenjaju alat, prava ili filter. |
| REQ-ADMIN-01 | R1 obavezno | ADR-0003 | Security/Operations | ADMIN-01 | AUTO-02, AUTO-03, AUTO-05 | Odvojene identitete, prava, deploy, audit i rollback testirati; runtime ne može pozvati write; male tipizirane operacije s očekivanom verzijom odbijaju stale write. |
| REQ-ADMIN-02 | R1 obavezno | ADR-0003 | Product/Data | ADMIN-02 | ADMIN-01, TAX-01, AUTO-04 | Kreiranje/čitanje nacrta i verzija, pretraga pojmova, ručno članstvo i korekcije, višejezični aliasi; dvosmislen alias/kontradikcija odbijeni server-side. |
| REQ-ADMIN-03 | R1 obavezno | ADR-0003 | Product/Data | ADMIN-02 | ADMIN-01 | Poluautomatski članstvo/alias prijedlog čuva izvor, razlog i confidence; nema automatske objave ili kopiranja kandidata/CV; preview samo minimizirani agregati. |
| REQ-ADMIN-04 | R1 obavezno | ADR-0003 | Product/Security | ADMIN-03 | ADMIN-02 | Potpun diff i validacija, zasebna potvrda tačne verzije; nepromjenjiva objava, zamjena/reaktivacija/arhiva bez nekontrolisanog brisanja; audit akter/vrijeme/razlog/verzija. |
| REQ-ADMIN-05 | R1 obavezno | ADR-0003 | Product/Data | ADMIN-03, SEARCH-02 | ADMIN-02, SEARCH-01 | Runtime čita samo objavljeno; promjena aktivnog profila ne mijenja postojeću verzijsku vezu/filter i ne prenosi raniju potvrdu na novi diff. |
| REQ-PRIV-01 | R1 obavezno | Brief MH8 | Privacy/Data | PRIV-01 | GOV-01, AUTO-02 | Dokumentovan retention, pristup, ispravka, brisanje, purpose/consent ograničenje i pravni/DPIA zaključak prema potrebi; zakonito obrisan kandidat nestaje iz svih prisutnih slojeva (DEL-01). |
| REQ-PRIV-03 | R1 obavezno | Brief MH8 i rizici | Product/Privacy | PRIV-01, CLIENT-01 | GOV-01, AUTO-02 | UI/klijentski tok čuva ljudsku procjenu prije odluke sa značajnim uticajem na kandidata; search/rank ne donosi automatsko odbijanje. Pregled test-scenarija i quality/fairness pokrivenosti je dokumentovan, bez izvedenih zaštićenih osobina. |
| REQ-PRIV-02 | R1 obavezno | Brief MH8/operations | Privacy/Operations | OPS-02 | AUTO-03, AUTO-05 | Log/trace/audit imaju correlation, verziju i minimizirani actor/filter signal; bez tajni, DOB, kontakata ili punog CV; retencija i pristup provjereni. |
| REQ-AUTO-01 | R1 obavezno | ADR-0004 | Operations | AUTO-03 | AUTO-02, ENV-01 | Reproducibilna lokalna sintetička baza, bez produkcijskih credentiala; pinovani alati/images i stvarne DB/extension sposobnosti (TEST-AUTO-01). |
| REQ-AUTO-02 | R1 obavezno | ADR-0004; A09 | Data/Security | AUTO-04 | AUTO-03 | Jedan lokalni/CI gate: lint s nonzero pragom, pgTAP, grants/RLS/RPC; negativni kontrolni kvar mora blokirati. Frischaufbau i upgrade iz prethodne verzije odvojeni (TEST-AUTO-02, MIG-01). |
| REQ-AUTO-03 | R1 obavezno | ADR-0004 | Security | AUTO-05 | AUTO-02, AUTO-03 | AI samo pregledljiv diff; contract i generirani artefakti provjereni; production apply nema automatsku putanju (TEST-AUTO-02/03). |
| REQ-PERF-01 | R1 obavezno | Brief MH9; ADR-0004 | Operations/Data | AUTO-06 | SEARCH-02, TOOL-02, TOOL-03, ADMIN-03, AUTH-02, OPS-01 | Selektivan/najširi query, concurrency i soak prolaze unaprijed odobrene numeričke p50/p95/p99/timeout/throughput/error/resource/cost ciljeve; reprezentativni volumen je mjeren, ne pretpostavljen (PERF-01/02, LOAD-01). |
| REQ-INDEX-01 | R1 obavezno | ADR-0004; Brief MH5 | Data | AUTO-06 | DATA-01, SEARCH-01 | Svaki indeks/query rewrite ima prije/poslije plan, read/write trošak, veličinu i odluku; Advisor sam ne primjenjuje ništa (TEST-AUTO-03). |
| REQ-OPS-01 | R1 obavezno | Brief operations/rollout | Operations | AUTO-07 | OPS-01, OPS-02, AUTO-06 | Prije rollouta readiness/liveness, dashboardi, threshold alarm i incident/on-call/mitigation put su testirani; MON-01 daje signal bez automatske mutacije. |
| REQ-RESTORE-01 | R1 obavezno | Q10.2a; Brief rollout | Operations/Data | OPS-03 | AUTO-04, GOV-01 | Zasebni dokaz restorea prema odobrenom putu, integritet, RTO/RPO; DB i eventualni Storage obuhvat jasno odvojeni; postojeći backup nije dokaz. |
| REQ-CLIENT-01 | R1 obavezno | ADR-0001; Brief acceptance | Product/Security | CLIENT-01 | SEARCH-02, TOOL-02, TOOL-03, AUTH-02, OPS-01 | ChatGPT, Claude, Codex, Grok i referentni klijent: tool schema/outputSchema/structuredContent/text, auth, cursor, greške, timeout i razumljiva/pristupačna pojašnjenja; CLIENT-01 bez kritičnih razlika. |
| REQ-RELEASE-01 | R1 obavezno | Q10.2a; ADR-0004 | Operations/Security/Product | REL-01 | AUTO-06, AUTO-07, CLIENT-01, PRIV-01, OPS-03, ADMIN-03 | Go/no-go artefakt za svaki R1 red; dry-run lista, lokalna migracijska proba, kompatibilna prethodna RPC/aplikacija i restore odvojeno dokazani; tačan diff/target posebno odobren, post-check pa tek sljedeći rez. |
| REQ-D-01 | Kasnije; R1 kompatibilnost obavezna | Q10.3 | Data/Operations | MIG-D-01 | REL-01 | Svaki naredni D rez ima mapping, lineage, reconciliation, RLS/contract, cutover i rollback; izvor se ne uklanja u istom rezu. |
| REQ-OPT-01 | Kasnije, zasebno odobrenje | Q4; Brief opcije | Product/Privacy | OPT-01 | DEC-01; nova freigabe | CONTACT-02, export, historija/saved searches i notifikacije ostaju izvan R1; svaki dobija scope, prava, retenciju, limite i test prije aktivacije. |
| REQ-OPT-02 | Opcionalno nakon dokaza | ADR-0004; semantic gate | Data/Operations | AUTO-08, OPT-02 | AUTO-07; reprezentativni workload | Native baseline prvo; pganalyze trenutno tek 4–8 sedmica i dokaz koristi. Vektori/cache/replika/search servisi samo iza potrebe, budžeta, lifecycle i rollback testa; nema R1 blokera samom dostupnošću. |

<!-- markdownlint-enable MD013 -->

## Otvoreni ugovor nije implementacijska sloboda

Q8.5 je potpuno OFFEN. Q4.5 nema rekonstruisanu formulaciju. Opća potvrda
pretrage i detaljni operatori ostaju VORLÄUFIGER VORSCHLAG, a Q7 ostaje
obavezan.
DEC-01 mora te statuse razriješiti prije zavisne implementacije. Registar ne
pretvara JSON primjer, predloženi tip indeksa ili postojeći naziv u dokaz sheme.

Obavezni su rezultat pretrage, sigurnost, stabilan cursor, DB ranking,
verzioniranje, sigurne greške, observability i sintetički testni skup. Izbor
FTS/trigram indeksa, cachea ili eksternog servisa zavisi od dokaza; nije zaseban
obavezni R1 proizvod. LLM reranking nije odobren runtime put prema ADR-0001.

Kontakt, export i vektori imaju odvojene kasnije pakete. Njihovo tehničko
razvijanje nije R1 zavisnost; formalno razdvajanje interview frontier-a ostaje
samo [ENTWURF E-01](decision-drafts.md) do izričite odluke.
