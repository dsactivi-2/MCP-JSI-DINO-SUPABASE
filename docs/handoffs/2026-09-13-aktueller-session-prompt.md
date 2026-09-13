<!-- markdownlint-disable MD013 -->
# Prompt: nächste Session (aktuell)

Datum: 2026-09-13

STOP: Die JSON-Prüfung ist bis zum Verifikations-Verdict unbewiesen.
Nicht diesen Block einfügen, bevor
[2026-09-13-verify-json-filter-review.md](2026-09-13-verify-json-filter-review.md)
VERDICT PASS oder PASS_WITH_GAPS geliefert hat.

Landkarte (zuerst lesen):
[crm-work-inventory.md](../discovery/crm-work-inventory.md).

Älteres Scan-Handoff (Dump, Q4, step1/step2; nächster Schritt darin ist
**veraltet**):
[2026-09-13-scan-to-mcp.md](2026-09-13-scan-to-mcp.md).

JSON-Entwurf:
[crm-json-filter-draft.md](../discovery/crm-json-filter-draft.md).

Block ungekürzt als erste Nachricht an den neuen Agenten einfügen.

~~~text
Du setzt die Arbeit am Supabase CRM MCP fort. Antworte auf Deutsch, einfache Worte. Code, Pfade und SQL-Namen nicht übersetzen.

Lies zuerst und arbeite danach, ohne den Scan von vorn zu beginnen:

1. /Users/activi/Documents/ChatGPT/Dino problem baza crm/docs/discovery/crm-work-inventory.md
2. docs/discovery/crm-json-filter-draft.md
3. docs/project.md
4. CONTEXT.md
5. docs/decisions/0002-search-design-interview.md — Q4 (ERSETZT), Q8.5, Q15, Q17–Q22
6. docs/discovery/crm-app-wiring.md
7. docs/discovery/crm-filter-sql-codebefund.md
8. docs/discovery/crm-status-codebefund.md
9. docs/discovery/crm-notify-codebefund.md

Arbeitsverzeichnis: /Users/activi/Documents/ChatGPT/Dino problem baza crm
Branch: codex/supabase-crm-auth-discovery
Dirty Tree nicht committen, nicht stashen, nicht resetten.

Phase: Discovery der alten PHP-Suche. JSON-Filter ist ENTWURF, kein Vertrag. Kein MCP-Server, kein App-Scaffold, kein Produktions-Apply, kein Wizard 01/02/04.

Verbindliche Quellen:
- Code nur /Users/activi/Downloads/crm-master-3/src/crm
- Kandidaten-Dump nur databaseDump/dump_20260226_081150.sql
- Nicht 2024_10_28.sql (Website, crmdb leer)
- Nicht /Users/activi/Projects/jobstep-crm
- Keine Dump-INSERT, keine Personenwerte in Git oder Chat
- CRM-Code nicht ins Doku-Repo kopieren

Schon erledigt, nicht wiederholen:
- Wizard 01 ohne 200-Zeilen-Deckel (RPC 21 / Tabellen 1732 / UI 2487)
- Hauptsuche: kandidati.php?page=list_ajax → serversidedata.php?page=lista_kandidata
- Filter-SQL (A): crm-filter-sql-codebefund.md
- Status-Klicks (B7): crm-status-codebefund.md
- Nachrichten C 4–9: crm-notify-codebefund.md (Produkt default aus)
- Wizard-03-Alltag: R1 = alte Recruiter-Hauptsuche
- step1 PASS, step2 PASS (CSS-IDs sind keine Tabellen)
- Linear-Karte ACT-100, Projekt Dino problem baza CRM
- JSON-Filter R1 gegen PHP/Heft geprüft (crm-json-filter-draft.md); bleibt Entwurf

Produktregeln, nicht neu aufrollen:
- Q4 intern: Entwickler, Sachbearbeiter, Teamleiter, Inhaber sehen Pool + Kontakte. Kunde nie den ganzen Pool. Vorschlagsfreigabe ohne Kontakt, Einstellungsfreigabe (CONTACT-02) mit Kontakt erst nach Zusage. Plugin nie auf Produktion.
- ADR-0001: LLM nur validiertes JSON. Kein LLM-SQL. Postgres sucht. Cap 50.
- Q17 Heft = alte UI/PHP.
- Q21 Funktionen erfassen, modern umsetzen, nicht PHP-SQL 1:1.
- Q22 jetzt nur altes CRM. occupation / Akten-Jahre / Stadt-Skills-als-Filter jetzt kein Scan.
- Q8.5.3–8 bestätigt für später; „5 Jahre“ ist kein R1-Filter. Wizard-03-Lücke Struke/Smjer und 5-Jahre-Filter bleibt OFFEN.
- Export Q15.6 OFFEN.
- Keine crm_api.search_candidates 1:1 wrappen.

Nächster Schritt:
Lege Tool-Namen und eine synthetische Eval für den JSON-Filter R1 an (keine Runtime, kein Scaffold). Lücken Struke/Smjer und „5 Jahre“ nicht schließen. Kein MCP bauen. Kein Wizard 01/04. Nach Doku-Änderungen: bash scripts/check-local.sh.

Offen merken, nicht jetzt lösen: restliche do.php-Cases ohne Statuswort; Prijave-Labels (DB); Auth/Hosting/Stack; zwei SQL-Dateien in databaseDump.
~~~
