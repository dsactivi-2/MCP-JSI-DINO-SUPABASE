<!-- markdownlint-disable MD013 -->
# Codebefund: Kandidatenstatus und Automatik

Stand: 2026-09-13

Status: ENTWURF. PHP gelesen, keine Datensätze. Quellenrang Q17.
Wizard 01 wurde dafür **nicht** erweitert. Rohzettel: Wizard 04.
Lesart dieser Datei: Agent liest PHP, kein 50-Fragen-Wizard.

Zettel: [crm-php-hits/status/](crm-php-hits/status/).
Filter-SQL (A): [crm-filter-sql-codebefund.md](crm-filter-sql-codebefund.md).

## Warum nicht Wizard 01 nochmal

01 sucht Suchwörter. Der 200-Zeilen-Deckel ist seit 2026-09-13 entfernt.
Status, Klick und Cron gehören trotzdem nicht in 01. Sie liegen in
`ajax.php`, `do.php`, `cron_*.php`, `includes/functions.php`.
Nochmal 01 würde den Pfad erneut abfragen und die Verdrahtung gefährden.

## Status-Ebenen (Code)

Vier parallele Skalen plus Task-Force. Sie überschreiben einander **nicht**.

### 1. Bearbeitung `kandidat_status`

Quelle: `includes/functions.php` `getStatusList` / `getStatusListNew`,
Filter in `kandidati.php`. IDs 7 und 8 sind auch **Zeit-Status**.

| ID | Label in PHP |
| --- | --- |
| 0 | Na provjeri |
| 1 | U obradi |
| 2 | Obrađen |
| 3 | Arhiviran |
| 4 | Kontrola |
| 5 | Dopuna |
| 6 | Odbio Messenger |
| 7 | U obradi više od 3 dana |
| 8 | Na dopuni više od 3 dana |

### 2. Anmeldung `kandidat_status_prijave`

Filter lädt Labels aus `idk_kandidat_status_prijave` (`status_id`,
`status_naziv`). Extra-Option `0` = Nedefinisan. Volle Label-Liste ist
DB, nicht hardcodiert — `DURCH DISCOVERY ZU PRÜFEN` (kein Dump-INSERT
in Git).

Zahlen, die der Code **setzt** (Namen der DB-Zeile unbelegt, außer 0):

| ID | Wo gesetzt | Note |
| --- | --- | --- |
| 0 | `ajax.php` `edit_projekat_status_p` wenn `nedefinisan` | manuell |
| 1 | Insert neuer Kandidat in `do.php` | Startwert |
| 2 | `checkCandidateInputs` BOT-ne-ispunjava; `kandidat_nije_dosao_na_intervju` | zwei Wege, gleiche Zahl |
| 3 | Go-Online manuell und Cron | Casting → Intervju |
| 4 | `edit_projekat_status_p` | legt Partner-Zahlung an, wenn Partner-ID da ist |
| 6 | `checkCandidateInputs` BOT-ispunjava | Kriterien erfüllt |
| 10 | `do.php` (weitere Stelle) | genauer Case `DURCH DISCOVERY ZU PRÜFEN` |
| 12 | `includes/functions.php` | genauer Caller `DURCH DISCOVERY ZU PRÜFEN` |
| 15 | `add_datum_termina` | Termin gesetzt, `kandidat_bio_na_terminu` leer |
| 18 | `kandidat_termin_check` ja; auch Visa `status_dopuna` / `status_odbijen` via `prebaci_na_status` | gleiche Zahl, verschiedene Masken |
| 21 / 24 / 27 | Visa-Fälle in `do.php` | 27 = Viza bekommen |

### 3. Messenger `kandidat_status_messenger`

Labels aus Button-Titeln in `ajax.php` case `candidate_status`
(`BELEGT DURCH QUELLCODE`). Keine 4 in dieser UI.

| ID | Farbe | Bedeutung in der UI |
| --- | --- | --- |
| 0 | schwarz | Ručna obrada |
| 1 | grau | SMS zur Messenger-Installation gesendet, wartet |
| 2 | grün | Kandidat hat sich in der Messenger-App angemeldet |
| 3 | rot | Installation abgelehnt, manuelle Bearbeitung |
| 5 | orange | Profil über Messenger nicht fertig, manuelle Bearbeitung |
| 6 | orange | dasselbe Label wie 5 (nach Cron aus Dopuna) |

### 4. DIPL-Status (Filter, nicht dasselbe Feld)

Join über `idk_nd_kandidata`. Parallel zur Kartei.

| ID | Label im Filter |
| --- | --- |
| 0 | Nije u Diplu |
| 1 | Lead |
| 2 | Prikupljanje dokumentacije |
| 3 | Poslana pošta |
| 4 | U obradi |
| 5 | Plaćena taksa / Poslana dopuna |
| 6 | Završen |
| 7 | Arhiviran |

### 5. Task-Force `kandidat_tf_status` / `idk_task_force`

Extra-Skala für Casting/Interview. Gesehen: 20 = gekommen,
22 = nicht erschienen. Cron `cron_nije_dosao_na_razgovor.php`
schiebt überfällige Termine auf 22.

## B7 — Klick im CRM (sehr wichtig, Q20)

Es gibt **keine** einzelne Trigger-Datei. Menschen klicken in der Akte;
PHP schreibt Status, Log und oft ein Projekt.

### Bearbeitung: Aktionsleiste

1. UI: `ajax.php?page=candidate_status` (Buttons Na provjeri … Arhiviran).
2. Klick POST an `ajax.php?page=candidate_status_edit` mit
   `id`, `status_k`, `status_mes`.
3. `UPDATE idk_kandidati SET kandidat_status = :status_k`.
   Messenger-Feld wird hier **nicht** mitgeschrieben.
4. Log in `idk_log_kandidat_statusi` (Bearbeitung + Messenger + Mitarbeiter).
5. Nur wenn neuer Status **2 (Obrađen)**: `checkCandidateInputs($id)`.

Buttons sind oft gesperrt, abhängig vom Messenger:

| Messenger | Sperre |
| --- | --- |
| 1 (SMS wartet) | alle Bearbeitungs-Buttons aus |
| 2 und Status nicht 4 | alle aus |
| 2 und Status 4 (Kontrola) | Obrađen nur wenn Validierung durch ist; Archiv frei |
| 5 oder 6 (Profil unfertig) | Na provjeri wird zu gesperrtem „Nezavršen messenger“; U obradi/Dopuna, Obrađen, Archiv an |
| sonst | alle an |

Kontrola-Button nur bei Messenger 1 oder 2. Bei Status 5 zeigt die Leiste
„Dopuna“ statt „U obradi“.

### Was „Obrađen“ auslöst

`checkCandidateInputs` in `includes/functions.php`:

- Wenn der Kandidat durch Prijave **reserviert** ist: nichts verschieben.
- Sonst: Nalog-Kriterien (Alter, Struke/Smjer, Führerschein, Deutsch, …).
- Pass: Prijave **6**, Projektname wie `BOT - ispunjava uslove`, raus aus
  Prijave-Projekt.
- Fail: Prijave **2**, Projekt `BOT - ne ispunjava uslove`.
- Kein Nalog: Rückgabe 4, keine Projektverschiebung.

Das ist **kein** Mail-Versand. Nur Status + Projekt + Log.

### Anmeldung: Projekt-Dropdown

`ajax.php?page=edit_projekat_status_p` setzt
`kandidat_status_prijave` auf die gewählte ID (oder 0). Bei ID **4**
und vorhandener Partner-ID: Zeile in `idk_partner_uplate`.

### `do.php` — Alltagsklicks neben der Leiste

| Case | Wirkung |
| --- | --- |
| `kandidat_go_online` | Prijave **3**; raus aus altem Projekt; rein in Projektname `%Intervju%` (Nalog 217–220 → Nalog 222); Log |
| `add_datum_termina` | Prijave **15**, Termin-Datum, Erinnerungstyp 15 |
| `kandidat_termin_check` ja | da gewesen, Prijave **18**, Erinnerung 16 |
| `kandidat_termin_check` nein | Flag 0 oder neues Datum; Prijave bleibt |
| `kandidat_dosao_na_intervju` | TF-Status **20**, keine Prijave-Zahl hier |
| `kandidat_nije_dosao_na_intervju` | TF **22**, Prijave **2**, Projekt Intervju → „Nije došao na razgovor“, Termin-Eintrag archiviert |
| `validacija_all*` | Bearbeitung **5** (Dopuna), wenn Inputs fehlen |
| `status_dopuna` / `status_odbijen` | Visa: `prebaci_na_status(..., 18)` |
| `add_kandidat_visa` Ausgang 1 | Prijave **27** |
| `upload_document` (Vertrag) | Prijave 8 oder 9, Erinnerung 5 oder 7 |
| `partner_notification` | Push an Partner-App, nicht Kandidaten-Status |

Neu-Insert oft: Bearbeitung 0, Messenger 1, Prijave 1.

## Automatik (Cron)

| Auslöser | Datei | Wirkung |
| --- | --- | --- |
| Casting mit Termin, Schule+Erfahrung | `cron_automatic_go_online.php` | wie Go-Online: Prijave 3, Casting → Intervju |
| Messenger eingeloggt, Bearbeitung 1 oder 5, länger offline | `cron_bot_obrada.php` | bis 3 Push „Kompletirajte svoju prijavu“; danach 1→7 und Messenger 5, oder 5→8 und Messenger 6 |
| Messenger 1, Bearbeitung 0, Install-SMS alt | `cron_bot_instal.php` | bis 3 Viber; danach Bearbeitung 6 und Messenger 3 |
| TF 16/18, Termin heute überfällig | `cron_nije_dosao_na_razgovor.php` | TF 22 |
| Geburtstag, nicht archiviert | `cron_rodjendan.php` | SMS (C9) |
| Casting-Termin in n Tagen | `cron_appointment_invite_links.php` | Einladungs-SMS mit Link (C8) |
| Termin heute, Ausgang fehlt | `cron_provjera_termina.php` | Mail an **Mitarbeiter**, nicht an Kandidat |

## C 4–9 — Nachrichten

Tiefscan: [crm-notify-codebefund.md](crm-notify-codebefund.md).
Q20: im Produkt **default aus**. Keine Empfängerwerte.

Kurz: Leisten-Klick sendet nichts. C4 Onboarding-SMS und Dopuna-Push.
C5 kein Kunden-Mail am Kandidatenstatus. C6/C7 Bot-Cron mit Kappe 3.
C8 Einladung ja, Go-Online/Nicht-erschienen ohne Kandidaten-Nachricht.
C9 Geburtstag ohne Statuswechsel.

## Lücken

- Volle Prijave-Labels (DB, kein Dump).
- Restliche `do.php`-Cases ohne Statuswort im Namen.
- Ob Supabase dieselben Cron-Jobs hat, oder nur die Tabellen.
- Welche Status der Runtime-MCP filtern soll (Wizard 03 / Interview).
- C 4–9 ist in der Notify-Datei; DIPL-Mails bleiben Punkt 10.

## Nächster Schritt

Nicht Wizard 04 wiederholen, nicht Wizard 01.
Wizard-03-Alltag bestätigt. JSON-Filter-Entwurf geprüft. Bericht-Audit
ausgeführt. Kein MCP-Bau, bis der Nutzer das startet.
