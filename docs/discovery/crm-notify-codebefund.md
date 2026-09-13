<!-- markdownlint-disable MD013 -->
# Codebefund: C 4–9 Nachrichten an Statuswechsel

Stand: 2026-09-13

Status: ENTWURF. PHP gelesen, keine Datensätze, keine Empfängerwerte,
keine Secrets. Quellenrang Q17. Produkt laut Q20: **default aus**,
einschaltbar.

Rohbasis: [crm-status-codebefund.md](crm-status-codebefund.md) (B7/Cron).
Inventar: [crm-work-inventory.md](crm-work-inventory.md).

Kein PHPMailer-Vendor zitieren. Kein Wizard 01/04.

## Kern

Die Bearbeitungs-Leiste sendet **keine** Nachricht. `ajax.php`
`candidate_status_edit` schreibt nur `kandidat_status` + Log; Status 2
ruft `checkCandidateInputs` (Projekt, keine Mail).

Nachrichten hängen an **anderen** Wegen: Messenger-Onboarding, Bot-Cron,
Termin-Cron, Validierung → Dopuna, Vertrag/DIPL-Mail, Partner-Push.
Kanal und Auslöser unten. Texte nur als Sinn, nicht als Produktvertrag.

## Kanäle (Code)

| Kanal | Wie im PHP | Typische C-Punkte |
| --- | --- | --- |
| SMS | Infobip oder NTH über `getActiveProviderForSendingMessages` | 4, 7, 8, 9 |
| Viber | Infobip Omni / NTH, oft SMS als Fallback | 7, 8, 9 |
| Messenger-Push | `send_bot_notification_android` / `_ios` | 6, 7 |
| Mail an Kandidat | PHPMailer-Hüllen; mehrere tot oder DIPL | 4 (tot), Vertrag/DIPL |
| Mail an Mitarbeiter | `cron_provjera_termina.php` | 8 (nicht Kandidat) |
| Partner-App-Push | OneSignal / `send_notification_partnerapp` | 5 (nicht Kandidatenstatus) |
| CRM-Reminder | `updateReminderStatusCRM` schließt Zeilen, sendet nicht | 6 intern |

Provider-Gruppen im Code (IDs, keine Werte): 3 Geburtstag, 4
Onboarding-SMS, 5 Install-Erinnerung.

## C4 — Kandidat benachrichtigen

| Auslöser | Statuswechsel | Kanal | Vorlage (Sinn) | Aktiv? |
| --- | --- | --- | --- | --- |
| `public_kandidati_messenger.php` nach User-Insert/Resend | kein Bearbeitungs-Klick; oft Start Messenger 1 / Bearbeitung 0 / Prijave 1 (B7) | SMS ×4 | 1 Dank für Registrierung; 2 Download-Link; 3 Nutzername+PIN; 4 Video-Hilfe | ja |
| dieselben 4 SMS in `do.php` `spremanje_u_dipl` / `szvinDIPL` | DIPL-Kandidat anlegen | SMS ×4 | wie oben | ja |
| `sendCandidateMessengerMail` | dieselben Insert-Pfade | Mail „Vaša prijava na konkurs“ + App-Links | Funktionskörper ist auskommentiert — Aufruf ohne Versand | tot |
| `sendCandidateRegMail` | Text aus `idk_email_text` `email_registracija` | Mail | **kein** Caller im PHP | tot |
| Validierung fehlender Inputs | Bearbeitung **5** (Dopuna), Messenger bleibt 2 | Push | DE „Korriegieren Sie Ihre Daten“ / BS „Niste unijeli dobre podatke!“ | ja in `ajax.php` `validacija_*` und `do.php` `validacija_all`; `validacija_all_sveodjednom` Push ist auskommentiert |
| Vertrag/Predračun | DIPL, nicht Bearbeitung 0–8 | Viber+SMS+Mail | Ugovor-Link / Rate zahlen | ja, gehört eher zu 10/11–16 |

Bearbeitungs-Klick Obrađen/Archiv **ohne** Mail an den Kandidaten.

## C5 — Kunde benachrichtigen

Kein Mail an den einstellenden Kunden beim Kandidaten-Statusklick.

| Auslöser | Was passiert | Kanal | Note |
| --- | --- | --- | --- |
| `do.php` Nalog-Status **8** (Completed) | Partner, der die Firma angelegt hat, wenn Preference an | OneSignal + interne Partner-Notification | Text: Auftrag abgeschlossen |
| `do.php` `edit_company` Statuswechsel | dieselbe Partner-App | OneSignal | Firma aktiv/archiv |
| `do.php` `partner_notification` | Marketing „neue Offerte“ | Partner-Push | ein hardcodierter Partner, kein Kandidatenstatus |
| Firmen-Anlage | Willkommensmail | HTML unter `mail-templates/company-registration/` | Firmen-Onboarding, nicht Zusage |
| `jobstep_pp/cron_reminders_email.php` | Mail an PP-User-Typen 1/2 (Liste: Vertrag posten, Dokumente, Qualiplan, …) | Mail | Datei beginnt mit `exit()` — **aus** |
| `jobstep_pp/cron_reminders.php` | gleiche Reminder-Typen | Mail | Versand auskommentiert |

Unterschrift/Zusage an den Kunden ist im PHP **kein** automatischer
Kandidaten-Status-Trigger. PP-Reminder-Texte liegen in der DB
(`idk_pp_reminder_types`), nicht im PHP — kein Dump.

## C6 — Erinnerung ohne Antwort

| Auslöser | Bedingung | Nachricht | Danach |
| --- | --- | --- | --- |
| `cron_bot_obrada.php` | Messenger **2**, Bearbeitung **1 oder 5**, last_online 1–10 Tage her | Push „Kompletirajte svoju prijavu“, max 3× (`idk_messenger_obavijesti` tip 2) | nach 3×: 1→Bearbeitung **7** + Messenger **5**, oder 5→Bearbeitung **8** + Messenger **6** |
| `updateReminderStatusCRM` | Klick Termin/Dokument/Vertrag/Visa | **kein** Versand, schließt CRM/PP-Reminder | Typen u. a. 5 Vertrag, 15 Termin gesetzt, 16 Termin-Check |

SMS-Resend in diesem Cron ist auskommentiert (`sendSmsToCandidateAgain`).

## C7 — Messenger unvollständig

| Auslöser | Bedingung | Nachricht | Danach |
| --- | --- | --- | --- |
| `cron_bot_instal.php` | Messenger **1**, Bearbeitung **0**, Anlage 1–10 Tage her | Viber+SMS `sendViberToCandidateAgain`: „Dovrsite svoju prijavu“ + Store-Links, max 3× (tip 1) | nach 3×: Bearbeitung **6**, Messenger **3** (Install abgelehnt), **ohne** weitere Nachricht |
| C6-Cron nach 3 Pushes | siehe oben | keine vierte Push | Messenger 5 oder 6 (Profil unfertig) |

Erst-SMS 1–4 (C4) sind die Installation. C7 ist die Wiederholung.

## C8 — Termin

| Auslöser | Status | Nachricht |
| --- | --- | --- |
| `cron_appointment_invite_links.php` | kein Prijave-Schreiben; Termin in N Tagen, Flags first/second send | SMS **und** Viber: Termin in N Tagen, Ort/Zeit, Link `public_appointment_invite_link.php` Button POTVRDI. Typ 1 erste, Typ 2 zweite Welle |
| `manual_appointment_invite_links.php` | manuell dieselbe Vorlage | SMS (Viber-Helfer vorhanden) |
| `do.php` `add_datum_termina` | Prijave **15** | nur Reminder-Typ 15 schließen, **keine** Kandidaten-SMS |
| `do.php` `kandidat_termin_check` | Prijave **18** wenn da | Reminder 16, keine SMS |
| `do.php` `kandidat_nije_dosao_na_intervju` | TF **22**, Prijave **2** | Projekt-Verschiebung, **keine** Kandidaten-Nachricht |
| `cron_nije_dosao_na_razgovor.php` | TF 16/18 überfällig → TF **22** | **keine** Nachricht; Datei startet mit `exit()` |
| `cron_automatic_go_online.php` | Prijave **3**, Casting → Intervju | **keine** Nachricht |
| `cron_provjera_termina.php` | Termin heute | Mail **Mitarbeiter** „Provjera termina kandidata“, nicht Kandidat |

Casting→Interview ist Status+Projekt, nicht Mail.

## C9 — Geburtstag

`cron_rodjendan.php`: Bearbeitung **nicht 3**, Geburtstag = heute,
Mobilnummern-Präfixe BA/RS/HR/ME/SI/MK.

Kanal: Viber+SMS, Bild-Button „Jobstep Web“.
Text: „Sretan rođendan … Jobstep tim!“.
Kein Statuswechsel. Provider-Gruppe 3.

## Was der Statusklick nicht tut

| Klick | Nachricht? |
| --- | --- |
| Bearbeitung 0–8 in der Leiste | nein |
| Obrađen → `checkCandidateInputs` | nein (nur Prijave 6/2 + Projekt) |
| Go-Online | nein |
| Automatisches Go-Online | nein |
| Nicht erschienen (Cron, tot) | nein |
| Prijave-Dropdown | nein (außer Folge-Reminder schließen) |

## Tot / aus / später

| Stück | Lage |
| --- | --- |
| `sendCandidateMessengerMail` | Körper auskommentiert |
| `sendCandidateRegMail` | kein Caller |
| `cron_nije_dosao_na_razgovor.php` | `exit()` oben |
| PP-Reminder-Mails | `cron_reminders_email.php` `exit()`; anderes Cron Mail auskommentiert |
| DIPL-Vertragsmails, Raten, Qualiplan | Punkt **10** / 11–16, nicht C 4–9 Kern |
| Prijave-Label-Texte | DB, kein Dump |
| Ob Supabase dieselben Cron-Jobs hat | offen |

## Produkt

Codebefund ≠ eingeschaltete Runtime. Q20: im neuen Produkt **default aus**.
Kein 1:1-Wrap dieser Sender.

## Nächster Schritt

Wizard-03-Alltag ist bestätigt (R1 = Hauptsuche). JSON-Filter-Entwurf
geprüft. Unabhängiger PASS liegt vor, Bericht-Audit offen. Nächster Schritt:
[verify-verifier-report.md](../handoffs/2026-09-13-verify-verifier-report.md).
Nicht Tool-Namen. Nicht MCP-Bau, nicht Wizard 01/04.
