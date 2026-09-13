<!-- markdownlint-disable MD013 -->
# Inventar: bisherige Arbeit (CRM-Scan bis MCP)

Stand: 2026-09-13

Status: Arbeitsindex. **Kein** Runtime-MCP gebaut. **Kein**
Produktions-SQL. **Keine** Kandidatenzeilen in Git. Dieser Text ist die
Landkarte, nicht der Vertrag. Bei Konflikt gilt die neueste ausdrückliche
Antwort in [ADR-0002](../decisions/0002-search-design-interview.md).

Projektstatus (Phase, Gate B, Rechte): [docs/project.md](../project.md).

## 1. Wo wir stehen

Discovery der **alten PHP-Suche und Businesslogik**. Filter-UI, Filter-SQL,
Status-Klicks (B7) und Nachrichten C 4–9 sind gelesen. Wizard-03-Alltag
ist bestätigt (R1 = alte Hauptsuche). JSON-Filter ist Entwurf, kein Vertrag.
MCP-Bau ist **nicht** dran.

JSON-Filter-Entwurf ist 2026-09-13 gegen PHP und Heft geprüft.
Struke/Smjer = Ausbildungsberuf: bestätigt. „5 Jahre“ nicht in R1:
bestätigt. INNER JOIN: nicht übernehmen, ohne Gruppe/Bearbeitung sichtbar.
Nutzer 2026-09-13 Punkt 1 **Ja:** Vorbericht-PASS zählt nicht.
Punkt 3 **Ja:** JSON bleibt Entwurf, kein Vertrag.
Punkt 2 **Ja:** Archiv-Satz bleibt (Zählfehler nicht kopieren).
Bestätigung vor jeder Suche: `BESTÄTIGT` (Filter zeigen, dann suchen).
Kein Tool-Namen. Kein Wizard 01/02/04. Kein MCP-Bau.

## 2. Verbindliche Quellen (nicht ins Doku-Git kopieren)

| Was | Absoluter Pfad | Rolle |
| --- | --- | --- |
| CRM-Code | `/Users/activi/Downloads/crm-master-3` | einzige App-Quelle |
| PHP | `/Users/activi/Downloads/crm-master-3/src/crm` | Legacy-PHP, Git `e9ec9e0` |
| Kandidaten-Dump | `.../databaseDump/dump_20260226_081150.sql` | ~1,53 GiB, 179 Tabellen |
| Website-Dump | `.../databaseDump/2024_10_28.sql` | nicht Kandidaten; `crmdb` leer |
| Zweite App | `/Users/activi/Projects/jobstep-crm` | ausgeschlossen |
| Doku-Repo | dieses Git | ADRs, Lesarten, Scripts |

Env aus Wizard 01: `/private/tmp/dino-crm-wiring.env`
(`CRM_PATH=.../src/crm`, RPC 21 / Tabellen 1732 / UI 2487).

## 3. Entscheidungen, die nicht neu aufgerollt werden

Volltext: [ADR-0002](../decisions/0002-search-design-interview.md).
Architektur: [ADR-0001](../decisions/0001-controlled-query-boundary.md).

| ID | Stand | Kern |
| --- | --- | --- |
| Q4 | `ERSETZT` 2026-09-12 | Interner Vermittler sieht Pool + Kontakte. Kunde nie den ganzen Pool. Vorschlagsfreigabe ohne Kontakt, Einstellungsfreigabe = CONTACT-02. Plugin nie auf Produktion. Discovery ohne Datensatz-Dump. |
| Q8.4 | bestätigt im Prinzip | drei Berufsschichten + Berufssuchprofile, auch wenn die alte Maske sie nicht so trennt |
| Q8.5 | `TEILWEISE` | 8.5.3–8 bestätigt; „5 Jahre“ nicht in R1 (`BESTÄTIGT` nein) |
| Q15.6 | `TEILWEISE` | Blättern und Datei; CSV+Excel; max. 500; JMBG+Kontakt; nicht ganzer Bestand |
| Q17 | `BESTÄTIGT` | Heft und alte UI/PHP gleichberechtigt; Heft ist keine Whitelist |
| Q18 | `TEILWEISE` | Codebefund + Alltag bestätigt; Struke/Smjer = Ausbildungsberuf; 5 Jahre nicht in R1; INNER JOIN nicht kopieren |
| Q19 | `TEILWEISE` | Status-Ebenen und Automatik als Codebefund |
| Q20 | `TEILWEISE` | Jetzt: Filter, alle Status, Auslöser, A, B7, C 4–9 Codebefund. Produkt default aus. 10 und 11–16 später |
| Q21 | `BESTÄTIGT` | Funktionen erfassen, modern umsetzen, nicht 1:1 PHP-SQL |
| Q22 | `BESTÄTIGT` | Jetzt nur altes CRM. occupation / Akten-Jahre / Stadt-Skills-als-Filter kein jetziger Scan |
| ADR-0001 | akzeptiert | LLM nur JSON-Filter; Postgres sucht; Cap 50 |

## 4. Gemappte Daten (Lesarten, nicht abschreiben)

### 4.1 Recruiter-Hauptsuche

Datei: [crm-app-wiring.md](crm-app-wiring.md). Rohzettel:
[crm-php-hits/](crm-php-hits/).

- Maske: `kandidati.php?page=list_ajax` → `serversidedata.php?page=lista_kandidata`.
- Filter-UI u. a. Alter, Führerschein, Erfahrung ja/nein, Deutsch/Englisch,
  Gruppe, Bearbeitung, Prijave, Quelle, Staatsangehörigkeit, Boravak EU,
  Struke, Schule, Smjer, DIPL-Status, Nostrifikation.
- Nicht in dieser Maske: drei getrennte Berufsschichten, Jahres-Erfahrung,
  Stadt/Wunschort, Skills, Freitext, occupation-Profil.
- `search.php` ist Menü-Volltext, keine Kandidatensuche.
- Keine Nutzung von `crm_api.search_candidates` in dieser PHP-Hauptsuche.

### 4.2 Filter-SQL (A, Q20)

Datei: [crm-filter-sql-codebefund.md](crm-filter-sql-codebefund.md).

- Leeres Feld → SQL `1` (zählt nicht).
- Gesetzte Felder mit **UND**.
- Archiv default raus (`kandidat_status != 3`).
- Erfahrung = mindestens eine Jobzeile.
- Deutsch/Englisch: Hörfeld `kj_slusanje`, Stufe oder höher.
- Struke über Schul-Smjer.
- Tabellen-Suchbox findet auch Name, E-Mail, Mobil (interne Sicht, Q4).
- SELECT enthält Kontakt/JMBG; Werte nicht in Git.

### 4.3 Status, Klick, Cron (B / B7 / Q19)

Datei: [crm-status-codebefund.md](crm-status-codebefund.md).
Rohzettel: [crm-php-hits/status/](crm-php-hits/status/).

Fünf parallele Skalen: Bearbeitung 0–8, Prijave (Labels in DB), Messenger
0/1/2/3/5/6, DIPL 0–7, Task-Force (20 gekommen / 22 nicht erschienen).

Klick: `ajax.php?page=candidate_status_edit` setzt nur Bearbeitung + Log.
Status 2 ruft `checkCandidateInputs` (BOT-Projekte, Prijave 6 oder 2).
`do.php`: Go-Online (Prijave 3), Termin 15/18, Interview, Dopuna 5.
Cron: Bot-Erinnerung, Install, Go-Online, nicht erschienen, Geburtstag,
Termin-Einladung, Mitarbeiter-Mail bei fehlendem Terminausgang.

Prijave-**Namen** außer 0 = Nedefinisan: DB, kein Dump in Git.

### 4.4 C 4–9 Nachrichten

Datei: [crm-notify-codebefund.md](crm-notify-codebefund.md).
Produkt: default aus, einschaltbar.

| Punkt | Codebefund |
| --- | --- |
| 4 | SMS ×4 bei Messenger-Onboarding; Push bei Dopuna 5. Kandidaten-Mail tot. Leisten-Klick ohne Mail |
| 5 | kein Kunden-Mail am Kandidaten-Status. Partner-Push bei Nalog 8 / Firmenstatus. PP-Reminder-Mails aus |
| 6 | Bot-Push Kompletirajte, max 3×, dann Bearbeitung 7/8 + Messenger 5/6 |
| 7 | Install-Viber/SMS max 3×, dann Bearbeitung 6 + Messenger 3 |
| 8 | Einladungs-SMS/Viber mit Bestätigungs-Link. Go-Online und Nicht-erschienen ohne Kandidaten-Nachricht. Mitarbeiter-Mail Termin heute |
| 9 | Geburtstags-Viber/SMS, kein Statuswechsel |
| 10 | DIPL-Erinnerung — später, nicht jetzt |

### 4.6 JSON-Filter R1

Datei: [crm-json-filter-draft.md](crm-json-filter-draft.md).
Nur alte Kandidati-Filter. Unbekannte Felder ablehnen. Leer = tot. UND
zwischen Kategorien. Cap 50. Keine Jahre, kein Ort, keine Skills, kein
Berufssuchprofil. C 4–9 nicht in diesem Filter.
2026-09-13 gegen PHP/Heft geprüft. Struke/Smjer = Ausbildungsberuf.
„5 Jahre“ nicht im R1-JSON.
Unabhängiger PASS 2026-09-13 nicht haltbar; Archiv-Satz korrigiert.

### 4.5 Postgres-Katalog (Gate B2 V3, nicht PHP)

Datei: [catalog-domain-mapping.md](catalog-domain-mapping.md).
~199 Relationen in `crm` / `crm_api` / `crm_auth`. occupation und
`job_occupation_map` existieren in Postgres; die alte Filter-UI nutzt sie
nicht (Q22: jetzt kein Scan-Auftrag). Q8.5 bleibt offen.

Kontakt in diesem Katalog: interne Produktsicht laut Q4 ja; Discovery
ohne Werte. Alte „R1 ohne Kontakt“-Zeilen sind `ERSETZT`.

## 5. Dateikarte

| Datei | Was sie festhält |
| --- | --- |
| [CONTEXT.md](../../CONTEXT.md) | Domänenwörterbuch |
| [docs/project.md](../project.md) | Phase, Gate B, nächster Zielkorb |
| [ADR-0002](../decisions/0002-search-design-interview.md) | Interview Q1–Q22 |
| [ADR-0001](../decisions/0001-controlled-query-boundary.md) | JSON-Filter, kein LLM-SQL |
| [crm-app-wiring.md](crm-app-wiring.md) | Maske und Feldkarte |
| [crm-filter-sql-codebefund.md](crm-filter-sql-codebefund.md) | Wie die Maske rechnet |
| [crm-status-codebefund.md](crm-status-codebefund.md) | Status, Klick, Cron |
| [crm-notify-codebefund.md](crm-notify-codebefund.md) | C 4–9 Kanal + Auslöser |
| [crm-json-filter-draft.md](crm-json-filter-draft.md) | R1 JSON-Filter Entwurf |
| [act-103-vertragspaket.md](act-103-vertragspaket.md) | ACT-103 Pack, kein Vertrag; drei Fragen zum Ankreuzen |
| [php-filter-catalog-name-map.md](php-filter-catalog-name-map.md) | PHP/JSON-Filter zu B2-Namen, ohne Werte |
| [2026-09-13-json-filter-draft.md](../worklogs/2026-09-13-json-filter-draft.md) | Worklog JSON-Entwurf |
| [2026-09-13-json-filter-verify.md](../worklogs/2026-09-13-json-filter-verify.md) | Worklog erster PASS, nicht Schluss |
| [2026-09-13-json-filter-audit.md](../worklogs/2026-09-13-json-filter-audit.md) | Worklog Bericht-Audit |
| [2026-09-13-c49-notify.md](../worklogs/2026-09-13-c49-notify.md) | Worklog C 4–9 |
| [crm-php-hits/](crm-php-hits/) | Wizard-01-Rohlisten |
| [crm-php-hits/status/](crm-php-hits/status/) | Wizard-04-Rohlisten |
| [2026-09-13-scan-to-mcp.md](../handoffs/2026-09-13-scan-to-mcp.md) | Session-Übergabe |
| [2026-09-13-verify-verifier-report.md](../handoffs/2026-09-13-verify-verifier-report.md) | Ablauf Bericht-Audit; Vorbericht-PASS nicht haltbar |
| [2026-09-13-session-handoff.md](../handoffs/2026-09-13-session-handoff.md) | Session-Übergabe nach Bericht-Audit |
| [2026-09-13-next-agent-prompt.md](../handoffs/2026-09-13-next-agent-prompt.md) | Zeigt auf das Verdict, nicht auf Tool-Namen |
| [crm-wiring-wizards.md](../runbooks/crm-wiring-wizards.md) | Welcher Wizard wann |
| Worklogs 2026-09-12/13 | Rescan, B7, C 4–9 |

Lokal, nicht Git: `/private/tmp/dino-crm-wiring.env`,
`/private/tmp/dino-crm-app-wiring.md`,
`/private/tmp/dino-crm-wiring-work/`,
`/private/tmp/dino-crm-step1-source-lock.txt`,
`/private/tmp/dino-crm-step2-search-wiring.md`.

## 6. Scripts

| Script | Rolle |
| --- | --- |
| `scripts/wizards/crm-wiring-01-locate-and-scan.sh` | Pfad + Scan, **ohne** 200-Deckel |
| `scripts/wizards/crm-wiring-02-map-search.sh` | optional; Mapping schon aus PHP |
| `scripts/wizards/crm-wiring-03-accept.sh` | Alltag/Abnahme, **nicht** jetzt |
| `scripts/wizards/crm-wiring-04-status-and-triggers.sh` | Rohzettel Status; Lesart ist die Status-Datei |
| `scripts/discovery/step1-source-lock.sh` | PASS; prüft noch den Website-Dump (Lücke) |
| `scripts/discovery/step2-search-wiring.py` | PASS; CSS-IDs sind keine Tabellen |
| `scripts/check-local.sh` | Doku-Gate |
| `scripts/discovery/build-act-103-vertragspaket.py` | ACT-103 Pack aus Inventar, JSON-Entwurf, ADR-0002 |
| `scripts/discovery/build-php-filter-catalog-name-map.py` | Namenslandkarte PHP-Filter zu B2, ohne Rohwerte |

## 7. Bewusst nicht gemacht / verboten

- Kein MCP-Server, kein abgenommener JSON-Vertrag, kein App-Scaffold.
- Kein 1:1-Wrap von `crm_api.search_candidates`.
- Kein Supabase-Plugin auf Produktion.
- Kein Dump, keine Secrets, keine Personenzeilen in Git/Chat.
- OrbStack ist kein Schema-Beweis.
- Wizard 01 nicht mit 200-Deckel. `*.sql` und `Info/` bleiben aus dem Scan.
- occupation nicht heimlich zum R1-Kern machen (Q22).

## 8. Offen (nicht verloren, nur unerledigt)

| Thema | Status | Liegt in |
| --- | --- | --- |
| C 4–9 Codebefund | gelesen | crm-notify-codebefund.md |
| Restliche `do.php`-Cases ohne Statuswort | Lücke | Status-Datei |
| Prijave-Labels | DB, kein Dump | Status-Datei |
| Wizard 03 Alltag | bestätigt; Struke/Smjer = Ausbildungsberuf; 5 Jahre nicht in R1; INNER JOIN nicht kopieren | ADR-0002 Q18 |
| Q8.5 | `TEILWEISE`; Jahre nicht in R1 | ADR-0002 |
| JSON-Filter R1 | Entwurf, kein Vertrag; ohne Gruppe/Bearbeitung sichtbar | crm-json-filter-draft.md |
| Bericht-Audit JSON-PASS | Punkte 1–3 bestätigt | json-filter-audit.md |
| JSON/MCP/RPC, Auth, Hosting | ein Such-MCP + Tokens; Hosting/SDK-Version OFFEN | ADR-0002 Q11 |
| Export | R1: blättern und CSV/Excel max. 500 inkl. JMBG/Kontakt | ADR-0002 Q15.6 |
| step1 Website-Dump | Script-Lücke | Handoff |
| Zwei SQL in `databaseDump` | Init-Risiko | Handoff |
| 11–16 zweiter MCP | merken, nicht tief | Q20 |

Linear: ACT-100, Projekt Dino problem baza CRM, Team Activi.
