# Katalog zu Domäne (Gate B2 V3)

Stand: 2026-09-12

Status: erste Zuordnung aus dem Katalog. Keine Datensätze gelesen. Keine
Foreign Keys erfunden. Schätzungen (`reltuples`) sind keine gezählten Stände.

Quelle: Gate B2 V3, Prüfrolle, Schemata `crm`, `crm_api`, `crm_auth`.
199 Relationen. Der Visualizer-Export bleibt enger und ersetzt dies nicht.

Legende: `BELEGT` Katalogname/FK/Schätzung. `ARBEITSANNAHME` fachliche Lesart.
`DURCH DISCOVERY ZU PRÜFEN` unbewiesen. R1-Ausschluss folgt Q4 und Q15.

## R1-Suchkern

<!-- markdownlint-disable MD013 -->

| Domäne | Physisch (BELEGT) | Schätzung | Lesart |
| --- | --- | --- | --- |
| Kandidat | `crm.idk_kandidati` | ~122004 | Kernakte. Intern mit Kontakt; Kunde ohne Kontakt bis Einstellungsfreigabe. Ausweis/Passwort nicht an Kunde. |
| Berufserfahrung | `crm.idk_kandidat_radno_iskustvo` | ~87844 | Perioden und freie Jobtitel. Q8.5 bleibt OPEN. |
| Ausbildungsberuf / Taxonomie | `crm.occupation`, `occupation_alias` | ~702 / ~1241 | Kontrollierte Slugs, BS/DE, Aliasse. |
| Jobtitel → Taxonomie | `crm.job_occupation_map` | ~87844 | FK auf Erfahrung **und** occupation. |
| Benannte Position | `crm.idk_kandidat_pozicija` | ~133 | Mehrsprachiger Name. |
| Position → Taxonomie | `crm.pozicija_occupations` | ~123 | FK auf Position und occupation. |
| Ausbildung | `crm.idk_kandidat_edukacija` | ~149473 | Schule, Zeitraum, Qualifikation. |
| Sprache | `crm.idk_kandidat_jezici` | ~82474 | Hör/Lese/Sprech/Schreib. |
| Verifizierte Sprache | `crm.idk_candidate_verified_languages` | ~3897 | Extra-Schicht, Semantik OPEN. |
| Fertigkeit | `crm.idk_kandidat_vjestine` | ~10211 | Freitext/Gruppe. |
| Status | `idk_kandidat_status`, `idk_kandidat_status_prijave` | 9 / 16 | Lookup, nicht der Lauf der Akte. |
| Auftrag / Stelle | `crm.idk_nalozi` | ~238 | Auftrag der Kundenfirma. |
| Auftrags-Suchprofil | `idk_nalog_profil`, `idk_profil_kriterij` | ~83 | Filter am Auftrag (Alter, Sprache, Erfahrung). Nicht automatisch Berufssuchprofil. |

<!-- markdownlint-enable MD013 -->

Belegte Filterfelder auf `idk_kandidati` (Namen, keine Werte): Ort
(`kandidat_grad`, `kandidat_drzava`), Wunschort, Führerschein, Status,
`kandidat_datumrodjenja` (Q5, sensibel), `kandidat_iskustvo_u_struci` und
`kandidat_iskustvo_u_struci_trajanje` (Q8.5, zweite Stelle neben den Perioden).

## Belegte Foreign Keys

Nur diese Kern-FKs sind im Katalog nachgewiesen:

- `job_occupation_map.kri_id` → `idk_kandidat_radno_iskustvo`
- `job_occupation_map.occupation_id` → `occupation`
- `occupation_alias.occupation_id` → `occupation`
- `pozicija_occupations.kp_id` → `idk_kandidat_pozicija`
- `pozicija_occupations.occupation_id` → `occupation`
- Embedding-Pipeline intern: documents → text → embeddings
- `crm_auth`: Rollen ↔ Permissions, `user_roles.role_id` → `roles`

`idk_kandidat_* .kandidat_id` → `idk_kandidati` ist **nicht** als FK belegt.
Lesart bleibt ARBEITSANNAHME.

## Akteure

<!-- markdownlint-disable MD013 -->

| Domäne | Physisch | Schätzung | Lesart |
| --- | --- | --- | --- |
| Kunde | `idk_clients` / `idk_companies` | ~387 / ~1223 | Welche Tabelle die Kundenfirma ist: OPEN. Q15.2: nur Freigaben. |
| Kundenkontakt | `idk_contacts` | ~628 | Nicht Kandidat. R1-Suche nicht. |
| Vermittler-Mitarbeiter | `idk_employees` | ~369 | Intern. Enthält Login-Felder; R1-Output nicht. |
| Team | `idk_timovi` | ~6 | ARBEITSANNAHME Teamleiter-Kreis. |
| Login-Kandidaten | `crm.users` | ~111121 | Nahe der Kandidatenzahl. Semantik OPEN. |
| Produkt-Auth | `crm_auth.*` | klein | Rollenmodell. Werte nicht gelesen. |
| Alt-Rechte | `idk_module_permissions` | 8 | Altes CRM-Modulrecht, nicht MCP-Vertrag. |

<!-- markdownlint-enable MD013 -->

## R1-Ausschluss (nicht an Kunde / nicht in Discovery-Dumps)

Q4: interne Suche **enthält** Kontakt. Kunde erst nach Einstellungsfreigabe.
Discovery speichert keine Werte. Ausweis/Passwort/JMBG nicht an Kunde.
Kontaktfelder: `kandidat_email`, `kandidat_mobitel`, `idk_kandidat_kontakt_info`
(~172673). Notizen
(`idk_notes`, `idk_nd_kandidata_biljeske`). Finanzen, Verträge, SMS/Viber,
Logs. CV-Text: `idk_kandidat_cv` (winzig) und leere
`candidate_document_*`. Ähnlichkeitssuche nach Q14.1 nicht R1.

## Nicht der R1-Kern, große Parallelwelt

`idk_nd_kandidata` ~81330 und viele `idk_nd_*` / `idk_pp_*`: zweiter Kandidat-
oder Partnerpfad. Wer autoritativ ist, bleibt DURCH DISCOVERY ZU PRÜFEN.
`idk_project_kandidati` ~207679 verknüpft Projekt und Kandidat-ID ohne belegten
FK.

## Berufssuchprofil

Q8.4 bleibt fachlich bestätigt. Physisch unklar, drei Kandidaten:

1. `occupation` plus `parent_slug` (Taxonomie).
2. `idk_kandidat_pozicija` plus `pozicija_occupations`.
3. `idk_nalog_profil` plus `idk_profil_kriterij` (Auftragskriterien).

Keine der drei ist ohne Entscheidung das Berufssuchprofil.

## Q8.5 Hinweis

Nutzer 2026-09-13: Zettel-2-Interpretation vorerst ignorieren.

Zwei Speicherorte, eine fachliche Wahrheit (Q8.5.1):

- Lebenslauf-Liste: `idk_kandidat_radno_iskustvo` (ein Job je Zeile).
- Kandidatenakte: `idk_kandidati` plus zwei Zahlenfelder zur Erfahrung.

Die zwei Zahlen sind Selbstangabe bei der Bewerbung (Formular Ja/Nein plus
kodierte Dauer in 5 Jahren), nicht die von–bis-Liste. MySQL-Kommentare und
`registracija_posao.php` belegen die Codes. Filter am Auftrag liegen analog in
`idk_nalozi_blokovi_prijave`.

## Nächster fachlicher Schritt

Menschliches Review dieser Zuordnung. Danach Q8.5 und welche Tabellen der
erste Such-RPC lesen darf. Kein SQL-Apply, kein Plugin, keine Embeddings.

PHP-Filter auf B2-Namen (ohne Werte):
[php-filter-catalog-name-map.md](php-filter-catalog-name-map.md).
