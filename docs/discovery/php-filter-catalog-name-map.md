<!-- markdownlint-disable MD013 -->
# PHP-Filter zu B2-Katalognamen

Stand: 2026-09-13

Status: **NAMEN ONLY**. Keine Werte, keine Kandidatenzeilen, kein RLS-Beweis,
kein Vertrag, kein MCP. Erzeugt von
scripts/discovery/build-php-filter-catalog-name-map.py.
B2-Rohdatei bleibt außerhalb Git. Diese Seite enthält nur Identifier.

Quelle Filter: [crm-app-wiring.md](crm-app-wiring.md),
[crm-json-filter-draft.md](crm-json-filter-draft.md).
Quelle Katalog: Gate B2 V3, nur schema_name / relation_name / column_name.
B3-Rohdatei wird nicht gelesen (Definitionen können Literale enthalten).

| JSON | PHP | Namen aus PHP-Befund | In B2 | Hinweis |
| --- | --- | --- | --- | --- |
| `age.min` / `age.max` | `starost_od`, `starost_do` | idk_kandidati.kandidat_datumrodjenja, idk_kandidati, kandidat_datumrodjenja | idk_kandidati.kandidat_datumrodjenja: ja (crm); idk_kandidati: ja (crm); kandidat_datumrodjenja: Spalte ja (crm) | Alter |
| `driving_license` | `vozacka_dozvola` = DA | idk_kandidati.kandidat_vozacka_dozvola, idk_kandidati, kandidat_vozacka_dozvola | idk_kandidati.kandidat_vozacka_dozvola: ja (crm); idk_kandidati: ja (crm); kandidat_vozacka_dozvola: Spalte ja (crm) | sonst |
| `driving_categories` | `filter_kategorija_vozacke[]` | idk_kandidati.kandidat_vozacka_kategorija, idk_kandidati, kandidat_vozacka_kategorija | idk_kandidati.kandidat_vozacka_kategorija: ja (crm); idk_kandidati: ja (crm); kandidat_vozacka_kategorija: Spalte ja (crm) | sonst |
| `has_work_experience` | `radno_iskustvo` = DA (Checkbox) | idk_kandidat_radno_iskustvo, kri_pozicija | idk_kandidat_radno_iskustvo: ja (crm); kri_pozicija: Spalte ja (crm, crm_api) | Erfahrung |
| `german` | `kj_znanje_njemacki` | idk_kandidat_jezici | idk_kandidat_jezici: ja (crm) | Sprache |
| `english` | `kj_znanje_engleski` | idk_kandidat_jezici | idk_kandidat_jezici: ja (crm) | Sprache |
| `groups` | `filter_grupe[]` | idk_kandidati.kandidat_group, idk_kandidati_grupe, idk_kandidati, kandidat_group | idk_kandidati.kandidat_group: ja (crm); idk_kandidati_grupe: ja (crm); idk_kandidati: ja (crm); kandidat_group: Spalte ja (crm) | Status |
| `processing_status` | `filter_status[]` | idk_kandidati.kandidat_status, idk_kandidati, kandidat_status | idk_kandidati.kandidat_status: ja (crm); idk_kandidati: ja (crm); kandidat_status: Spalte ja (crm, crm_api) | Status |
| `application_status` | `filter_status_prijave[]` | idk_kandidat_status_prijave | idk_kandidat_status_prijave: ja (crm) | Status |
| `source` | `filter_izvor[]` | idk_kandidati.kandidat_porijeklo, idk_kandidati, kandidat_porijeklo | idk_kandidati.kandidat_porijeklo: ja (crm); idk_kandidati: ja (crm); kandidat_porijeklo: Spalte ja (crm) | sonst |
| `citizenship` | `filter_drzavljanstvo[]` EU/NON-EU | idk_kandidati.kandidat_drzavljanstvo_vrsta, idk_kandidati, kandidat_drzavljanstvo_vrsta | idk_kandidati.kandidat_drzavljanstvo_vrsta: ja (crm); idk_kandidati: ja (crm); kandidat_drzavljanstvo_vrsta: Spalte ja (crm) | sonst |
| `eu_residence` | `filter_boravak[]` | idk_kandidati.boravak_eu, idk_kandidati, boravak_eu | idk_kandidati.boravak_eu: ja (crm); idk_kandidati: ja (crm); boravak_eu: Spalte ja (crm) | Ort |
| `struke` | `filter_struke[]` | idk_struke, idk_skole_smjerovi.ss_naziv, ke_naziv_kvalifikacije, idk_skole_smjerovi, ss_naziv | idk_struke: ja (crm); idk_skole_smjerovi.ss_naziv: ja (crm); ke_naziv_kvalifikacije: Spalte ja (crm, crm_api); idk_skole_smjerovi: ja (crm); ss_naziv: Spalte ja (crm) | Ausbildungsberuf |
| `schools` | `filter_skole[]` | idk_skole, idk_kandidat_edukacija.ke_naziv, idk_kandidat_edukacija, ke_naziv | idk_skole: ja (crm); idk_kandidat_edukacija.ke_naziv: ja (crm); idk_kandidat_edukacija: ja (crm); ke_naziv: Spalte ja (crm, crm_api) | Ausbildungsberuf |
| `smjer` | `filter_smjer[]` | idk_kandidat_edukacija.ke_naziv_kvalifikacije, idk_kandidat_edukacija, ke_naziv_kvalifikacije | idk_kandidat_edukacija.ke_naziv_kvalifikacije: ja (crm); idk_kandidat_edukacija: ja (crm); ke_naziv_kvalifikacije: Spalte ja (crm, crm_api) | Ausbildungsberuf |
| `dipl_status` | `filter_dipl_status[]` | DIPL-Workflow, nicht Berufssuche | kein Name im PHP-Befund | sonst |
| `nostrification` | `filter_vrsta_nostrifikacije[]` | Nostrifikation | kein Name im PHP-Befund | sonst |
| nicht in R1-JSON | — | — | kein Name im PHP-Befund | Erfahrungsberuf |
| nicht in R1-JSON | — | — | kein Name im PHP-Befund | Tätigkeitsart |
| nicht in R1-JSON | — | occupation, job_occupation_map | occupation: ja (crm); job_occupation_map: ja (crm) | Berufssuchprofil |
| nicht in R1-JSON | — | idk_kandidati, kandidat_iskustvo_u_struci | idk_kandidati: ja (crm); kandidat_iskustvo_u_struci: Spalte ja (crm) | Erfahrung (Dauer) |
| nicht in R1-JSON | — | kandidat_grad, kandidat_zeljeni_grad | kandidat_grad: Spalte ja (crm); kandidat_zeljeni_grad: Spalte ja (crm) | Ort |
| nicht in R1-JSON | — | idk_kandidat_vjestine | idk_kandidat_vjestine: ja (crm) | Skill |
| - | fehlt in UI der Hauptsuche | — | kein Name im PHP-Befund | Freitext |

B2 Relationen gelesen: 398. B2 Spalten gelesen: 1960.
Zahlen oben sind Katalog-Anzahlen, keine Kandidatenwerte.

Das ersetzt nicht das Review von RLS, Grants und PII.
