<!-- markdownlint-disable MD013 -->
# Handoff: CRM-Scan bis Runtime-Such-MCP

**Stand dieser Datei:** historisch für Dump, Q4, step1/step2. Der **nächste
Schritt A–C hierin ist überholt.** Aktuelle Landkarte:
[crm-work-inventory.md](../discovery/crm-work-inventory.md).
Aktueller Session-Prompt:
[2026-09-13-aktueller-session-prompt.md](2026-09-13-aktueller-session-prompt.md).

Datum: 2026-09-13

Status: Session-Übergabe. **Kein** Runtime-Such-MCP gebaut. **Kein**
Produktions-SQL. **Kein** Plugin an das echte Supabase-Projekt.

Dieses Dokument übergibt den Chat, der den lokalen CRM-Scan, die Dump-Korrektur,
Q4 und die ersten Verdrahtungs-Scripts gemacht hat. Es ersetzt nicht
[ADR-0002](../decisions/0002-search-design-interview.md). Bei Konflikt gilt die
neueste ausdrückliche Nutzerantwort dort.

Doku-Repo: `/Users/activi/Documents/ChatGPT/Dino problem baza crm`

Linear: [Lokalen CRM-Scan in den Runtime-Suchvertrag übersetzen](https://linear.app/activi/issue/ACT-100/lokalen-crm-scan-in-den-runtime-suchvertrag-ubersetzen)
(Projekt **Dino problem baza CRM**, Team Activi). Nicht mit EnergyWarm-Tickets
vermischen.

## 1. Prompt für die nächste Session

Ungekürzt als erste Nachricht einfügen. Kopie:
[2026-09-13-next-agent-prompt.md](2026-09-13-next-agent-prompt.md).

~~~text
Du setzt die Arbeit am Supabase CRM MCP fort. Lies in dieser Reihenfolge und arbeite danach, ohne den Scan von vorn zu beginnen:

1. docs/discovery/crm-work-inventory.md
2. docs/handoffs/2026-09-13-scan-to-mcp.md
3. docs/project.md
4. CONTEXT.md
5. docs/decisions/0002-search-design-interview.md — mindestens Q4 (ERSETZT), Q8.5 (OFFEN), Q15, Q17, Q18, Q19, Q20, Q21, Q22
6. docs/discovery/crm-app-wiring.md, crm-filter-sql-codebefund.md, crm-status-codebefund.md
7. docs/runbooks/crm-wiring-wizards.md

Phase: Discovery und Verdrahtung der alten CRM-Suche. Noch kein MCP-Server, kein JSON-Vertrag, kein App-Scaffold, kein Produktions-Apply.

Verbindliche Quellen:
- Code nur /Users/activi/Downloads/crm-master-3 (PHP unter src/crm).
- Kandidaten-Dump nur .../databaseDump/dump_20260226_081150.sql (179 Tabellen, etwa 1,53 GiB).
- Nicht 2024_10_28.sql (Website; Datenbank crmdb darin angelegt aber leer).
- Nicht /Users/activi/Projects/jobstep-crm (zweite App-Kopie; kandidati.php bytegleich; Nutzer hat sie ausgeschlossen).
- CRM-Code nicht ins Doku-Repo kopieren. Dump-INSERT, E-Mails, Telefone, JMBG, Passwörter nicht in Git oder Chat schreiben.

Produktregeln, die schon stehen:
- Q4 intern: Entwickler, Sachbearbeiter, Teamleiter und Inhaber sehen den ganzen Pool und alle Felder inklusive Kontakt.
- Kunde sieht nie den ganzen Pool. Nach Vertrag Vorschlagsfreigabe ohne Kontakt. Nach Zusage/Einstellung Einstellungsfreigabe (CONTACT-02) mit Kontakt nur dieses Kandidaten.
- Entwickler-Plugin niemals an Produktion oder Restore-Klon. Produktsicht ist nicht Plugin-Zugang.
- ADR-0001: LLM erzeugt nur validiertes JSON. Kein LLM-SQL. Postgres filtert, cap 50.
- Q17: Heft und alte UI/PHP sind gleichberechtigt.
- Q21: Funktionen aus dem PHP erfassen und modern umsetzen, nicht 1:1 kopieren.
- Q22: Jetzt nur altes CRM scannen. occupation und andere PG-Zusatzfelder sind jetzt kein Scan-Auftrag.
- Q8.5 bleibt vollständig OFFEN (was „5 Jahre Erfahrung“ zählt).
- Export Q15.6 bleibt OFFEN.

Bereits gelaufen:
- Großen Dump nach crm-master-3/databaseDump kopiert; 2024_10_28.sql liegt noch daneben.
- scripts/discovery/step1-source-lock.sh = PASS, prüft aber noch den Website-Dump (Script-Lücke).
- scripts/discovery/step2-search-wiring.py = PASS; /private/tmp/dino-crm-step2-search-wiring.md. CSS-Klassen (idk_color_green usw.) sind kein Tabellenbeleg.
- Wizard 01 ohne 200-Zeilen-Deckel: RPC 21, Tabellen 1732, UI 2487. kandidati.php ist in den Zetteln.
- Hauptsuche laut Code: kandidati.php?page=list_ajax → serversidedata.php?page=lista_kandidata.
- Linear-Karte ACT-100.

Bereits in dieser Phase gelesen: Filter-SQL lista_kandidata, B7-Klicks, C 4–9, Wizard-03-Alltag.
JSON-Filter-Entwurf: crm-json-filter-draft.md (nur alte Filter).
Nächster Arbeitsschritt — kein MCP-Bau:
D. Entwurf prüfen, dann Tool-Namen/synthetische Eval. Drei Berufsschichten bleiben Fachmodell, nicht R1-Felder.
E. Keine crm_api.search_candidates 1:1 wrappen. Nicht Wizard 01/04 wiederholen. Nach Doku: bash scripts/check-local.sh.

Nicht tun: OrbStack als Schema-Beweis, Demo candidate-search-mcp als echte Daten, Supabase-Plugin auf Produktion, Dump ins Dino-Git, Scan von vorn ohne dieses Handoff.
~~~

## 2. Auftrag und Ziel

Der Nutzer wollte die Verdrahtung der lokal vorliegenden CRM-App plus Dump
scannen, dokumentieren und daraus ableiten, was auf Supabase und im MCP
einzurichten ist, damit Recruiter in einfacher Sprache suchen und der Agent
weiß, wonach und wie.

Das ist nicht „die ganze Datenbank automatisch zum MCP machen“. Auto-SQL-MCP
und 1:1-Wrap der alten Funktion `crm_api.search_candidates` bleiben NO-GO.

Zielprodukt: interne Recruiter (kleine Gruppe, Q2) suchen auf B/H/S, Deutsch
und Englisch. Das LLM übersetzt in einen kleinen, validierten JSON-Filter.
PostgreSQL filtert, rangiert, paginiert. Höchstens 50 Treffer. Fachmodell: drei
Berufsschichten plus Berufssuchprofile (Q8.4), auch wenn die alte Maske das so
nicht abbildet (Q17, Q21).

## 3. Verbindliche Pfade

| Was | Absoluter Pfad | Rolle |
| --- | --- | --- |
| CRM-Code | `/Users/activi/Downloads/crm-master-3` | einzige Code-Quelle |
| PHP | `/Users/activi/Downloads/crm-master-3/src/crm` | Legacy-PHP |
| Kandidaten-Dump | `/Users/activi/Downloads/crm-master-3/databaseDump/dump_20260226_081150.sql` | 1529458810 Bytes, 179 Tabellen |
| Original derselben Bytes | `/Users/activi/Downloads/dump_20260226_081150.sql` | Quelle der Kopie |
| Website-Dump | `/Users/activi/Downloads/crm-master-3/databaseDump/2024_10_28.sql` | Website; `crmdb` leer |
| Doku-Repo | dieses Git | ADRs und Scripts, keine Dumps |
| Zweite App | `/Users/activi/Projects/jobstep-crm` | nicht verwenden |

`crmdb` ist in docker-compose der Soll-Name. Im Website-Dump steht nur CREATE
und USE, dann `idkdev_jobstep`. Die 179 Tabellen liegen im großen Dump ohne
USE-Zeile. Beide SQL-Dateien liegen in `databaseDump/`; ein MySQL-Init würde
beide ausführen. Die Website-Datei wurde nicht gelöscht.

## 4. Entscheidungen, die nicht neu aufgerollt werden

### Q4 Kontakte (früheres „R1 ohne Kontakt“ ist ERSETZT)

| Akteur | Sicht |
| --- | --- |
| Sachbearbeiter, Teamleiter, Inhaber, Entwickler | ganzer Pool, alle Felder inklusive Kontakt |
| Kunde | nie ganzer Pool |
| Kunde nach Vertrag (Vorschlagsfreigabe) | vorgeschlagene Kandidaten ohne Kontakt |
| Kunde nach Zusage (Einstellungsfreigabe = CONTACT-02) | Kontakte nur dieses Kandidaten |

Plugin an Produktion/Klon verboten. Export Q15.6 OFFEN.

### Q17–Q22

| Q | Kern |
| --- | --- |
| Q17 | Heft und alte UI/PHP gleichberechtigt |
| Q18 | PHP-Filterbefund TEILWEISE; SQL in crm-filter-sql-codebefund.md |
| Q19 | Status-Ebenen und Automatik; Wizard 04, nicht Wizard 01 wiederholen |
| Q20 | R1: Filter, alle Status, Auslöser, A = Filter-SQL, B7 = do.php/ajax.php; C4–C9 tief scannen, Produkt Default-aus |
| Q21 | Funktionen erfassen, modern umsetzen, nicht 1:1 |
| Q22 | Jetzt nur altes CRM; occupation jetzt kein Scan |

Q8.5 bleibt vollständig OFFEN. Q8.4 bleibt bestätigt.

## 5. Was konkret gelaufen ist

1. Linear-Karte ACT-100, Projekt Dino problem baza CRM.
2. Read-only Docker: JobstepCRM :81, MySQL 8; synthetische Demo
   candidate-search-mcp ist kein Beweis.
3. Website-Dump entlarvt; großer Dump 179 Tabellen. Keine occupation* im
   MySQL-Dump.
4. Große Datei nach crm-master-3/databaseDump kopiert.
5. Q4/Q15 in ADR-0002, CONTEXT.md, AGENTS.md, ADR-0001, Brief, project.md.
6. step1 PASS 2026-09-12T20:50:38Z; dump_file noch 2024_10_28.sql.
7. step2 PASS; Filter aus kandidati.php. CSS-IDs als falsche Tabellen.
8. Wizard 01 ohne 200-Deckel; crm-app-wiring.md. Hauptsuche list_ajax.

## 6. Wo wir stehen

Discovery/Verdrahtung. Bevorzugte Maske: crm-app-wiring.md, nicht der step2-Rohbericht.

Filter-SQL `lista_kandidata`, B7-Klicks, C 4–9 und Wizard-03-Alltag sind dokumentiert.
JSON-Filter-Entwurf: [crm-json-filter-draft.md](../discovery/crm-json-filter-draft.md).
Nächster Schritt: Entwurf prüfen. Nicht Wizard 01/04 wiederholen.

Inventar: [crm-work-inventory.md](../discovery/crm-work-inventory.md).

Danach JSON-Filter, drei MCP-Tools, neue RPC, lokal synthetisch Option 1, dann
Freigabe. Siehe runtime-search-mcp-end-to-end.md.

## 7. Offen

| Thema | Status |
| --- | --- |
| Filter-SQL serversidedata.php | gelesen, siehe crm-filter-sql-codebefund.md |
| Manuelle Statuswege do.php / ajax.php | B7 gelesen, siehe crm-status-codebefund.md; Rest-Cases offen |
| Wizard 03 Alltag | bestätigt; Rest: Struke/Smjer, 5-Jahre-Filter |
| Q8.5 | OFFEN |
| idk_kandidati vs idk_nd_* | DURCH DISCOVERY |
| JSON-Filter R1 | Entwurf crm-json-filter-draft.md |
| JSON/MCP/RPC, Auth, Hosting | nicht gewählt |
| Export | Q15.6 OFFEN |
| step1 Website-Dump | Script-Lücke |
| Zwei SQL in databaseDump | Init-Risiko |
| C 4–9 Nachricht je Wechsel | gelesen, crm-notify-codebefund.md; Produkt default aus |
| occupation als R1-Kern | Q22: jetzt nicht scannen |

## 8. Verbote

- Kein Supabase-Plugin auf Produktion mit echten Kandidaten.
- Kein Auto-SQL-MCP / PostgREST auf crm.*.
- Kein 1:1-Wrap von crm_api.search_candidates.
- Keine Dump-Zeilen oder Secrets in Git, Chat, Reports.
- Dump und CRM nicht löschen; 2024_10_28.sql nicht ohne Auftrag entfernen.
- OrbStack nicht als Restore- oder Schema-Beweis.
- Q8.5 nicht aus PHP als BESTÄTIGT eintragen.
- occupation nicht heimlich zum R1-Kern machen.

## 9. Dateien

- [ADR-0001](../decisions/0001-controlled-query-boundary.md)
- [ADR-0002](../decisions/0002-search-design-interview.md)
- [CONTEXT.md](../../CONTEXT.md)
- [crm-work-inventory.md](../discovery/crm-work-inventory.md)
- [crm-app-wiring.md](../discovery/crm-app-wiring.md)
- [crm-filter-sql-codebefund.md](../discovery/crm-filter-sql-codebefund.md)
- [crm-status-codebefund.md](../discovery/crm-status-codebefund.md)
- [crm-php-hits](../discovery/crm-php-hits/)
- [crm-wiring-wizards.md](../runbooks/crm-wiring-wizards.md)
- Scripts: `scripts/discovery/step1-source-lock.sh`,
  `scripts/discovery/step2-search-wiring.py`, `scripts/wizards/`

OS-Temp-Handoff (Matt): `/private/tmp/dino-crm-session-handoff-2026-09-13.md`.
Lokal: `/private/tmp/dino-crm-step1-source-lock.txt`,
`/private/tmp/dino-crm-step2-search-wiring.md`,
`/private/tmp/dino-crm-wiring.env`,
`/private/tmp/dino-crm-app-wiring.md`.

Nach Doku: `bash scripts/check-local.sh`.
