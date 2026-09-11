# MCP i Supabase SDK: provjerena integracijska osnova

Datum provjere: 2026-09-11. Status: istraživanje i preporuka; integracija nije
implementirana, instalirana ni izvršno testirana. Pregled obuhvata javne
primarne izvore i projektne odluke; nema pristupa bazi ili kandidatskim podacima.

## Glavni nalaz i korekcija ranijeg savjeta

Službeni MCP SDK i Supabase biblioteke rješavaju različite zadatke. Prednost
ima mali MCP server s odvojenim auth i podatkovnim adapterima. Supabase server
je kandidat za te adaptere; dodatna middleware kompozicija mora dokazati korist.
To je preporučeni evaluacijski pravac, ne konačan izbor aplikacijskog stacka.

<!-- markdownlint-disable MD013 -->

| Komponenta | Provjereno stanje | Zaključak za projekt |
| --- | --- | --- |
| Službeni MCP TypeScript SDK | README označava v2 kao stabilnu granu uz specifikaciju 2026-07-28; paket za server je `@modelcontextprotocol/server`. | Za novi TS prototip evaluirati v2; raniji naziv `@modelcontextprotocol/sdk` označava v1 i ne smije se miješati s v2 importima. |
| MCP v1 | Dobija bug/security održavanje najmanje šest mjeseci nakon v2 izlaska. | Samo eksplicitno obrazložen compatibility izbor, ne automatski izbor iz starog primjera. |
| `@supabase/server` | Verificira JWT, razrješava API ključeve i stvara Supabase kontekst. | Koristan adapter ako odobreni identitet i downstream credential model odgovaraju; ne zamjenjuje MCP. |
| `@supabase/middleware` | Alpha; kompozicija Fetch handlera i tipiziranog konteksta. | Opcionalan; minimalni MCP put ne zahtijeva ovu dodatnu biblioteku. |
| OpenAI model/Agents SDK | Odvojen sloj od MCP protokola. | Postojeći projektni tok već koristi LLM u MCP klijentu; dodatni serverski modelni poziv nema potvrđen zahtjev. |

Izvori: [službeni MCP README](https://github.com/modelcontextprotocol/typescript-sdk),
[Supabase Server](https://supabase.com/docs/reference/server/introduction) i
[Middleware](https://supabase.com/docs/reference/middleware/introduction),
pročitani 2026-09-11. Zaključak o modelnom SDK-u je projektna procjena prema
[ADR-0001](../decisions/0001-controlled-query-boundary.md).

## Najvažnija sigurnosna praznina: dva tokena i dvije granice

MCP mora provjeriti da je ulazni token izdat baš za njegov resource/audience.
Potpis, važeći Supabase JWT ili uspješan PostgREST poziv sami to ne dokazuju.
Aktuelna MCP specifikacija zahtijeva autorizaciju u svakom HTTP zahtjevu i
zabranjuje prosljeđivanje primljenog MCP tokena upstream API-ju. Za upstream
se koristi zaseban token. [Auth specifikacija](https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization),
[sigurnosne obaveze](https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization/security-considerations).

`withSupabaseClient` samostalno priključuje dolazni Bearer token bez lokalne
verifikacije; PostgREST ga provjerava pri upitu. To je dokumentovano ponašanje
biblioteke, ali nije dovoljan MCP auth dizajn. Njegova kompozabilna površina je
Alpha. [Referenca](https://supabase.com/docs/reference/server/middleware-withsupabaseclient).

Prije implementacije treba odobriti: MCP issuer/resource, identitet korisnika,
scopeove po alatu, njihovo mapiranje na poslovna prava te zaseban način
pribavljanja downstream credentiala koji čuva korisnička ograničenja.
Ne pretpostavljati da Supabase podržava potreban token-exchange tok; to je
`OFFEN`. Ne rješavati nedostatak zajedničkim `service_role`/admin fallbackom.
Dok taj put nije dokazan, kombinacija nema produkcijski GO.

## Minimalno povezivanje bez duplih provjera

Preporučeni redoslijed odgovornosti, koji tek treba potvrditi testom:

1. Transport adapter određuje odobreni protokol, limite i Origin/Host pravila.
2. Jedan sloj objavljuje OAuth metadata/challenge i provjerava ulazni token.
3. Verificirani kontekst zahtjeva daje identitet i scopeove MCP handleru.
4. Poslovni sloj provodi prava, kanonske filtere i strogu validaciju ugovora.
5. Zaseban podatkovni adapter koristi odobreni downstream identitet i samo
   kontrolisane RPC operacije. PostgreSQL provodi prava i filtriranje.
6. Izlazna allowlista ograničava rezultat na najviše 50 kandidata bez kontakata;
   redakcija vrijedi i za greške, tekstualni izlaz i logove.

MCP v2 već nudi `requireBearerAuth`, metadata pomoćnike i predaju `authInfo`
web-standard handleru. Implementacija mora isporučiti vlastiti token verifier;
SDK nije authorization server. To smanjuje potrebu za dodatnim OAuth wrapperom.
[Službeni auth vodič](https://github.com/modelcontextprotocol/typescript-sdk/blob/main/docs/serving/authorization.md).

Supabase `withOAuthProtectedResource` je Alpha metadata/challenge pomoćnik.
Ako se zasebno odabere, ide izvan obaveznog auth gatea radi discoveryja i
preflighta; ne treba istovremeno montirati dva vlasnika istih ruta i challengea.
Sam helper ne dokazuje izdavanje tokena, audience provjeru ili CRM prava.
[Referenca](https://supabase.com/docs/reference/server/middleware-withoauthprotectedresource).

`withRequiredClaims` zahtijeva važeći user JWT; `withClaims` dopušta i zahtjeve
bez tokena. Ne slagati oba niti dodatni claims gate nakon `withSupabase` koji
već daje isti kontekst. Te kompozabilne površine su Alpha, što ne znači da je
cijeli paket `@supabase/server` označen Alpha.
[Claims gate](https://supabase.com/docs/reference/server/middleware-withrequiredclaims).

## Transport i verzije: ne kopirati stare primjere

MCP 2026-07-28 uklanja protokolske sesije i GET stream endpoint. Svaki zahtjev
koristi POST, a odgovor je JSON ili SSE vezan za zahtjev; potrebni su novi
metadata headeri. Zato session-ID, GET i DELETE nisu univerzalni testovi za
novi protokol. Podršku starijim verzijama voditi kao zasebnu compatibility
matricu po klijentu, uz pravila odabranog SDK-a.
[Streamable HTTP](https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/streamable-http).

Preporuka: autentificirani kontekst i downstream klijent izolirati po zahtjevu;
ne mijenjati globalni korisnički token. Poslovnu historiju i paginaciju ne
vezati za MCP sesiju. Ako se podrži stari protokol, sesija nije dokaz identiteta.
To treba dokazati paralelnim sintetičkim pozivima dva korisnika i negativnim
testom zamjene konteksta, nakon definisanja stvarnog auth/tenant ugovora.

Supabase `bufferRequest` kešira body za višestruko čitanje metodama poput
`json()`, dok čitanje sirovog `req.body` zaobilazi taj cache. Ne tretirati to
kao streaming adapter. Provjeriti samo jedno parsiranje, limite prije
bufferiranja, kompatibilnost odabranog MCP handlera, abort/timeout te očuvanje
SSE odgovora kroz middleware i proxy.
[Body model](https://supabase.com/docs/reference/middleware/composition-bufferrequest).

Supabase je za `supabase-js` porodicu završio podršku za Node 20 dana
2026-06-30; ako se odabere Node, potreban je podržani Node 22 ili noviji.
Za `supabase-js` je najavljen TypeScript 5.0+ od 2027-01-31. Izbor mora pratiti
presjek podržanih runtima svih odabranih paketa, ne minimum jednog tutoriala.
[Node obavijest, 2026-05-08](https://supabase.com/changelog/45715-deprecation-notice-dropping-support-for-node-js-20),
[TypeScript obavijest](https://supabase.com/changelog/47812-deprecation-notice-supabase-supabase-js-will-require-typescript-5-0).

Tačni patch brojevi, peer dependencies, lockfile i sigurnosni status još nisu
provjereni instalacijom. Ne unositi izmišljene verzije; prije scaffolda
zabilježiti paket, tačnu verziju, runtime, MCP wire verziju i testirane klijente.

## Obavezni dokazi i optimizacije

| Prioritet | Potreban dokaz / naredni korak |
| --- | --- |
| P0 | Token s pogrešnim issuerom/audienceom, bez scopea ili istekao token ne dolazi do RPC-ja; metadata/preflight ostaju dostupni. |
| P0 | Nema token passthrougha, admin fallbacka ni identiteta uzetog iz korisničkog filtera; downstream čuva prava. |
| P0 | Paralelni pozivi ne miješaju identitete; cross-tenant negativni test nastaje tek iz odobrenog tenant modela. |
| P0 | Svaki alat i izlazni kanal poštuje svoj limit: search najviše 50 kandidata, profile jedan dozvoljeni zapis, options zasebno ograničena lista pojmova; greške i svi izlazi ostaju bez kontakata. |
| P1 | Tačna SDK/protokol/runtime/klijent matrica; nepoznata ili nepodržana verzija odbijena predvidljivo. |
| P1 | JSON/SSE, body limit, Origin, timeout, cancellation i headeri prolaze izabrani proxy/hosting; OAuth metadata nema route konflikt. |
| P1 | Jedan token verifier i jedan vlasnik OAuth odgovora; tipizirani mali adapter umjesto više preklopljenih wrappera. |
| P2 | Korist dodatne Alpha pipeline mjeriti složenošću, latencijom i testovima; zadržati samo ako pojednostavljuje sistem. |

Prvih P0 dokaza nema; tabela je plan provjere. SDK prisutnost ili prolaz
TypeScript kompilacije ne znače da su prava, RPC ili RLS implementirani.
Cache, replike, embeddings i dodatni workflow servisi i dalje čekaju mjerljivu
potrebu prema [ADR-0004](../decisions/0004-automated-database-development.md).

## Granice i verifikacijske praznine

Ovaj nalaz ne mijenja [ADR-0001](../decisions/0001-controlled-query-boundary.md),
[ADR-0003](../decisions/0003-separated-profile-administration-mcp.md) ni
[ADR-0004](../decisions/0004-automated-database-development.md). Profilna
administracija zadržava zasebne identitete, prava, deployment i objavu verzija.
Developer Supabase MCP ostaje odvojen od planiranog runtimea i ne dobija
produkcijski pristup. Schema, auth model i intervju nisu ovim završeni.

`changelog.md` nije dohvaćen: web parser odbio je Markdown content type, a
lokalni curl nije razriješio DNS. Pročitan je službeni HTML
[changelog](https://supabase.com/changelog) i povezane runtime obavijesti.
Nisu testirani paketni API-ji, login, RPC, RLS, performanse, deployment niti
kompatibilnost klijenata. Izvještaj dokumentuje provjerene javne činjenice i
preporuke; ne tvrdi da biblioteke već besprijekorno rade zajedno.

<!-- markdownlint-enable MD013 -->
