<!-- markdownlint-disable MD013 -->
# CRM-Suchverdrahtung

Stand: 2026-09-12

Status: ENTWURF — Codebefund nach Wizard 01. Formularfelder der alten
Filter-UI aus PHP. Filter-SQL von `lista_kandidata` ist gelesen:
[crm-filter-sql-codebefund.md](crm-filter-sql-codebefund.md).
Keine Kandidatenzeilen kopiert.

Quellenrang (ADR-0002 Q17): Heft und alte UI sind gleichberechtigt. Dieser
Befund schließt keine Heft-Ziele aus und wird nicht verworfen, nur weil ein
Feld in älteren Q8-Fragen fehlte.

Suchzettel (nicht abschreiben): [crm-php-hits/](crm-php-hits/).

Rohzettel-Stand 2026-09-13 ohne 200-Deckel: RPC 21, Tabellen-Fundstellen 1732,
UI-Fundstellen 2487 (Code-Treffer, keine Postgres-Tabellen). Grobes
`rg kandidati.php`: 171 / 152; davon `src/crm/kandidati.php` 58 / 49.
`*.sql`/`Info/` ausgeschlossen.

CRM-Pfad: /Users/activi/Downloads/crm-master-3/src/crm

Stack: php (Legacy, ohne composer.json)

Git-Revision CRM: e9ec9e0 (aus Wizard-Zustand)

Datenbank in diesem Lauf: keine

## 1. Suchmasken

| Maske (UI-Name) | Datei / Symbol | Ruft | Kontakte im Ergebnis | Note |
| --- | --- | --- | --- | --- |
| Kandidati → Filter (`page=list_ajax`) | `kandidati.php` case `list_ajax`, Formular `#filterKandidata` | POST an dieselbe Seite, Liste über `serversidedata.php?page=lista_kandidata` | ja (DataTables-Spalte Mobitel, Export) | `BELEGT DURCH QUELLCODE` |
| Älterer Filter (`page=list`) | `kandidati.php` Modal `#filterKandidati` | GET `kandidati.php?page=list&search=yes` | ja (Profil/Export-Pfade) | `BELEGT DURCH QUELLCODE` |
| Menü-Suche „Pretraga“ | `search.php` | SQL `idk_search` (Seiten/Links, keine Kandidaten) | nein | `BELEGT DURCH QUELLCODE` — nicht die Recruiter-Kandidatensuche |
| Partner-Namenssuche | `jobstep_pp/ajax.php` action `get_search_candidates` | SQL auf `idk_kandidati` nach Name | `DURCH DISCOVERY ZU PRÜFEN` | `BELEGT DURCH QUELLCODE` — andere App-Oberfläche |
| Nalog/Bot-Liste | `ssdata_search.php` | SQL `idk_kandidati` + Deutsch-Filter, SELECT enthält E-Mail | ja | Nebenmaske; interne Kontaktsicht laut Q4 |
| QC „Nova pretraga“ | `jobstep_qc/profileCandidates.php?page=searchCandidateJob` | `DURCH DISCOVERY ZU PRÜFEN` | `OFFEN` | Nebenmaske |

Hauptsuche laut Code: `kandidati.php?page=list_ajax` (Menü: Kandidati).

## 2. Feldkarte

Quelle: Filterformular in `kandidati.php` (list_ajax), Parameter gehen an `serversidedata.php?page=lista_kandidata`.

Wie die SQL wirklich rechnet: [crm-filter-sql-codebefund.md](crm-filter-sql-codebefund.md).

| UI-Label | Code-Symbol | RPC-Argument / POST | Physisch (Tabelle.spalte) | Schicht | Note |
| --- | --- | --- | --- | --- | --- |
| Starost od/do | `starost_od`, `starost_do` | dieselben | Alter aus `idk_kandidati.kandidat_datumrodjenja` (Jahresdifferenz in serversidedata) | Alter | `BELEGT DURCH QUELLCODE`; Formel in crm-filter-sql-codebefund.md |
| Vozačka dozvola | `vozacka_dozvola` = DA | `vozacka_dozvola` | `idk_kandidati.kandidat_vozacka_dozvola` | sonst | `BELEGT DURCH QUELLCODE` |
| Kategorija vozacke | `filter_kategorija_vozacke[]` | `filter_kategorija_vozacke` | `idk_kandidati.kandidat_vozacka_kategorija` | sonst | `ARBEITSANNAHME` Spalte |
| Radno iskustvo | `radno_iskustvo` = DA (Checkbox) | `radno_iskustvo` | Existenz von Zeilen in `idk_kandidat_radno_iskustvo` (alte list-Seite liest `kri_pozicija`) | Erfahrung | `BELEGT DURCH QUELLCODE`: nur ja/nein, **keine** Monate/Jahre |
| Znanje njemačkog | `kj_znanje_njemacki` | `znanje_njemacki` | `idk_kandidat_jezici` (Niveau A1–C2 / Bezznanja / nemainfo / svi) | Sprache | `BELEGT DURCH QUELLCODE` |
| Znanje engleskog | `kj_znanje_engleski` | `znanje_engleski` | `idk_kandidat_jezici` | Sprache | `BELEGT DURCH QUELLCODE` |
| Grupe | `filter_grupe[]` | `filter_grupe` | `idk_kandidati.kandidat_group` → `idk_kandidati_grupe` | Status | `BELEGT DURCH QUELLCODE` |
| Status | `filter_status[]` | `filter_status` | `idk_kandidati.kandidat_status` | Status | `BELEGT DURCH QUELLCODE` |
| Status prijave | `filter_status_prijave[]` | `filter_status_prijave` | `idk_kandidat_status_prijave` | Status | `BELEGT DURCH QUELLCODE` |
| Izvor | `filter_izvor[]` | `filter_izvor` | `idk_kandidati.kandidat_porijeklo` | sonst | `BELEGT DURCH QUELLCODE` (SQL `lista_kandidata`) |
| Državljanstvo | `filter_drzavljanstvo[]` EU/NON-EU | `filter_drzavljanstvo` | `idk_kandidati.kandidat_drzavljanstvo_vrsta` | sonst | `ARBEITSANNAHME` |
| Boravak u EU | `filter_boravak[]` | `filter_boravak` | `idk_kandidati.boravak_eu` | Ort | `BELEGT DURCH QUELLCODE` — nicht Stadt/Wunschort |
| Struke | `filter_struke[]` | `filter_struke` | `idk_struke` → `idk_skole_smjerovi.ss_naziv` → `ke_naziv_kvalifikacije` | Ausbildungsberuf | UI `BELEGT`; ob das Ausbildungsberuf ist: Wizard 03 **OFFEN**; tot wenn Smjer gesetzt |
| Škole | `filter_skole[]` | `filter_skole` | `idk_skole` / `idk_kandidat_edukacija.ke_naziv` | Ausbildungsberuf | `BELEGT DURCH QUELLCODE` |
| Smjerovi | `filter_smjer[]` | `filter_smjer` | `idk_kandidat_edukacija.ke_naziv_kvalifikacije` | Ausbildungsberuf | `BELEGT DURCH QUELLCODE`; verdrängt Schule und Struke; Deutung Wizard 03 **OFFEN** |
| DIPL status | `filter_dipl_status[]` | `filter_dipl_status` | DIPL-Workflow, nicht Berufssuche | sonst | `BELEGT DURCH QUELLCODE` |
| Vrsta nostrifikacije | `filter_vrsta_nostrifikacije[]` | `filter_vrsta_nostrifikacije` | Nostrifikation | sonst | `BELEGT DURCH QUELLCODE` |
| fehlt in UI | — | — | — | Erfahrungsberuf | `OFFEN` in dieser Hauptsuche |
| fehlt in UI | — | — | — | Tätigkeitsart | `OFFEN` in dieser Hauptsuche |
| fehlt in UI | — | — | occupation / job_occupation_map | Berufssuchprofil | `OFFEN` in dieser Hauptsuche |
| fehlt in UI | — | — | `idk_kandidati.kandidat_iskustvo_u_struci(_trajanje)` | Erfahrung (Dauer) | Felder existieren auf der Akte (`kandidati.php` SELECT), **nicht** im Filter |
| fehlt in UI | — | — | `kandidat_grad` / `kandidat_zeljeni_grad` | Ort | auf der Akte, nicht im list_ajax-Filter |
| fehlt in UI | — | — | `idk_kandidat_vjestine` | Skill | Bearbeitung auf der Akte, nicht im Filter |
| Freitext | fehlt in UI der Hauptsuche | — | — | Freitext | `OFFEN` / `search.php` ist nur Menü-Volltext |

## 3. RPC-Karte

Kein Aufruf von `search_candidates_filtered` / `search_candidates_by_occupation` / `crm_api.search_candidates` im PHP der Hauptsuche gefunden.

| Schema.funktion | Argumente (ohne Werte) | Von Maske | Kontaktfelder | Note |
| --- | --- | --- | --- | --- |
| (keine Postgres-RPC) `serversidedata.php?page=lista_kandidata` | POST-Filter wie Tabelle 2 | Kandidati list_ajax | ja (Mobitel-Spalte im Grid) | `BELEGT DURCH QUELLCODE` — SQL liegt in PHP, nicht in crm_api |
| `jobstep_pp/ajax.php` `get_search_candidates` | Namensstring | Partner-UI | `DURCH DISCOVERY ZU PRÜFEN` | Namenssuche |
| `ssdata_search.php` | nalog_id, uslovi, njem_uslov | Bot/Nalog | ja (E-Mail in SELECT) | `R1-AUSSCHLUSS` |

Nicht wrappen: `crm_api.search_candidates` (im PHP dieser App nicht gefunden; Signatur in Supabase trotzdem Kontakt).

## 4. Beruf und Erfahrung

| Frage | Befund | Note |
| --- | --- | --- |
| Kann die Hauptsuche Ausbildung ohne Erfahrung setzen? | ja: Struke/Schule/Smjer ohne Checkbox Radno iskustvo | `BELEGT DURCH QUELLCODE` |
| Kann sie Erfahrung ohne Ausbildung setzen? | ja: nur Checkbox Radno iskustvo | `BELEGT DURCH QUELLCODE` |
| Tätigkeitsart getrennt? | nein in dieser Maske | `OFFEN` / fehlt |
| Welches Feld zählt Dauer? | Filter zählt **keine** Dauer, nur ob Erfahrung existiert. Aktenfelder `kandidat_iskustvo_u_struci(_trajanje)` und Perioden `idk_kandidat_radno_iskustvo` bleiben Q8.5 | `OFFEN` für „5 Jahre“ |
| Berufssuchprofil = welche Tabelle? | Hauptsuche nutzt `idk_struke` + Schule/Smjer, nicht `occupation` / `idk_nalog_profil` | `OFFEN` für MCP-Profil; UI-Befund `BELEGT` |

## 5. Personenfelder in der alten Suche

| Fläche | Vorkommen in Maske/RPC | Folge |
| --- | --- | --- |
| E-Mail / Telefon | list_ajax: Spalte Mobitel; `ssdata_search.php` SELECT E-Mail; Akte mit Kontaktfeldern | Q4: interne Rollen sehen Kontakte. Kunde erst nach Einstellungsfreigabe. Discovery liest SQL/PHP-Felder, kopiert keine Datensätze. |
| CV-Text | Spalte CV generiert; Detail lädt cv_de/cv_ba | in der alten UI vorhanden; MCP-Abbildung OFFEN |
| Notizen | nicht im Filter | — |

## 6. Lücken

- GELESEN: Filter-SQL `lista_kandidata` in [crm-filter-sql-codebefund.md](crm-filter-sql-codebefund.md). JSON-Entwurf geprüft, Bericht-Audit ausgeführt. Struke/Smjer = Ausbildungsberuf. Jahresfilter R1: Q8.5.9.
- OFFEN: ob Recruiter zusätzlich Nalog-Profile (`idk_nalog_profil`) als Suche nutzen.
- DURCH DISCOVERY ZU PRÜFEN: Mapping `idk_struke` ↔ `occupation` / `job_occupation_map`.
- ARBEITSANNAHME: list_ajax ist die interne Recruiter-Hauptsuche, weil das Menü „Kandidati“ dorthin zeigt.

## 7. Nicht entschieden (bewusst leer)

Filter-SQL ist gelesen. JSON-Filter-Entwurf geprüft (nicht Vertrag):
[crm-json-filter-draft.md](crm-json-filter-draft.md).
Ranking R1: `kandidat_id` absteigend. Ein Such-MCP, Tokens je Rolle.
Hosting/SDK-Version offen. Kein Scaffold, bis der Nutzer es startet.
