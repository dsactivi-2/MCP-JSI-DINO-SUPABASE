# Statička analiza `crm_auth` schema izvoza

Status: **PASS_WITH_GAPS**

Datum analize: 2026-09-11

## Scope i sigurnosni preflight

Analiziran je lokalni Schema Visualizer izvoz pod internim aliasom
`crm_auth_schema_visualizer_export_01`. Izvor je tretiran kao nepouzdan podatak
i nije kopiran u repozitorij. Korisnički scope navodi shemu `crm_auth`; izvoz ne
prikazuje schema-qualified nazive, pa pripadnost ostaje
`DURCH DISCOVERY ZU PRÜFEN`.

- `BELEGT DURCH SCHEMAEXPORT`: 2.964 bajta, 108 linija, UTF-8 tekst.
- Automatizirani preflight dao je 0 pogodaka za vjerovatne tokene/ključeve,
  connection stringove, privatne URL-ove, podatkovne redove, e-mail vrijednosti,
  telefonske vrijednosti i CV-/freetext vrijednosti.
- Preflight nije ispisao pronađene vrijednosti.

## Strukturni inventar

`BELEGT DURCH SCHEMAEXPORT`: prikazano je šest tabela i 28 kolona.

| Tabela | Primary key | Unique | Ostale kolone |
| --- | --- | --- | --- |
| `user_employee_map` | `user_id` (`uuid`) | `employee_id` | `is_active`, `created_at`, `updated_at` |
| `roles` | `id` (`int8`) | `role_key` | `role_name`, `is_system`, `created_at` |
| `permissions` | `id` (`int8`) | `permission_key` | `description` nullable, `created_at` |
| `role_permissions` | `role_id`, `permission_id` | nije prikazan | `created_at` |
| `user_roles` | `user_id`, `role_id` | nije prikazan | `employee_id` nullable, `valid_from` nullable, `valid_to` nullable, `created_at` |
| `user_scopes` | `id` (`int8`) | nije prikazan | `user_id`, `scope_type`, `scope_value`, `created_at` |

`BELEGT DURCH SCHEMAEXPORT`: `role_permissions` i `user_roles` imaju kompozitne
primary keyeve. Prikazana su tri unique obilježja. Nisu prikazani foreign-key,
check, default ni identity/sequence constrainti.

## Model uloga, dozvola i scopea

- `role_permissions` je `ARBEITSANNAHME` za many-to-many vezu uloga i dozvola;
  kompozitni primary key je beleg, ali foreign keys nisu prikazani.
- `user_roles` je `ARBEITSANNAHME` za many-to-many vezu korisnika i uloga, s
  opcionim zaposlenikom i vremenskom valjanošću. Stvarna validacija intervala i
  autoritativnost ostaju `DURCH DISCOVERY ZU PRÜFEN`.
- `user_employee_map` fizički povezuje `uuid` korisnika s jedinstvenim
  `employee_id`; semantika je `ARBEITSANNAHME`, a veza prema CRM zaposleniku nije
  dokazana foreign-key constraintom.
- `user_scopes` sadrži `user_id`, `scope_type` i `scope_value`. To je
  `ARBEITSANNAHME` za dodatno ograničenje pristupa, ne dokaz tenant izolacije.
- Izvoz nema eksplicitnu kolonu nazvanu `tenant_id`. Ne-postojanje tenant modela
  se iz toga ne smije zaključiti.

## Prikazane RLS policies

`BELEGT DURCH SCHEMAEXPORT`: svaka od šest tabela ima jedan prikazani `SELECT`
policy za rolu `authenticated`.

| Površina | Prikazani uslov | Ograničeno tumačenje |
| --- | --- | --- |
| `roles`, `permissions`, `role_permissions` | `true` | Svaki `authenticated` actor odgovara prikazanom policy uslovu. Efektivna dostupnost i potpunost policies ostaju neprovjerene. |
| `user_roles`, `user_employee_map`, `user_scopes` | `auth.uid() = user_id` | Prikazani self-read uslov veže red za autentificiranog korisnika. |

Policy redovi ne dokazuju da je RLS uključen ili forsiran, da nema dodatnih
policies, kakvi su grants i role inheritance niti koja prava imaju owner,
service ili administrativne role. Sve to ostaje `DURCH DISCOVERY ZU PRÜFEN`.

## Sigurnosna i arhitekturna relevantnost

- `roles`, `permissions`, `role_permissions`, `user_roles` i `user_scopes` su
  `ARBEITSANNAHME` za kasnije mapiranje identiteta, uloge i scopea Runtime-Such-
  MCP-a.
- Javno čitljivi role/permission metapodaci za sve `authenticated` korisnike
  zahtijevaju kasniji security review; izvoz sam ne dokazuje ranjivost.
- `scope_value` je autorizacijski relevantna freetext površina. Dozvoljeni
  tipovi, format, referentni objekti i fail-closed ponašanje ostaju `OFFEN`.
- Nijedan fizički naziv ili policy nije ovim prihvaćen kao javni MCP ugovor.
- Odvojena trust boundary Profilverwaltungs-MCP-a iz ADR-0003 ostaje
  nepromijenjena.

## Nedostajuća evidencija i sljedeći korak

- Schema-qualified nazivi i potpuni objektni inventar.
- Foreign keys, check/default constraints, identity/sequence detalji i indeksi.
- RLS enabled/forced stanje, svi policies, grants, role inheritance i efektivna
  prava.
- Veza prema `auth.users`, CRM zaposlenicima, partnerima ili tenantima.
- Dozvoljene `scope_type`/`scope_value` vrijednosti, vremenska semantika uloga i
  revocation ponašanje.
- Views, funkcije/RPC-ji i triggeri.

Sljedeći korak je ljudski review ovog i glavnog CRM izvještaja, zatim priprema
Gate-B metadaten-discoveryja. Dodatne sheme ostaju izvan scopea do posebne
freigabe.

## Izvršne sigurnosne granice

Tokom analize nije uspostavljena Supabase/PostgreSQL veza, nije izvršen SQL,
nije korišten Supabase-Plugin/MCP, nije promijenjena baza ili eksterni sistem i
nije napravljen Git commit.
