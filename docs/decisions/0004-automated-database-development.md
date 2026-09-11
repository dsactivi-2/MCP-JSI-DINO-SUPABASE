# ADR-0004: Automatizirani razvoj i optimizacija baze

Datum: 2026-09-11

Status: Prihvaćeno

## Kontekst

Prihvaćeni dizajn zahtijeva kontrolisanu PostgreSQL RPC granicu, strogi JSON
ugovor i aditivni Release-1 sloj. Ručno pisanje i ponavljanje migracija,
RLS/RPC testova, lintanja, planova upita i release provjera povećalo bi trajanje
svake promjene i rizik od različitih rezultata između okruženja.

Primarne reference i poređenje alata nalaze se u
<!-- markdownlint-disable-next-line MD013 -->
[istraživanju optimalnog puta](../research/optimaler-sql-und-automatisierungsweg.md)
<!-- markdownlint-disable-next-line MD013 -->
i [verifikaciji minimalnog stacka](../research/werkzeugempfehlung-verifikation-ohne-umbau.md).
Korisnik je 2026-09-11 prihvatio novi plan kao osnovu za ažuriranje projekta.

## Odluka

Projekt uvodi automatiziranu, Supabase-native razvojnu i verifikacijsku
putanju čim discovery, ugovor i aplikacijski scaffold omoguće reproducibilno
izvršenje:

1. Supabase CLI i lokalna baza sa sintetičkim seedovima predstavljaju
   ponovljivo razvojno okruženje.
2. Svaka promjena baze je mala, aditivna i verzionirana migracija.
3. Automatski gate izvršava obnovu lokalne baze, SQL lint, pgTAP testove za
   strukturu, grantove, RLS i RPC, MCP contract testove te provjeru generiranih
   tipova kada ih odabrani stack koristi.
4. Kontrolisani `EXPLAIN` testovi, Supabase Advisors, `index_advisor` i
   `pg_stat_statements` vode optimizaciju na osnovu dokaza.
5. AI Assistant ili lokalni coding agent smije pisati SQL, migracije i testove
   samo kao preglediv prijedlog. Njegov izlaz nema pravo automatskog applyja.
6. Produkcijski apply ostaje odvojena akcija nakon uspješnog dry-runa,
   pregleda i izričite freigabe. Nakon applyja slijede health, contract, RLS i
   performance provjere.

Runtime granica iz [ADR-0001](0001-controlled-query-boundary.md) ostaje
nepromijenjena: korisnički tekst nikada se ne pretvara u proizvoljni SQL za
izvršenje. Ova odluka automatizira razvojni proces, ne širi produkcijski MCP.

## Izbor dodatnih alata

- pganalyze se razmatra tek nakon četiri do osam sedmica reprezentativnog
  workload-a i zadržava samo ako mjerljivo štedi više vremena od ugrađenih
  Supabase/PostgreSQL izvještaja.
- pgMustard je opcionalna pomoć za pojedinačne složene planove.
- Supabase Cron ima prednost za male DB-interne rasporede. n8n se koristi samo
  za vanjske obavijesti i odobrene prateće procese, ne za search ili migracije.
- Bytebase se ponovo razmatra tek kod većeg tima, više baza ili čestih
  produkcijskih migracija.
- InsightBase može imati zaseban BI POC, ali ne zamjenjuje JSON validator,
  kontrolisanu RPC ili release gate.
- Readyset, Zero, Electric, cache, replika i eksterni search ostaju iza
  mjerljivog performance ili UI triggera.

## Posljedice

Početni scaffold dobija dodatni trošak za lokalnu bazu, seedove, testove i CI.
Nakon toga se smanjuju ponovljivi ručni rad, regresije i vrijeme dijagnostike.
Discovery, poslovne odluke, auth/tenant model, numerički SLO-i i produkcijska
freigabe ne mogu se automatizirati ovom odlukom i ostaju zasebni gateovi.

Komande se ne upisuju kao projektni standard dok odabrani stack i scaffold ne
dokažu da su reproduktivne. Prema auditu od 2026-09-11 Supabase CLI je blokiran
sandbox zabrannom
telemetrijskog pisanja; to ne dokazuje neispravnu instalaciju. Promptfoo ima
zaseban `better-sqlite3` ABI-konflikt. Oba zahtijevaju zasebnu dijagnostiku
(ENV-01/02) i ponovnu provjeru prije obavezne gate upotrebe. Ovo je korekcija
vremenski vezanog tehničkog statusa, bez promjene prihvaćenog razvojnog pravca.

## Verifikacija odluke

Odluka je provedena samo ako:

- jedan lokalni ili CI tok reproducibilno gradi bazu iz verzioniranih migracija;
- negativni RLS, privilege i RPC testovi padaju kada se zaštita namjerno ukloni;
- AI-generirana izmjena ne može zaobići review i produkcijski apply gate;
- svaki prihvaćeni indeks ili query rewrite ima ponovljiv prije/poslije dokaz;
- monitoring samo predlaže ili alarmira i ne mijenja produkciju;
- dodatni alat ulazi tek nakon dokumentovanog triggera i izlaznog kriterija.
