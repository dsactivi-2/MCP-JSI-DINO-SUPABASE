# ADR-0001: Kontrolisana granica između LLM-a i PostgreSQL-a

Datum: 2026-09-10

Status: Prihvaćeno

## Kontekst

CRM s približno 200.000 kandidata mora omogućiti višejezično pretraživanje kroz
MCP klijente. Broj kandidata je projektna procjena, DURCH DISCOVERY ZU PRÜFEN;
prihvaćena arhitekturna odluka ne predstavlja audit stvarnog broja zapisa.
Slanje cijele baze modelu stvara neprihvatljive rizike za
privatnost, trošak, latenciju i tačnost. Slobodno generirani SQL može zaobići
sigurnosne kontrole, otkriti osjetljive podatke ili proizvesti skupe upite.

## Razmotrene mogućnosti

1. Slati veliki skup kandidata LLM-u i filtrirati u kontekstu modela.
2. Dopustiti LLM-u da generira i izvršava SQL.
3. Ograničiti LLM na strukturiranje namjere, a izvršavanje prepustiti
   kontrolisanoj PostgreSQL RPC granici.

## Odluka

Prihvaćena je treća mogućnost.

LLM smije proizvesti samo mali JSON filter koji prolazi strogu shematsku i
poslovnu validaciju. MCP primjenjuje identitet, autorizaciju, allowliste, limite
i timeout te poziva unaprijed definiranu PostgreSQL RPC funkciju.

PostgreSQL autoritativno filtrira, rangira i paginira rezultate. Osnovni search
vraća najviše 50 kandidata po stranici, stabilne identifikatore i dokaz
poklapanja. Projekcija polja ovisi o akteru: interni Vermittler vidi i kontakte;
Kunde vidi kontakte samo nakon Einstellungsfreigabe.

Fizički view, RPC potpis, auth model, tenant mapiranje i ranking formula bit će
odlučeni tek nakon read-only audita stvarne sheme.

## Posljedice

Pozitivne posljedice:

- baza provodi sigurnost i determinističko filtriranje;
- količina podataka poslana modelu ostaje ograničena;
- rezultati se mogu objasniti i auditirati;
- MCP ugovor ostaje prenosiv između različitih klijenata.

Troškovi i ograničenja:

- potreban je kanonski model i održavana višejezična taksonomija;
- svaka promjena ugovora zahtijeva verzioniranje i compatibility test;
- potrebni su RLS, contract, injection, pagination i performance testovi;
- nejasni korisnički zahtjevi moraju izazvati pojašnjenje.

## Verifikacija

Razvojna automatizacija ove granice definirana je u
[ADR-0004](0004-automated-database-development.md). AI može pripremati SQL diff,
ali nijedan runtime ili produkcijski apply put ne smije zaobići ovu odluku.

Odluka je ispravno provedena samo ako:

- runtime ne sadrži putanju za proizvoljni SQL;
- nepoznata JSON polja i vrijednosti izvan granica budu odbijeni;
- RLS negativni testovi sprečavaju cross-tenant pristup;
- search nikada ne vraća više od 50 kandidata;
- nula rezultata ostaje nula bez izmišljenih profila;
- kontaktni podaci zahtijevaju zasebnu autorizaciju po akteru (interni pool
  s kontaktima; Kunde tek nakon Einstellungsfreigabe);
- isti ugovor prolazi test u svakom podržanom MCP klijentu.
